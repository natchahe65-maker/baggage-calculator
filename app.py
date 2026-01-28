import streamlit as st

# 1. การตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="Baggage Weight Calculation",
    page_icon="✈️",
    layout="centered"
)

# 2. ส่วนการตกแต่ง CSS แบบ Responsive และระบบ PWA
st.markdown("""
    <head>
        <link rel="manifest" href="manifest.json">
        <link rel="apple-touch-icon" href="logo.png">
        <link rel="icon" type="image/png" href="logo.png">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    
    <script>
        let deferredPrompt;
        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            deferredPrompt = e;
            const installBtn = document.getElementById('install-btn-pwa');
            if(installBtn) installBtn.style.display = 'block';
        });

        function triggerInstall() {
            if (deferredPrompt) {
                deferredPrompt.prompt();
                deferredPrompt.userChoice.then((choiceResult) => {
                    deferredPrompt = null;
                });
            }
        }
    </script>

    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@400;700;800;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Sarabun', sans-serif;
        background: #f8fafc;
        color: #1e293b;
    }

    [data-testid="stSidebar"] { display: none; }

    /* ปุ่มติดตั้งแอป */
    #install-btn-pwa {
        display: none;
        position: fixed;
        bottom: 25px;
        right: 25px;
        z-index: 9999;
        background: linear-gradient(135deg, #fbbf24 0%, #d97706 100%);
        color: #000;
        border: 2px solid #ffffff;
        padding: 12px 20px;
        border-radius: 50px;
        font-weight: 900;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
        cursor: pointer;
    }

    /* Header ที่ยืดหยุ่น */
    .luxury-header {
        text-align: center;
        padding: clamp(40px, 8vw, 65px) 15px;
        background: linear-gradient(135deg, #001f3f 0%, #1e40af 100%, #581c87 100%);
        border-radius: 0 0 35px 35px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin-bottom: 25px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .header-title {
        font-family: 'Playfair Display', serif;
        font-size: clamp(22px, 5.5vw, 40px);
        color: #fbbf24; 
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 900;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
        line-height: 1.2;
    }

    /* ปุ่มเมนูขาวตัวหนาพิเศษ คมชัด */
    .stRadio div[role="radiogroup"] {
        background: #ffffff;
        padding: 10px;
        border-radius: 15px;
        border: 2px solid #fbbf24;
        display: flex;
        flex-wrap: wrap; 
        justify-content: center;
        gap: 10px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    
    .stRadio label {
        background: #ffffff !important;
        color: #000000 !important;
        font-weight: 900 !important;
        padding: 10px 20px !important;
        border: 2px solid #fbbf24 !important;
        border-radius: 10px !important;
        font-size: clamp(14px, 4vw, 17px) !important;
        flex: 1 1 auto;
        text-align: center;
        min-width: 100px;
    }

    .stRadio label:hover {
        background: #fbbf24 !important;
        box-shadow: 0 0 12px rgba(251, 191, 36, 0.6);
    }

    .glow-card {
        background: #ffffff;
        padding: clamp(25px, 5vw, 40px);
        border-radius: 25px;
        border: 4px solid #38bdf8;
        box-shadow: 0 12px 30px rgba(56, 189, 248, 0.15);
        margin: 20px 0;
        color: #000 !important;
        font-weight: 800;
        word-wrap: break-word;
    }

    div.stButton > button {
        background: linear-gradient(135deg, #001f3f 0%, #1e40af 100%);
        color: #ffffff !important;
        border-radius: 12px;
        padding: 15px;
        font-weight: 900;
        border: 2px solid #fbbf24;
        width: 100%;
    }
    </style>
    
    <div class="luxury-header">
        <div class="header-title">Baggage Weight Calculation</div>
    </div>

    <button id="install-btn-pwa" onclick="triggerInstall()">📲 ติดตั้งแอปไว้บนมือถือ</button>
    """, unsafe_allow_html=True)

