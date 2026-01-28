import streamlit as st

# 1. การตั้งค่าหน้าเว็บและไอคอน
st.set_page_config(
    page_title="Baggage Weight Calculation",
    page_icon="✈️",
    layout="centered"
)

# 2. ส่วนการตกแต่ง CSS แบบ Responsive (รองรับทุกอุปกรณ์และตัวหนังสือคมชัด)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@400;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&display=swap');
    
    /* พื้นหลังสีสว่าง Luxury White */
    html, body, [class*="css"] {
        font-family: 'Sarabun', sans-serif;
        background: #f1f5f9;
        color: #1e293b;
    }

    [data-testid="stSidebar"] { display: none; }

    /* --- Header แบบ Responsive ที่แสดงคำว่า Weight ครบถ้วน --- */
    .luxury-header {
        text-align: center;
        padding: clamp(40px, 10vw, 70px) 20px;
        background: linear-gradient(135deg, #001f3f 0%, #1e40af 100%, #581c87 100%);
        border-radius: 0 0 40px 40px;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 160px;
    }
    
    .header-title {
        font-family: 'Playfair Display', serif;
        font-size: clamp(26px, 5.5vw, 45px); /* ปรับขนาดอัตโนมัติตามหน้าจอ */
        color: #fbbf24; 
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 900;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
        line-height: 1.2;
        width: 100%;
    }

    /* --- แถบเมนู Navigation แบบปุ่มสีขาวตัวหนาชัดเจน --- */
    .stRadio div[role="radiogroup"] {
        background: #ffffff;
        padding: 10px;
        border-radius: 15px;
        border: 2px solid #fbbf24;
        display: flex;
        flex-wrap: wrap; 
        justify-content: center;
        gap: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    
    .stRadio label {
        background: #ffffff !important;
        color: #000000 !important;
        font-weight: 900 !important;
        padding: 12px 25px !important;
        border-radius: 10px !important;
        font-size: clamp(14px, 4vw, 18px) !important;
        border: 2px solid #fbbf24 !important;
        flex: 1 1 auto;
        text-align: center;
        min-width: 110px;
        transition: 0.3s;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }

    .stRadio label:hover {
        background: #fbbf24 !important;
        box-shadow: 0 0 15px #fbbf24;
        transform: translateY(-2px);
    }

    /* --- การ์ดเนื้อหาเรืองแสงสีฟ้าสไตล์ Luxury --- */
    .glow-card {
        background: #ffffff;
        padding: clamp(25px, 6vw, 45px);
        border-radius: 30px;
        border: 4px solid #38bdf8;
        box-shadow: 0 15px 35px rgba(56, 189, 248, 0.15);
        margin: 20px 0;
        color: #000000 !important;
        font-weight: 800;
        word-wrap: break-word;
    }

    /* --- ส่วนประกอบอื่นๆ --- */
    div.stButton > button {
        background: linear-gradient(135deg, #001f3f 0%, #1e40af 100%);
        color: #ffffff !important;
        border-radius: 15px;
        padding: 18px;
        font-weight: 900;
        font-size: 20px;
        width: 100%;
        border: 2px solid #fbbf24;
        transition: 0.3s;
    }

    [data-testid="stMetricValue"] {
        color: #1e40af !important;
        font-weight: 900 !important;
    }
    </style>
    
    <div class="luxury-header">
        <div class="header-title">Baggage Weight Calculation</div>
    </div>
    """, unsafe_allow_html=True)

# 3. ข้อมูลสายการบินทั้งหมด 100% ครบถ้วนตามที่คุณต้องการ
airline_full_data = {
    "แอร์เอเชีย (Air Asia)": {
        "text": """• <b>Carry-on:</b> ฟรี 1 ชิ้น รวมไม่เกิน 7 กก. (56x23x36 ซม.)
• <b>Fast Pass:</b> ถือขึ้นเครื่องได้สูงสุด 14 กก. (ซื้อเพิ่มตอนจอง)
• <b>โหลดใต้ท้องเครื่อง (Checked Baggage):</b> ราคาประหยัดกว่าเมื่อซื้อพร้อมตั๋ว
  - 20 กก.: 400 - 450 บาท
  - 25 กก.: 550 - 600 บาท
  - 30 กก.: 800 - 850 บาท
  - 40 กก.: 1,500 - 1,600 บาท""",
        "free": 0, "fee": 425
    },
    "การบินไทย (Thai Airways)": {
        "text": """นโยบายใหม่เริ่ม 1 เม.ย. 68:
• <b>ชั้นประหยัด Saver/Standard:</b> 23 กก. (ปรับจาก 25 กก.)
• <b>ชั้นประหยัด Flexi/Full Flex:</b> 30 กก.
• <b>ชั้นประหยัดพิเศษ:</b> 35 กก. / <b>ชั้นธุรกิจ:</b> 40 กก.
• <b>Carry-on:</b> ไม่เกิน 7 กก. (56x45x25 ซม.) ทุกชั้น""",
        "free": 23, "fee": 60
    },
    "เวียตเจ็ท (Vietjet Air)": {
        "text": """• <b>Carry-on:</b> จำกัด 1 ชิ้นหลัก + กระเป๋าเล็ก 1 ใบ รวมกันไม่เกิน 7 กก.
• <b>Checked Baggage:</b> SkyBoss (30 กก.), Deluxe (20 กก.), Eco ไม่ฟรีน้ำหนัก
• <b>ซื้อล่วงหน้า:</b> เริ่มที่ 15 กก. (350-450 บ.) ถึง 30 กก. (800-1,200 บ.)
• <b>ส่วนเกินที่สนามบิน:</b> ประมาณ 320 บาท ต่อ 1 กก.""",
        "free": 0, "fee": 320
    },
    "นกแอร์ (Nok Air)": {
        "text": """• <b>Nok Lite:</b> ฟรีโหลด 10 กก.
• <b>Nok X-tra:</b> ฟรีโหลด 15 กก. (บางโปรโมชั่น 20 กก.)
• <b>Nok Max:</b> ฟรีโหลด 30 กก.
• <b>Carry-on:</b> ฟรี 1 ใบ ไม่เกิน 7 กก. (56x36x23 ซม.)""",
        "free": 10, "fee": 350
    },
    "ไทยไลอ้อนแอร์ (Thai Lion Air)": {
        "text": """• <b>Domestic (Economy):</b> ปกติฟรีโหลด 10 กก.
• <b>Premium Economy:</b> ฟรีโหลด 20 กก. (ระหว่างประเทศสูงสุด 30 กก.)
• <b>Carry-on:</b> ฟรี 7 กก. ทุกประเภทตั๋ว""",
        "free": 10, "fee": 350
    }
}

# 4. เมนู Navigation
page = st.radio("", ["🏠 HOME", "🧮 CALCULATE", "📘 ABOUT"], horizontal=True, label_visibility="collapsed")

# 5. การแสดงผลเนื้อหา
if page == "🏠 HOME":
    st.markdown("""
    <div style="text-align: center;">
        <img src="https://images.unsplash.com/photo-1542296332-2e4473faf563?auto=format&fit=crop&w=1200&q=80" 
             style="width:100%; max-width:700px; border-radius:25px; box-shadow: 0 10px 20px rgba(0,0,0,0.1);">
        <div class="glow-card" style="margin-top:-30px; position:relative; z-index:10; border:2px solid #fbbf24;">
            <h3 style="margin:0; color:#001f3f; font-size: clamp(20px, 5vw, 26px);">Smart Baggage Calculation System</h3>
            <p style="color:#1e40af; font-weight:bold; font-size: clamp(14px, 3vw, 17px);">Developing a Web-based Order Management Application</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

elif page == "🧮 CALCULATE":
    st.markdown('<div class="glow-card"><h3>🧮 Calculator</h3>', unsafe_allow_html=True)
    selected = st.selectbox("เลือกสายการบินที่คุณต้องการตรวจสอบ:", list(airline_full_data.keys()))
    user_w = st.number_input("ใส่น้ำหนักสัมภาระรวม (กก.):", min_value=0.0, step=0.1)
    
    info = airline_full_data[selected]
    if st.button("PROCESS CALCULATION"):
        if user_w <= info["free"]:
            st.balloons(); st.success(f"น้ำหนัก {user_w} กก. อยู่ในเกณฑ์ฟรีสำหรับ {selected}!")
        else:
            excess = user_w - info["free"]; total = excess * info["fee"]
            st.metric("Estimated Fee (THB)", f"{total:,.0f}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    
    
    st.markdown(f'<div class="glow-card"><h3>✈️ Airline Policy: {selected}</h3>{info["text"]}</div>', unsafe_allow_html=True)

elif page == "📘 ABOUT":
    st.markdown("""
    <div class="glow-card" style="color:#000000 !important;">
        <h3 style="color:#001f3f;">📘 About Project</h3>
        <p><b>ชื่อวิจัย:</b> Developing a Web-based Order Management Application</p>
        <p>ระบบคำนวณน้ำหนักสัมภาระนี้ถูกพัฒนาขึ้นเพื่อรวบรวมนโยบายล่าสุดของสายการบินหลักในประเทศไทย 
        ช่วยให้นักเดินทางคำนวณค่าธรรมเนียมส่วนเกินได้อย่างแม่นยำ อ้างอิงนโยบายปี 2568</p>
    </div>
    """, unsafe_allow_html=True)