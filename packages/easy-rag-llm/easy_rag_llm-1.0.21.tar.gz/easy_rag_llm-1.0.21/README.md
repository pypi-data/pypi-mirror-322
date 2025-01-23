# easy_rag_llm

## CAUTION
- easy-rag-llm==1.0.* version is testing version. These versions are usually invalid.

## 🇰🇷 소개
- easy_rag_llm는 OpenAI 및 DeepSeek 모델을 지원하는 간단한 RAG(정보 검색 및 생성) 기반 서비스를 제공합니다. 간단하게 RAG LLM을 서비스에 통합시킬 수 있도록 만들어졌습니다.
- (2025.01.16 기준/ v1.1.0) 학습가능한 자료 포맷은 PDF입니다.

## 🇺🇸 Introduction
- easy_rag_llm is a lightweight RAG-based service that supports both OpenAI and DeepSeek models.
It is designed to seamlessly integrate RAG-based LLM functionalities into your service.
- As of 2025-01-15 (v1.1.0), the supported resource format for training is PDF.

## Usage
#### Install (https://pypi.org/project/easy-rag-llm/)
```bash
pip install easy_rag_llm
```

#### How to integrate to your service?
```python
from easy_rag import RagService

rs = RagService(
    embedding_model="text-embedding-3-small", #Fixed to OpenAI model
    response_model="deepseek-chat",  # Options: "openai" or "deepseek-chat"
    open_api_key="your_openai_api_key_here",
    deepseek_api_key="your_deepseek_api_key_here",
    deepseek_base_url="https://api.deepseek.com",
)

rs2 = RagService( # this is example for openai chat model
    embedding_model="text-embedding-3-small",
    response_model="gpt-3.5-turbo",
    open_api_key="your_openai_api_key_here",
)

# Learn from all files under ./rscFiles
resource = rs.rsc("./rscFiles", force_update=False, max_workers=5, embed_workers=10) # default workers are 10.

query = "Explain what is taught in the third week's lecture."
response, top_evidence = rs.generate_response(resource, query, evidence_num=5) # default evidence_num is 3.

print(response)
```

### 🇰🇷 안내.
- pdf 제목을 명확하게 적어주세요. 메타데이터에는 pdf제목이 추출되어 들어가며, 답변 근거를 출력할때 유용하게 사용될 수 있습니다.
- `rs.rsc("./folder")` 작동시 `faiss_index.bin`과 `metadata.json`이 생성됩니다. 이후엔 이미 만들어진 .bin과 .json으로 답변을 생성합니다. 만약 폴더에 새로운 파일을 추가하거나 제거하여 변경하고 싶다면 `force_update=True`로 설정하여 강제업데이트가 가능합니다.
- max_worker는 pdf 분할 병렬처리를 위한 동시작업 개수이고, embed_worker는 임베딩 작업 병렬처리를 위한 동시작업 개수입니다. 둘다 기본값 10으로 각각 CPU 코어개수와 api ratelimit에 영향을 받으므로 적절히 조절해야합니다.

### 🇺🇸 Note.
- Ensure that your PDFs have clear titles. Extracted titles from the PDF metadata are used during training and for generating evidence-based responses.
- Running `rs.rsc("./folder")` generates `faiss_index.bin` and `metadata.json` files. Subsequently, the system uses the existing .bin and .json files to generate responses. If you want to reflect changes by adding or removing files in the folder, you can enable forced updates by setting `force_update=True`.

### release version.
- 1.0.12 : Supported. However, the embedding model and chat model are fixed to OpenAI's text-embedding-3-small and deepseek-chat, respectively. Fixed at threadpool worker=10, which may cause errors in certain environments.
- 1.1.0 : LTS version.

### TODO
- 폴더기반 정리 지원. ./rscFiles 입력했으면 rscFilesIndex 생성하고
그 아래로 인덱스 정리.
index/아래에 생성된 임베딩이 있으면 그거 쓰도록 함.
- Replace threadPool to asyncio (v1.2.* ~)
- L2 기반 벡터검색외 HNSW 지원. (체감성능 비교) (v1.3.0~)
- 입력포맷 다양화. pdf외 지원. (v1.4.* ~)


### What can you do with this?
https://github.com/Aiden-Kwak/ClimateJudgeLLM



### Author Information
- 곽병혁 (https://github.com/Aiden-Kwak)
