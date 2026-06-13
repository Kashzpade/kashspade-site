import os
import time
import requests
import streamlit as st

# --- 1. INFINITEX WINDOW CONFIG ---
st.set_page_config(
    page_title="Kashspade Core Matrix",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="collapsed" # Kita collapse bawaannya karena kita bikin CUSTOM SIDEBAR
)

# --- 2. INFINITEX V2 ULTRA LUXURY CYBERPUNK CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Reset & Deep Space Black */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #070709 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #f3f4f6 !important;
    }
    
    /* Sembunyikan elemen default Streamlit biar ga ngerusak pemandangan */
    [data-testid="stSidebar"], header, footer { display: none !important; }
    .stMainBlockContainer { padding: 0px !important; max-width: 100% !important; }
    
    /* LAUNCHING INFINITEX GRID LAYOUT */
    .infinitex-container {
        display: flex;
        height: 100vh;
        width: 100vw;
        overflow: hidden;
    }
    
    /* PERMANENT CUSTOM SIDEBAR (ANTI NGUMPET) */
    .custom-sidebar {
        width: 280px;
        background-color: #0d0d11;
        border-right: 1px solid #1a1a22;
        display: flex;
        flex-direction: column;
        padding: 20px;
        flex-shrink: 0;
        z-index: 999;
    }
    
    .sidebar-header {
        display: flex;
        align-items: center;
        gap: 12px;
        padding-bottom: 20px;
        border-bottom: 1px solid #1a1a22;
        margin-bottom: 20px;
    }
    
    .spade-badge {
        width: 38px; height: 38px;
        background: linear-gradient(135deg, #10b981, #059669);
        border-radius: 10px;
        display: flex; align-items: center; justify-content: center;
        font-weight: 800; color: white; font-size: 20px;
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.3);
    }
    
    .sidebar-title {
        font-size: 18px; font-weight: 800; color: #ffffff;
        letter-spacing: -0.5px;
    }
    
    .menu-indicator {
        font-size: 12px; font-weight: 700; color: #10b981;
        background: rgba(16, 185, 129, 0.1);
        padding: 6px 12px; border-radius: 8px;
        margin-bottom: 20px; display: flex; align-items: center; gap: 8px;
    }
    
    /* MAIN CHAT INTERFACE AREA */
    .main-chat-area {
        flex-grow: 1;
        display: flex;
        flex-direction: column;
        background-color: #070709;
        position: relative;
        height: 100vh;
        overflow-y: auto;
    }
    
    /* GREETING DASHBOARD */
    .greeting-wrapper {
        margin: auto; max-width: 760px; text-align: left;
        padding: 40px 20px; width: 100%;
    }
    .hero-text {
        font-size: 52px; font-weight: 800;
        background: linear-gradient(135deg, #10b981, #3b82f6);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        letter-spacing: -1.5px; margin-bottom: 5px;
    }
    .sub-hero {
        font-size: 46px; font-weight: 800; color: #16161c;
        letter-spacing: -1.5px; margin-top: -15px; margin-bottom: 40px;
    }
    
    /* SUGGESTION LUXURY CARDS */
    .card-grid {
        display: grid; grid-template-columns: repeat(3, 11fr); gap: 16px;
    }
    .luxury-card {
        background: #0d0d11; border: 1px solid #1a1a22;
        border-radius: 16px; padding: 20px; transition: all 0.2s ease;
    }
    .luxury-card:hover {
        border-color: #10b981; background: #121218; transform: translateY(-2px);
    }
    
    /* CHAT STREAM ENGINE BUBBLES */
    .stream-container {
        max-width: 760px; width: 100%; margin: 40px auto 140px auto;
        padding: 0 20px; display: flex; flex-direction: column; gap: 28px;
    }
    .chat-block { display: flex; width: 100%; }
    .block-user { justify-content: flex-end; }
    .block-ai { justify-content: flex-start; }
    
    .msg-bubble { max-width: 85%; font-size: 15.5px; line-height: 1.6; }
    .bubble-user {
        background: #16161e; border: 1px solid #22222a;
        padding: 14px 20px; border-radius: 20px 20px 4px 20px; color: #f3f4f6;
    }
    .bubble-ai { width: 100%; color: #e4e4e7; }
    
    .ai-identity {
        display: flex; align-items: center; gap: 10px;
        font-weight: 600; color: #ffffff; font-size: 14px; margin-bottom: 6px;
    }
    .ai-dot { width: 8px; height: 8px; background: #10b981; border-radius: 50%; }
    
    /* FIXED FLOATING BOTTOM BAR INPUT */
    .bottom-bar-lock {
        position: fixed; bottom: 0; right: 0;
        width: calc(100% - 280px); /* Presisi memotong lebar custom sidebar */
        background: linear-gradient(to top, #070709 70%, transparent);
        padding: 30px 40px 20px 40px; z-index: 99;
    }
    
    .input-wrapper-box { max-width: 760px; margin: 0 auto; }
    
    /* Custom style override buat inputbox streamlit biar makin blend-in */
    div[data-testid="stChatInput"] {
        background-color: #0d0d11 !important;
        border: 1px solid #1a1a22 !important;
        border-radius: 16px !important;
    }
    
    .footer-credits {
        text-align: center; color: #44444f; font-size: 11px; margin-top: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. PERSISTENT STORAGE ENGINE CORE ---
SECRET_FILE = "secret.txt"
CHAT_FILE = "chat_storage.txt"

def load_accounts():
    users = {"spade1234": "abangkesped", "spade": "kashspade123"}
    if os.path.exists(SECRET_FILE):
        try:
            with open(SECRET_FILE, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and ":" in line:
                        u, p = line.split(":", 1)
                        users[u.strip().lower()] = p.strip()
        except: pass
    return users

def save_account(username, password):
    try:
        with open(SECRET_FILE, "a") as f: f.write(f"{username}:{password}\n")
        return True
    except: return False

def load_chat_history():
    store = {}
    if os.path.exists(CHAT_FILE):
        try:
            with open(CHAT_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and "||" in line:
                        parts = line.split("||")
                        if len(parts) == 4:
                            user, topic, role, content = parts
                            content = content.replace("<br_marker>", "\n")
                            if user not in store: store[user] = {}
                            if topic not in store[user]: store[user][topic] = []
                            store[user][topic].append({"role": role, "content": content})
        except: pass
    return store

def save_chat_line(user, topic, role, content):
    try:
        safe_content = content.replace("\n", "<br_marker>")
        with open(CHAT_FILE, "a", encoding="utf-8") as f:
            f.write(f"{user}||{topic}||{role}||{safe_content}\n")
    except: pass

# Sync Database
st.session_state.global_users = load_accounts()
if "global_chat_store" not in st.session_state:
    st.session_state.global_chat_store = load_chat_history()

# --- 4. SESSION MATRIX SYNC ---
query_params = st.query_params

if "logged_in" not in st.session_state:
    if "session_token" in query_params and query_params["session_token"] == "active":
        st.session_state.logged_in = True
        st.session_state.username = query_params.get("user", "").lower()
    else:
        st.session_state.logged_in = False
        st.session_state.username = ""

my_user = st.session_state.username
if st.session_state.logged_in:
    if my_user not in st.session_state.global_chat_store or not st.session_state.global_chat_store[my_user]:
        st.session_state.global_chat_store[my_user] = {"Sesi Baru": []}
    if "current_session" not in st.session_state:
        st.session_state.current_session = list(st.session_state.global_chat_store[my_user].keys())[0]

# --- 5. SECURE MAINFRAME ENGINE API ---
GROQ_API_KEY = os.environ.get("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", "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")
API_URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = """
Lu adalah Kashspade Core, sistem AI asisten pintar besutan Spade Network. Lu cowok asli, kalem, cerdas, berwibawa, dan ramah.
Aturan: Lu berjalan menggunakan basis model "kspade-3.3-70b-versatile". JANGAN PERNAH sebut kata Llama/Meta/Groq.
Respon: Santai kasual sehari-hari (gw, lu, gak, santai). Layout wajib super rapi enter paragraf. Pencipta: Spade Network.
"""

def query_groq(messages):
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    data = {"model": "llama-3.3-70b-versatile", "messages": messages, "temperature": 0.5}
    try:
        res = requests.post(API_URL, headers=headers, json=data, timeout=30)
        if res.status_code == 200: return res.json()["choices"][0]["message"]["content"].strip()
    except: pass
    return None

def make_title(msg):
    prompt = [{"role": "system", "content": "Buat judul singkat 2-3 kata sesuai pesan user, tanpa tanda petik."}, {"role": "user", "content": msg}]
    res = query_groq(prompt)
    return res if res and len(res) <= 25 else msg[:15] + "..."

# --- 6. INTERFACE: AUTH GATEWAY (LOGIN / REGISTER) ---
def render_auth():
    st.write("\n\n")
    st.markdown('''
        <div class="auth-card">
            <div style="display: inline-flex; align-items: center; gap: 14px; margin-bottom: 25px;">
                <div class="spade-badge">S</div>
                <div class="logo-text" style="font-size: 26px; font-weight:800; color:white;">Spade Core</div>
            </div>
            <p style="color: #666673; font-size: 14px; margin-bottom: 35px;">Sign in to connect to the InfiniteX Infrastructure.</p>
    ''', unsafe_allow_html=True)
    
    mode = st.radio("Access Model:", ["Sign In", "Sign Up"], horizontal=True, label_visibility="collapsed")
    st.write("")
    
    with st.form("infinitex_auth"):
        u = st.text_input("Username", placeholder="Username...", autocomplete="off").strip().lower()
        p = st.text_input("Password", type="password", placeholder="Password...")
        st.write("\n")
        if st.form_submit_button("Establish Connection", use_container_width=True):
            if not u or not p: st.error("Isi semua field bro!")
            elif "Sign In" in mode:
                if u in st.session_state.global_users and st.session_state.global_users[u] == p:
                    st.session_state.logged_in = True
                    st.session_state.username = u
                    st.query_params["session_token"] = "active"
                    st.query_params["user"] = u
                    st.session_state.current_session = list(st.session_state.global_chat_store[u].keys())[0]
                    st.rerun()
                else: st.error("Kredensial salah atau tidak terdaftar!")
            else:
                if len(u) < 3 or len(p) < 5: st.error("Username min 3, Password min 5 karakter!")
                elif u in st.session_state.global_users: st.error("Username udah diambil!")
                else:
                    if save_account(u, p):
                        st.session_state.global_users[u] = p
                        st.session_state.global_chat_store[u] = {"Sesi Baru": []}
                        st.success("Sukses terdaftar! Silakan beralih ke Sign In.")
                    else: st.error("Storage Error.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 7. INTERFACE: INFINITEX CORE DASHBOARD APPLICATION ---
def render_dashboard():
    # MEMBUAT LAYOUT KUSTOM BERSAMA SIDEBAR PERMANEN MURNI HTML
    sidebar_html = f'''
    <div class="custom-sidebar">
        <div class="sidebar-header">
            <div class="spade-badge">S</div>
            <div class="sidebar-title">Spade Core</div>
        </div>
        <div class="menu-indicator">
            <span>☰</span> Mainframe Menu Active
        </div>
        <p style="font-size: 11px; color: #44444f; text-transform: uppercase; letter-spacing: 1px; font-weight:700; margin-bottom: 12px; padding-left: 5px;">Operator: {my_user.upper()}</p>
    '''
    st.sidebar.markdown(sidebar_html, unsafe_allow_html=True) # Inject background CSS dasar
    
    # KONTEN INTERAKTIF DI DALAM CUSTOM SIDEBAR KIRI MENGGUNAKAN STREAMLIT COLUMN LOCK
    with st.html('<div class="infinitex-container">'):
        # --- KOLOM 1: SIDEBAR INTERAKTIF ---
        col_side, col_main = st.columns([2.8, 12], gap="small")
        
        with col_side:
            # Render HTML Mockup atas biar UI nyatu sempurna
            st.markdown(f'''
                <div style="display: flex; align-items: center; gap: 12px; padding: 10px 0 20px 0; border-bottom: 1px solid #1a1a22; margin-bottom: 15px;">
                    <div class="spade-badge">S</div>
                    <div class="sidebar-title">Spade Core</div>
                </div>
                <div class="menu-indicator"><span>☰</span> Mainframe Menu Active</div>
                <p style="font-size: 11px; color: #525263; text-transform: uppercase; letter-spacing: 0.5px; font-weight:700; margin-bottom: 10px; padding-left: 5px;">Operator: {my_user.upper()}</p>
            ''', unsafe_allow_html=True)
            
            # Tombol New Chat Sakral
            if st.button("➕ New Chat Room", use_container_width=True):
                if "Sesi Baru" not in st.session_state.global_chat_store[my_user]:
                    st.session_state.global_chat_store[my_user]["Sesi Baru"] = []
                st.session_state.current_session = "Sesi Baru"
                st.rerun()
                
            st.write("")
            st.markdown("<p style='font-weight:700; font-size:11px; color:#525263; text-transform:uppercase; letter-spacing:0.5px; padding-left:5px; margin-bottom:10px;'>Recent Mainframes</p>", unsafe_allow_html=True)
            
            # Rendering List History Chat Room Utama
            user_rooms = st.session_state.global_chat_store[my_user]
            for room_title in list(user_rooms.keys()):
                is_current = (room_title == st.session_state.current_session)
                btn_label = f"✨  {room_title}" if is_current else f"💬  {room_title}"
                if st.button(btn_label, key=f"room_{room_title}", use_container_width=True):
                    st.session_state.current_session = room_title
                    st.rerun()
            
            # Dorong paksa tombol logout ke dasar sidebar paling bawah
            for _ in range(12): st.write("")
            st.markdown("<div style='border-top: 1px solid #1a1a22; margin-bottom:15px;'></div>", unsafe_allow_html=True)
            if st.button("🚪 Disconnect System", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.username = ""
                st.query_params.clear()
                st.rerun()

        # --- KOLOM 2: INTERFACE AREA CHAT UTAMA ---
        with col_main:
            active_history = st.session_state.global_chat_store[my_user][st.session_state.current_session]
            
            # TAMPILKAN HERO GREETING KALAU ROOM MASIH KOSONG
            if len(active_history) == 0:
                st.markdown(f'''
                    <div class="greeting-wrapper">
                        <div class="hero-text">Welcome back, {my_user.capitalize()}.</div>
                        <div class="sub-hero">How can I assist your network today?</div>
                        <div class="card-grid">
                            <div class="luxury-card">
                                <p style="font-weight:700; font-size:15px; margin:0; color:#ffffff;">Core Framework</p>
                                <p style="font-size:12.5px; color:#525263; margin-top:8px; line-height:1.5;">Config proxy networks, server nodes, or plugin databases seamlessly.</p>
                            </div>
                            <div class="luxury-card">
                                <p style="font-weight:700; font-size:15px; margin:0; color:#ffffff;">Automation Scripts</p>
                                <p style="font-size:12.5px; color:#525263; margin-top:8px; line-height:1.5;">Optimize Luau scripts hubs, build custom GUIs, or fix logical handlers.</p>
                            </div>
                            <div class="luxury-card">
                                <p style="font-weight:700; font-size:15px; margin:0; color:#ffffff;">Mainframe Core</p>
                                <p style="font-size:12.5px; color:#525263; margin-top:8px; line-height:1.5;">Engage with kspade-3.3-70b-versatile dedicated model engine.</p>
                            </div>
                        </div>
                    </div>
                ''', unsafe_allow_html=True)
            else:
                # RENDERING OPERASI BUBBLE CHAT PREMIUM
                st.markdown('<div class="stream-container">', unsafe_allow_html=True)
                for msg in active_history:
                    if msg["role"] == "user":
                        st.markdown(f'<div class="chat-block block-user"><div class="msg-bubble bubble-user">{msg["content"]}</div></div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'''
                            <div class="chat-block block-ai">
                                <div class="msg-bubble bubble-ai">
                                    <div class="ai-identity"><div class="ai-dot"></div>Kashspade Core</div>
                                    {msg["content"]}
                                </div>
                            </div>
                        ''', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # --- INPUT PROMPT CONTAINER DENGAN DUDUKAN FIXED BOTTOM BAR ---
            st.markdown('<div class="bottom-bar-lock">', unsafe_allow_html=True)
            st.markdown('<div class="input-wrapper-box">', unsafe_allow_html=True)
            
            if user_prompt := st.chat_input("Ketik instruksi mainframe di sini..."):
                is_new_room = (st.session_state.current_session == "Sesi Baru")
                room_key = st.session_state.current_session
                
                if is_new_room:
                    room_key = make_title(user_prompt)
                    st.session_state.global_chat_store[my_user][room_key] = []
                    st.session_state.global_chat_store[my_user].pop("Sesi Baru", None)
                    st.session_state.current_session = room_key
                
                # Simpan Prompt User
                st.session_state.global_chat_store[my_user][room_key].append({"role": "user", "content": user_prompt})
                save_chat_line(my_user, room_key, "user", user_prompt)
                
                # Request Payload Core AI
                payload = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.global_chat_store[my_user][room_key]
                ai_res = query_groq(payload)
                if not ai_res: ai_res = "Mainframe engine error. Re-try sending transmission bre."
                
                # Simpan Respon AI
                st.session_state.global_chat_store[my_user][room_key].append({"role": "assistant", "content": ai_res})
                save_chat_line(my_user, room_key, "assistant", ai_res)
                st.rerun()
                
            st.markdown('<div class="footer-credits">Kashspade Core Framework v2.0 • InfiniteX Premium UI Model</div>', unsafe_allow_html=True)
            st.markdown('</div></div>', unsafe_allow_html=True) # Tutup Input & Bottom Bar Box
    st.markdown('</div>', unsafe_allow_html=True) # Tutup Container Grid Utama

# --- 8. RUNTIME DISPATCHER ---
if not st.session_state.logged_in: render_auth()
else: render_dashboard()
