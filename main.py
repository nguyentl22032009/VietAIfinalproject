import pandas as pd
import joblib
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel

# Khởi tạo FastAPI app
app = FastAPI()

# Tải pipeline đã được huấn luyện
try:
    pipeline = joblib.load('./model/medical_cost_prediction_pipeline.joblib')
    print("Model pipeline loaded successfully!")
except FileNotFoundError:
    print("Error: Model pipeline file not found. Please check the file path.")
    pipeline = None

# Định nghĩa cấu trúc dữ liệu đầu vào sử dụng Pydantic
class InsuranceData(BaseModel):
    age: int
    sex: str
    bmi: float
    children: int
    smoker: str
    region: str

# Định nghĩa endpoint '/predict' với phương thức POST
@app.post("/predict")
def predict(data: InsuranceData):
    """
    Nhận dữ liệu bệnh nhân và trả về dự đoán chi phí y tế.
    """
    if pipeline is None:
        return {"error": "Model not loaded"}
    try:

        data_dict = data.dict()
        input_df = pd.DataFrame([data_dict])
        # bmi_obese (BMI >= 30)
        input_df['bmi_obese'] = (input_df['bmi'] >= 30).astype(int)
        # smoker_encoded (mã hóa smoker thành số)
        smoker_map = {'yes': 1, 'no': 0}
        input_df['smoker_encoded'] = input_df['smoker'].map(smoker_map)

        input_df['age_smoker'] = input_df['age'] * input_df['smoker_encoded']
        # Sử dụng pipeline để dự đoán
        prediction_log = pipeline.predict(input_df)

        # Chuyển đổi kết quả dự đoán từ thang đo log về thang đo ban đầu 
        # Chúng ta đã dùng np.log1p(y) khi huấn luyện, nên giờ dùng np.expm1(y_pred) để đảo ngược
        prediction = np.expm1(prediction_log[0])

        # Trả về kết quả dưới dạng JSON
        return {"predicted_charge": float(prediction)}
    
    except Exception as e:
        print(f"Error in prediction: {str(e)}")
        return {"error": f"Prediction failed: {str(e)}"}

# Endpoint gốc để kiểm tra API có hoạt động không
@app.get("/")
def read_root():
    return {"message": "Welcome to the Medical Cost Prediction API"}

