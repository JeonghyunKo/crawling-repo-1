# 유튜브 채널 크롤링을 통한 트렌드 분석 프로젝트


![nordwood-themes-8LfE0Lywyak-unsplash-2](https://user-images.githubusercontent.com/80465347/128330807-7eeb4c07-3877-4708-9bd1-4d2a4deeda1b.jpg)


2020년 기준 한국인이 가장 많이 사용하는 앱 1위가 바로 Youtube라고 합니다.

그런 만큼 소셜블레이드, 블링 등 이미 활발하게 운영 중인 유튜브 분석 서비스들은 많습니다. 하지만 대체로 개별 채널 단위의 분석(이를테면, '어느 분야에서는 누가 잘 나가는가?'와 같은 질문에 포커스를 두고 있습니다.)이 목적이고, 유튜브를 산업의 관점에서 보는 서비스는 없습니다.

이에 저희가 착안한 부분은 특정 산업과 연관된 채널들을 크롤링하여, 산업 현황을 파악해보자는 것입니다. 특정 산업과 연관된 브랜드 채널, 인플루언서 채널의 정보를 수집함으로써 광고주나, 산업의 이해관계자들을 대상으로 간편하게 볼 수 있는 일종의 트렌드 리포트를 제공할 수 있을 것이라 생각했습니다. 뿐만 아니라 다른 산업군에도 이와 동일한 구조를 적용할 수 있어 산업별로 확장이 가능할 수 있습니다. 
(참고. 이번 프로젝트에서는 자동차 산업을 대상으로 하였습니다. 크롤링 대상 채널 등 세부적인 내용은 [발표자료](https://drive.google.com/file/d/1jGTwHEqVpJSZVmavaZ-DgCPNKNqHfmKO/view?usp=sharing)에 첨부되어 있습니다.) 


## 1. Project Summary 


### 1.1 목적 

유튜브 채널 데이터에 기반한 산업 트렌드 분석 


### 1.2 대상 사이트 

- 대상 사이트는 Youtube이며, Youtube에서는 공식 API를 제공하여 데이터 수집이 용이합니다. [Youtube API Document 보기](https://developers.google.com/youtube/v3/getting-started?hl=ko) 
- 채널명, 채널 구독자 수 등의 채널 기본 정보, 동영상 별 좋아요, 조회수 등의 지표, 댓글 등 다양한 항목을 수집할 수 있습니다.  
- 다만 수집 항목과 구조가 세분화되어 있기 때문에 크롤링을 단계화하여 순차적으로 진행할 필요가 있으며, 일 쿼리량 제한도 고려해야 합니다.  
- 또한 채널에 따라 댓글을 달지 못하게 막아두었거나, 구독자 수를 표시하지 않게 해놓는 등 다양한 옵션이 있어 이에 대한 예외 처리를 고려해야 했습니다. 
- 크롤링 단계
  - 1. 채널 ID 수집
   - 1.1. 채널 ID를 기준으로 해당 채널의 기본 정보 수집 
  - 2. 채널 ID를 기준으로 해당 채널에 생성되어 있는 재생목록 ID 수집
  - 3. 재생목록 ID를 기준으로 해당 재생목록 내의 동영상 ID 수집 
  - 4. 동영상 ID를 기준으로 동영상 정보 수집  


### 1.3 결과

총 13개의 자동차 브랜드 채널, 9개의 인플루언서 채널을 크롤링하여 
측정 지표에 대한 주간 증가량이 가장 많은 채널, 주간 인기동영상 등의 정보를 제공하는 웹 어플리케이션을 제작하였습니다. 
<img width="666" alt="image" src="https://user-images.githubusercontent.com/80465347/128343905-11602bc3-9b63-4a68-b8aa-7191c27ec03a.png">


### 1.4 진행순서 

- 크롤링 기획 : 채널 및 항목 선정
- 크롤러 제작(+주기적 크롤링 시작)  
- 데이터베이스 셋팅(+Power BI를 이용한 리포트 초안 제작)   
- 크롤링 자동화
- 웹 어플리케이션 제작 


### 1.5 구조
<img width="644" alt="image" src="https://user-images.githubusercontent.com/80465347/128333248-d3518160-53a1-43a2-820d-254c83e1225c.png">



## 2. Contributors

* [정현](https://github.com/JeonghyunKo) - 크롤링 / Flask / 디자인 / README
* [동주](https://github.com/lee-edgar) - 크롤링 / Flask / 서버 
* [상윤](https://github.com/metahong) - 데이터베이스 / 기획 및 PowerBI 


## 3. What We Learned, and more... 

- 심화된 댓글 분석 결과를 반영하고 싶었으나, 프로젝트 기간 내에는 진행하지 못하여 아쉽습니다. 또한 프로토타입은 완성되었지만 내부적으로 일부 완성도가 부족한 면이 있습니다. 이 부분을 반영하여 프로젝트 종료 후에도 꾸준히 개선해나갈 예정입니다. 
- DB 스키마를 수정하여 데이터를 가져올 때 웹 어플리케이션의 반응속도를 높일 필요가 있습니다. 


## 4. Acknowledgments 

* [Radajin](https://github.com/radajin)  


## 프레젠테이션 

* [최종 발표자료](https://drive.google.com/file/d/1jGTwHEqVpJSZVmavaZ-DgCPNKNqHfmKO/view?usp=sharing)
* [이미지 출처](https://unsplash.com/photos/8LfE0Lywyak?utm_source=unsplash&utm_medium=referral&utm_content=creditShareLink)

## 진행중인 후속작업

* 웹 어플리케이션의 반응속도 저하 문제로 DB 스키마 수정 필요 
* AWS 서버 작업  
