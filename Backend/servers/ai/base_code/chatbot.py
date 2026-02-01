import os
import re
import sys

from openai import OpenAI

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.logger.log_handler import get_logger
from src.ai.db_builder import VectorDBHandler
from src.dto.query_result_dto import QueryResultDto

log = get_logger('chatbot')


class RAGChatbot:
    """
    벡터 데이터베이스에 저장된 채팅 기록을 바탕으로 질문에 답변하는
    RAG(검색 증강 생성) 챗봇입니다.
    """

    def __init__(self, vector_db_handler: VectorDBHandler):
        """
        RAGChatbot을 초기화합니다.
        Args:
            vector_db_handler (VectorDBHandler): 벡터 데이터베이스를 쿼리하기 위한
                                                 VectorDBHandler의 인턴스.
        """
        self.vector_db_handler = vector_db_handler
        # Ollama 클라이언트를 초기화합니다.
        try:
            self.client = OpenAI(
                base_url='http://localhost:11434/v1',
                api_key='ollama',  # required but ignored
            )
        except Exception as e:
            raise Exception("Failed to initialize Ollama client. "
                            "Please make sure Ollama is running.") from e

    def _filter_korean_response(self, text: str) -> str:
        """
        텍스트에서 한글, 숫자, 기본 문장 부호만 남도록 필터링하고,
        그 과정에서 발생할 수 있는 서식 문제를 정리합니다.
        """
        # 1단계: 한글, 숫자, 기본 문장 부호가 아닌 모든 문자를 제거합니다.
        pattern = r'[^가-힣ㄱ-ㅎㅏ-ㅣ0-9\s.,?!]'
        filtered_text = re.sub(pattern, '', text)

        # 2단계: 필터링으로 인해 발생한 서식 문제를 정리합니다.
        # 여러 개의 공백을 하나의 공백으로 축소합니다.
        cleaned_text = re.sub(r'\s+', ' ', filtered_text)
        # 문장 부호 앞에 있는 공백을 제거합니다.
        cleaned_text = re.sub(r'\s+([.,?!])', r'\1', cleaned_text)
        # 반복되거나 섞인 문장 부호들을 정리합니다.
        cleaned_text = re.sub(r'([.,?!])([.,?!\s]){2,}', r'\1', cleaned_text)

        return cleaned_text.strip()

    def generate_response(self, user_query: str, n_results: int = 3):
        """
        RAG를 사용하여 사용자 쿼리에 대한 응답을 생성합니다.
        Args:
            user_query (str): 사용자의 질문.
            n_results (int): DB에서 가져올 관련 문서의 수.
        Returns:
            str: 언어 모델이 생성한 응답.
        """
        # 1. 벡터 데이터베이스에서 관련성 높은 문맥을 검색합니다.
        retrieved_results: QueryResultDto = self.vector_db_handler.query_messages(
            query_text=user_query,
            n_results=n_results
        )

        if (retrieved_results.documents is None or
                not retrieved_results.documents or
                not retrieved_results.documents[0]):
            context = "No relevant chat history found."
        else:
            documents = [doc for doc in retrieved_results.documents[0] if doc is not None]
            context = "\n".join(documents)

        # 2. 언어 모델을 위한 프롬프트를 구성합니다.
        system_prompt = (
            "당신은 사용자의 과거 대화 기록을 정확하게 기억하고, 그 내용을 바탕으로 질문에 정중하게 답변하는 AI 비서입니다.\n\n"
            "## 답변 지침:\n"
            "1. **정중한 어조:** 모든 답변은 격식 있고 정중한 한국어(~습니다, ~합니다 체)를 사용해야 합니다.\n"
            "2. **사실 기반 추론:** 대화 기록에 명시된 사실을 바탕으로 한 논리적이고 상식적인 추론은 가능합니다. 예를 들어, '피자를 주문하겠다'는 기록이 있다면, '피자를 드셨을 것으로 판단됩니다.' 와 같이 답변할 수 있습니다.\n"
            "3. **명확한 근거 제시:** 답변의 근거가 되는 대화 내용을 명확히 언급해주세요. 예: '기록에 따르면, OOO님께서 \"피자를 주문하겠다\"고 말씀하셨습니다.'\n"
            "4. **신중한 표현:** 추론에 기반한 답변을 할 경우, 단정적으로 말하지 말고 '...로 추정됩니다' 또는 '...하셨을 가능성이 높습니다' 와 같이 신중한 표현을 사용하세요.\n"
            "5. **정보 부재 시:** 질문에 대한 정보를 기록에서 찾을 수 없는 경우, '죄송하지만, 해당 내용에 대한 기록을 찾을 수 없었습니다.' 라고 명확하게 답변해주세요.\n"
            "6. **문자 사용 규칙:** 답변에는 한글, 숫자, 그리고 기본적인 문장 부호(. , ? !) 외에 다른 언어의 문자(영어, 러시아어 등)나 특수기호를 절대 사용해서는 안 됩니다."
        )

        user_prompt = f"과거 대화 기록:\n---\n{context}\n---\n\n사용자 질문: {user_query}"

        # 3. Ollama API를 호출하여 응답을 가져옵니다.
        try:
            response = self.client.chat.completions.create(
                model="llama3",  # 로컬 Ollama 모델 사용
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.2,
            )
            raw_response = response.choices[0].message.content
            # 응답을 필터링하여 깨끗한 한국어만 남깁니다.
            filtered_response = self._filter_korean_response(raw_response)
            return filtered_response
        except Exception as e:
            log.error(f"Ollama API와 통신하는 중 오류가 발생했습니다: {e}")
            return "챗봇과 통신하는 중 오류가 발생했습니다. 자세한 내용은 로그를 확인해주세요."


if __name__ == '__main__':
    # ===========================================================================
    # 1. 벡터 DB 핸들러 초기화
    # ===========================================================================
    db_directory = 'db'
    collection_name = 'chat_collection'

    # 데이터베이스 디렉토리가 존재하지 않으면 생성합니다.
    if not os.path.exists(db_directory):
        os.makedirs(db_directory)
        print(f"'{db_directory}' 디렉토리를 생성했습니다.")

    vector_db_handler = VectorDBHandler(
        db_path=db_directory,
        collection_name=collection_name
    )

    # ===========================================================================
    # 2. RAG 챗봇 실행
    # ===========================================================================
    print("\nRAG 챗봇을 시작합니다. (종료하려면 'exit' 또는 Ctrl+C 입력)")
    chatbot = RAGChatbot(vector_db_handler=vector_db_handler)

    while True:
        try:
            user_input = input("무엇이 궁금하신가요?: ")
            if user_input.lower() in ['exit', 'quit']:
                break

            response = chatbot.generate_response(user_input)
            print(f"답변: {response}")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\n오류가 발생했습니다: {e}")
            break

    print("\n챗봇을 종료합니다.")