# 3. ข้อมูลสายการบิน (แสดงข้อมูลทั้งหมดที่คุณให้มา)
airline_full_data = {
    "เวียตเจ็ท (Vietjet Air)": {
        "text": """
        <b>สัมภาระถือขึ้นเครื่อง (Carry-on):</b> จำกัด 1 ชิ้นหลัก (ไม่เกิน 56x36x23 ซม.) และกระเป๋าเล็ก 1 ใบ น้ำหนักรวมกันไม่เกิน 7 กก. ทุกประเภทตั๋ว <br><br>
        <b>สัมภาระโหลดใต้ท้องเครื่อง (Checked Baggage):</b> <br>
        • <b>SkyBoss:</b> ได้น้ำหนัก 30 กก. (รวมถุงกอล์ฟ 15 กก. ถ้ามี) <br>
        • <b>Deluxe:</b> ได้น้ำหนัก 20 กก. (บางโปรโมชั่น/เส้นทางอาจสูงกว่า) <br>
        • <b>Eco/Promo:</b> ไม่มีน้ำหนักฟรี ต้องซื้อเพิ่ม <br><br>
        <b>ซื้อน้ำหนักล่วงหน้า (Pre-paid):</b> <br>
        • 15 กก. (350-450 บาท) <br>
        • 20 กก. (480-700 บาท) <br>
        • 25 กก. (650-900 บาท) <br>
        • 30 กก. (800-1,200 บาท) <br><br>
        <b>ซื้อที่สนามบิน (Overweight):</b> ประมาณ 320 บาท ต่อ 1 กก.
        """,
        "free": 0, "fee": 320
    },
    "นกแอร์ (Nok Air)": {
        "text": """
        <b>รายละเอียดค่าน้ำหนักกระเป๋า (เส้นทางในประเทศ):</b> <br>
        • <b>Nok Lite:</b> ฟรีน้ำหนักโหลดใต้ท้องเครื่อง 10 กิโลกรัม <br>
        • <b>Nok X-tra:</b> ฟรีน้ำหนักโหลดใต้ท้องเครื่อง 15 กิโลกรัม (บางโปรโมชั่นอาจได้ 20 กก.) <br>
        • <b>Nok Max:</b> ฟรีน้ำหนักโหลดใต้ท้องเครื่อง 30 กิโลกรัม <br>
        • <b>กระเป๋าถือขึ้นเครื่อง (Carry-on):</b> ฟรี 1 ใบ น้ำหนักไม่เกิน 7 กิโลกรัม (ขนาดไม่เกิน 56x36x23 ซม.) <br><br>
        <b>การซื้อน้ำหนักล่วงหน้า:</b> เริ่มต้นประมาณ 350-400 บาท สำหรับ +10 กก.
        """,
        "free": 10, "fee": 350
    },
    "ไทยไลอ้อนแอร์ (Thai Lion Air)": {
        "text": """
        <b>สัมภาระถือขึ้นเครื่อง (Carry-on):</b> ฟรี 7 กิโลกรัม ทุกประเภทตั๋ว <br><br>
        <b>สรุปค่าน้ำหนักกระเป๋า (โหลดใต้ท้องเครื่อง):</b> <br>
        • <b>ภายในประเทศ (Domestic):</b> <br>
        - Lion Economy / Promo: ไม่มีโหลดฟรี (ต้องซื้อเพิ่ม) <br>
        - Premium Economy: โหลดฟรี 20 กก. <br>
        • <b>ระหว่างประเทศ (International):</b> <br>
        - Economy / Promo: มักไม่มีโหลดฟรี หรือตรวจสอบตามโปรโมชั่น <br>
        - Premium Economy: โหลดฟรี 2 ชิ้น รวมสูงสุด 30 กก.
        """,
        "free": 10, "fee": 350
    },
    "การบินไทย (Thai Airways)": {
        "text": """
        <b>นโยบายใหม่เริ่ม 1 เมษายน 2568 เป็นต้นไป:</b> <br><br>
        <b>น้ำหนักกระเป๋าโหลดใต้ท้องเครื่อง (Checked Baggage):</b> <br>
        • <b>ชั้นประหยัด (Economy Class):</b> <br>
        - Saver / Standard: 23 กก. (เริ่ม 1 เม.ย. 68) <br>
        - Flexi / Full Flex: 30 กก. <br>
        • <b>ชั้นประหยัดพิเศษ (Premium Economy):</b> 35 กก. <br>
        • <b>ชั้นธุรกิจ (Royal Silk Class):</b> 40 กก. <br>
        • <b>ทารก (Infant - ไม่ใช้ที่นั่ง):</b> 10 กก. <br><br>
        <b>สัมภาระถือขึ้นเครื่อง (Carry-on):</b> <br>
        - น้ำหนักไม่เกิน 7 กก. ขนาดไม่เกิน 56x45x25 ซม. ทุกชั้นโดยสาร
        """,
        "free": 23, "fee": 60
    },
    "แอร์เอเชีย (Air Asia)": {
        "text": """
        <b>กระเป๋าถือขึ้นเครื่อง (Carry-on):</b> ฟรี 1 ชิ้น รวมน้ำหนักไม่เกิน 7 กก. ขนาดไม่เกิน 56x23x36 ซม. <br>
        • <b>Fast Pass:</b> นำขึ้นเครื่องได้สูงสุด 14 กก. (ซื้อเพิ่มตอนจอง) <br><br>
        <b>โหลดใต้ท้องเครื่อง (Checked Baggage):</b> <br>
        • 20 kg: 400-450 บาท <br>
        • 25 kg: 550-600 บาท <br>
        • 30 kg: 800-850 บาท <br>
        • 40 kg: 1,500-1,600 บาท
        """,
        "free": 0, "fee": 425
    }
}

