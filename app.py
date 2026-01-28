import streamlit as st

# 1. การตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="Baggage Weight Calculation",
    page_icon="✈️",
    layout="centered"
)

# 2. ส่วนการตกแต่ง CSS (ปรับปรุงความคมชัดและฟอนต์)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@400;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap');
    
    /* พื้นหลัง Luxury Dark Mode */
    html, body, [class*="css"] {
        font-family: 'Sarabun', sans-serif;
        background: radial-gradient(circle, #1e293b 0%, #0f172a 100%);
        color: #ffffff;
    }

    /* ซ่อน Sidebar */
    [data-testid="stSidebar"] { display: none; }

    /* ส่วนหัวแอป (App Header) - เน้นสีน้ำเงินเข้มและตัวอักษรชัดเจน */
    .luxury-header {
        text-align: center;
        padding: 50px 0 30px 0;
        background: linear-gradient(180deg, rgba(30,58,138,0.9) 0%, rgba(15,23,42,0) 100%);
        margin-bottom: 20px;
    }
    .header-title {
        font-family: 'Playfair Display', serif;
        font-size: 36px;
        color: #1e40af; /* เปลี่ยนเป็นสีน้ำเงินเข้ม Navy Blue ที่ชัดเจน */
        text-transform: uppercase;
        letter-spacing: 4px;
        font-weight: 800;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5), 0 0 10px rgba(59, 130, 246, 0.4);
    }

    /* แถบเมนู Navigation แบบปุ่มชัดเจน */
    .stRadio div[role="radiogroup"] {
        background: rgba(255, 255, 255, 0.08);
        padding: 8px;
        border-radius: 12px;
        border: 1px solid rgba(59, 130, 246, 0.4);
        display: flex;
        justify-content: center;
        gap: 15px;
    }
    .stRadio label {
        color: #ffffff !important;
        font-weight: 700 !important;
        padding: 8px 25px !important;
        border-radius: 8px !important;
        font-size: 16px !important;
        transition: 0.3s;
    }
    .stRadio label:hover {
        background: rgba(59, 130, 246, 0.2) !important;
    }

    /* การ์ดเนื้อหา (Content Card) - เพิ่มความสว่างให้อ่านง่ายขึ้น */
    .luxury-card {
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(12px);
        padding: 30px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
        margin-bottom: 25px;
        line-height: 1.8;
        color: #ffffff;
    }
    
    /* เน้นหัวข้อในการ์ด */
    .card-title {
        color: #38bdf8;
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 15px;
        border-bottom: 2px solid rgba(56, 189, 248, 0.3);
        padding-bottom: 8px;
    }

    /* ปุ่มประมวลผล (Action Button) - ทำให้เด่นและดูเหมือนปุ่มจริง */
    div.stButton > button {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        color: #ffffff !important;
        border-radius: 12px;
        padding: 12px 20px;
        font-weight: 700;
        font-size: 18px;
        width: 100%;
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: 0 4px 15px rgba(30, 64, 175, 0.5);
        transition: 0.3s;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.7);
    }

    /* ปรับแต่ง Input Field ให้มองเห็นง่าย */
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: #ffffff !important;
        border: 1px solid rgba(59, 130, 246, 0.5) !important;
        border-radius: 10px !important;
    }
    
    /* ปรับขนาดตัวอักษร Metric (ผลลัพธ์) */
    [data-testid="stMetricValue"] {
        color: #fbbf24 !important;
        font-weight: 700 !important;
        font-size: 40px !important;
    }
    </style>
    
    <div class="luxury-header">
        <div class="header-title">Baggage Weight Calculation</div>
    </div>
    """, unsafe_allow_html=True)

# 3. ข้อมูลสายการบินทั้งหมด (จัดระเบียบใหม่ให้ชัดเจน)
airline_full_data = {
    "เวียตเจ็ท (Vietjet Air)": {
        "text": """• <b>Carry-on:</b> ฟรี 7 กก. (1 ชิ้นหลัก 56x36x23 ซม. + กระเป๋าเล็ก 1 ใบ)
• <b>SkyBoss:</b> ฟรี 30 กก. (รวมถุงกอล์ฟ)
• <b>Deluxe:</b> ฟรี 20 กก.
• <b>Eco:</b> ไม่มีน้ำหนักฟรี (ซื้อล่วงหน้าเริ่ม 350-450 บาท)
• <b>ส่วนเกินที่สนามบิน:</b> ประมาณ 320 บาท/กก.""",
        "free": 0, "fee": 320
    },
    "นกแอร์ (Nok Air)": {
        "text": """• <b>Carry-on:</b> ฟรี 7 กก.
