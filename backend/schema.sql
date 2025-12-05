-- Prayer Note Database Schema for PostgreSQL

-- UUID 확장 활성화
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 기존 테이블 삭제 (개발 환경용, 프로덕션에서는 주의)
DROP TABLE IF EXISTS prayer_progress CASCADE;
DROP TABLE IF EXISTS prayers CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- ENUM 타입 삭제 (존재하는 경우)
DROP TYPE IF EXISTS prayer_status CASCADE;

-- ENUM 타입 생성
CREATE TYPE prayer_status AS ENUM ('active', 'answered');

-- 사용자 테이블
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 사용자 테이블 인덱스
CREATE INDEX idx_users_email ON users(email);

-- 기도 테이블
CREATE TABLE prayers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    -- 기본 정보
    subject VARCHAR(100) NOT NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    prayer_type VARCHAR(50) NOT NULL,

    -- JSON 배열 필드
    prayer_targets JSONB NOT NULL DEFAULT '[]'::jsonb,
    category_tags JSONB NOT NULL DEFAULT '[]'::jsonb,

    -- 상태 및 날짜
    status prayer_status NOT NULL DEFAULT 'active',
    start_date DATE NOT NULL,
    answer_date DATE,
    answer_content TEXT,

    -- 타임스탬프
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 기도 테이블 인덱스
CREATE INDEX idx_prayers_user_id ON prayers(user_id);
CREATE INDEX idx_prayers_subject ON prayers(subject);
CREATE INDEX idx_prayers_status ON prayers(status);
CREATE INDEX idx_prayers_start_date ON prayers(start_date);

-- 기도 응답 과정 기록 테이블
CREATE TABLE prayer_progress (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    prayer_id UUID NOT NULL REFERENCES prayers(id) ON DELETE CASCADE,

    -- 기록 내용
    content TEXT NOT NULL,
    recorded_date DATE NOT NULL,
    tags JSONB NOT NULL DEFAULT '[]'::jsonb,

    -- 타임스탬프
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 기도 응답 과정 테이블 인덱스
CREATE INDEX idx_prayer_progress_prayer_id ON prayer_progress(prayer_id);
CREATE INDEX idx_prayer_progress_recorded_date ON prayer_progress(recorded_date);

-- updated_at 자동 업데이트 함수
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- users 테이블 트리거
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- prayers 테이블 트리거
CREATE TRIGGER update_prayers_updated_at
    BEFORE UPDATE ON prayers
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- prayer_progress 테이블 트리거
CREATE TRIGGER update_prayer_progress_updated_at
    BEFORE UPDATE ON prayer_progress
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- 샘플 데이터 삽입 (선택사항)
-- INSERT INTO users (email, hashed_password, name) VALUES
-- ('test@example.com', '$2b$12$...', 'Test User');
