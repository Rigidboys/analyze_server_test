# logger.py
import logging
import os
from flask import request

os.makedirs("logs", exist_ok=True)

# 분석 로그
analyze_logger = logging.getLogger("analyze")
analyze_logger.setLevel(logging.INFO)
analyze_handler = logging.FileHandler("logs/analyze.log", encoding="utf-8")
analyze_handler.setFormatter(logging.Formatter('%(asctime)s | %(message)s'))
analyze_logger.addHandler(analyze_handler)

# 에러 로그
error_logger = logging.getLogger("error")
error_logger.setLevel(logging.ERROR)
error_handler = logging.FileHandler("logs/error.log", encoding="utf-8")
error_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s'))
error_logger.addHandler(error_handler)

# ✅ 공용 분석 로그 함수
def log_analysis(route: str, desc: str = "", params: dict = None):
    ip = request.remote_addr
    param_str = f" | params={params}" if params else ""
    analyze_logger.info(f"{ip} | {route} | 분석: {desc}{param_str}")

# ✅ 공용 에러 로그 함수
def log_error(route: str, error: Exception):
    error_logger.error(f"{route} | {str(error)}")
