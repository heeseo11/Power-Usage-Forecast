# 전력 사용량 예측 

### 데이터 전처리 및 데이터 탐색

#### **train 데이터** 

![image](https://user-images.githubusercontent.com/61724682/127728960-1bd94528-1941-4fd7-9660-99fb7d0ac03b.png)

  - 60개 건물들의 2020년 6월 1일 부터 2020년 8월 24일까지의 데이터
  - 1시간 단위로 제공
  - 전력사용량(kWh) 포함 
  - train.shape: (122400, 10)

#### **test 데이터**

![image](https://user-images.githubusercontent.com/61724682/127732812-e47ef05a-bbb5-4b7e-8a70-97d4b2ccb5ce.png)

  - 60개 건물들의 2020년 8월 25일 부터 2020년 8월 31일까지의 데이터
  - 3시간 단위로 제공(강수량의 경우 6시간 단위로 제공, 예보데이터)
  - 전력사용량(kWh) 미포함 => 예측 변수
  - test.shape: (10080, 9)
  
#### **파생변수 생성**

![image](https://user-images.githubusercontent.com/61724682/127732659-0b9a88d0-cdd4-4df5-9f21-570feff41cac.png)

  1. **시간 (time)**
      - 군집화를 위해 생성
      
  2. **요일 (weekend)**
      - 군집화를 위해 생성
     
  3. **불쾌지수 (discomfort)**
      - 1.8 * 기온 - 0.55 * (1-습도) * (1.8 * 기온 - 26) + 32
    
  4. **체감온도 (sensible)**
      - 13.12+0.6215*T-11.37*V+0.3965V*T (T:기온 , V:풍속)
    
  5. **코로나 확진자 수 변수 생성 (조인 id : date / 누적 확진자 : decideCnt / 일별 확진자 : corona_count)**
      - [open API 활용](https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15043376)

  6. **군집화 변수 추가**
   
          1. 시계열 간의 유사도 판단
          - Euclidean
           - 유클리디안 거리 계산
           - time series.길이가 같을 경우에 사용 가능

          - DTW
           - 두 개의 시간 sequence의 유사도를 측정하는 알고리즘
           - sequence 길이가 달라도 유사도 측정 가능

          2. Euclidean 과 DTW 비교

          - 최종적으로 euclidean사용

          - DTW 단점
           - 모든 시간대를 비교하기 떄문에 관계 없는 시간대까지 알고리즘 결과에 반영될 수 있음
           - 최소 거리를 과도하게 매칭하면 정확도가 떨어짐

          - 결론 : 데이터의 시간대가 똑같아서 오히려 DTW 사용시 다른 트렌드끼리 묶이는 경향이 있는 것 같음

      - **시간별 전력사용량에 따라 건물 유형 군집화** 

        - cluster0 : 뚜렷한 특징 없음
        - cluster1 : 출근시간에 뚜렷하게 높음
        - cluster2 : 새벽시간(5시경)부터 저녁(20시경)까지 증가추세

        ![image](https://user-images.githubusercontent.com/61724682/127873877-5ecd5648-8144-4770-b5e8-145384ae1596.png)

      - **요일별 전력사용량에 따라 건물 유형 군집화** 

        - cluster0 : 일주일 내내 큰 변화없음 or 뚜렷한 특징 없음 
        - cluster1 : 평일 > 주말
        - cluster2 : 평일 < 주말

        ![image](https://user-images.githubusercontent.com/61724682/127873837-b13e677a-52bb-4086-be29-f10d9eb02084.png)

      - **최종 클러스터**
      - 위의 군집화를 바탕으로 경우의 수를 구해서 총 4개의 cluster를 생성(0,1,2,3)
        - cluster(요일_클러스터, 시간_클러스터)
        - cluster0 (0) : 뒤죽박죽
        - cluster1 (1,1) : 평일 활동시간
        - cluster2 (1,2) : 평일 저녁시간
        - cluster3 (2,1) : 주말 활동시간
        - ~~cluster4 (2,2) : 주말 저녁시간~~

        ![image](https://user-images.githubusercontent.com/61724682/127874205-c2ab361c-b04f-4757-9c9d-3c0a69850497.png)


 #### **데이터 변수 유형 및 설명**

     - num: 건물 번호(1~60) (범주형 변수) 
     - date_time : 각 변수의 측정 시간 (time) 
     - 기온(°C) (tempe(°C)) : 기온 (연속형 변수)
     - 풍속(m/s) (wind(m/s)) : 풍속 (연속형 변수)
     - 습도(%) (hum(%)) : 습도 (연속형 변수)
     - 강수량(mm, 6시간) (rain(mm)) : 강수량 (연속형 변수)
     - 일조(hr, 3시간) (sol(hr)) : 일조 (연속형 변수)
     - 비전기냉방설비운영 (ne_cool) : 0(운영X)과 1(운영O) (범주형 변수)
     - 태양광 보유 (sol_energy) : 0(보유X)과 1(보유O)(범주형 변수)
     - time: 한시간 단위로 측정됨 0~23 (범주형 변수)
     - weekday: 요일 0:월 / 1:화 / 2:수 / 3:목 / 4:금 / 5:토 / 6:일 (범주형 변수)
     - 전력사용량(kWh): 전력사용량 (연속형 변수)
     - 불쾌지수(discomfort) : 불쾌지수 (연속형 변수)
     - 체감온도(sensible) : 체감온도 (연속형 변수)
     - 누적 확진자 (decideCnt) : 코로나 누적 확진자 (연속형 변수)
     - 일별 확진자 (corona_count) : 코로나 일별 확진자 (연속형 변수)
     - 시간별 군집 변수 () : 시간별 전력 사용량 군집 변수 (범주형 변수)   
     - 요일별 군집 변수 () : 요일별 젼력 사용량 군집 변수 (범주형 변수)
    
#### **결측치 처리**
  
  - 결측치 선형 보간 방법 활용
    - test 결측값 보간하기
    - test 데이터의 변수는 예보 데이터이며, 예보 데이터는 train 데이터의 기간에 생성된 것이기에 활용 가능
    - interpolate(method='values') 
      - DataFrame 값에 선형으로 비례하는 방식으로 결측값 보간
      - 결과 plot : 선형으로 결측치가 처리됨
      - <img src = "https://user-images.githubusercontent.com/61724682/127728869-9adf2ef9-c611-46cc-a4ef-76eca0176f52.png" width="40%" height="40%">



#### 시계열 분해

  - 시계열 분해를 통해 건물별 전력사용량을 추세, 계절성, 잔차로 분해

    - example : 건물 1번

![image](https://user-images.githubusercontent.com/61724682/127875948-541aafbf-a9ac-4584-a7a7-a46222237dba.png)

#### cluster별 상관분석

  - cluster0

![image](https://user-images.githubusercontent.com/61724682/127876639-02a68b44-3fed-4046-be8c-21444af5814d.png)

  - cluster1

![image](https://user-images.githubusercontent.com/61724682/127876663-92a3a687-4fd5-40d1-9d1f-82e60bf4b660.png)

  - cluster2

![image](https://user-images.githubusercontent.com/61724682/127876679-aab476ad-cc89-4e93-bbfe-2bf8718903c1.png)

  - cluster3

![image](https://user-images.githubusercontent.com/61724682/127876705-5926e819-99ca-4397-9a22-19942b2a143d.png)




-------------------------------


## Model

### RNN
##### 단순 RNN 모델은 입력을 순차적으로 받고 반복적으로 출력을 업데이트 하는 모델임 
<img src = "https://user-images.githubusercontent.com/61724682/172044000-a4b07756-dc3f-4727-8662-510de5830f56.png" width="40%" height="40%">

### LSTM
##### RNN의  문제인 장기 의성을 해결하기 위해 Long Term Memory와Short Term Memory를 함께 가지도록 만든 모델
<img src = "https://user-images.githubusercontent.com/61724682/172044023-afed3b0f-db02-420f-88f4-12e618bbc505.png" width="40%" height="40%">

### GRU
##### LSTM의  간소화된   버전
<img src = "https://user-images.githubusercontent.com/61724682/172044008-22cb99fc-83f8-48b5-85c8-ad45d2ea27b7.png" width="40%" height="40%">

## data 생성 

### time step 5로 설정

![image](https://user-images.githubusercontent.com/61724682/178744352-809aa691-f23c-4210-98c6-6a18895d3ad3.png)

## 평가지표

  - SMAPE는 Symmetric Mean Absolute Percentage Error

  - MAPE의 경우 Actual 값이 0이거나 작은 경우 MAPE값이 지나치게 커지는 문제가 있으므로 SMAPE는 이를 개선한 Metric

![image](https://user-images.githubusercontent.com/61724682/178745089-1a91d168-6b9d-48cd-846b-35dbff0ec94d.png)

## 결과
![image](https://user-images.githubusercontent.com/61724682/178744661-1352645e-8082-410c-ab7e-86d0431344bd.png)

  - SMAPE가 가장 작은 Simple RNN의 성능이 가장 좋음.
  - 60개의 각각 건물에 대한 개인화된 모델을 생성
  - epoch : 기본 100 (early stop을 설정하여 loss값이 3번이상 발산하면 학습 중단)
  - activation function : linear
  - hidden size : 10
  - optimizer : Adam
  - batch size : 8


## 건물별 예측 plot 
![image](https://user-images.githubusercontent.com/61724682/178744135-c94a968f-28e9-4607-8617-565ebefd725e.png)

  - test에 대한 실제 값은 제공되지 않음 따라서 건물별 예측 정확도는 산출하지 못함.  

## time series 영상
![image](https://user-images.githubusercontent.com/61724682/178744007-48a7c94e-69ff-46a2-829b-2271724d1152.png)

