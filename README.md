# LumenServer

## 작업목표

### Phase 1
- Rest API 구조를 활용하여 Google Cloud/AWS에 올라가는 형태로 백엔드를 작업
- 기본 상정하는 구조는 카드의 단일구조 관리(이미지 포함) + 효과의 기계적 분류 및 정리 작업

### Phase 2
- 간단한 형태의 프론트엔드를 구성해서 실제 테스트 확인
- 계정 및 관리 시스템 작업 진행
- API-based 자동 판정 시스템 제작

### Phase 3
- 해당 백엔드 구조에 맞춰 독립적인 웹/unity 프론트엔드를 제작
- 베타 서비스 시작, 최종적으로는 hinoto/lumenGG와 통합을 목표로

### Phase 4
- 프론트엔드에 미니게임 기획 및 제작
- 장기 서비스를 위한 서비스 간략화


---

## 실제 작업 로그
### Phase 1
- LumenGG 코드리뷰 및 정제 작업 시작
    - 백엔드/프론트엔드 코드가 동일선에 작성되어 있음 + 기능 위주의 추가기 떄문에 오히려 코드통일성이 없는 단점을 리팩토링하며 해결
- 최우선적으로 구현해야 할 기능을 체크하고 확인


⸻
# 서버 명세 및 구성 확인

# 1. 예상 인프라 구성 및 요구 사항

## 1.1 트래픽 특성 및 요구 사항
- **일반 상황:**
  - 총 3000명의 유저가 로그인, 프로필 및 카드 정보 조회 등 기본 기능 사용
- **대회 당일:**
  - 2000명 정도의 동시 접속자가 자신의 덱을 확인하고 대회 신청 진행
  - **필수 요소:** 부하 분산(Load Balancer) 및 자동 확장(Auto Scaling)

## 1.2 서버 구성 요소 예시
- **애플리케이션 서버:**
  - REST API 혹은 GraphQL을 통해 클라이언트 요청 처리
  - Auto Scaling 그룹 또는 컨테이너 오케스트레이션(Kubernetes, ECS/EKS, Cloud Run 등) 활용
- **데이터베이스 서버:**
  - 회원 정보, 카드 데이터, 대회 신청 내역 저장
  - 관리형 DB 서비스(RDS, Cloud SQL, Azure Database 등) 권장
- **정적 파일/프론트엔드 호스팅:**
  - S3, GCS, Azure Blob Storage 등의 객체 스토리지와 CDN 활용
- **부가 서비스:**
  - 캐싱 (Redis, Memcached)
  - 로깅 및 모니터링, 보안 그룹/방화벽 등

# 2. 클라우드 서비스 제공업체별 옵션

## 2.1 Amazon Web Services (AWS)
- **장점:**
  - 다양한 인프라 구성 옵션 (EC2, ECS/EKS, Lambda, RDS, S3, CloudFront 등)
  - 서울 리전 운영으로 국내 사용자에 대해 빠른 응답속도 제공
  - Auto Scaling 및 부하 분산(ALB) 지원으로 동시 접속자 급증 대응 가능
- **예상 인프라 구성 및 대략적 비용:**
  - **애플리케이션 서버:**
    - 예: m5.large 인스턴스 2대 (24/7 운영)
    - 시간당 약 \$0.11 ~ \$0.12 → 월 약 \$170 (2대 기준)
  - **데이터베이스:**
    - 예: RDS db.t3.medium (MySQL/PostgreSQL 등) → 월 약 \$70~\$80
  - **부하 분산 및 기타:**
    - Application Load Balancer 및 네트워크 비용 약 \$20~\$30
  - **총계:** 약 \$260 ~ \$300/월  
  - *참고:* 예약 인스턴스, 스팟 인스턴스 등에 따라 비용 절감 가능

## 2.2 Google Cloud Platform (GCP)
- **장점:**
  - Compute Engine, GKE, Cloud Run 등 다양한 인스턴스 운영 선택 가능
  - 지속 사용 할인(Sustained Use Discount)으로 장기간 운영 시 비용 절감
  - 서울 리전(또는 인접 아시아 리전) 운영으로 낮은 지연시간 보장
- **예상 인프라 구성 및 대략적 비용:**
  - **애플리케이션 서버:**
    - 예: n2-standard-2 또는 유사 사양 인스턴스 2대 (24/7 운영)
    - 시간당 약 \$0.10 ~ \$0.12 → 월 약 \$160~\$170
  - **데이터베이스:**
    - 예: Cloud SQL 인스턴스 → 월 약 \$70~\$80
  - **부하 분산 및 네트워크:**
    - 부하 분산(LB) 및 네트워크 비용 약 \$20~\$30
  - **총계:** 약 \$250 ~ \$280/월

