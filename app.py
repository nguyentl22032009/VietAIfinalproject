# -*- coding: utf-8 -*-
import streamlit as st
import requests
import pandas as pd
import base64
import os


st.set_page_config(page_title="Dự đoán Chi phí Y tế", layout="wide")

bg_base64 = None
bg_path = "background.jpg"
if os.path.exists(bg_path):
    with open(bg_path, "rb") as img_file:
        bg_base64 = base64.b64encode(img_file.read()).decode()

if bg_base64:
    bg_css = f"""
    <style>
    .stApp {{
        background: #f8fafc;
        background-image: url('data:image/jpg;base64,{bg_base64}');
        background-size: cover;
        background-position: center center;
        background-repeat: no-repeat;
        min-height: 100vh;
    }}
    """
else:
    bg_css = """
    <style>
    .stApp {
        background: #f8fafc;
        min-height: 100vh;
    }
    """

st.markdown(bg_css + """
.main > div {
    background: rgba(255, 255, 255, 0.92);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 20px;
    margin: 10px;
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.10);
    border: 1px solid rgba(200, 200, 200, 0.18);
}

.stMetric {
    background: linear-gradient(135deg, #fffbe6 0%, #ffe0f7 100%);
    padding: 20px;
    border-radius: 15px;
    color: #2c3e50;
    text-align: center;
    box-shadow: 0 4px 15px 0 rgba(255, 182, 193, 0.10);
}

.stButton > button {
    background: linear-gradient(135deg, #ffb6b9, #fcdff0);
    color: #2c3e50;
    border: none;
    border-radius: 25px;
    padding: 10px 30px;
    font-weight: bold;
    box-shadow: 0 4px 15px 0 rgba(255, 182, 193, 0.15);
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px 0 rgba(255, 182, 193, 0.25);
}

.stSelectbox > div > div {
    background: rgba(255, 255, 255, 0.95) !important;
    border-radius: 8px;
    border: 1px solid #ddd;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.stSelectbox label {
    font-size: 1em !important;
    font-weight: 600 !important;
    color: white !important;
    margin-bottom: 8px;
}

.stNumberInput label {
    font-size: 1em !important;
    font-weight: 600 !important;
    color: white !important;
    margin-bottom: 8px;
}

.stSelectbox div[data-baseweb="select"] > div {
    background: #262730 !important;
    color: white !important;
    border: 1px solid #ccc !important;
    border-radius: 6px !important;
}

.stNumberInput > div > div > input {
    background: white !important;
    color: white !important;
    border: 1px solid #ccc !important;
    border-radius: 6px !important;
    font-size: 0.95em !important;
    padding: 8px 12px !important;
}


.rgb-title {
    font-size: 3.2em;
    font-weight: bold;
    text-align: center;
    background: linear-gradient(270deg, #ff6b6b, #f7d716, #1de9b6, #2196f3, #ff6b6b);
    background-size: 1000% 1000%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: rgbmove 6s linear infinite;
    margin-bottom: 20px;
}
@keyframes rgbmove {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}
</style>
""", unsafe_allow_html=True)

# --- Tiêu đề và mô tả ---
st.markdown("""
<div class='rgb-title'>🏥✨ Ứng dụng Dự đoán Chi phí Y tế Cá nhân ✨🏥</div>
<div style='text-align: center; margin-bottom: 30px;'>
    <h3 style='color: #ff6b6b;'>💫 Nhập thông tin của bạn để nhận được ước tính chi phí y tế hàng năm 💫</h3>
</div>
""", unsafe_allow_html=True)

# --- Tạo các cột để nhập liệu ---
col1, col2, col3 = st.columns(3)

with col1:
    st.header("👤 Thông tin Cá nhân")
    age = st.number_input("🎂 Tuổi (Age)", min_value=18, max_value=100, value=30, step=1)
    sex = st.selectbox("⚧️ Giới tính (Sex)", ("male", "female"))
    bmi = st.number_input("📊 Chỉ số BMI", min_value=15.0, max_value=55.0, value=25.0, step=0.1)

with col2:
    st.header("👨‍👩‍👧‍👦 Gia đình & Lối sống")
    children = st.number_input("👶 Số con (Children)", min_value=0, max_value=10, value=0, step=1)
    smoker = st.selectbox("🚬 Hút thuốc (Smoker)", ("yes", "no"))
    region = st.selectbox("🗺️ Khu vực (Region)", ("southwest", "southeast", "northwest", "northeast"))

with col3:
    st.header("🎯 Kết quả Dự đoán")
    if st.button("✨ Dự đoán (Predict) ✨"):
        input_data = {
            "age": age,
            "sex": sex,
            "bmi": bmi,
            "children": children,
            "smoker": smoker,
            "region": region
        }

        # URL của FastAPI endpoint
        # Lưu ý: Đảm bảo server FastAPI đang chạy ở địa chỉ này
        api_url = "http://127.0.0.1:8000/predict"

        try:
    
            headers = {"Content-Type": "application/json"}
            response = requests.post(api_url, json=input_data, headers=headers)


            if response.status_code == 200:
                prediction = response.json()
                predicted_charge = prediction.get("predicted_charge")


                if predicted_charge is not None:
                    st.markdown(f"""
                    <div style='
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        padding: 25px;
                        border-radius: 20px;
                        text-align: center;
                        color: white;
                        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
                        margin: 20px 0;
                    '>
                        <h2 style='margin: 0; color: white;'>💰 Chi phí uớc tính</h2>
                        <h1 style='margin: 10px 0; color: #FFD700; font-size: 2.5em;'>${predicted_charge:,.2f}</h1>
                        <p style='margin: 0; opacity: 0.9;'>✅ Dự đoán thành công!</p>
                    </div>
                    """, unsafe_allow_html=True)
                    

                    st.balloons()
                else:
                    st.error("API trả về kết quả không hợp lệ.")
                    st.json(prediction)  
            else:
                st.error(f"Lỗi từ API: {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("Không thể kết nối đến API. Hãy đảm bảo server FastAPI đang chạy.")
        except Exception as e:
            st.error(f"Đã xảy ra lỗi: {e}")
            st.write("Debug info:")
            st.write(f"Input data: {input_data}")

st.sidebar.header("📋 Hướng dẫn")
st.sidebar.info(
    "✨ **Cách sử dụng ứng dụng:**\n\n"
    "1. 📝 **Nhập thông tin:** Điền đầy đủ các thông tin vào các ô tương ứng.\n\n"
    "2. 🎯 **Dự đoán:** Nhấn nút 'Dự đoán' để xem kết quả.\n\n"
    "3. 🤖 **Lưu ý:** Ứng dụng này sử dụng mô hình XGBoost đã được huấn luyện để đưa ra ước tính.\n\n"
    "💡 **Mẹo:** BMI = Cân nặng(kg) / Chiều cao²(m)"
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='text-align: center; padding: 10px;'>
    <h4 style='color: #ff6b6b;'>🎨 Made by author with ❤️</h4>
    <p style='font-size: 12px; opacity: 0.7;'>Ứng dụng AI dự đoán chi phí y tế</p>
</div>
""", unsafe_allow_html=True)