• <b>Nok Lite:</b> ฟรีโหลด 10 กก.
• <b>Nok X-tra:</b> ฟรีโหลด 15-20 กก.
• <b>Nok Max:</b> ฟรีโหลด 30 กก.""",
        "free": 10, "fee": 350
    },
    "ไทยไลอ้อนแอร์ (Thai Lion Air)": {
        "text": """• <b>Carry-on:</b> ฟรี 7 กก.
• <b>ภายในประเทศ:</b> ฟรีโหลด 10 กก. (ชั้นประหยัด)
• <b>Premium Economy:</b> ฟรีโหลด 20 กก.""",
        "free": 10, "fee": 350
    },
    "การบินไทย (Thai Airways)": {
        "text": """อัปเดตนโยบาย (เริ่ม 1 เม.ย. 68):
• <b>Saver/Standard:</b> ฟรี 23 กก.
• <b>Flexi/Full Flex:</b> ฟรี 30 กก.
• <b>Premium Economy:</b> ฟรี 35 กก.
• <b>Royal Silk:</b> ฟรี 40 กก.
• <b>Carry-on:</b> ฟรี 7 กก. ทุกชั้น""",
        "free": 23, "fee": 60
    },
    "แอร์เอเชีย (Air Asia)": {
        "text": """• <b>Carry-on:</b> ฟรี 7 กก. (56x23x36 ซม.)
• <b>Fast Pass:</b> ถือขึ้นเครื่องได้สูงสุด 14 กก.
• <b>น้ำหนักโหลด:</b> ต้องซื้อเพิ่ม (20 กก. เริ่มต้น 400-450 บาท)""",
        "free": 0, "fee": 400
    }
}

# 4. เมนู Navigation
page = st.radio("", ["HOME", "CALCULATE", "ABOUT"], horizontal=True, label_visibility="collapsed")

# 5. การแสดงผลตามเมนู
if page == "HOME":
    st.markdown("""
    <div class="luxury-card" style="text-align: center;">
        <img src="https://images.unsplash.com/photo-1542296332-2e4473faf563?auto=format&fit=crop&w=1000&q=80" 
             style="width:100%; border-radius:15px; margin-bottom:20px; border: 1px solid rgba(255,255,255,0.2);">
        <div class="glow-border">
            <h4 style="color:#38bdf8; margin:0; font-size:20px;">Introducing the Smart Baggage Calculator</h4>
            <p style="margin:5px 0 0 0; opacity:0.9;">Your Ultimate Travel Companion</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

elif page == "CALCULATE":
    st.markdown('<div class="luxury-card"><div class="card-title">⚙️ เครื่องคำนวณน้ำหนักอัจฉริยะ</div>', unsafe_allow_html=True)
    selected = st.selectbox("เลือกสายการบินที่คุณต้องการตรวจสอบ:", list(airline_full_data.keys()))
    user_w = st.number_input("ใส่น้ำหนักสัมภาระรวม (กก.):", min_value=0.0, step=0.1)
    
    info = airline_full_data[selected]
    if st.button("PROCESS CALCULATION"):
        if user_w <= info["free"]:
            st.balloons()
            st.success(f"น้ำหนัก {user_w} กก. อยู่ในเกณฑ์ฟรีสำหรับ {selected}!")
        else:
            excess = user_w - info["free"]
            total = excess * info["fee"]
            st.warning(f"เกินโควตาฟรี {excess:.2f} กก.")
            st.metric("ค่าธรรมเนียมโดยประมาณ (บาท)", f"{total:,.0f}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # แสดงรูปภาพประกอบประเภทกระเป๋า
    
    
    st.markdown(f'<div class="luxury-card"><div class="card-title">✈️ นโยบายของ {selected}</div>', unsafe_allow_html=True)
    st.markdown(f"<div style='font-size: 16px;'>{info['text']}</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "ABOUT":
    st.markdown("""
    <div class="luxury-card">
        <div class="card-title">📘 เกี่ยวกับโปรเจกต์</div>
        <p style="font-size: 16px;">
            <b>Developing a Web-based Order Management Application</b><br>
            ระบบนี้พัฒนาขึ้นเพื่อรวบรวมนโยบายสัมภาระและคำนวณค่าธรรมเนียมส่วนเกินอย่างแม่นยำ 
            ช่วยให้นักเดินทางวางแผนงบประมาณได้อย่างมีประสิทธิภาพ
        </p>
        <div style="margin-top:20px; padding:15px; background:rgba(255,255,255,0.05); border-radius:10px;">
            <b>Version:</b> 1.0.1 (Stable)<br>
            <b>Framework:</b> Streamlit 1.41.1<br>
            <b>Status:</b> Ready for Deployment
        </div>
    </div>
    """, unsafe_allow_html=True)