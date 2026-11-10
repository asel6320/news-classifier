# 📰 BERT News Classifier

**BERT 기반 뉴스 기사 자동 분류 시스템**

뉴스 기사의 텍스트를 분석하여 **Business(경제), Sports(스포츠), Technology(기술)** 세 가지 카테고리 중 하나로 자동 분류하는 자연어 처리(NLP) 프로젝트입니다.

본 프로젝트는 Google Colab 환경에서 사전 학습된 BERT 모델을 Fine-tuning하여 구현하였으며, 학습된 모델을 활용한 뉴스 분류 웹 애플리케이션을 제공합니다.

학습된 모델의 가중치는 향후 **Hugging Face Hub**에서 다운로드하도록 구성하여 GitHub 저장소의 용량을 줄이고 배포 과정을 간소화할 예정입니다.

---

## 🚀 주요 기능

- BERT 기반 뉴스 기사 자동 분류
- Business, Sports, Technology 3개 카테고리 지원
- 사전 학습된 BERT 모델 Fine-tuning
- 뉴스 텍스트 전처리 및 토큰화
- 카테고리별 예측 확률 계산
- 웹 인터페이스를 통한 뉴스 분류
- 학습 모델 성능 평가
- Docker 기반 실행 환경 구성
- Hugging Face Hub를 이용한 모델 가중치 관리 *(전환 예정)*

## 🧠 모델 및 학습 방법

### 1. 기본 모델

사전 학습된 Hugging Face Transformers 모델을 사용했습니다.

```python
model_checkpoint = "bert-base-uncased"
```

BERT는 문장의 양방향 문맥을 학습하는 Transformer 기반 언어 모델입니다.

본 프로젝트에서는 `BertForSequenceClassification` 구조를 사용하여 뉴스 기사를 세 가지 카테고리로 분류하도록 Fine-tuning하였습니다.

### 2. 데이터셋

**AG News Dataset**을 사용했습니다.

원본 데이터셋에는 네 가지 카테고리가 포함되어 있으나, 본 프로젝트에서는 World 카테고리를 제외하고 세 가지 카테고리만 사용했습니다.

| Label | 카테고리 |
|---|---|
| 0 | Business |
| 1 | Sports |
| 2 | Technology |

학습 및 평가 데이터 구성:

| 구분 | 데이터 수 |
|---|---:|
| Training | 90,000 |
| Test | 5,700 |
| **전체** | **95,700** |

### 3. 텍스트 전처리

뉴스 기사의 Description을 대상으로 다음 전처리 과정을 수행했습니다.

- 소문자 변환
- URL 제거
- HTML 태그 제거
- 불필요한 특수문자 제거
- 중복 공백 제거
- BERT Tokenizer 적용
- 최대 토큰 길이 128로 제한

### 4. 학습 설정

| 항목 | 설정 |
|---|---|
| Base Model | bert-base-uncased |
| Epochs | 3 |
| Learning Rate | 2e-5 |
| Batch Size | 16 |
| Max Sequence Length | 128 |
| Optimizer | AdamW |
| Loss Function | CrossEntropyLoss |
| Training Environment | Google Colab |
| GPU | NVIDIA Tesla T4 |

---

## 📊 모델 성능

Fine-tuning 완료 후 5,700개의 테스트 데이터로 모델 성능을 평가했습니다.

<box gap={2}>
  <text color="secondary" weight="medium" size="xs">TEST ACCURACY</text>
  <title size="2xl" color="default" tabularNums={true}>94.54%</title>
</box>

### 분류 성능

| Category | Precision | Recall | F1-score |
|---|---:|---:|---:|
| Business | 0.9367 | 0.9116 | 0.9240 |
| Sports | 0.9817 | 0.9889 | 0.9853 |
| Technology | 0.9179 | 0.9358 | 0.9268 |
| **Weighted Avg** | **0.9455** | **0.9454** | **0.9454** |

### 학습 Loss

| Epoch | Loss |
|---|---:|
| 1 | 0.1716 |
| 2 | 0.1095 |
| 3 | 0.0735 |

학습이 진행됨에 따라 Loss가 감소하였으며, 최종 테스트 Accuracy는 94.54%를 기록했습니다.

---

## 🏗 시스템 아키텍처

현재 프로젝트는 프론트엔드, 백엔드 및 학습된 BERT 분류 모델로 구성되어 있습니다.

```text
            사용자
               │
               ▼
         Frontend UI
               │
               ▼
           Backend
               │
               ▼
       Text Preprocessing
               │
               ▼
         BERT Tokenizer
               │
               ▼
       Fine-tuned BERT
               │
               ▼
      Classification Result
               │
      ┌────────┼─────────┐
      ▼        ▼         ▼
   Business  Sports  Technology
```

### Hugging Face 연동 계획

모델 가중치를 GitHub에서 분리하여 Hugging Face Hub에 저장할 예정입니다.

```text
         GitHub Repository
                 │
                 ▼
          Backend 실행
                 │
                 ▼
          Hugging Face Hub
                 │
                 ▼
       Fine-tuned BERT 다운로드
                 │
                 ▼
          Model Pipeline
                 │
                 ▼
          뉴스 카테고리 예측
```

