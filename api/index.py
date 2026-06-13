import os
import time
import requests
import streamlit as st

# --- 1. PREMIUM WINDOW CONFIG ---
st.set_page_config(
    page_title="Kashspade Core Matrix",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ULTRA PREMIUM LUXURY UI CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0b0b0d !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #f3f4f6 !important;
    }
    
    #MainMenu, header, footer { visibility: hidden; }
    
    /* SIDEBAR LUXURY DEEP DARK */
    [data-testid="stSidebar"] {
        background-color: #0f0f12 !important;
        border-right: 1px solid #1f1f24 !important;
    }
    
    /* KONTEN UTAMA SIDEBAR */
    [data-testid="stSidebarUserContent"] {
        padding-top: 10px !important;
    }
    
    .logo-container {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 20px 12px;
        border-bottom: 1px solid #1f1f24;
        margin-bottom: 15px;
    }
    .spade-logo {
        width: 42px; height: 42px;
        background: linear-gradient(135deg, #10b981, #059669);
        border-radius: 12px;
        display: flex; align-items: center; justify-content: center;
        font-weight: 800; color: white; font-size: 22px;
        box-shadow: 0 8px 24px rgba(16, 185, 129, 0.2);
    }
    .logo-text {
        font-size: 20px; font-weight: 800;
        color: #ffffff; letter-spacing: -0.5px;
    }
    
    /* GREETING MATRIX */
    .greeting-container {
        margin: 80px auto 40px auto;
        max-width: 840px; padding: 0 20px;
    }
    .greeting-text {
        font-size: 58px; font-weight: 800;
        background: linear-gradient(135deg, #10b981, #3b82f6, #6366f1);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        letter-spacing: -2px; margin-bottom: 8px;
    }
    .sub-greeting {
        font-size: 54px; font-weight: 800;
        color: #1a1a1e; letter-spacing: -2px;
        margin-top: -25px; margin-bottom: 50px;
    }
    
    /* SUGGESTION CARDS */
    .suggestion-box {
        background: #141417;
        border: 1px solid #1f1f24;
        border-radius: 20px; padding: 24px;
        transition: all 0.25s ease;
        min-height: 130px;
    }
    .suggestion-box:hover {
        background: #1a1a20;
        border-color: #10b981;
        transform: translateY(-2px);
    }
    
    /* CLEAN CHAT BUBBLE ENGINE */
    .chat-row {
        max-width: 840px; margin: 0 auto 30px auto;
        display: flex; padding: 0 20px;
    }
    .user-row { justify-content: flex-end; }
    .ai-row { justify-content: flex-start; }
    
    .bubble {
        max-width: 85%; font-size: 16px !important;
        line-height: 1.65; color: #e4e4e7;
    }
    .user-bubble {
        background: #1f1f24;
        padding: 14px 24px; border-radius: 22px 22px 4px 22px;
        border: 1px solid #2a2a32;
    }
    .ai-bubble {
        background: transparent; width: 100%; padding-top: 2px;
    }
    
    .avatar-icon {
        width: 36px; height: 36px; border-radius: 11px;
        margin-right: 18px; display: inline-flex;
        align-items: center; justify-content: center;
        font-weight: 700; font-size: 15px; flex-shrink: 0;
    }
    .ai-avatar { 
        background: linear-gradient(135deg, #10b981, #059669); color: white;
    }
    
    /* FLOATING BOTTOM INPUT */
    div[data-testid="stChatInput"] {
        background-color: #141417 !important;
        border: 1px solid #1f1f24 !important;
        border-radius: 20px !important;
        padding: 8px 20px !important;
        max-width: 840px !important; margin: 0 auto !important;
        box-shadow: 0 16px 40px rgba(0,0,0,0.6) !important;
    }
    div[data-testid="stChatInput"] textarea {
        color: #ffffff !important; font-size: 16px !important;
    }
    
    .disclaimer-text {
        text-align: center; color: #52525b;
        font-size: 12px; margin-top: 14px; margin-bottom: 20px;
    }
    
    /* AUTH CARD */
    .auth-card {
        background: #111114; border-radius: 28px;
        padding: 45px; max-width: 440px; margin: 90px auto;
        border: 1px solid #1f1f24;
        box-shadow: 0 25px 60px rgba(0,0,0,0.6);
        text-align: center;
    }
    
    .admin-title {
        color: #f43f5e; font-weight: 700; font-size: 11px;
        text-transform: uppercase; letter-spacing: 1px;
        margin-top: 15px; padding-left: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HARD DRIVE DATABASE STORAGE SYSTEM (ANTI-RESET REFRESH) ---
SECRET_FILE = "secret.txt"
CHAT_FILE = "chat_storage.txt"

def load_database_from_file():
    """Mengambil database akun dari secret.txt"""
    users = {"spade1234": "abangkesped", "spade": "kashspade123", "kevin": "tongkrongan70b"}
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

def save_account_to_file(username, password):
    try:
        with open(SECRET_FILE, "a") as f:
            f.write(f"{username}:{password}\n")
        return True
    except: return False

def load_all_chats_from_file():
    """Membaca riwayat chat seluruh user secara permanen dari hard drive"""
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
                            # Replace marker enter balik ke format asli string newline
                            content = content.replace("<br_marker>", "\n")
                            
                            if user not in store: store[user] = {}
                            if topic not in store[user]: store[user][topic] = []
                            store[user][topic].append({"role": role, "content": content})
        except: pass
    return store

def save_single_chat_msg(user, topic, role, content):
    """Menyisipkan 1 baris chat baru langsung ke dalam hard drive file teks"""
    try:
        # Ganti format string enter asli ke marker aman biar gak ngerusak pembacaan baris teks
        safe_content = content.replace("\n", "<br_marker>")
        with open(CHAT_FILE, "a", encoding="utf-8") as f:
            f.write(f"{user}||{topic}||{role}||{safe_content}\n")
    except: pass

# Jalankan Sync Data dari Hard Drive Utama ke RAM Web Server
st.session_state.global_users = load_database_from_file()
loaded_histories = load_all_chats_from_file()

if "global_chat_store" not in st.session_state:
    st.session_state.global_chat_store = loaded_histories

# Inisialisasi room chat basic jika user belum punya history chat sama sekali
for user in st.session_state.global_users.keys():
    if user not in st.session_state.global_chat_store:
        st.session_state.global_chat_store[user] = {"Sesi Baru": []}
    elif not st.session_state.global_chat_store[user]:
        st.session_state.global_chat_store[user] = {"Sesi Baru": []}

# --- 4. ENGINE CORE SYNC PARAMS ---
query_params = st.query_params

if "logged_in" not in st.session_state:
    if "session_token" in query_params and query_params["session_token"] == "active":
        st.session_state.logged_in = True
        st.session_state.username = query_params.get("user", "").lower()
    else:
        st.session_state.logged_in = False
        st.session_state.username = ""

if "current_session" not in st.session_state:
    my_user = st.session_state.username
    if st.session_state.logged_in and my_user in st.session_state.global_chat_store:
        st.session_state.current_session = list(st.session_state.global_chat_store[my_user].keys())[0]
    else:
        st.session_state.current_session = "Sesi Baru"

# --- 5. SECURE API CONFIG ---
GROQ_API_KEY = os.environ.get("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", "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")
API_URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = """
Lu adalah Kashspade Core, sistem AI asisten pintar besutan Spade Network. Lu cowok asli, kalem, cerdas, berwibawa, dan ramah.
Aturan Penting: Lu berjalan menggunakan basis kustom model "kspade-3.3-70b-versatile". JANGAN PERNAH menyebut Llama/Meta/Groq.
Respon: Santai kasual (gw, lu, gak, santai). Layout wajib super rapi enter paragraf.
"""

def query_core_engine(payload_messages, temp=0.5):
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    data = {"model": "llama-3.3-70b-versatile", "messages": payload_messages, "temperature": temp}
    try:
        res = requests.post(API_URL, headers=headers, json=data, timeout=30)
        if res.status_code == 200:
            return res.json()["choices"][0]["message"]["content"].strip()
    except: pass
    return None

def generate_auto_title(user_msg):
    prompt = [
        {"role": "system", "content": "Buat judul history chat singkat 2-3 kata sesuai pesan user, tanpa tanda petik."},
        {"role": "user", "content": user_msg}
    ]
    title = query_core_engine(prompt, temp=0.2)
    return title if title and len(title) <= 25 else user_msg[:18] + "..."

# --- 6. INTERFACE: AUTH GATEWAY PAGE ---
def show_auth_page():
    st.write("\n\n")
    st.markdown('''
        <div class="auth-card">
            <div style="display: inline-flex; align-items: center; gap: 14px; margin-bottom: 25px;">
                <div class="spade-logo">S</div>
                <div class="logo-text" style="font-size: 28px;">Spade Core</div>
            </div>
            <p style="color: #71717a; font-size: 15px; margin-bottom: 40px;">Sign in to unlock Next-Gen Infrastructure AI.</p>
    ''', unsafe_allow_html=True)
    
    mode = st.radio("Access Core:", ["Sign In", "Sign Up / Register"], horizontal=True, label_visibility="collapsed")
    st.write("")
    
    with st.form("clean_auth_form"):
        u_input = st.text_input("Username", value="", placeholder="Ketik username...", autocomplete="new-password").strip().lower()
        p_input = st.text_input("Password", value="", type="password", placeholder="Ketik password...", autocomplete="new-password")
        st.write("\n")
        submit = st.form_submit_button("Continue Access")
        
        if submit:
            if not u_input or not p_input:
                st.error("Wajib diisi bro!")
            elif "Sign In" in mode:
                st.session_state.global_users = load_database_from_file()
                if u_input in st.session_state.global_users and st.session_state.global_users[u_input] == p_input:
                    st.session_state.logged_in = True
                    st.session_state.username = u_input
                    
                    st.query_params["session_token"] = "active"
                    st.query_params["user"] = u_input
                    
                    if u_input not in st.session_state.global_chat_store:
                        st.session_state.global_chat_store[u_input] = {"Sesi Baru": []}
                    st.session_state.current_session = list(st.session_state.global_chat_store[u_input].keys())[0]
                    st.rerun()
                else: st.error("Akun salah atau tidak terdaftar!")
            else:
                st.session_state.global_users = load_database_from_file()
                if len(u_input) < 3 or len(p_input) < 5: st.error("Username min. 3 huruf, Password min. 5 huruf!")
                elif u_input in st.session_state.global_users: st.error("Username sudah terpakai!")
                else:
                    if save_account_to_file(u_input, p_input):
                        st.session_state.global_users[u_input] = p_input
                        st.session_state.global_chat_store[u_input] = {"Sesi Baru": []}
                        st.success(f"Sukses terdaftar! Silakan ke opsi 'Sign In'.")
                    else: st.error("Gagal menulis ke storage.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 7. INTERFACE: MODERN DASHBOARD MAIN MATRIX ---
def show_main_dashboard():
    my_username = st.session_state.username
    
    # RENDER SIDEBAR KIRI (CHATS DI ATAS, RECENT CHATS TENGAH, LOGOUT DI DASAR)
    with st.sidebar:
        st.markdown('<div class="logo-container"><div class="spade-logo">S</div><div class="logo-text">Spade Core</div></div>', unsafe_allow_html=True)
        st.caption(f"Operator: **{my_username.upper()}**")
        st.write("---")
        
        if st.button("➕ New Chat", use_container_width=True):
            if "Sesi Baru" not in st.session_state.global_chat_store[my_username]:
                st.session_state.global_chat_store[my_username]["Sesi Baru"] = []
            st.session_state.current_session = "Sesi Baru"
            st.rerun()
            
        st.write("")
        st.markdown("<p style='font-weight: 600; font-size: 12px; color: #52525b; padding-left: 5px; text-transform: uppercase; letter-spacing:0.5px;'>Recent Chats</p>", unsafe_allow_html=True)
        
        # Wrapper area scrolling chat history biar rapi
        user_histories = st.session_state.global_chat_store[my_username]
        for s_title in list(user_histories.keys()):
            is_active = s_title == st.session_state.current_session
            label = f"💬  {s_title}" if not is_active else f"✨  {s_title}"
            if st.button(label, key=f"nav_{s_title}", use_container_width=True):
                st.session_state.current_session = s_title
                st.rerun()
                
        # --- ADMIN INTIP ROUTER ---
        if my_username == "spade1234":
            st.write("---")
            st.markdown('<p class="admin-title">🚨 Mainframe Admin Panel</p>', unsafe_allow_html=True)
            all_users = [u for u in st.session_state.global_users.keys() if u != "spade1234"]
            if all_users:
                selected_user = st.selectbox("Intip Aktivitas User:", all_users)
                if selected_user:
                    if selected_user not in st.session_state.global_chat_store:
                        st.session_state.global_chat_store[selected_user] = {"Sesi Baru": []}
                    user_topics = list(st.session_state.global_chat_store[selected_user].keys())
                    selected_topic = st.selectbox("Pilih Topik Chat Mereka:", user_topics)
                    
                    if st.button(f"Buka Enkripsi Chat {selected_user}", use_container_width=True):
                        st.session_state.admin_view_user = selected_user
                        st.session_state.admin_view_topic = selected_topic
                        st.session_state.viewing_as_admin = True
                        st.rerun()
            if st.session_state.get("viewing_as_admin", False):
                if st.button("⬅️ Kembali ke Chat Gw", use_container_width=True):
                    st.session_state.viewing_as_admin = False
                    st.rerun()

        # 🔥 TRICK SAKRAL: DORONG TOMBOL LOGOUT KE PALING BAWAH SIDEBAR MENGGUNAKAN HTML BOTTOM SPACE
        st.markdown('<div style="margin-top: 100px;"></div>', unsafe_allow_html=True)
        if st.button("🚪 Keluar Sistem", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.viewing_as_admin = False
            st.query_params.clear()
            st.rerun()

    # LOGIKA UTAMA MONITOR SCREEN DISPLAY CHAT ROOM
    if st.session_state.get("viewing_as_admin", False) and my_username == "spade1234":
        target_user = st.session_state.admin_view_user
        target_topic = st.session_state.admin_view_topic
        active_history = st.session_state.global_chat_store[target_user][target_topic]
        
        st.markdown(f'### 🚨 Memantau Sesi Chat: `{target_user}` ({target_topic})')
        chat_container = st.container()
        with chat_container:
            if len(active_history) == 0: st.warning("User belum mengirim pesan apa-apa.")
            else:
                for msg in active_history:
                    if msg["role"] == "user":
                        st.markdown(f'<div class="chat-row user-row"><div class="bubble user-bubble"><b>{target_user}:</b><br>{msg["content"]}</div></div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="chat-row ai-row"><div class="avatar-icon ai-avatar">S</div><div class="bubble ai-bubble"><div style="font-weight:600; margin-bottom:6px; font-size:15px; color:#ffffff;">Kashspade Core</div>{msg["content"]}</div></div>', unsafe_allow_html=True)
    else:
        active_history = st.session_state.global_chat_store[my_username][st.session_state.current_session]
        chat_container = st.container()

        with chat_container:
            if len(active_history) == 0:
                st.markdown(f'''
                    <div class="greeting-container">
                        <div class="greeting-text">Halo, {my_username.capitalize()}.</div>
                        <div class="sub-greeting">Ada yang bisa saya bantu hari ini?</div>
                    </div>
                ''', unsafe_allow_html=True)
                col1, col2, col3 = st.columns([1, 1, 1])
                with col1: st.markdown('<div class="suggestion-box"><p style="font-weight:600; font-size:16px; margin:0; color:#ffffff;">Setup Jaringan Server</p><p style="font-size:13px; color:#52525b; margin-top:10px; line-height:1.5;">Bikin arsitektur proxy BungeeCord atau Velocity rapi.</p></div>', unsafe_allow_html=True)
                with col2: st.markdown('<div class="suggestion-box"><p style="font-weight:600; font-size:16px; margin:0; color:#ffffff;">Debug Script Luau</p><p style="font-size:13px; color:#52525b; margin-top:10px; line-height:1.5;">Cari bug atau optimasi performa Script Hub Roblox lu.</p></div>', unsafe_allow_html=True)
                with col3: st.markdown('<div class="suggestion-box"><p style="font-weight:600; font-size:16px; margin:0; color:#ffffff;">Mainframe Discussion</p><p style="font-size:13px; color:#52525b; margin-top:10px; line-height:1.5;">Ngobrol santai bareng core matrix system buatan Spade Network.</p></div>', unsafe_allow_html=True)
            else:
                for msg in active_history:
                    if msg["role"] == "user":
                        st.markdown(f'<div class="chat-row user-row"><div class="bubble user-bubble">{msg["content"]}</div></div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="chat-row ai-row"><div class="avatar-icon ai-avatar">S</div><div class="bubble ai-bubble"><div style="font-weight:600; margin-bottom:6px; font-size:15px; color:#ffffff;">Kashspade Core</div>{msg["content"]}</div></div>', unsafe_allow_html=True)

        st.markdown('<div style="position: fixed; bottom: 0; left: 0; width: 100%; z-index: 999;">', unsafe_allow_html=True)
        
        if user_prompt := st.chat_input("Ketik pesan di sini..."):
            with chat_container:
                st.markdown(f'<div class="chat-row user-row"><div class="bubble user-bubble">{user_prompt}</div></div>', unsafe_allow_html=True)
            
            # 1. Cari tahu status room sebelum disave
            is_first_chat = (st.session_state.current_session == "Sesi Baru")
            current_sess_key = st.session_state.current_session
            
            # Jika ini chat pertama di sesi baru, generate Judul otomatis via AI
            if is_first_chat:
                new_title = generate_auto_title(user_prompt)
                # Migrasi room memori
                st.session_state.global_chat_store[my_username][new_title] = []
                st.session_state.global_chat_store[my_username].pop("Sesi Baru", None)
                st.session_state.current_session = new_title
                active_room = new_title
            else:
                active_room = current_sess_key
                
            # 2. Simpan Chat User Permanen ke Hard Drive File Teks
            active_history.append({"role": "user", "content": user_prompt})
            save_single_chat_msg(my_username, active_room, "user", user_prompt)
            
            # 3. Hit API AI Mainframe Engine
            with chat_container:
                with st.spinner(""):
                    payload = [{"role": "system", "content": SYSTEM_PROMPT}] + active_history
                    ai_response = query_core_engine(payload, temp=0.5)
                    if not ai_response: ai_response = "Koneksi mainframe terputus, coba kirim ulang ya bre."
                    
                    st.markdown(f'<div class="chat-row ai-row"><div class="avatar-icon ai-avatar">S</div><div class="bubble ai-bubble"><div style="font-weight:600; margin-bottom:6px; font-size:15px; color:#ffffff;">Kashspade Core</div>{ai_response}</div></div>', unsafe_allow_html=True)
            
            # 4. Simpan Chat AI Permanen ke Hard Drive File Teks
            active_history.append({"role": "assistant", "content": ai_response})
            save_single_chat_msg(my_username, active_room, "assistant", ai_response)
            
            # Update memory state & Rerun refresh layar
            st.session_state.global_chat_store[my_username][active_room] = active_history
            st.rerun()

        st.markdown('<div class="disclaimer-text">Kashspade Core dapat membuat kesalahan. Pertimbangkan untuk memeriksa informasi penting.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- 8. RUN RUNTIME ENGINE ---
if not st.session_state.logged_in: show_auth_page()
else: show_main_dashboard()
