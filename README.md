# main
하하호호 신나는 웹 개발


## 파이썬, Django 버전

>$ python --version

Python 3.9.0

> $ python -m django --version

4.2.16

# PATCH
09/27
  - cvss 그래프 구현

09/30
  - epss 그래프 구현

10/02
  - /analytics/?cpe={cpe}로 GET 전송시 해당 cpe의 분석 그래프를 출력.
  - cpe 검색 후 클릭하면 해당 url로 뛰게하면 그래프가 출력되게 만들면 좋을듯.

## 디렉토리 구조 
.  
├── search_engine _` ← 기본 Project`_  
│   ├── search_engine _` ← 기본 App`_  
│   ├── analytics _` ← 분석 결과 출력 App`_  
│   ├── api_search _` ← api 사용한 검색 App`_  
│   └── home _` ← 서비스 메인 화면 App`_  

