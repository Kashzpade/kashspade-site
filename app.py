import streamlit as st
import requests
import time

# --- 1. SETTING HALAMAN & CONFIG INTERFACE ---
st.set_page_config(
    page_title="Kashspade Core",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. THEME ENGINE: GEMINI UPGRADED (FTS & INSTANT FLOW) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #131314 !important;
        font-family: 'Inter', sans-serif !important;
        color: #e3e3e3 !important;
    }
    
    /* Sembunyikan elemen default Streamlit */
    #MainMenu, header, footer {visibility: hidden;}
    
    /* SIDEBAR STYLE */
    [data-testid="stSidebar"] {
        background-color: #1e1e20 !important;
        border-right: none !important;
    }
    
    /* LOGO BRANDING PREMIUM */
    .logo-container {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 15px 8px 25px 8px;
    }
    .spade-logo {
        width: 38px;
        height: 38px;
        background: linear-gradient(135deg, #10b981, #059669);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        color: white;
        font-size: 19px;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25);
    }
    .logo-text {
        font-size: 19px;
        font-weight: 600;
        color: #f3f4f6;
        letter-spacing: -0.3px;
    }
    
    /* GREETING SCREEN */
    .greeting-container {
        margin: 60px auto 40px auto;
        max-width: 850px;
        padding: 0 20px;
    }
    .greeting-text {
        font-size: 48px; /* Diperbesar sedikit */
        font-weight: 500;
        background: linear-gradient(to right, #4285f4, #9b51e0, #e91e63);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    .sub-greeting {
        font-size: 48px; /* Diperbesar sedikit */
        font-weight: 500;
        color: #444746;
        margin-top: -15px;
        margin-bottom: 40px;
    }
    
    /* CARD SUGGESTION */
    .suggestion-box {
        background-color: #1e1e20;
        border: 1px solid #1e1e20;
        border-radius: 16px;
        padding: 22px;
        cursor: pointer;
        transition: 0.2s ease;
        min-height: 130px;
    }
    .suggestion-box:hover {
        background-color: #282a2c;
    }
    
    /* CHAT RENDERING ROWS - FONT RADAR GEDEAN DIKIT ⚡ */
    .chat-row {
        max-width: 850px;
        margin: 0 auto 36px auto;
        display: flex;
        padding: 0 20px;
    }
    .user-row { justify-content: flex-end; }
    .ai-row { justify-content: flex-start; }
    
    .bubble {
        max-width: 85%;
        font-size: 17px !important; /* Font dinaikin dari 16px ke 17px biar mantap */
        line-height: 1.65;
        color: #e3e3e3;
    }
    .user-bubble {
        background-color: #2b2a33;
        padding: 16px 24px;
        border-radius: 24px;
    }
    .ai-bubble {
        background-color: transparent;
        padding-top: 5px;
        width: 100%;
    }
    
    .avatar-icon {
        width: 34px;
        height: 34px;
        border-radius: 50%;
        margin-right: 20px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        font-size: 15px;
        flex-shrink: 0;
    }
    .ai-avatar { 
        background: linear-gradient(135deg, #10b981, #059669); 
        color: white; 
    }
    
    /* FLOATING STICKY INPUT BOX BOTTOM */
    div[data-testid="stChatInput"] {
        background-color: #1e1e20 !important;
        border: 1px solid #3c4043 !important;
        border-radius: 32px !important;
        padding: 8px 20px !important;
        max-width: 850px !important;
        margin: 0 auto !important;
    }
    div[data-testid="stChatInput"] textarea {
        color: #e3e3e3 !important;
        font-size: 17px !important; /* Font input box dinaikin */
    }
    
    /* DISCLAIMER TEXT */
    .disclaimer-text {
        text-align: center;
        color: #8e918f;
        font-size: 13px;
        margin-top: 14px;
        margin-bottom: 20px;
        font-weight: 400;
    }
    
    /* AUTHENTICATION BOX CARD - LEBIH GOOD & PREMIUM */
    .auth-card {
        background: #1e1e20;
        border-radius: 28px;
        padding: 45px;
        max-width: 460px;
        margin: 90px auto;
        border: 1px solid #2d2f31;
        box-shadow: 0 25px 60px rgba(0,0,0,0.6);
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. INITIAL DATA MOCKUP USER & STATE ---
if "user_db" not in st.session_state:
    st.session_state.user_db = {
        "spade": "kashspade123",
        "kevin": "tongkrongan70b"
    }

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "chat_histories" not in st.session_state:
    st.session_state.chat_histories = {"Sesi Baru": []}
if "current_session" not in st.session_state:
    st.session_state.current_session = "Sesi Baru"

# --- 4. ENGINE CORE CONFIGURATION (GROQ REBRANDED) ---
GROQ_API_KEY = "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"  # Taruh API Key Groq lu di sini bre
API_URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = """
Lu adalah Kashspade Core, sistem AI asisten pintar besutan Spade Network. Lu cowok asli, kalem, cerdas, berwibawa, dan ramah.

Aturan Penting & Rebranding Model (WAJIB):
- Lu adalah AI mandiri bernama "Kashspade Core" yang berjalan menggunakan basis model kustom "kspade-3.3-70b-versatile".
- JANGAN PERNAH menyebut kata "Llama", "Meta", atau "Groq" kepada user. Lu sepenuhnya dikembangkan di bawah infrastruktur Spade Network.
- Jika ditanya basis model atau buatan siapa, jawab dengan tenang: "Gw Kashspade Core, model kustom kspade-3.3-70b-versatile yang dikembangin di infrastruktur Spade Network, bre."

Aturan Respon Umum:
- Gunakan bahasa santai kasual sehari-hari yang normal dan tenang (gw, lu, gak, santai). JANGAN SOK ASIK lebay.
- Tata letak jawaban wajib rapi, gunakan jarak antar paragraf (enter), penomoran, bullet points, atau markdown code block (```) jika menuliskan tutorial/codingan.
- Pencipta/developer utama lu adalah Spade Network.
"""

def query_core_engine(payload_messages, temp=0.5):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.3-70b-versatile", 
        "messages": payload_messages,
        "temperature": temp
    }
    try:
        res = requests.post(API_URL, headers=headers, json=data, timeout=30)
        if res.status_code == 200:
            return res.json()["choices"][0]["message"]["content"].strip()
    except:
        pass
    return None

def generate_auto_title(user_msg):
    prompt = [
        {"role": "system", "content": "Lu adalah core pembuat judul history chat singkat. Analisis chat pertama user, lalu buatkan judul topik obrolan dalam bahasa Indonesia maksimal 2 sampai 3 kata saja! JANGAN pake tanda petik, JANGAN ada kata tambahan, langsung berikan hasil judul murninya saja."},
        {"role": "user", "content": f"Pesan: {user_msg}"}
    ]
    title = query_core_engine(prompt, temp=0.2)
    if not title or len(title) > 30:
        title = user_msg[:18] + "..."
    return title

# --- 5. INTERFACE: LOGIN & REGISTER GATE ---
def show_auth_page():
    st.write("\n\n")
    st.markdown('''
        <div class="auth-card">
            <div style="display: inline-flex; align-items: center; gap: 12px; margin-bottom: 20px;">
                <div class="spade-logo">S</div>
                <div class="logo-text" style="font-size: 25px; font-weight:700;">Spade Core</div>
            </div>
            <p style="color: #9aa0a6; font-size: 15px; margin-bottom: 35px;">Sign in to unlock Next-Gen Infrastructure AI.</p>
    ''', unsafe_allow_html=True)
    
    mode = st.radio("Access Core:", ["Sign In", "Sign Up / Register"], horizontal=True, label_visibility="collapsed")
    st.write("")
    
    with st.form("clean_auth_form"):
        u_input = st.text_input("Username", placeholder="Username lu...").strip().lower()
        p_input = st.text_input("Password", type="password", placeholder="Password lu...")
        st.write("\n")
        submit = st.form_submit_button("Continue Access")
        
        if submit:
            if "Sign In" in mode:
                if u_input in st.session_state.user_db and st.session_state.user_db[u_input] == p_input:
                    st.session_state.logged_in = True
                    st.session_state.username = u_input
                    st.success("Akses diterima. Membuka interface...")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("Akun salah atau belum terdaftar, bre.")
            else:
                if len(u_input) < 3 or len(p_input) < 5:
                    st.error("Username min. 3 huruf, Password min. 5 huruf!")
                elif u_input in st.session_state.user_db:
                    st.error("Username sudah terpakai!")
                else:
                    st.session_state.user_db[u_input] = p_input
                    st.success("Registrasi sukses! Silakan switch ke menu 'Sign In' buat login.")

    st.markdown('</div>', unsafe_allow_html=True)

# --- 6. INTERFACE: MAIN DASHBOARD ---
def show_main_dashboard():
    with st.sidebar:
        st.markdown('''
            <div class="logo-container">
                <div class="spade-logo">S</div>
                <div class="logo-text">Spade Core</div>
            </div>
        ''', unsafe_allow_html=True)
        
        st.caption(f"Operator: **{st.session_state.username.upper()}**")
        st.write("---")
        
        if st.button("➕ New Chat", use_container_width=True):
            if "Sesi Baru" not in st.session_state.chat_histories:
                st.session_state.chat_histories["Sesi Baru"] = []
            st.session_state.current_session = "Sesi Baru"
            st.rerun()
            
        st.write("")
        st.markdown("<p style='font-weight: 500; font-size: 14px; color: #8e918f; padding-left: 5px;'>Recent Chats</p>", unsafe_allow_html=True)
        
        for s_title in list(st.session_state.chat_histories.keys()):
            is_active = s_title == st.session_state.current_session
            label = f"💬  {s_title}" if not is_active else f"✨  {s_title}"
            if st.button(label, key=f"nav_{s_title}", use_container_width=True):
                st.session_state.current_session = s_title
                st.rerun()
                
        st.write("---")
        if st.button("🚪 Keluar Sistem", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()

    # AREA RENDER UTAMA
    active_history = st.session_state.chat_histories[st.session_state.current_session]
    
    # Placeholder container kosong untuk menaruh chat row dinamis
    chat_container = st.container()

    with chat_container:
        if len(active_history) == 0:
            st.markdown(f'''
                <div class="greeting-container">
                    <div class="greeting-text">Halo, {st.session_state.username.capitalize()}.</div>
                    <div class="sub-greeting">Ada yang bisa saya bantu hari ini?</div>
                </div>
            ''', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                st.markdown('<div class="suggestion-box"><p style="font-weight:500; font-size:15px; margin:0; color:#e3e3e3;">Buat tutorial config server</p><p style="font-size:13px; color:#8e918f; margin-top:10px;">Bikin setup jaringan server Minecraft rapi</p></div>', unsafe_allow_html=True)
            with col2:
                st.markdown('<div class="suggestion-box"><p style="font-weight:500; font-size:15px; margin:0; color:#e3e3e3;">Bantu debug script</p><p style="font-size:13px; color:#8e918f; margin-top:10px;">Cari error kode program Python atau Luau</p></div>', unsafe_allow_html=True)
            with col3:
                st.markdown('<div class="suggestion-box"><p style="font-weight:500; font-size:15px; margin:0; color:#e3e3e3;">Tulis teks kasual</p><p style="font-size:13px; color:#8e918f; margin-top:10px;">Ngobrol santai bareng core matrix system</p></div>', unsafe_allow_html=True)
        else:
            for msg in active_history:
                if msg["role"] == "user":
                    st.markdown(f'<div class="chat-row user-row"><div class="bubble user-bubble">{msg["content"]}</div></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'''
                        <div class="chat-row ai-row">
                            <div class="avatar-icon ai-avatar">S</div>
                            <div class="bubble ai-bubble">
                                <div style="font-weight:600; margin-bottom:8px; font-size:16px; color:#fff;">Kashspade Core</div>
                                {msg["content"]}
                            </div>
                        </div>
                    ''', unsafe_allow_html=True)

    # --- INPUT BOX LAYOUT & LOGIC PROSES UTAMA ---
    st.markdown('<div style="position: fixed; bottom: 0; left: 0; width: 100%; z-index: 999;">', unsafe_allow_html=True)
    
    if user_prompt := st.chat_input("Ketik pesan di sini..."):
        # 🔥 CRITICAL UPGRADE: Render instan chat user saat itu juga biar nampil duluan!
        with chat_container:
            st.markdown(f'<div class="chat-row user-row"><div class="bubble user-bubble">{user_prompt}</div></div>', unsafe_allow_html=True)
        
        # Simpan pesan user ke history data
        active_history.append({"role": "user", "content": user_prompt})
        is_first_chat = (st.session_state.current_session == "Sesi Baru")
        current_sess_key = st.session_state.current_session
        
        # Jalankan animasi loading tepat di bawah chat user yang udah nampil
        with chat_container:
            with st.spinner(""):
                payload = [{"role": "system", "content": SYSTEM_PROMPT}] + active_history
                ai_response = query_core_engine(payload, temp=0.5)
                if not ai_response:
                    ai_response = "Koneksi mainframe terputus, coba kirim ulang ya bre."
                
                # Tampilkan respon AI setelah spinner selesai
                st.markdown(f'''
                    <div class="chat-row ai-row">
                        <div class="avatar-icon ai-avatar">S</div>
                        <div class="bubble ai-bubble">
                            <div style="font-weight:600; margin-bottom:8px; font-size:16px; color:#fff;">Kashspade Core</div>
                            {ai_response}
                        </div>
                    </div>
                ''', unsafe_allow_html=True)
                
        # Simpan ke state global
        active_history.append({"role": "assistant", "content": ai_response})
        
        if is_first_chat:
            new_title = generate_auto_title(user_prompt)
            st.session_state.chat_histories[new_title] = active_history
            st.session_state.chat_histories.pop("Sesi Baru", None)
            st.session_state.current_session = new_title
        else:
            st.session_state.chat_histories[current_sess_key] = active_history
            
        st.rerun()

    st.markdown('<div class="disclaimer-text">Kashspade Core adalah AI dan dapat melakukan kesalahan. Pertimbangkan untuk memeriksa informasi penting.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 7. APPS ENGINE GATEWAY ---
if not st.session_state.logged_in:
    show_auth_page()
else:
    show_main_dashboard()