import streamlit as st

# 1. การตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="Baggage Weight Calculation",
    page_icon="✈️",
    layout="centered"
)

# 2. ส่วนการตกแต่ง CSS และ JavaScript สำหรับ PWA
st.markdown("""
    <head>
        <link rel="manifest" href="manifest.json">
        <link rel="apple-touch-icon" href="https://cdn-icons-png.flaticon.com/512/723/723955.png">
        <meta name="apple-mobile-web-app-capable" content="yes">
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
    
    html, body, [class*="css"] {
        font-family: 'Sarabun', sans-serif;
        background: #f1f5f9;
        color: #1e293b;
    }

    [data-testid="stSidebar"] { display: none; }

    /* ปุ่มแจ้งเตือนติดตั้งแอป */
    #install-btn-pwa {
        display: none;
        position: fixed;
        bottom: 30px;
        right: 30px;
        z-index: 9999;
        background: linear-gradient(135deg, #fbbf24 0%, #d97706 100%);
        color: #000;
        border: 2px solid #ffffff;
        padding: 15px 25px;
        border-radius: 50px;
        font-weight: 900;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
        cursor: pointer;
    }

    .luxury-header {
        text-align: center;
        padding: clamp(40px, 8vw, 60px) 15px;
        background: linear-gradient(135deg, #001f3f 0%, #1e40af 100%);
        border-radius: 0 0 35px 35px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin-bottom: 25px;
    }
    
    .header-title {
        font-size: clamp(24px, 5vw, 40px);
        color: #fbbf24; 
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    /* ปุ่มเมนูพื้นหลังสีขาว ตัวหนังสือสีดำหนาพิเศษ (High Contrast) */
    .stRadio div[role="radiogroup"] {
        background: #ffffff;
        padding: 10px;
        border-radius: 15px;
        border: 2px solid #fbbf24;
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 10px;
    }
    
    .stRadio label {
        background: #ffffff !important;
        color: #000000 !important;
        font-weight: 900 !important;
        padding: 12px 25px !important;
        border: 2.5px solid #fbbf24 !important;
        border-radius: 10px !important;
        font-size: clamp(14px, 4vw, 17px) !important;
        transition: 0.3s;
    }

    .stRadio label:hover {
        background: #fbbf24 !important;
        box-shadow: 0 0 15px rgba(251, 191, 36, 0.6);
    }

    .glow-card {
        background: #ffffff;
        padding: 35px;
        border-radius: 30px;
        border: 4px solid #38bdf8;
        box-shadow: 0 12px 30px rgba(56, 189, 248, 0.15);
        margin: 20px 0;
        color: #000;
        font-weight: 800;
    }

    div.stButton > button {
        background: linear-gradient(135deg, #001f3f 0%, #1e40af 100%);
        color: #ffffff !important;
        border-radius: 12px;
        padding: 15px;
        font-weight: 900;
        border: 2px solid #fbbf24;
    }
    </style>
    
    <div class="luxury-header">
        <div class="header-title">Baggage Weight Calculation</div>
    </div>

    <button id="install-btn-pwa" onclick="triggerInstall()">📲 ติดตั้งแอปไว้บนมือถือ</button>
    """, unsafe_allow_html=True)

# 3. ข้อมูลสายการบิน (รวบรวมครบถ้วน 100%)
airline_full_data = {
    "แอร์เอเชีย (Air Asia)": {
        "text": """• <b>ถือขึ้นเครื่อง (Carry-on):</b> ฟรี 1 ชิ้น รวมไม่เกิน 7 กก. (56x23x36 ซม.)
• <b>Fast Pass:</b> สามารถถือขึ้นเครื่องได้สูงสุด 14 กก. (ซื้อเพิ่มตอนจอง)
• <b>โหลดใต้ท้องเครื่อง (Checked):</b>
  - 20 กก.: 400 - 450 บาท
  - 25 กก.: 550 - 600 บาท
  - 30 กก.: 800 - 850 บาท
  - 40 กก.: 1,500 - 1,600 บาท""",
        "free": 0, "fee": 425
    },
    "การบินไทย (Thai Airways)": {
        "text": """อัปเดตนโยบาย 1 เม.ย. 68:
• <b>Economy Saver/Standard:</b> ฟรี 23 กก. (ปรับจาก 25 กก.)
• <b>Economy Flexi/Full Flex:</b> ฟรี 30 กก.
• <b>Premium Economy:</b> 35 กก. / <b>Royal Silk:</b> 40 กก.
• <b>Carry-on:</b> ไม่เกิน 7 กก. (56x45x25 ซม.) ทุกชั้น""",
        "free": 23, "fee": 60
    },
    "เวียตเจ็ท (Vietjet Air)": {
        "text": """• <b>ถือขึ้นเครื่อง (Carry-on):</b> จำกัดไม่เกิน 7 กก.
• <b>SkyBoss:</b> ฟรีโหลด 30 กก. (รวมถุงกอล์ฟ)
• <b>Deluxe:</b> ฟรีโหลด 20 กก.
• <b>Eco:</b> ไม่มีน้ำหนักฟรี (ซื้อล่วงหน้าเริ่มที่ 15 กก. 350-450 บ.)
• <b>ส่วนเกินสนามบิน:</b> ประมาณ 320 บาท ต่อ 1 กก.""",
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
        "text": """• <b>ถือขึ้นเครื่อง:</b> ฟรี 7 กก. ทุกประเภทตั๋ว
• <b>Domestic Economy:</b> ฟรีโหลด 10 กก. (Lion Promo ไม่มีฟรี)
• <b>Premium Economy:</b> ฟรีโหลด 20 กก. (ระหว่างประเทศ 30 กก.)""",
        "free": 10, "fee": 350
    }
}

# 4. เมนู Navigation
page = st.radio("", ["🏠 HOME", "🧮 CALCULATE", "📘 ABOUT"], horizontal=True, label_visibility="collapsed")

if page == "🏠 HOME":
    st.markdown("""
    <div style="text-align: center;">
        <img src="https://images.unsplash.com/photo-1542296332-2e4473faf563?auto=format&fit=crop&w=1200&q=80" style="width:100%; max-width:650px; border-radius:30px;">
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
        ช่วยให้คุณวางแผนการเดินทางและบริหารงบประมาณได้อย่างแม่นยำที่สุด</p>
    </div>
    """, unsafe_allow_html=True)