"""API 클라이언트"""
import requests
import streamlit as st
from typing import Dict, List, Optional, Any
from config.settings import API_URL


class APIClient:
    """API 통신을 담당하는 클래스"""
    
    def __init__(self):
        self.base_url = API_URL
        
    def _get_headers(self) -> Dict[str, str]:
        """인증 헤더 생성"""
        headers = {"Content-Type": "application/json"}
        
        if "token" in st.session_state and st.session_state.token:
            headers["Authorization"] = f"Bearer {st.session_state.token}"
        
        return headers
    
    def _handle_response(self, response: requests.Response) -> Any:
        """응답 처리 및 에러 핸들링"""
        if response.status_code == 401:
            st.session_state.authenticated = False
            st.session_state.token = None
            st.error("로그인이 만료되었습니다. 다시 로그인해주세요.")
            st.rerun()
        
        if response.status_code >= 400:
            error_detail = response.json().get("detail", "알 수 없는 오류가 발생했습니다.")
            raise Exception(error_detail)
        
        return response.json()
    
    # ===== 인증 =====
    def register(self, email: str, username: str, password: str) -> Dict:
        """회원가입"""
        url = f"{self.base_url}/auth/register"
        data = {
            "email": email,
            "name": username,
            "password": password
        }
        response = requests.post(url, json=data)
        return self._handle_response(response)
    
    def login(self, email: str, password: str) -> Dict:
        """로그인"""
        url = f"{self.base_url}/auth/login"
        data = {
            "email": email,
            "password": password
        }
        response = requests.post(url, json=data)
        return self._handle_response(response)
    
    def get_current_user(self) -> Dict:
        """현재 사용자 정보 조회"""
        url = f"{self.base_url}/auth/me"
        response = requests.get(url, headers=self._get_headers())
        return self._handle_response(response)
    
    # ===== 기도 =====
    def get_prayers(self,
                    status: Optional[str] = None,
                    subject: Optional[str] = None,
                    search: Optional[str] = None,
                    sort_by: Optional[str] = None,
                    page: int = 1,
                    size: int = 100) -> List[Dict]:
        """기도 목록 조회"""
        url = f"{self.base_url}/prayers"
        params = {"page": page, "size": size}

        if status:
            params["status"] = status
        if subject:
            params["subject"] = subject
        if search:
            params["search"] = search
        if sort_by:
            params["sort_by"] = sort_by

        response = requests.get(url, headers=self._get_headers(), params=params)
        result = self._handle_response(response)

        # 응답이 dict이고 items 필드가 있으면 items 반환, 아니면 그대로 반환
        if isinstance(result, dict) and "items" in result:
            return result["items"]
        return result if isinstance(result, list) else []
    
    def get_prayer(self, prayer_id: str) -> Dict:
        """기도 상세 조회"""
        url = f"{self.base_url}/prayers/{prayer_id}"
        response = requests.get(url, headers=self._get_headers())
        return self._handle_response(response)
    
    def create_prayer(self, data: Dict) -> Dict:
        """기도 등록"""
        url = f"{self.base_url}/prayers"
        response = requests.post(url, headers=self._get_headers(), json=data)
        return self._handle_response(response)
    
    def update_prayer(self, prayer_id: str, data: Dict) -> Dict:
        """기도 수정"""
        url = f"{self.base_url}/prayers/{prayer_id}"
        response = requests.patch(url, headers=self._get_headers(), json=data)
        return self._handle_response(response)
    
    def delete_prayer(self, prayer_id: str) -> Dict:
        """기도 삭제"""
        url = f"{self.base_url}/prayers/{prayer_id}"
        response = requests.delete(url, headers=self._get_headers())
        return self._handle_response(response)
    
    def mark_as_answered(self, prayer_id: str, answer_data: Dict) -> Dict:
        """기도 응답 처리"""
        url = f"{self.base_url}/prayers/{prayer_id}/answer"
        response = requests.post(url, headers=self._get_headers(), json=answer_data)
        return self._handle_response(response)
    
    # ===== 응답 과정 기록 =====
    def get_prayer_logs(self, prayer_id: str) -> List[Dict]:
        """응답 과정 기록 목록"""
        url = f"{self.base_url}/prayers/{prayer_id}/progress"
        response = requests.get(url, headers=self._get_headers())
        result = self._handle_response(response)
        return result.get("items", []) if isinstance(result, dict) else result

    def create_prayer_log(self, prayer_id: str, data: Dict) -> Dict:
        """응답 과정 기록 추가"""
        url = f"{self.base_url}/prayers/{prayer_id}/progress"
        response = requests.post(url, headers=self._get_headers(), json=data)
        return self._handle_response(response)

    def update_prayer_log(self, prayer_id: str, log_id: str, data: Dict) -> Dict:
        """응답 과정 기록 수정"""
        url = f"{self.base_url}/prayers/progress/{log_id}"
        response = requests.patch(url, headers=self._get_headers(), json=data)
        return self._handle_response(response)

    def delete_prayer_log(self, prayer_id: str, log_id: str) -> Dict:
        """응답 과정 기록 삭제"""
        url = f"{self.base_url}/prayers/progress/{log_id}"
        response = requests.delete(url, headers=self._get_headers())
        return self._handle_response(response)
    
    # ===== 대시보드 =====
    def get_dashboard_stats(self) -> Dict:
        """대시보드 통계"""
        url = f"{self.base_url}/dashboard/stats"
        response = requests.get(url, headers=self._get_headers())
        return self._handle_response(response)
    
    def get_subject_stats(self) -> List[Dict]:
        """주제별 통계"""
        url = f"{self.base_url}/dashboard/subject-stats"
        response = requests.get(url, headers=self._get_headers())
        result = self._handle_response(response)

        # 리스트가 아니면 빈 리스트 반환
        return result if isinstance(result, list) else []

    def get_answered_without_content(self) -> List[Dict]:
        """응답 받았지만 내용 미작성 기도 목록"""
        url = f"{self.base_url}/dashboard/answered-without-content"
        response = requests.get(url, headers=self._get_headers())
        result = self._handle_response(response)

        # 리스트가 아니면 빈 리스트 반환
        return result if isinstance(result, list) else []


# 싱글톤 인스턴스
api_client = APIClient()