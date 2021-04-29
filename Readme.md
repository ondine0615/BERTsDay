![버츠데이 우리팀](https://user-images.githubusercontent.com/79948405/116493353-805ed400-a8d9-11eb-8d33-0b28518328eb.jpg)

## 1. 프로젝트 주제
- BERT 기반 슬롯태깅을 활용한 스터디룸 예약 챗봇

## 2. 프로젝트 개요
- 사전훈련된 BERT에 슬롯태깅 테스크를 수행하는 레이어를 붙여 미세조정 훈련을 진행하여 스터디룸 예약 요청 문장을 처리하는 모델을 만들고, 문장을 처리한 결과물을 활용하여 스터디룸에 예약에 필요한 정보를 질문하는 규칙 기반 멀티턴 챗봇을 만들어 웹으로 구현하였다.

## 3. 프로젝트 구현 과정
3-1. 프로젝트 사전 교육
	- 먼저 BERT를 활용하기 위해 필요한 딥러닝 기반 자연어처리 이론, Bash와 파이썬 기초에 대하여 1주차에 학습했으며, 2주차와 3주차에 걸쳐서는 크롤링과 정규표현식을 활용하여 직접 BERT 사전학습에 필요한 데이터를 구축해보고 사전훈련을 진행해 보았다.

3-2. 프로젝트 준비 및 구현
	- 프로젝트 주제를 정한 뒤 슬롯태깅 미세조정을 위한 데이터를 구축했다. 슬롯은 다른 스터디룸 업체들의 예약 시스템을 참고하여 <이름>, <전화번호>, <사용인원>, <예약날짜>, <시작시간>, <종료시간> 총 6가지로 구성하였다. 해당 슬롯이 아예 없는 문장부터 전부 있는 문장까지 다양한 문장으로 예약 요청 문장을 생성하였다. 문장을 생성하는 데에는 파이썬 코드를 사용하여 총 3000여 문장을 생성하고, 해당 데이터를 보완하기 위해 1000여 문장을 직접 수기로 생성하였다.

	- 구축한 문장 데이터를 사용하여 슬롯태깅 테스크를 위한 파인튜닝(미세조정) 훈련을 진행하였다. 이후 평가 코드를 돌려 훈련한 미세조정 모델 성능을 확인한 뒤, 해당 모델을 웹 프레임워크인 플라스크와 연동하여 웹으로 띄울 수 있도록 했다.

	- 이후 예약 요청 문장인 인풋 문장을 인퍼런스 한 결과물에 대하여, 해당 문장에 포함되어 있지 않은 슬롯에 대해 질문을 하는 대화 형태를 위한 조건문을 코드로 구현하여 챗봇 스크립트에 추가하였다. 

	- 이러한 과정을 통해 챗봇 사용자가 보내는 첫 예약 요청 인풋 문장에 모든 슬롯이 포함되어 있지 않더라도, 슬롯 태깅 모델을 사용하여 비어있는 슬롯을 파악하고, 이후 룰 기반 멀티턴 대화를 통해 빈 슬롯을 채워나가며 최종적으로는 챗봇 사용자가 스터디룸 예약에 필요한 모든 정보를 전달할 수 있도록 구현하였다.

	- 스터디룸 예약에 필요한 모든 슬롯이 채워지면 해당 정보를 사용하여 대화 이후 챗봇 사용자의 전화번호로 예약이 완료된 문자메세지를 전송하도록 구현하였다.


## 실행 방법

---
1. 여기에 있는 소스 파일들 이외에도 `Bert_pretrained, Fine_tuned` 폴더가 있는지 확인해주세요
    - `Bert_pretrained`는 모듈화된 프리트레인 모델이 들어갑니다
    - `Fine_tuned`는 공동 드라이브의 `프로젝트관련자료` 내에 `Fine_tuned`라는 폴더가 있습니다. 그것을 다운받아서 넣어주세요
2. Anaconda Propmpt를 실행해주세요
3. `conda activate {가상환경 이름}` 실행
4. `pip install -r requirements.txt`로 필요한 패키지 설치
5. `cd /d {프로젝트 최상위 디렉토리}`  실행
6. `python web_demo/run.py` 실행
