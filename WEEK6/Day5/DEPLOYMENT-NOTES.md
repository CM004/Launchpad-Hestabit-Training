
DAY 5 - HOUSE PRICE CLASSIFIER DEPLOYMENT 
=========================================

Day5
├── API: Running & Predicting
├── Logs: prediction_logs.csv (created)
├── Drift: Monitoring working (DRIFT detected)
├── Docker: Built & Ready
└── Model: Loaded successfully

CURRENT STRUCTURE (Day5/)
========================
![alt text](image.png)

QUICK START COMMANDS
================
# 1. LOCAL API (Terminal 1)
source venv/bin/activate
uvicorn src.deployment.api:app --host 0.0.0.0 --port 8000 --reload

![alt text](<screenshots/Screenshot from 2025-12-23 18-12-54.png>)

# 2. TEST API (Terminal 2)
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"longitude":-122.23,"latitude":37.88,"housing_median_age":41,"total_rooms":880,"total_bedrooms":129,"population":322,"households":126,"median_income":1.23}'

![alt text](<screenshots/Screenshot from 2025-12-23 18-16-08.png>)

# 3. CHECK LOGS
tail prediction_logs.csv

timestamp,request_id,prediction,probability,longitude,latitude,housing_median_age,total_rooms,total_bedrooms,population,households,median_income
2025-12-23T11:20:27.424560,eb26f24c-9010-49da-8dbb-bc2406002502,1,0.7088514566421509,-122.23,37.88,41.0,880.0,129.0,322.0,126.0,1.23
2025-12-23T11:21:10.172178,de78d975-9a7a-40a4-85f1-7b5358efed37,1,0.7088514566421509,-122.23,37.88,41.0,880.0,129.0,322.0,126.0,1.23
2025-12-23T11:21:26.335416,cc4c41ab-35be-401a-a59c-617b755e7f59,1,0.7088514566421509,-122.23,37.88,41.0,880.0,129.0,322.0,126.0,1.23
2025-12-23T11:21:35.551442,7498308f-56e8-4d2e-96f9-a3256862d8a5,1,0.9322736859321594,-122.23,37.88,20.0,2000.0,400.0,800.0,300.0,5.0
2025-12-23T11:24:22.697931,c73af298-3655-4a00-a48f-c17df39dad06,1,0.7088514566421509,-122.23,37.88,41.0,880.0,129.0,322.0,126.0,1.23
2025-12-23T12:16:27.889360,992c8e4a-4288-4dd0-87cf-b60de1b92c17,1,0.7088514566421509,-122.23,37.88,41.0,880.0,129.0,322.0,126.0,1.23

# 4. DRIFT MONITORING
python3 monitoring/drift_checker.py
Output: {'total_bedrooms': 'DRIFT', 'population': 'DRIFT', ...}

![alt text](<screenshots/Screenshot from 2025-12-23 18-14-58.png>)

# 5. DOCKER (Production)
docker build -t house-classifier -f deployment/Dockerfile .
docker run -p 8000:8000 house-classifier

![alt text](<screenshots/Screenshot from 2025-12-23 18-12-04.png>)

![alt text](<screenshots/Screenshot from 2025-12-23 18-12-17.png>)

![alt text](<screenshots/Screenshot from 2025-12-23 18-10-22.png>)

![alt text](<screenshots/Screenshot from 2025-12-23 18-10-07.png>)

![alt text](<screenshots/Screenshot from 2025-12-23 18-11-11.png>)

![alt text](<screenshots/Screenshot from 2025-12-23 18-17-24.png>)

![alt text](<screenshots/Screenshot from 2025-12-23 18-18-00.png>)

![alt text](<screenshots/Screenshot from 2025-12-23 18-18-36.png>)

EXPECTED RESPONSES
================
HEALTH:        {"status": "ok", "model_loaded": True}
PREDICTION:    {"request_id": "uuid", "prediction": 0, "probability": 0.456}
DRIFT:         {'longitude': 'DRIFT', 'latitude': 'OK', ...}

ENDPOINTS WORKING
================
GET    http://localhost:8000/          # Status
POST   http://localhost:8000/predict   # Classify house
GET    http://localhost:8000/health    # Health check

