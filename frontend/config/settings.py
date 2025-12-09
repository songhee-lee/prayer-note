"""환경 설정"""
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# API 설정
API_BASE_URL = st.secrets.get("API_URL", "http://localhost:8000")
API_V1_PREFIX = st.secrets.get("API_V1_PREFIX", "/api/v1")

# 디버그 모드
DEBUG_MODE = st.secrets.get("DEBUG_MODE", "False").lower() == "true"

# 전체 API URL
API_URL = f"{API_BASE_URL}{API_V1_PREFIX}"