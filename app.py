import streamlit as st
import time
import requests
import pandas as pd
import numpy as np
import pydeck as pdk
from streamlit_lottie import st_lottie
import random
import string
import json 

# --- IMPORT SQUAD MODULES ---
import scam_tool
import pass_tool
import leak_tool

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="SentinL Cyber Defense", 
    page_icon="🛡️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ASSETS & SETUP ---
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200: return None
        return r.json()
    except: return None

# Lottie Animations (Web Assets)
lottie_radar = load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_2LdXSt.json")
lottie_alert = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_QpolL2.json")

# NEW: Password Animation
lottie_password = load_lottieurl("https://lottie.host/b6b4f688-08e2-435e-bccc-51ac8ec98fdb/1O6vsONLre.json")

# Command Center Animation
lottie_computer = load_lottieurl("https://lottie.host/1b40d8ac-8f04-4944-8b19-e8c94c6db4b0/WsubMMSCSb.json")

# Custom CSS for Dark Mode / Hacker Vibe
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #0E1117;
    }
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #000000;
    }
    /* Buttons */
    div.stButton > button {
        background-color: #00FF41;
        color: black;
        font-family: monospace;
        font-weight: bold;
        border: none;
        padding: 10px 24px;
        transition: all 0.3s;
    }
    div.stButton > button:hover {
        background-color: #00CC33;
        box-shadow: 0 0 10px #00FF41;
        color: white;
    }
    /* Text headers */
    h1, h2, h3 {
        color: #00FF41 !important;
        font-family: 'Courier New', monospace;
    }
    p, li, div {
        color: #E0E0E0;
        font-family: monospace;
    }
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #1F2937;
        color: #00FF41;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    if lottie_radar:
        st_lottie(lottie_radar, height=150)
    st.title("SENTINL v2.0")
    st.markdown("---")
    menu = st.radio("SELECT MODULE:", 
        ["🏠 COMMAND CENTER", "🛑 SCAM INTERCEPTOR", "🔓 PASSWORD CRACKER", "📡 LEAK RADAR"]
    )
    st.markdown("---")
    
    # Live System Metrics
    st.markdown("### 🖥️ SYSTEM RESOURCES")
    col1, col2 = st.columns(2)
    col1.metric("CPU", "12%", "-1%")
    col2.metric("RAM", "86%", "+4%")
    st.progress(86)
    st.caption("Secure Node: US-EAST-1")

# --- PAGE 1: COMMAND CENTER ---
if menu == "🏠 COMMAND CENTER":
    st.title("COMMAND CENTER")
    st.write("Welcome, Agent. Select a defense module from the sidebar to begin.")
    
    # Top Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Global Threat Level", value="CRITICAL", delta="Elevated")
    with col2:
        st.metric(label="System Integrity", value="100%", delta="Secure")
    with col3:
        st.metric(label="AI Neural Link", value="ONLINE", delta="Active")
    
    st.markdown("### 🌐 NETWORK TOPOLOGY")
    
    # Computer Animation (URL Version)
    if lottie_computer:
        st_lottie(lottie_computer, height=400, key="computer_anim")
    else:
        st.warning("⚠️ Animation could not be loaded from URL.")

