#!/bin/bash

# PostgreSQL 데이터베이스 설정 스크립트

echo "🔧 PostgreSQL 데이터베이스 설정 중..."

# 환경 변수 로드
export $(cat .env | grep -v '^#' | xargs)

# PostgreSQL 접속 정보
DB_NAME="prayer_note"
DB_USER="prayer_user"
DB_PASSWORD="prayer_password"
DB_HOST="localhost"
DB_PORT="5432"

# 데이터베이스 및 사용자 생성
echo "📦 데이터베이스 및 사용자 생성..."
PGPASSWORD=postgres psql -h $DB_HOST -p $DB_PORT -U postgres <<EOF
-- 데이터베이스가 존재하면 삭제 (개발 환경용)
DROP DATABASE IF EXISTS $DB_NAME;

-- 사용자가 존재하면 삭제 (개발 환경용)
DROP USER IF EXISTS $DB_USER;

-- 사용자 생성
CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';

-- 데이터베이스 생성
CREATE DATABASE $DB_NAME OWNER $DB_USER;

-- 권한 부여
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
EOF

echo "✅ 데이터베이스 및 사용자 생성 완료"

# 스키마 적용
echo "📋 스키마 적용 중..."
PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f schema.sql

if [ $? -eq 0 ]; then
    echo "✅ 스키마 적용 완료"
else
    echo "❌ 스키마 적용 실패"
    exit 1
fi

echo "🎉 데이터베이스 설정 완료!"
