import os
import time
import requests
import streamlit as st

# --- 1. PREMIUM WINDOW CONFIG ---
st.set_page_config(
    page_title="Kashspade Core",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ULTRA PREMIUM UI CSS INJECTION ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0f0f11 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #f3f4f6 !important;
    }
    
    #MainMenu, header, footer { visibility: hidden; }
    
    /* SIDEBAR MODERNIZE */
    [data-testid="stSidebar"] {
        background-color: #161619 !important;
        border-right: 1px solid #232329 !important;
    }
    
    .logo-container {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 20px 10px;
        border-bottom: 1px solid #232329;
        margin-bottom: 20px;
    }
    .spade-logo {
        width: 42px; height: 42px;
        background: linear-gradient(135deg, #10b981, #059669);
        border-radius: 14px;
        display: flex; align-items: center; justify-content: center;
        font-weight: 800; color: white; font-size: 22px;
        box-shadow: 0 8px 20px rgba(16, 185, 129, 0.3);
    }
    .logo-text {
        font-size: 20px; font-weight: 700;
        color: #ffffff; letter-spacing: -0.5px;
    }
    
    /* GREETING DASHBOARD (EMPTY STATE) */
    .greeting-container {
        margin: 60px auto 40px auto;
        max-width: 880px; padding: 0 20px;
    }
    .greeting-text {
        font-size: 54px; font-weight: 700;
        background: linear-gradient(135deg, #3b82f6, #8b5cf6, #ec4899);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        letter-spacing: -1.5px; margin-bottom: 12px;
    }
    .sub-greeting {
        font-size: 54px; font-weight: 700;
        color: #27272a; letter-spacing: -1.5px;
        margin-top: -20px; margin-bottom: 50px;
    }
    
    /* CARD SUGGESTIONS */
    .suggestion-box {
        background: #161619;
        border: 1px solid #232329;
        border-radius: 20px; padding: 24px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        min-height: 140px;
    }
    .suggestion-box:hover {
        background: #1e1e24;
        border-color: #10b981;
        transform: translateY(-4px);
        box-shadow: 0 12px 30px rgba(0,0,0,0.4);
    }
    
    /* STREAMING CHAT RENDER */
    .chat-row {
        max-width: 880px; margin: 0 auto 40px auto;
        display: flex; padding: 0 20px;
    }
    .user-row { justify-content: flex-end; }
    .ai-row { justify-content: flex-start; }
    
    .bubble {
        max-width: 82%; font-size: 17px !important;
        line-height: 1.7; color: #e4e4e7;
    }
    .user-bubble {
        background: #27272a;
        padding: 16px 26px; border-radius: 24px 24px 4px 24px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
    }
    .ai-bubble {
        background: transparent; width: 100%; padding-top: 4px;
    }
    
    .avatar-icon {
        width: 38px; height: 38px; border-radius: 12px;
        margin-right: 20px; display: inline-flex;
        align-items: center; justify-content: center;
        font-weight: 700; font-size: 16px; flex-shrink: 0;
    }
    .ai-avatar { 
        background: linear-gradient(135deg, #10b981, #059669); color: white;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
    }
    
    /* STICKY BOTTOM CHAT BOX INPUT */
    div[data-testid="stChatInput"] {
        background-color: #161619 !important;
        border: 1px solid #232329 !important;
        border-radius: 24px !important;
        padding: 10px 24px !important;
        max-width: 880px !important; margin: 0 auto !important;
        box-shadow: 0 20px 40px rgba(0,0,0,0.5) !important;
    }
    div[data-testid="stChatInput"] textarea {
        color: #ffffff !important; font-size: 17px !important;
    }
    
    /* PREMIUM BOTTOM DISCLAIMER */
    .disclaimer-text {
        text-align: center; color: #71717a;
        font-size: 13px; margin-top: 16px; margin-bottom: 24px;
        font-weight: 400; letter-spacing: 0.2px;
    }
    
    /* GATEWAY AUTH CARD */
    .auth-card {
        background: #161619; border-radius: 32px;
        padding: 50px; max-width: 480px; margin: 100px auto;
        border: 1px solid #232329;
        box-shadow: 0 30px 70px rgba(0,0,0,0.7);
        text-align: center;
    }
    
    /* ADMIN PANEL BRANDING */
    .admin-title {
        color: #ef4444; font-weight: 700; font-size: 13px;
        text-transform: uppercase; letter-spacing: 0.8px;
        margin-top: 15px; padding-left: 5px;
    }
    .admin-card {
        background: #1f1f23; border: 1px solid #ef4444;
        border-radius: 12px; padding: 12px; margin-bottom: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. MAINFRAME GLOBAL DATABASE (PERSISTENT VIA STATE) ---
if "global_users" not in st.session_state:
    st.session_state.global_users = {
        "spade1234": "abangkesped",
        "spade": "kashspade123",
        "kevin": "tongkrongan70b"
    }

if "global_chat_store" not in st.session_state:
    st.session_state.global_chat_store = {
        "spade1234": {"Sesi Baru": []},
        "spade": {"Sesi Baru": []},
        "kevin": {"Sesi Baru": []}
    }

# Local Temporary State per runtime user
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "current_session" not in st.session_state:
    st.session_state.current_session = "Sesi Baru"

# --- 4. SECURE ENGINE CONFIG ---
GROQ_API_KEY = os.environ.get("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", "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")
API_URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = """
Lu adalah Kashspade Core, sistem AI asisten pintar besutan Spade Network. Lu cowok asli, kalem, cerdas, berwibawa, dan ramah.
Aturan Penting & Rebranding Model (WAJIB):
- Lu adalah AI mandiri bernama "Kashspade Core" yang berjalan menggunakan basis model kustom "kspade-3.3-70b-versatile".
- JANGAN PERNAH menyebut kata "Llama", "Meta", atau "Groq".
- Jika ditanya basis model, jawab dengan tenang: "Gw Kashspade Core, model kustom kspade-3.3-70b-versatile yang dikembangin di infrastruktur Spade Network, bre."
Aturan Respon: Gunakan bahasa santai kasual sehari-hari (gw, lu, gak, santai). JANGAN SOK ASIK lebay. Layout wajib rapi, gunakan jarak antar paragraf (enter), penomoran, atau markdown code block jika menuliskan codingan. Pencipta lu adalah Spade Network.
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

# --- 5. INTERFACE: HIGH-END AUTH PAGE (SECURE ANTI-AUTOFILL) ---
def show_auth_page():
    st.write("\n\n")
    st.markdown('''
        <div class="auth-card">
            <div style="display: inline-flex; align-items: center; gap: 14px; margin-bottom: 25px;">
                <div class="spade-logo">S</div>
                <div class="logo-text" style="font-size: 28px;">Spade Core</div>
            </div>
            <p style="color: #a1a1aa; font-size: 15px; margin-bottom: 40px; letter-spacing:0.2px;">Sign in to unlock Next-Gen Infrastructure AI.</p>
    ''', unsafe_allow_html=True)
    
    mode = st.radio("Access Core:", ["Sign In", "Sign Up / Register"], horizontal=True, label_visibility="collapsed")
    st.write("")
    
    with st.form("clean_auth_form"):
        # 🔥 AMAN TOTAL: Value di-set kosong ("") & dipaksa ketik manual tanpa auto-fill browser
        u_input = st.text_input("Username", value="", placeholder="Ketik username lu...", autocomplete="new-password").strip().lower()
        p_input = st.text_input("Password", value="", type="password", placeholder="Ketik password lu...", autocomplete="new-password")
        st.write("\n")
        submit = st.form_submit_button("Continue Access")
        
        if submit:
            if not u_input or not p_input:
                st.error("Wajib diisi dulu bro, jangan dikosongin!")
            elif "Sign In" in mode:
                if u_input in st.session_state.global_users and st.session_state.global_users[u_input] == p_input:
                    st.session_state.logged_in = True
                    st.session_state.username = u_input
                    
                    if u_input not in st.session_state.global_chat_store:
                        st.session_state.global_chat_store[u_input] = {"Sesi Baru": []}
                    
                    st.session_state.current_session = list(st.session_state.global_chat_store[u_input].keys())[0]
                    st.rerun()
                else: 
                    st.error("Akun salah atau tidak terdaftar, bre!")
            else:
                if len(u_input) < 3 or len(p_input) < 5: 
                    st.error("Username min. 3 huruf, Password min. 5 huruf!")
                elif u_input in st.session_state.global_users: 
                    st.error("Username sudah terpakai!")
                else:
                    st.session_state.global_users[u_input] = p_input
                    st.session_state.global_chat_store[u_input] = {"Sesi Baru": []}
                    st.success(f"Registrasi Sukses! Silakan ganti opsi ke 'Sign In' lalu ketik manual.")
                    
    st.markdown('</div>', unsafe_allow_html=True)

# --- 6. INTERFACE: MAIN DASHBOARD CORE ---
def show_main_dashboard():
    my_username = st.session_state.username
    
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
        st.markdown("<p style='font-weight: 600; font-size: 13px; color: #71717a; padding-left: 5px; text-transform: uppercase; letter-spacing:0.5px;'>Recent Chats</p>", unsafe_allow_html=True)
        
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
            selected_user = st.selectbox("Intip Aktivitas User:", all_users)
            
            if selected_user:
                st.caption(f"Status Data: **REAL-TIME STORAGE**")
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
        
        st.write("---")
        if st.button("🚪 Keluar Sistem", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.viewing_as_admin = False
            st.rerun()

    if st.session_state.get("viewing_as_admin", False) and my_username == "spade1234":
        target_user = st.session_state.admin_view_user
        target_topic = st.session_state.admin_view_topic
        active_history = st.session_state.global_chat_store[target_user][target_topic]
        
        st.markdown(f'### 🚨 Memantau Sesi Chat: `{target_user}` ({target_topic})')
        st.info("Lu berada dalam mode spectator admin. Seluruh chat baru yang diketik target user bakal muncul di sini pas lu refresh.")
        
        chat_container = st.container()
        with chat_container:
            if len(active_history) == 0:
                st.warning("User ini belum mengirim pesan apa-apa pada sesi ini.")
            else:
                for msg in active_history:
                    if msg["role"] == "user":
                        st.markdown(f'<div class="chat-row user-row"><div class="bubble user-bubble"><b>{target_user}:</b><br>{msg["content"]}</div></div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'''
                            <div class="chat-row ai-row">
                                <div class="avatar-icon ai-avatar">S</div>
                                <div class="bubble ai-bubble">
                                    <div style="font-weight:600; margin-bottom:8px; font-size:16px; color:#ffffff;">Kashspade Core</div>
                                    {msg["content"]}
                                </div>
                            </div>
                        ''', unsafe_allow_html=True)
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
                with col1: st.markdown('<div class="suggestion-box"><p style="font-weight:600; font-size:16px; margin:0; color:#ffffff;">Setup Jaringan Server</p><p style="font-size:13px; color:#71717a; margin-top:12px; line-height:1.5;">Bikin arsitektur proxy BungeeCord atau Velocity rapi.</p></div>', unsafe_allow_html=True)
                with col2: st.markdown('<div class="suggestion-box"><p style="font-weight:600; font-size:16px; margin:0; color:#ffffff;">Debug Script Luau</p><p style="font-size:13px; color:#71717a; margin-top:12px; line-height:1.5;">Cari bug atau optimasi performa Script Hub Roblox lu.</p></div>', unsafe_allow_html=True)
                with col3: st.markdown('<div class="suggestion-box"><p style="font-weight:600; font-size:16px; margin:0; color:#ffffff;">Mainframe Discussion</p><p style="font-size:13px; color:#71717a; margin-top:12px; line-height:1.5;">Ngobrol santai bareng core matrix system buatan Spade Network.</p></div>', unsafe_allow_html=True)
            else:
                for msg in active_history:
                    if msg["role"] == "user":
                        st.markdown(f'<div class="chat-row user-row"><div class="bubble user-bubble">{msg["content"]}</div></div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'''
                            <div class="chat-row ai-row">
                                <div class="avatar-icon ai-avatar">S</div>
                                <div class="bubble ai-bubble">
                                    <div style="font-weight:600; margin-bottom:8px; font-size:16px; color:#ffffff;">Kashspade Core</div>
                                    {msg["content"]}
                                </div>
                            </div>
                        ''', unsafe_allow_html=True)

        st.markdown('<div style="position: fixed; bottom: 0; left: 0; width: 100%; z-index: 999;">', unsafe_allow_html=True)
        
        if user_prompt := st.chat_input("Ketik pesan di sini..."):
            with chat_container:
                st.markdown(f'<div class="chat-row user-row"><div class="bubble user-bubble">{user_prompt}</div></div>', unsafe_allow_html=True)
            
            active_history.append({"role": "user", "content": user_prompt})
            is_first_chat = (st.session_state.current_session == "Sesi Baru")
            current_sess_key = st.session_state.current_session
            
            with chat_container:
                with st.spinner(""):
                    payload = [{"role": "system", "content": SYSTEM_PROMPT}] + active_history
                    ai_response = query_core_engine(payload, temp=0.5)
                    if not ai_response: ai_response = "Koneksi mainframe terputus, coba kirim ulang ya bre."
                    
                    st.markdown(f'''
                        <div class="chat-row ai-row">
                            <div class="avatar-icon ai-avatar">S</div>
                            <div class="bubble ai-bubble">
                                <div style="font-weight:600; margin-bottom:8px; font-size:16px; color:#ffffff;">Kashspade Core</div>
                                {ai_response}
                            </div>
                        </div>
                    ''', unsafe_allow_html=True)
                    
            active_history.append({"role": "assistant", "content": ai_response})
            
            if is_first_chat:
                new_title = generate_auto_title(user_prompt)
                st.session_state.global_chat_store[my_username][new_title] = active_history
                st.session_state.global_chat_store[my_username].pop("Sesi Baru", None)
                st.session_state.current_session = new_title
            else:
                st.session_state.global_chat_store[my_username][current_sess_key] = active_history
            st.rerun()

        st.markdown('<div class="disclaimer-text">Kashspade Core dapat membuat kesalahan. Pertimbangkan untuk memeriksa informasi penting.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- 7. RUN ENGINE ---
if not st.session_state.logged_in: show_auth_page()
else: show_main_dashboard()
