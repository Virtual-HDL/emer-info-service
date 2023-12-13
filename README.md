# 응급행

## 기획 의도
> 복잡하고 느린 기존의 응급 정보 제공 서비스를 탈피   
> 응급 상황에서 증상별로 빠르고 간단하게 주변 응급실 정보를 제공!

## Skills
- python 3.11.1
- Streamlit
- OpenAPI
    - 국립중앙의료원_전국 병·의원 찾기 서비스
    - 국립중앙의료원_전국 응급의료기관 정보 조회 서비스

## 실행
1. config.json 수정
> 각 API에 해당하는 Key 입력
```json
{
    "ErmctInfoInqireService": "",
    "HsptlAsembySearchService": ""
}
```
2. 라이브러리 설치
```bash
pip install -r requirements.txt
```

3. streamlit 실행
```bash
streamlit run Index.py
```