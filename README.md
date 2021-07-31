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

      - 시간별 전력사용량에 따라 건물 유형 군집화 

      - 요일별 전력사용량에 따라 건물 유형 군집화 

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



#### 시계열 군집 분석

-------------------------------

  - #시계열 군집 분석
- **최적 클러스터 수 찾기**
 - 시계열에서 최적 클러스터를 찾는 방법을 잘모루겠다
 - 그냥 kmean이랑 똑같이 해도되는건지

#시계열 간의 유사도 판단
- **Euclidean**
 - 유클리디안 거리 계산
 - time series.길이가 같을 경우에 사용 가능

- **DTW**
 - 두 개의 시간 sequence의 유사도를 측정하는 알고리즘
 - sequence 길이가 달라도 유사도 측정 가능

#Euclidean 과 DTW 비교

- **클러스터링 결과는 Euclidean이 깔끔함**

- **DTW 단점**
 - 모든 시간대를 비교하기 떄문에 관계 없는 시간대까지 알고리즘 결과에 반영될 수 있음
 - 최소 거리를 과도하게 매칭하면 정확도가 떨어짐

 
- **결론**: 데이터의 시간대가 똑같아서 오히려 DTW 사용시 다른 트렌드끼리 묶이는 경향이 있는 것 같음


#### 코로나 확진자 수에 따른 전력 사용량 연관성 확인


#### XGBOOST


#### LGBM

