import streamlit as st

# 1. การตั้งค่าหน้าเว็บและไอคอนบนแท็บเบราว์เซอร์
st.set_page_config(
    page_title="Baggage Weight Calculation",
    page_icon="logo.png", 
    layout="centered"
)

# 2. ส่วนการตกแต่ง CSS แบบ Responsive และ Metadata สำหรับติดตั้งแอป (PWA)
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

    /* ปุ่มติดตั้งแอปแบบลอย (Floating Button) */
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

    /* Header ที่หรูหราและยืดหยุ่น */
    .luxury-header {
        text-align: center;
        padding: clamp(35px, 8vw, 65px) 15px;
        background: linear-gradient(135deg, #001f3f 0%, #1e40af 100%, #581c87 100%);
        border-radius: 0 0 35px 35px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin-bottom: 25px;
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

    /* ปุ่มเมนูขาวตัวหนาพิเศษ คมชัดมาก (High Contrast) */
    .stRadio div[role="radiogroup"] {
        background: #ffffff;
        padding: 10px;
        border-radius: 15px;
        border: 2px solid #fbbf24;
        display: flex;
        flex-wrap: wrap; 
        justify-content: center;
        gap: 12px;
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

    /* การ์ดเนื้อหาเรืองแสงสีฟ้า */
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

# 3. ข้อมูลสายการบิน (รวบรวมข้อมูลทั้งหมดที่คุณส่งมา)
airline_full_data = {
    "เวียตเจ็ท (Vietjet Air)": {
        "text": """
        <b>ค่าน้ำหนักกระเป๋าเวียตเจ็ท (Vietjet Air):</b><br>
        • <b>ถือขึ้นเครื่อง (Carry-on):</b> จำกัด 1 ชิ้นหลัก (ไม่เกิน 56x36x23 ซม.) และกระเป๋าเล็ก 1 ใบ น้ำหนักรวมกันไม่เกิน 7 กก.<br>
        • <b>โหลดใต้ท้องเครื่อง (Checked Baggage):</b> SkyBoss 30 กก., Deluxe 20 กก., Eco ไม่ฟรีต้องซื้อเพิ่ม<br>
        • <b>ซื้อล่วงหน้า (Pre-paid):</b> 15 กก. (350-450 บ.), 20 กก. (480-700 บ.), 30 กก. (800-1,200 บ.)<br>
        • <b>ซื้อที่สนามบิน:</b> ประมาณ 320 บาท ต่อ 1 กก.
        """,
        "free": 0, "fee": 320
    },
    "นกแอร์ (Nok Air)": {
        "text": """
        <b>รายละเอียดค่าน้ำหนักกระเป๋า นกแอร์ (เส้นทางในประเทศ):</b><br>
        • <b>Nok Lite:</b> ฟรีโหลดใต้ท้องเครื่อง 10 กก.<br>
        • <b>Nok X-tra:</b> ฟรีโหลดใต้ท้องเครื่อง 15-20 กก.<br>
        • <b>Nok Max:</b> ฟรีโหลดใต้ท้องเครื่อง 30 กก.<br>
        • <b>Carry-on:</b> ไม่เกิน 7 กก. (56x36x23 ซม.)<br>
        • <b>ซื้อล่วงหน้า:</b> เริ่มต้นประมาณ 350-400 บาท สำหรับ +10 กก.
        """,
        "free": 10, "fee": 350
    },
    "การบินไทย (Thai Airways)": {
        "text": """
        <b>นโยบายใหม่เริ่ม 1 เม.ย. 68:</b><br>
        • <b>Economy Saver / Standard:</b> 23 กก.<br>
        • <b>Flexi / Full Flex:</b> 30 กก.<br>
        • <b>Premium Economy:</b> 35 กก. / <b>Business:</b> 40 กก.<br>
        • <b>Carry-on:</b> ไม่เกิน 7 กก. (56x45x25 ซม.)
        """,
        "free": 23, "fee": 60
    },
    "ไทยไลอ้อนแอร์ (Thai Lion Air)": {
        "text": """
        <b>สรุปค่าน้ำหนักกระเป๋าไลอ้อนแอร์:</b><br>
        • <b>Domestic:</b> Economy ไม่มีโหลดฟรี, Premium โหลดฟรี 20 กก.<br>
        • <b>International:</b> Premium Economy โหลดฟรี 2 ชิ้น รวมสูงสุด 30 กก.<br>
        • <b>Carry-on:</b> ฟรี 7 กก. ทุกประเภทตั๋ว
        """,
        "free": 10, "fee": 350
    },
    "แอร์เอเชีย (Air Asia)": {
        "text": """
        <b>รายละเอียด แอร์เอเชีย:</b><br>
        • <b>Carry-on:</b> ฟรี 1 ชิ้น รวมน้ำหนักไม่เกิน 7 กก. (56x23x36 ซม.)<br>
        • <b>Fast Pass:</b> ถือขึ้นเครื่องได้สูงสุด 14 กก.<br>
        • <b>โหลดสัมภาระ (20 กก.):</b> ประมาณ 400-450 บาท<br>
        • <b>สูงสุด 40 กก.:</b> 1,500-1,600 บาท
        """,
        "free": 0, "fee": 425
    }
}

# 4. การแสดงผลเนื้อหาหน้า HOME, CALCULATE, ABOUT
page = st.radio("", ["🏠 HOME", "🧮 CALCULATE", "📘 ABOUT"], horizontal=True, label_visibility="collapsed")

if page == "🏠 HOME":
    # แก้ไขดึงรูปจากลิงก์เว็บโดยตรงเพื่อให้รูปขึ้นแน่นอน
    st.image("https://www.dataubcc.com/uploads/0d4b704564f0d13fb3d3cc79945cb4c7.jpg", use_container_width=True)
    st.markdown("""
        <div class="glow-card" style="border:2.5px solid #fbbf24; text-align: center;">
            <h3 style="margin:0; color:#001f3f;">Smart Baggage Calculation System</h3>
            <p style="color:#1e40af; font-weight:bold; margin-top:10px;">Your Ultimate Travel Companion</p>
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
            st.metric("Estimated Fee (THB)", f"{total:,.0f}")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="glow-card"><h3>✈️ Policy: {selected}</h3>{info["text"]}</div>', unsafe_allow_html=True)

elif page == "📘 ABOUT":
    st.markdown("""
    <div class="glow-card">
        <h3>📘 About</h3>
        <p>ระบบคำนวณสัมภาระอัจฉริยะ อ้างอิงนโยบายสายการบินล่าสุดปี 2568</p>
    </div>
    """, unsafe_allow_html=True)