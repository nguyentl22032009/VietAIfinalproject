# 🏥 Medical Cost Prediction App (Final Project - VietAI)

> **Final project của khóa học VietAI.**
> 
> 👉 **See it live:** [Hugging Face Spaces](https://huggingface.co/spaces/nguyentl2203/xgbmodelVietAI)
> 
> 📄 ***More at:*** baocao.pdf


Ứng dụng dự đoán chi phí y tế cá nhân sử dụng Machine Learning (XGBoost) với giao diện Streamlit và API FastAPI.

## 📁 Cấu trúc Project

```
root/
├── main.py                                    # FastAPI backend
├── app.py                                     # Streamlit frontend
├── notebook.ipynb                             # Jupyter notebook huấn luyện model
├── requirements.txt                           # Dependencies
├── README.md                                 # This
└── model/
    └── medical_cost_prediction_pipeline.joblib # Model đã huấn luyện bằng kaggle
```

## 🚀 Hướng dẫn Chạy Ứng dụng

> 📺 **Demo usage:** demo.mp4

### Bước 1: Cài đặt Dependencies

```bash
pip install -r requirements.txt
```

### Bước 2: Chạy FastAPI Backend

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

API sẽ chạy tại: http://127.0.0.1:8000

### Bước 3: Chạy Streamlit Frontend (Terminal mới)

```bash
streamlit run app.py
```

Giao diện web sẽ mở tại: http://localhost:8501

## 🎯 Cách Sử dụng

1. **Khởi động Backend**: Chạy FastAPI server trước
2. **Khởi động Frontend**: Chạy Streamlit app
3. **Nhập thông tin**: Điền các thông tin trong form
4. **Xem kết quả**: Nhấn nút "Dự đoán" để xem ước tính chi phí

## 📊 Thông tin Model

- **Algorithm**: XGBoost Regressor
- **Features**: age, sex, bmi, children, smoker, region + engineered features
- **Target**: charges (chi phí y tế hàng năm)
- **Performance**: R² score > 0.85

## 🔧 API Endpoints

### GET /
- Kiểm tra trạng thái API

### POST /predict
- Input: JSON với các trường age, sex, bmi, children, smoker, region
- Output: JSON với predicted_charge

Ví dụ request:
```json
{
    "age": 30,
    "sex": "male", 
    "bmi": 25.5,
    "children": 1,
    "smoker": "no",
    "region": "southeast"
}
```



---
*Ứng dụng được phát triển với ❤️ sử dụng Python, FastAPI, Streamlit và XGBoost*