## 2.3 Microsoft Azure
- **장점:**
  - Windows 환경과의 연동 및 엔터프라이즈 통합이 강점
  - Azure App Service, Virtual Machines, Azure Database 등 다양한 관리형 서비스 제공
  - 한국(한국 중부, 한국 남부) 리전 운영
- **예상 인프라 구성 및 대략적 비용:**
  - **애플리케이션 서버:**
    - 예: D2 v3 시리즈 인스턴스 2대 → 월 약 \$170 ~ \$180
  - **데이터베이스:**
    - 예: Azure Database for MySQL/PostgreSQL → 월 약 \$70~\$80
  - **부하 분산 및 네트워크:**
    - Azure Load Balancer, CDN 등 → 월 약 \$20~\$30
  - **총계:** 약 \$260 ~ \$300/월

## 2.4 국내 클라우드 서비스 (예: 네이버 클라우드, 카카오 클라우드)
- **장점:**
  - 한국 내 데이터 센터 운영으로 낮은 지연시간 및 현지화된 기술 지원
  - 국내 사용자 대상 최적화된 네트워크와 경쟁력 있는 가격 정책
- **예상 인프라 구성 및 대략적 비용:**
  - **애플리케이션 서버:**
    - 유사 사양 인스턴스 2대 → 월 약 \$150~\$200
  - **데이터베이스:**
    - 관리형 DB 서비스 → 월 약 \$60~\$80
  - **부하 분산 및 네트워크:**
    - 기본 제공 로드밸런싱/네트워크 비용 → 월 약 \$20~\$40
  - **총계:** 약 \$230 ~ \$280/월  
  - *참고:* 업체마다 요금 체계와 부가 서비스는 다를 수 있음

# 3. 비용 비교 및 고려 사항

| 항목                      | AWS (서울 리전)          | GCP (서울/인접 리전)         | Azure (한국 리전)          | 국내 클라우드 (예: 네이버 클라우드)  |
|---------------------------|-------------------------|-----------------------------|--------------------------|--------------------------------------|
| **애플리케이션 서버 (2대)** | 약 \$170/월             | 약 \$160~\$170/월             | 약 \$170~\$180/월          | 약 \$150~\$200/월                      |
| **데이터베이스**           | 약 \$70~\$80/월          | 약 \$70~\$80/월              | 약 \$70~\$80/월           | 약 \$60~\$80/월                        |
| **부하 분산/네트워크**       | 약 \$20~\$30/월          | 약 \$20~\$30/월              | 약 \$20~\$30/월           | 약 \$20~\$40/월                        |
| **총계 (대략)**           | \$260 ~ \$300/월         | \$250 ~ \$280/월            | \$260 ~ \$300/월          | \$230 ~ \$280/월                       |

