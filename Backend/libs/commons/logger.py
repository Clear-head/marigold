import logging
import os
import sys
from logging.handlers import RotatingFileHandler


class MarigoldLogger:
    def __init__(self, service_name: str):
        self.logger = logging.getLogger(service_name)
        self.logger.setLevel(logging.INFO)

        # 로그 포맷 정의
        formatter = logging.Formatter(
            '[%(asctime)s] [%(name)s] [%(levelname)s] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

        log_dir = "/app/logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        file_handler = RotatingFileHandler(
            filename=f"{log_dir}/{service_name}.log",
            maxBytes=10 * 1024 * 1024,  # 10MB마다 파일 롤링
            backupCount=5,  # 최대 5개까지 보관
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)


def get_marigold_logger(service_name: str):
    return MarigoldLogger(service_name).logger