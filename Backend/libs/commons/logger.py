import logging
import os
import sys
from logging.handlers import RotatingFileHandler

import os
import sys
import logging
from logging.handlers import RotatingFileHandler


class MarigoldLogger:
    def __init__(self, service_name: str):
        self.logger = logging.getLogger(service_name)
        self.logger.setLevel(logging.INFO)

        # 1. 로그 경로 결정 (환경 변수 사용 혹은 로컬 상대 경로)
        # Docker 환경이면 /app/logs, 로컬이면 프로젝트 루트의 logs 폴더 사용
        base_dir = os.getenv("LOG_DIR", os.path.join(os.getcwd(), "logs"))

        if not os.path.exists(base_dir):
            try:
                os.makedirs(base_dir, exist_ok=True)
            except OSError:
                # 권한 문제 등으로 실패할 경우 임시 디렉토리 사용
                base_dir = "/tmp/logs"
                os.makedirs(base_dir, exist_ok=True)

        formatter = logging.Formatter(
            '[%(asctime)s] [%(name)s] [%(levelname)s] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # 콘솔 출력 설정
        if not self.logger.handlers:  # 핸들러 중복 등록 방지
            stream_handler = logging.StreamHandler(sys.stdout)
            stream_handler.setFormatter(formatter)
            self.logger.addHandler(stream_handler)

            # 파일 출력 설정
            file_handler = RotatingFileHandler(
                filename=os.path.join(base_dir, f"{service_name}.log"),
                maxBytes=10 * 1024 * 1024,
                backupCount=5,
                encoding='utf-8'
            )
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)


def get_marigold_logger(service_name: str):
    return MarigoldLogger(service_name).logger