# 4. การแสดงผล
page = st.radio("", ["🏠 HOME", "🧮 CALCULATE", "📘 ABOUT"], horizontal=True, label_visibility="collapsed")

if page == "🏠 HOME":
    st.markdown("""
    <div style="text-align: center;">
        <img src="https://images.unsplash.com/photo-1542296332-2e4473faf563?auto=format&fit=crop&w=1200&q=80" style="width:100%; max-width:650px; border-radius:25px;">
        <div class="glow-card" style="border:2.5px solid #fbbf24;">
            <h3 style="margin:0; color:#001f3f;">Smart Baggage Calculation System</h3>
            <p style="color:#1e40af; font-weight:bold; margin-top:10px;">Your Ultimate Travel Companion</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

elif page == "🧮 CALCULATE":
    st.markdown('<div class="glow-card"><h3>🧮 Calculator</h3>', unsafe_allow_html=True)
    selected = st.selectbox("เลือกสายการบิน:", list(airline_full_data.keys()))
    user_w = st.number_input("ใส่น้ำหนักสัมภาระรวม (กก.):", min_value=0.0, step=0.1)
    info = airline_full_data[selected]
    if st.button("PROCESS CALCULATION"):
        if user_w <= info["free"]:
            st.balloons(); st.success(f"น้ำหนัก {user_w} กก. อยู่ในเกณฑ์ฟรีสำหรับ {selected}!")
        else:
            total = (user_w - info["free"]) * info["fee"]
            st.metric("ค่าธรรมเนียมประมาณ (บาท)", f"{total:,.0f}")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="glow-card"><h3>✈️ Policy: {selected}</h3>{info["text"]}</div>', unsafe_allow_html=True)

elif page == "📘 ABOUT":
    st.markdown("""
    <div class="glow-card">
        <h3>📘 About</h3>
        <p>ระบบคำนวณน้ำหนักสัมภาระอัจฉริยะ อ้างอิงนโยบายสายการบินล่าสุดปี 2568 
        ช่วยให้นักเดินทางคำนวณค่าธรรมเนียมส่วนเกินได้อย่างแม่นยำ</p>
    </div>
    """, unsafe_allow_html=True)