# --- PAGE 2: SCAM INTERCEPTOR ---
elif menu == "🛑 SCAM INTERCEPTOR":
    st.title("🛑 SCAM THREAT ANALYZER")
    
    col_main, col_anim = st.columns([2, 1])
    
    with col_main:
        st.write("Paste suspicious text below. AI will analyze phrasing and psychology.")
        user_text = st.text_area("INPUT DATA STREAM:", height=150)
        
        if st.button("INITIATE SCAN"):
            if user_text:
                # Terminal Loader Effect
                with st.status("INITIALIZING NEURAL NETWORKS...", expanded=True) as status:
                    st.write("⚡ Connecting to Threat Database...")
                    time.sleep(0.5)
                    st.write("🔍 Parsing Keywords...")
                    time.sleep(0.5)
                    st.write("🧠 Running Gemini Sentiment Analysis...")
                    time.sleep(1)
                    status.update(label="SCAN COMPLETE", state="complete", expanded=False)
                
                # CALL TOOL
                result = scam_tool.check_scam(user_text)
                
                # Display Results
                st.markdown("---")
                if result["risk_level"] == "CRITICAL":
                    st.toast('🚨 THREAT BLOCKED! Do not click.', icon='🔥')
                    st.error(f"🚨 CRITICAL THREAT DETECTED (Score: {result['score']}%)")
                elif result["risk_level"] == "MODERATE":
                    st.toast('⚠️ Warning: Suspicious Content.', icon='⚠️')
                    st.warning(f"⚠️ MODERATE RISK (Score: {result['score']}%)")
                else:
                    st.toast('✅ Scan Complete. No threats found.', icon='🛡️')
                    st.success(f"✅ SYSTEM CLEAN (Score: {result['score']}%)")
                
                # AI INSIGHT
                with st.chat_message("assistant", avatar="🤖"):
                     st.write(f"**AI Analysis:** {result['ai_analysis']}")

                with st.expander("🔍 VIEW RAW TRIGGERS"):
                    st.write(f"**Triggers Found:** {', '.join(result['triggers'])}")
            else:
                st.warning("DATA STREAM EMPTY.")
    
    with col_anim:
        if lottie_alert:
            st_lottie(lottie_alert, height=200)

# --- PAGE 3: PASSWORD CRACKER ---
elif menu == "🔓 PASSWORD CRACKER":
    st.title("🔓 PASSWORD RESILIENCE TEST")
    
    col_main, col_anim = st.columns([2,1])
    
    with col_main:
        st.write("Test your password against brute-force algorithms & AI critique.")
        password = st.text_input("ENTER CREDENTIALS:", type="password")
        
        if password:
            # 1. Matrix Animation Effect
            crack_placeholder = st.empty()
            for i in range(10):
                random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
                crack_placeholder.markdown(f"### 🔓 DECRYPTING: `{random_str}`")
                time.sleep(0.05)
            crack_placeholder.empty()

            # 2. CALL TOOL
            data = pass_tool.test_password_strength(password)
            
            st.markdown("---")
            
            # 3. Rank & Badge Display
            st.markdown(f"<h1 style='text-align: center; color: white;'>{data['badge']} {data['rank']}</h1>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center;'>SECURITY CLEARANCE LEVEL {data['score']}</p>", unsafe_allow_html=True)
            
            # 4. AI Roast (New Feature)
            with st.chat_message("assistant", avatar="🤖"):
                 st.write(f"**AI Feedback:** {data['ai_analysis']}")

            st.markdown("---")
            c1, c2 = st.columns(2)
            c1.metric("Entropy Score", f"{data['score']}/4")
            c2.metric("Time to Crack", data['crack_time'])
            
            if data['score'] < 3:
                st.toast(f'Alert: Rank downgraded to {data["rank"]}', icon='📉')
                st.error("❌ VULNERABLE: Hash collision imminent.")
            else:
                st.toast(f'Upgrade: Rank promoted to {data["rank"]}', icon='📈')
                st.balloons()
                st.success("✅ SECURE: Encryption adequate.")

    with col_anim:
        if lottie_password:
            st_lottie(lottie_password, height=200)

# --- PAGE 4: LEAK RADAR ---
elif menu == "📡 LEAK RADAR":
    st.title("📡 DARK WEB LEAK RADAR")
    st.write("Search known data breaches for your identity.")
    
    email = st.text_input("TARGET IDENTIFIER (Email):")
    
    if st.button("SCAN DARK WEB NODES"):
        # Fake loading
        progress = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress.progress(i + 1)
            
        # CALL TOOL
        result = leak_tool.check_email_leak(email)
        
        st.markdown("---")
        if result['found']:
            st.toast('⚠️ ALERT: Data Breach Found!', icon='☠️')
            st.error(f"⚠️ ALERT: DATA COMPROMISE DETECTED")
            
            # AI Advice (New Feature)
            with st.chat_message("assistant", avatar="🤖"):
                 st.write(f"**AI Advisory:** {result['ai_advice']}")
                 
            st.json({
                "Sources": result['sources'],
                "Data Types": result['data_leaked']
            })
        else:
            st.toast('✅ No Leaks Found.', icon='✨')
            st.success("✅ STATUS CLEAR: No indicators found in known breaches.")
            st.info(f"**AI Advisory:** {result['ai_advice']}")