# 데이터베이스 설정 가이드

## PostgreSQL 설치 (macOS)

```bash
# Homebrew로 PostgreSQL 설치
brew install postgresql@15

# PostgreSQL 서비스 시작
brew services start postgresql@15

# 또는 수동 시작
pg_ctl -D /opt/homebrew/var/postgresql@15 start
```

## 데이터베이스 설정

### 방법 1: 자동 설정 스크립트 사용

```bash
# 스크립트 실행 권한 부여
chmod +x setup_db.sh

# 데이터베이스 설정 실행
./setup_db.sh
```

### 방법 2: 수동 설정

```bash
# PostgreSQL 접속
psql -U postgres

# 사용자 및 데이터베이스 생성
CREATE USER prayer_user WITH PASSWORD 'prayer_password';
CREATE DATABASE prayer_note OWNER prayer_user;
GRANT ALL PRIVILEGES ON DATABASE prayer_note TO prayer_user;

# 데이터베이스 선택 및 스키마 적용
\c prayer_note
\i schema.sql
```

### 방법 3: Python으로 테이블 생성 (SQLAlchemy 모델 사용)

```bash
# 가상환경 활성화
source .venv/bin/activate

# 테이블 생성
python init_db.py
```

## 환경 변수 설정

`.env` 파일을 확인하고 데이터베이스 연결 정보를 수정하세요:

```env
DATABASE_URL="postgresql+asyncpg://prayer_user:prayer_password@localhost:5432/prayer_note"
```

## 데이터베이스 확인

```bash
# PostgreSQL 접속
psql -U prayer_user -d prayer_note

# 테이블 목록 확인
\dt

# 테이블 구조 확인
\d users
\d prayers
\d prayer_progress

# 종료
\q
```

## 트러블슈팅

### 연결 오류 발생 시

1. PostgreSQL 서비스가 실행 중인지 확인
   ```bash
   brew services list
   ```

2. 연결 정보 확인
   - 호스트: localhost
   - 포트: 5432 (기본값)
   - 사용자: prayer_user
   - 비밀번호: prayer_password
   - 데이터베이스: prayer_note

3. asyncpg 드라이버 설치 확인
   ```bash
   pip install asyncpg
   ```

### Internal Server Error 발생 시

1. 데이터베이스가 생성되었는지 확인
2. 테이블이 생성되었는지 확인
3. `.env` 파일의 DATABASE_URL이 올바른지 확인
4. 로그 확인 (FastAPI 서버 실행 시 콘솔 출력 확인)

## 데이터베이스 스키마

### users 테이블
- 사용자 정보 저장
- UUID 기본 키
- 이메일 중복 방지 (UNIQUE 제약)

### prayers 테이블
- 기도 제목 정보 저장
- user_id로 사용자와 연결
- JSONB 필드로 배열 데이터 저장 (prayer_targets, category_tags)
- ENUM 타입으로 상태 관리 (active, answered)

### prayer_progress 테이블
- 기도 응답 과정 기록
- prayer_id로 기도와 연결
- JSONB 필드로 태그 저장

## 개발 팁

### 데이터베이스 초기화 (모든 데이터 삭제)

```bash
# setup_db.sh 실행하면 자동으로 DROP DATABASE 수행
./setup_db.sh
```

### 마이그레이션 (Alembic 사용 권장)

추후 스키마 변경 시 Alembic을 사용하여 마이그레이션 관리를 권장합니다.

```bash
pip install alembic
alembic init alembic
```
