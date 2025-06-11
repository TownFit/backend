# 동네Fit 백엔드

![데이터베이스 제안서 001](https://github.com/user-attachments/assets/68106c71-2a8c-4946-b1c8-dd8a1f7e2dff)

![CI](https://github.com/TownFit/backend/actions/workflows/deploy.yml/badge.svg)
![Release](https://img.shields.io/github/v/release/TownFit/backend)
![Language](https://img.shields.io/github/languages/top/TownFit/backend)

나에게 딱! 맞는 스마트한 동네 추천, **동네Fit**

동네Fit은 개인별 생활 환경과 조건에 맞는 동네를 추천해주는 맞춤형 동네 추천 서비스입니다.

## ✨ 주요 기능

- **설문 기반 맞춤 동네 추천**: 사용자 설문 응답을 바탕으로 최적의 동네를 추천합니다.
- **LLM(Gemini API) 분석**: Google Gemini API를 활용하여 동네 인프라를 분석하고 추천 근거를 제시합니다.
- **지도 연동 시각화**: 추천 동네와 주요 시설 정보를 Naver Map API를 통해 지도에 표시합니다. (in [Frontend](https://github.com/TownFit/frontend))

## 🛠️ 주요 기술 스택

### 벡엔드 (Backend)

- **Language**: Python 3.13
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **Data Validation**: Pydantic
- **ORM**: SQLAlchemy
- **AI**: Google Gemini API (맞춤형 동네 추천용)

### 인프라 (Infrastructure - AWS)

- **Compute**: EC2
- **Database**: RDS (PostgreSQL)
- **Load Balancer**: Classic Load Balancer (CLB)
- **DNS**: Route53

### CI/CD & 컨테이너

- **CI/CD**: GitHub Actions
- **Containerization**: Docker
- **Image Registry**: Docker Hub

## 🏃‍♂️ 로컬 실행 방법

1. **Clone the repository**

```bash
git clone https://github.com/TownFit/backend.git
```

2. **의존성 설치**

```bash
cd backend
pip install -r requirements.txt
```

3. **환경변수 설정**

```bash
cp .env.example .env
vi .env
```

`.env` 파일을 열어 필요한 환경변수를 설정합니다.

4. **서버 실행**

```bash
uvicorn app.main:app --reload
```

### Docker를 이용한 방법

1. **Docker 이미지 빌드**

```bash
docker build -t backend .
```

2. **Docker 컨테이너 실행**

```bash
docker run -d -p 8000:8000 --env-file .env backend
```

## 📚 API 문서

- Swagger UI: `/docs`
- ReDoc: `/redoc`
