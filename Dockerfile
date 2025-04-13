# Dockerfile
FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 업데이트와 netcat 설치 (DB 접속 대기를 위해)
RUN apt-get update && apt-get install -y netcat && rm -rf /var/lib/apt/lists/*

# 의존성 파일 복사 및 설치
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# 전체 프로젝트 복사
COPY . /app

# entrypoint 스크립트에 실행 권한 부여
RUN chmod +x /app/entrypoint.sh

# 서버 포트 노출
EXPOSE 8000

# entrypoint 스크립트를 실행하여 컨테이너 구동
ENTRYPOINT ["/app/entrypoint.sh"]