이를 통해 대용량 모델 파일을 GitHub에 직접 포함하지 않고 애플리케이션을 배포할 수 있습니다.

---

## 📁 프로젝트 구조

```text
news-classifier/
│
├── backend/
│   └── 백엔드 애플리케이션
│
├── frontend/
│   └── 프론트엔드 애플리케이션
│
├── classifier_clean/
│   └── 학습된 BERT 모델 및 Tokenizer
│
├── screenshots/
│   └── 프로젝트 실행 화면
│
├── Dockerfile
├── requirements.txt
├── .gitignore
│
└── README.md
```

향후 Hugging Face Hub 연동이 완료되면 `classifier_clean/`의 대용량 모델 가중치를 GitHub에서 제거하고, 실행 시 Hugging Face에서 모델을 불러오도록 변경할 예정입니다.

---

## 🤗 Hugging Face 모델 연동

학습된 모델은 Hugging Face Hub에서 관리할 예정입니다.

**예정 모델 저장소:**

`asel6320/news-classifier`

### 모델 업로드

Google Colab에서 학습 완료 후 모델과 Tokenizer를 저장합니다.

```python
SAVE_PATH = "/content/classifier_clean"

model.save_pretrained(SAVE_PATH)
tokenizer.save_pretrained(SAVE_PATH)
```

Hugging Face Hub에 업로드합니다.

```python
from huggingface_hub import HfApi

api = HfApi(endpoint="https://huggingface.co")

api.create_repo(
    repo_id="asel6320/news-classifier",
    repo_type="model",
    exist_ok=True
)

api.upload_folder(
    folder_path="/content/classifier_clean",
    repo_id="asel6320/news-classifier",
    repo_type="model"
)
```

### 모델 다운로드 및 추론

업로드가 완료되면 애플리케이션에서 모델을 직접 불러올 수 있습니다.

```python
from transformers import pipeline

classifier = pipeline(
    "text-classification",
    model="asel6320/news-classifier"
)

result = classifier(
    "Apple announced a new artificial intelligence system."
)

print(result)
```

모델 파일은 최초 실행 시 Hugging Face에서 다운로드되며, 이후 로컬 캐시를 활용할 수 있습니다.

**참고:** 위 코드는 Hugging Face 연동을 위한 예시이며, 실제 백엔드 적용은 별도로 진행할 예정입니다.

---

## 🛠 기술 스택

| 구분 | 기술 |
|---|---|
| Language | Python |
| Deep Learning | PyTorch |
| NLP | Hugging Face Transformers |
| Model | BERT (bert-base-uncased) |
| Dataset | AG News |
| Evaluation | Scikit-learn |
| Model Hosting | Hugging Face Hub (예정) |
| Training | Google Colab |
| Containerization | Docker |
| Version Control | Git, GitHub |

---

## 🐳 Docker 실행

### 1. 저장소 복제

```bash
git clone https://github.com/asel6320/news-classifier.git
cd news-classifier
```

### 2. Docker 이미지 빌드

```bash
docker build -t news-classifier .
```

### 3. 컨테이너 실행

```bash
docker run --rm news-classifier
```

실제 웹 서비스 접속을 위한 포트 매핑 및 실행 설정은 프로젝트의 `Dockerfile`과 백엔드 구성에 따라 조정해야 합니다.

---

## 🧪 뉴스 분류 예시

### Technology

**Input**

```text
Apple announced a new artificial intelligence system for its devices.
```

**Prediction**

```text
Technology: 98.62%
Business: 1.33%
Sports: 0.05%
```

### Sports

**Input**

```text
The football team won the championship after scoring three goals.
```

**Prediction**

```text
Sports: 100.00%
Business: 0.00%
Technology: 0.00%
```

### Business

**Input**

```text
The company reported strong quarterly revenue and higher profits.
```

**Prediction**

```text
Business: 55.19%
Technology: 43.94%
Sports: 0.87%
```

---

## ⚠️ 제한 사항

- 영어 뉴스 기사 분류를 중심으로 학습되었습니다.
- 현재 세 가지 카테고리만 지원합니다.
- 학습 데이터와 다른 분야의 뉴스에서는 정확도가 낮아질 수 있습니다.
- 예측 확률은 모델의 출력값이며, 실제 정답 확률을 보장하지 않습니다.
- Hugging Face 모델 다운로드 기능은 백엔드에 적용할 예정입니다.

---

## 🎯 프로젝트 목표

본 프로젝트는 사전 학습된 BERT 모델을 Fine-tuning하여 실제 뉴스 분류 서비스에 적용하는 전체 과정을 구현하는 것을 목표로 합니다.

향후 Hugging Face Hub를 통해 모델 가중치를 별도로 관리하고, GitHub 저장소에는 애플리케이션 코드와 실행 환경만 유지하여 보다 효율적인 배포 구조로 개선할 예정입니다.

---

## 🔗 프로젝트 링크

**GitHub:** https://github.com/asel6320/news-classifier

**Hugging Face 모델 저장소(예정):** https://huggingface.co/asel6320/news-classifier
