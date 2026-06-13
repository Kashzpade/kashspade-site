import streamlit as st
import requests
import json
import time
import hashlib
import uuid
import base64
from datetime import datetime

# optional mini vector DB
import numpy as np

# =========================
# CONFIG
# =========================
API_URL = "https://api.groq.com/openai/v1/chat/completions"
API_KEY = "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"

st.set_page_config(page_title="Kashspade Core v6 GOD MODE", layout="wide")

# =========================
# SECURITY (HASH LOGIN)
# =========================
def hash_pass(p):
    return hashlib.sha256(p.encode()).hexdigest()

# =========================
# INIT STATE
# =========================
if "users" not in st.session_state:
    st.session_state.users = {
        "spade": hash_pass("12345")
    }

if "auth" not in st.session_state:
    st.session_state.auth = False

if "user" not in st.session_state:
    st.session_state.user = None

if "chats" not in st.session_state:
    st.session_state.chats = {
        "root": {
            "id": "root",
            "title": "New Chat",
            "messages": [],
            "children": []
        }
    }

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "root"

# =========================
# MINI VECTOR MEMORY (FAKE EMBEDDING)
# =========================
if "memory" not in st.session_state:
    st.session_state.memory = []

def embed(text):
    # fake embedding (biar jalan di browser)
    return np.array([hash(text) % 1000])

def store_memory(text):
    st.session_state.memory.append({
        "text": text,
        "vec": embed(text)
    })

def recall_memory(query):
    if not st.session_state.memory:
        return []
    qv = embed(query)
    return [m["text"] for m in st.session_state.memory[-5:]]

# =========================
# AI STREAM (REAL TOKEN + SMOOTH RENDER)
# =========================
def stream_ai(messages):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": messages,
        "stream": True,
        "temperature": 0.7
    }

    r = requests.post(API_URL, json=payload, headers=headers, stream=True)

    output = ""
    box = st.empty()

    for line in r.iter_lines():
        if line:
            try:
                data = json.loads(line.decode().replace("data: ", ""))

                delta = data["choices"][0]["delta"].get("content", "")
                output += delta

                # smooth typing animation
                box.markdown(f"""
                <div style="
                    font-family: Inter;
                    padding:10px;
                    border-radius:12px;
                    background:#1f1f1f;
                    color:#eaeaea;
                ">
                🤖 {output}
                <span style="opacity:0.5;">▍</span>
                </div>
                """, unsafe_allow_html=True)

                time.sleep(0.01)

            except:
                pass

    return output

# =========================
# LOGIN SYSTEM
# =========================
def login():
    st.title("🔐 Kashspade Core Secure Login")

    u = st.text_input("Username").lower()
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if u in st.session_state.users and st.session_state.users[u] == hash_pass(p):
            st.session_state.auth = True
            st.session_state.user = u
            st.rerun()
        else:
            st.error("Login gagal")

    if st.button("Register"):
        if u not in st.session_state.users:
            st.session_state.users[u] = hash_pass(p)
            st.success("Registered")
        else:
            st.error("User exist")

# =========================
# CHAT TREE SYSTEM (BRANCHING)
# =========================
def add_message(chat_id, role, content):
    st.session_state.chats[chat_id]["messages"].append({
        "role": role,
        "content": content,
        "id": str(uuid.uuid4())
    })

def new_branch(parent_id):
    new_id = str(uuid.uuid4())
    st.session_state.chats[new_id] = {
        "id": new_id,
        "title": "Branch Chat",
        "messages": [],
        "children": []
    }
    st.session_state.chats[parent_id]["children"].append(new_id)
    return new_id

# =========================
# SIDEBAR TREE UI
# =========================
def render_tree(chat_id, level=0):
    chat = st.session_state.chats[chat_id]

    if st.button("  " * level + "💬 " + chat["title"], key=chat_id):
        st.session_state.current_chat = chat_id
        st.rerun()

    for child in chat["children"]:
        render_tree(child, level + 1)

# =========================
# IMAGE GENERATION (MOCK)
# =========================
def generate_image(prompt):
    return f"https://image.pollinations.ai/prompt/{prompt}"

# =========================
# UI ROUTER
# =========================
if not st.session_state.auth:
    login()
    st.stop()

st.sidebar.title("🌳 Chat Tree")

if st.sidebar.button("+ New Branch"):
    st.session_state.current_chat = new_branch(st.session_state.current_chat)
    st.rerun()

render_tree("root")

chat = st.session_state.chats[st.session_state.current_chat]["messages"]

st.title("Kashspade Core v6 GOD MODE")

# =========================
# RENDER CHAT
# =========================
for i, m in enumerate(chat):
    if m["role"] == "user":
        st.markdown(f"🧑 {m['content']}")
    else:
        st.markdown(f"🤖 {m['content']}")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button(f"♻ Regenerate {i}"):
                history = chat[:i]
                reply = stream_ai(history)
                chat[i]["content"] = reply
                st.rerun()

        with col2:
            if st.button(f"✏ Edit {i}"):
                new = st.text_input("Edit:", chat[i]["content"], key=f"edit{i}")
                if new:
                    chat[i]["content"] = new
                    st.rerun()

        with col3:
            if st.button(f"🗑 Delete {i}"):
                chat.pop(i)
                st.rerun()

# =========================
# INPUT
# =========================
prompt = st.chat_input("Type...")

if prompt:
    add_message(st.session_state.current_chat, "user", prompt)

    store_memory(prompt)

    memory_context = recall_memory(prompt)

    messages = [
        {"role":"system","content":"You are Kashspade Core GOD MODE AI"}
    ] + chat + [
        {"role":"system","content":"Memory: " + str(memory_context)}
    ]

    reply = stream_ai(messages)

    add_message(st.session_state.current_chat, "assistant", reply)

    st.rerun()

# =========================
# EXPORT CHAT
# =========================
st.sidebar.write("---")

if st.sidebar.button("Export JSON"):
    st.sidebar.download_button(
        "Download",
        json.dumps(st.session_state.chats, indent=2),
        file_name="chat_tree.json"
    )

# =========================
# IMAGE GEN
# =========================
st.sidebar.write("🎨 Image Gen")

img_prompt = st.sidebar.text_input("Prompt")

if st.sidebar.button("Generate"):
    url = generate_image(img_prompt)
    st.sidebar.image(url)