# Prayer Note Backend

기도 노트 웹 애플리케이션의 백엔드 API 서버입니다.

## 기술 스택

- **FastAPI** - 웹 프레임워크
- **SQLAlchemy 2.0** - ORM (비동기)
- **PostgreSQL** - 데이터베이스
- **Alembic** - 데이터베이스 마이그레이션
- **Pydantic** - 데이터 검증
- **JWT** - 인증

## 설치 및 실행

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 환경변수 설정

`.env` 파일을 생성하고 다음 내용을 설정하세요:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/prayer_note
SECRET_KEY=your-secret-key-here
```

### 3. 데이터베이스 마이그레이션

```bash
# 마이그레이션 생성
alembic revision --autogenerate -m "Initial migration"

# 마이그레이션 적용
alembic upgrade head
```

### 4. 서버 실행

```bash
# 개발 모드 (hot reload)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 프로덕션 모드
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

서버가 실행되면 다음 URL에서 접근 가능합니다:
- API 문서 (Swagger): http://localhost:8000/docs
- API 문서 (ReDoc): http://localhost:8000/redoc

## API 엔드포인트

### 인증 (`/api/v1/auth`)
- `POST /register` - 회원가입
- `POST /login` - 로그인
- `GET /me` - 현재 사용자 정보
- `POST /refresh` - 토큰 갱신

### 기도 (`/api/v1/prayers`)
- `GET /` - 기도 목록 조회
- `POST /` - 기도 등록
- `GET /{id}` - 기도 상세 조회
- `PATCH /{id}` - 기도 수정
- `DELETE /{id}` - 기도 삭제
- `POST /{id}/answer` - 최종 응답 기록

### 응답 과정 (`/api/v1/prayers`)
- `GET /{prayer_id}/progress` - 응답 과정 목록
- `POST /{prayer_id}/progress` - 응답 과정 추가
- `PATCH /progress/{id}` - 응답 과정 수정
- `DELETE /progress/{id}` - 응답 과정 삭제

### 대시보드 (`/api/v1/dashboard`)
- `GET /stats` - 대시보드 통계
- `GET /recent` - 최근 기도 목록

## 테스트

```bash
# 전체 테스트 실행
pytest

# 커버리지 포함
pytest --cov=app

# 특정 테스트 파일
pytest tests/test_auth.py
```

## 프로젝트 구조

```
app/
├── core/           # 핵심 설정 (config, database, security)
├── models/         # SQLAlchemy 모델
├── schemas/        # Pydantic 스키마
├── api/            # API 라우터
│   └── v1/         # API v1 엔드포인트
├── services/       # 비즈니스 로직
├── utils/          # 유틸리티 함수
└── main.py         # FastAPI 애플리케이션
```

## 데이터베이스 스키마

### Users
- id (UUID)
- email (unique)
- hashed_password
- name
- created_at, updated_at

### Prayers
- id (UUID)
- user_id (FK)
- subject, title, content
- prayer_type
- prayer_targets (JSONB)
- category_tags (JSONB)
- status (active/answered)
- start_date, answer_date
- answer_content
- created_at, updated_at

### PrayerProgress
- id (UUID)
- prayer_id (FK)
- content
- recorded_date
- tags (JSONB)
- created_at, updated_at

## 개발 가이드

### 새로운 마이그레이션 생성

```bash
alembic revision --autogenerate -m "Add new column"
alembic upgrade head
```

### 마이그레이션 롤백

```bash
alembic downgrade -1
```

### 코드 포맷팅

```bash
black app/
flake8 app/
```

## 배포

### Docker 사용 (선택사항)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 라이선스

MIT License
