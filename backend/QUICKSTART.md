# Prayer Note Backend - 빠른 시작 가이드

## 로컬 개발 환경 설정

### 1. PostgreSQL 설치 및 설정

#### macOS (Homebrew)
```bash
brew install postgresql@15
brew services start postgresql@15
createdb prayer_note
```

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo -u postgres createdb prayer_note
sudo -u postgres createuser prayer_user
sudo -u postgres psql -c "ALTER USER prayer_user WITH PASSWORD 'prayer_password';"
```

#### Windows
1. PostgreSQL 공식 웹사이트에서 설치 프로그램 다운로드
2. 설치 후 pgAdmin 또는 psql로 데이터베이스 생성

### 2. Python 가상환경 생성

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### 3. 의존성 설치

```bash
pip install -r requirements.txt
```

### 4. 환경변수 설정

`.env` 파일을 생성하고 아래 내용을 작성:

```env
PROJECT_NAME="Prayer Note API"
VERSION="1.0.0"
API_V1_PREFIX="/api/v1"
DEBUG=True

# PostgreSQL 연결 정보 (본인 환경에 맞게 수정)
DATABASE_URL=postgresql+asyncpg://prayer_user:prayer_password@localhost:5432/prayer_note

# JWT 시크릿 키 (운영 환경에서는 반드시 변경!)
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS 설정 (프론트엔드 URL)
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:3001"]
```

### 5. 데이터베이스 마이그레이션

```bash
# 초기 마이그레이션 생성
alembic revision --autogenerate -m "Initial migration"

# 마이그레이션 적용
alembic upgrade head
```

### 6. 서버 실행

```bash
# 방법 1: 직접 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 방법 2: 스크립트 사용
./run_dev.sh

# 방법 3: Makefile 사용
make run
```

### 7. API 문서 확인

서버가 실행되면 브라우저에서 다음 주소로 접속:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Docker 사용 (권장)

Docker를 사용하면 PostgreSQL 설치 없이 바로 실행 가능합니다.

### 1. Docker 및 Docker Compose 설치

- Docker Desktop 설치 (macOS/Windows)
- Docker Engine 설치 (Linux)

### 2. 컨테이너 실행

```bash
# 컨테이너 빌드 및 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f backend

# 컨테이너 중지
docker-compose down
```

Docker 환경에서는 다음 주소로 접속:
- API: http://localhost:8000
- API 문서: http://localhost:8000/docs

## 테스트 실행

```bash
# 전체 테스트
pytest

# 특정 테스트 파일
pytest tests/test_auth.py

# 커버리지 포함
pytest --cov=app --cov-report=html
```

## 일반적인 명령어

```bash
# 새 마이그레이션 생성
make migrate

# 마이그레이션 적용
make upgrade

# 마이그레이션 롤백
make downgrade

# 코드 포맷팅
make format

# 코드 린팅
make lint

# 캐시 정리
make clean
```

## 문제 해결

### 데이터베이스 연결 오류
```
sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) could not connect to server
```

**해결 방법:**
1. PostgreSQL이 실행 중인지 확인
2. `.env` 파일의 `DATABASE_URL`이 올바른지 확인
3. 데이터베이스와 사용자가 생성되었는지 확인

### 포트 충돌
```
ERROR:    [Errno 48] error while attempting to bind on address ('0.0.0.0', 8000)
```

**해결 방법:**
1. 다른 포트 사용: `uvicorn app.main:app --port 8001`
2. 기존 프로세스 종료: `lsof -ti:8000 | xargs kill -9`

### 패키지 설치 오류

**해결 방법:**
1. pip 업그레이드: `pip install --upgrade pip`
2. 가상환경 재생성
3. 개별 패키지 설치 후 나머지 설치

## 다음 단계

1. 프론트엔드 개발 시작
2. 추가 기능 구현 (Phase 2)
3. 배포 환경 설정

## 지원

문제가 발생하면 GitHub Issues에 등록해주세요.