> **주의 사항:**
> - 위 비용은 단순 추정치입니다.
> - 실제 비용은 사용량, 예약 할인, 스팟/선예약 인스턴스 사용, 데이터 전송, 스토리지 및 추가 서비스에 따라 달라질 수 있습니다.
> - 각 클라우드 제공업체의 **[AWS 가격 계산기](https://aws.amazon.com/calculator/)**, **[GCP 가격 계산기](https://cloud.google.com/products/calculator)**, **[Azure 가격 계산기](https://azure.microsoft.com/ko-kr/pricing/calculator/)** 등을 참고해 보다 정밀한 견적을 산출하는 것을 권장합니다.

# 4. 결론 및 추천 전략

## 4.1 직접 서버 코드를 작성하여 백엔드/프론트엔드 구축 시
- **장점:**
  - 인프라 구성의 자유도가 높으며, 전체 스택을 직접 관리 가능
  - 원하는 기능에 맞게 세부적으로 구성 및 최적화 가능
- **단점:**
  - 서버, 데이터베이스, 부하 분산 등을 직접 관리해야 하므로 운영 및 유지보수 부담이 있음

## 4.2 추천 옵션 및 운영 전략
1. **AWS 또는 GCP 활용:**
   - 다양한 서비스 옵션과 확장성, 그리고 기능 면에서 우수
   - 서울 리전 운영으로 국내 사용자에 유리
2. **Azure 선택:**
   - MS 환경과의 연동 필요 시 적합
   - 기존 Windows Server나 .NET 기반 개발 환경에 유리
3. **국내 클라우드 업체 고려:**
   - 한국 내 사용자 대상 최적화된 지연시간과 현지 지원
   - 경우에 따라 경쟁력 있는 가격 제공 가능

- **운영 전략:**
  - **초기 단계:** 최소 인스턴스 구성으로 비용 최적화 후 부하 테스트를 통해 실제 트래픽에 맞춘 Auto Scaling, 캐싱 전략 적용
  - **대회 당일 피크:** 사전 워밍업된 인스턴스 또는 서버리스/컨테이너 기반 서비스를 이용하여 급격한 부하에 대비


-----
# API 명세 초안

# LumenGG REST API 및 데이터베이스 설계안

## REST API 명세

### 인증 (Auth)

- **POST** `/api/auth/signup`  
  **요청**:  
  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string"
  }
  ```  
  **응답**:  
  ```json
  {
    "token": "string"
  }
  ```

- **POST** `/api/auth/login`  
  **요청**:  
  ```json
  {
    "username": "string", // 또는 email
    "password": "string"
  }
  ```  
  **응답**:  
  ```json
  {
    "token": "string"
  }
  ```

- **POST** `/api/auth/logout`  
  **요청**:  
  ```json
  {
    "token": "string"
  }
  ```  
  **응답**:  
  ```json
  {
    "message": "string"
  }
  ```

---

### 카드 (Card)

- **GET** `/api/cards/`  
  **요청 파라미터**: `query?, character?, tags?`  
  **응답**: 카드 목록 JSON

- **GET** `/api/cards/{id}/`  
  **응답**: 카드 상세 정보 JSON

- **POST** `/api/cards/` *(관리자용)*  
  **요청**: 카드 생성 정보 JSON  
  **응답**: 생성된 카드 JSON

---

### 덱 (Deck)

- **GET** `/api/decks/`  
  **요청 파라미터**: `query?, character?, author?`  
  **응답**: 덱 목록 JSON

- **POST** `/api/decks/`  
  **요청**:  
  ```json
  {
    "name": "string",
    "character_id": 1,
    "cards": [
      {
        "card_id": 1,
        "count": 2,
        "side": false,
        "hand": false
      }
    ],
    "private": false,
    "description": "string",
    "tags": ["tag1", "tag2"]
  }
  ```  
  **응답**: 생성된 덱 JSON

- **GET** `/api/decks/{id}/`  
  **응답**: 덱 상세 정보 JSON

- **PUT** `/api/decks/{id}/`  
  **요청**: 덱 수정 정보 JSON  
  **응답**: 수정된 덱 JSON

- **DELETE** `/api/decks/{id}/`  
  **응답**:  
  ```json
  {
    "message": "Deleted successfully"
  }
  ```

---

### 콜렉션 (Collection)

- **GET** `/api/collection/`  
  **응답**: 사용자 콜렉션 JSON

- **POST** `/api/collection/`  
  **요청**:  
  ```json
  {
    "collected_cards": [
      {
        "collection_card_id": 1,
        "amount": 2
      }
    ]
  }
  ```  
  **응답**: 업데이트된 콜렉션 JSON

---

### Q&A

- **GET** `/api/qna/`  
  **요청 파라미터**: `query?, faq?`  
  **응답**: 질문 목록 JSON

- **POST** `/api/qna/` *(관리자용)*  
  **요청**:  
  ```json
  {
    "title": "string",
    "question": "string",
    "answer": "string",
    "faq": true,
    "cards": [1, 2]
  }
  ```  
  **응답**: 생성된 Q&A JSON

- **GET** `/api/qna/{id}/`  
  **응답**: 질문 상세 정보 JSON

---

## 데이터베이스 구조

### User
- `id`, `username`, `email`, `password`, `date_joined`, `last_login`

### Character
- `id`, `name`, `description`, `faction`, `health`, `hand_limit`

### Card
- `id`, `character_id (FK)`, `name`, `speed`, `damage`, `hit_area`, `effects`, `image_url`, `keywords`

### Tag
- `id`, `name`, `description`

### CardTag (중개 테이블)
- `id`, `card_id (FK)`, `tag_id (FK)`

### Deck
- `id`, `author_id (FK)`, `name`, `character_id (FK)`, `description`, `private`, `created_at`

### CardInDeck
- `id`, `deck_id (FK)`, `card_id (FK)`, `count`, `side`, `hand`

### Pack
- `id`, `name`, `code`, `release_date`

### CollectionCard
- `id`, `card_id (FK)`, `pack_id (FK)`, `rarity`, `code`, `name`, `image_url`

### Collected
- `id`, `user_id (FK)`, `collection_card_id (FK)`, `amount`

### QNA
- `id`, `title`, `question`, `answer`, `faq`, `created_at`

### QNACard (중개 테이블)
- `id`, `qna_id (FK)`, `card_id (FK)`

---
