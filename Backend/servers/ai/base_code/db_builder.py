import argparse
import os
import re
import sys
import uuid
import json

import chromadb
from sentence_transformers import SentenceTransformer

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.logger.log_handler import get_logger
from src.dto.chat_data_dto import ChatDataDto
from src.dto.query_result_dto import QueryResultDto

log = get_logger('vector_db_builder')


class VectorDBHandler:
    """
    ChromaDB와 SentenceTransformers를 사용하여 채팅 메시지용 벡터 데이터베이스의
    생성, 업데이트, 관리를 처리합니다.
    """

    def __init__(self, db_path: str, collection_name: str = "chat_messages"):
        """
        VectorDBHandler를 초기화합니다.
        Args:
            db_path (str): 데이터베이스가 저장될 디렉토리 경로.
            collection_name (str, optional): 사용할 컬렉션의 이름.
                                             기본값은 "chat_messages"입니다.
        """
        self.db_path = db_path
        self.collection_name = collection_name

        # 1. 임베딩을 위한 SentenceTransformer 모델 초기화
        # 한국어를 지원하는 다국어 모델을 사용합니다.
        self.embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

        # 2. ChromaDB 클라이언트 초기화
        self.client = chromadb.PersistentClient(path=self.db_path)

        # 3. 컬렉션 가져오기 또는 생성
        self.collection = self.client.get_or_create_collection(name=self.collection_name)

    def process_and_upsert_contextual(self, json_data: dict):
        """
        채팅 데이터를 컨텍스트 문장으로 만들어 DB에 업서트(upsert)합니다.
        """
        try:
            chat_data = ChatDataDto.model_validate(json_data)
        except Exception as e:
            log.error(f"Error validating JSON data: {e}")
            return

        documents_to_embed = []
        metadatas_to_upsert = []
        ids_to_upsert = []

        log.info("Constructing contextual documents for embedding...")

        for _, message in chat_data.body.items():
            contextual_doc = (
                f"날짜: {message.date}, 시간: {message.time}, "
                f"작성자: {message.name}\n"
                f"내용: {message.contents}"
            )
            documents_to_embed.append(contextual_doc)

            metadatas_to_upsert.append({
                "name": message.name,
                "time": message.time,
                "date": message.date,
                "contents": message.contents,
                "room-id": message.room_id if message.room_id else ""
            })
            ids_to_upsert.append(str(uuid.uuid4()))
            log.info(f"  - Generated: {contextual_doc}")

        if not documents_to_embed:
            log.warning("No valid documents to process.")
            return

        log.info("Embedding documents and upserting into the database...")
        self.collection.upsert(
            embeddings=self.embedding_model.encode(documents_to_embed).tolist(),
            documents=documents_to_embed,
            metadatas=metadatas_to_upsert,
            ids=ids_to_upsert
        )
        log.info(f"Successfully upserted {len(documents_to_embed)} documents.")

    def query_messages(self, query_text: str, n_results: int = 5) -> QueryResultDto:
        """
        벡터 데이터베이스에서 쿼리 텍스트와 유사한 메시지를 검색합니다.
        Args:
            query_text (str): 검색할 텍스트.
            n_results (int, optional): 반환할 결과의 수. 기본값은 5입니다.
        Returns:
            QueryResultDto: ChromaDB의 쿼리 결과.
        """
        query_embedding = self.embedding_model.encode(query_text).tolist()

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

        return QueryResultDto.model_validate(results)


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
    # 2. JSON 파일 처리 및 벡터 DB 저장
    # ===========================================================================
    # 명령어의 인자(argument)로 JSON 파일 경로를 받습니다.
    if len(sys.argv) < 2:
        print("\n[사용법]")
        print("DB 적재: python src/ai/db_builder.py <json_파일_경로>")
        print("\n[예시]")
        print("python src/ai/db_builder.py data/yesterday_chat.json\n")
        sys.exit(1)

    json_file_path = sys.argv[1]  # 첫 번째 인자를 파일 경로로 사용

    if not os.path.exists(json_file_path):
        print(f"오류: JSON 파일('{json_file_path}')을 찾을 수 없습니다.")
        sys.exit(1)

    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            chat_data = json.load(f)
    except json.JSONDecodeError:
        print(f"오류: '{json_file_path}' 파일의 JSON 형식이 올바르지 않습니다.")
        sys.exit(1)

    print(f"'{json_file_path}'의 내용을 벡터 DB에 저장합니다...")
    vector_db_handler.process_and_upsert_contextual(chat_data)
    print("벡터 DB 저장 완료.")