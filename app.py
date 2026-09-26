import os
import sys
import json
import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime
import streamlit as st
import streamlit.components.v1 as components

# Configure root path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.config import (
    POLICY_PATH, 
    SAMPLE_RECEIPTS_DIR, 
    ORDERS_CSV_PATH,
    ORDERS_DB_PATH,
    CURRENT_DATE, 
    URGENT_DAYS_THRESHOLD,
    GROQ_MODEL
)
from src.loaders import load_policy, load_receipt, init_orders_db
from src.agent import ingest_receipt_proactively, answer_shopper_query, CODEXSession, search_google_or_gemini, run_chartgpt_or_ai_engine
from src import shared_state
from src.components_3d import render_3d_order_animation, render_cinematic_3d_background

# Streamlit Page Setup
st.set_page_config(
    page_title="CODEX - Order & Warranty Agent",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Digital Look & Glassmorphism Styling
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500;700&family=DM+Sans:wght@400;500;600;700&display=swap');

    /* ========================================================
       🎬 3D CINEMATIC FULL-SCREEN BACKGROUND ENGINE
       ======================================================== */
    iframe.cinematic-bg-frame,
    iframe[data-testid="cinematic-3d-bg-iframe"],
    div:has(> iframe.cinematic-bg-frame),
    div:has(> iframe[data-testid="cinematic-3d-bg-iframe"]) {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        width: 100vw !important;
        height: 100vh !important;
        z-index: 0 !important;
        pointer-events: none !important;
        border: none !important;
        opacity: 0.88 !important;
    }

    .stApp {
        background: transparent !important;
        color: #f1f5f9;
    }

    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at 18% 18%, rgba(2, 132, 199, 0.16) 0%, transparent 50%),
                    radial-gradient(circle at 82% 22%, rgba(124, 58, 237, 0.14) 0%, transparent 50%),
                    radial-gradient(circle at 50% 85%, rgba(16, 185, 129, 0.10) 0%, transparent 50%),
                    rgba(6, 9, 19, 0.78) !important;
        backdrop-filter: blur(2px) !important;
        -webkit-backdrop-filter: blur(2px) !important;
    }

    /* ========================================================
       🌐 STREAMLIT SIDEBAR: COMMERCIAL LOOK & RE-OPEN CONTROL
       ======================================================== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(10, 15, 29, 0.96) 0%, rgba(15, 23, 42, 0.94) 50%, rgba(30, 41, 59, 0.92) 100%) !important;
        backdrop-filter: blur(24px) saturate(200%) !important;
        -webkit-backdrop-filter: blur(24px) saturate(200%) !important;
        border-right: 1px solid rgba(56, 189, 248, 0.35) !important;
        box-shadow: 10px 0 35px rgba(0, 0, 0, 0.65), inset -1px 0 0 rgba(56, 189, 248, 0.15) !important;
    }

    [data-testid="stSidebar"] * {
        font-family: 'DM Sans', sans-serif;
    }

    /* Fix Sidebar Scrolling */
    [data-testid="stSidebarContent"] {
        overflow-y: auto !important;
        scrollbar-width: thin !important;
        scrollbar-color: #38bdf8 rgba(15, 23, 42, 0.8) !important;
    }
    [data-testid="stSidebarContent"]::-webkit-scrollbar {
        width: 8px !important;
    }
    [data-testid="stSidebarContent"]::-webkit-scrollbar-track {
        background: rgba(15, 23, 42, 0.6) !important;
    }
    [data-testid="stSidebarContent"]::-webkit-scrollbar-thumb {
        background: rgba(56, 189, 248, 0.45) !important;
        border-radius: 999px !important;
    }
    [data-testid="stSidebarContent"]::-webkit-scrollbar-thumb:hover {
        background: #38bdf8 !important;
    }

    /* Floating Re-Open Button for Collapsed Sidebar (Guarantees it can always be opened) */
    [data-testid="collapsedControl"],
    button[kind="header"] {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        background: rgba(15, 23, 42, 0.95) !important;
        border: 1px solid #38bdf8 !important;
        border-radius: 8px !important;
        color: #38bdf8 !important;
        box-shadow: 0 0 16px rgba(56, 189, 248, 0.5) !important;
        z-index: 999999 !important;
        cursor: pointer !important;
        pointer-events: auto !important;
        margin: 8px !important;
    }
    [data-testid="collapsedControl"]:hover,
    button[kind="header"]:hover {
        background: #0284c7 !important;
        color: #ffffff !important;
    }
    [data-testid="collapsedControl"] svg,
    button[kind="header"] svg {
        fill: #38bdf8 !important;
        color: #38bdf8 !important;
    }

    /* Sidebar Headers */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] h4 {
        font-family: 'DM Mono', monospace !important;
        color: #38bdf8 !important;
        letter-spacing: 0.05em !important;
        text-shadow: 0 0 16px rgba(56, 189, 248, 0.4) !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        margin-top: 0.8rem !important;
        margin-bottom: 0.4rem !important;
    }

    /* Sidebar Text & Captions */
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] label {
        color: #cbd5e1 !important;
        font-size: 0.86rem !important;
    }
    [data-testid="stSidebar"] .stCaption, 
    [data-testid="stSidebar"] small {
        color: #94a3b8 !important;
        font-size: 0.78rem !important;
    }

    /* Sidebar Glassmorphic Buttons */
    [data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.85), rgba(15, 23, 42, 0.95)) !important;
        backdrop-filter: blur(14px) !important;
        -webkit-backdrop-filter: blur(14px) !important;
        border: 1px solid rgba(56, 189, 248, 0.35) !important;
        border-radius: 11px !important;
        color: #f1f5f9 !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.86rem !important;
        font-weight: 600 !important;
        padding: 0.65rem 0.95rem !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.12) !important;
        width: 100% !important;
        text-align: left !important;
        margin-bottom: 8px !important;
        display: flex !important;
        align-items: center !important;
        cursor: pointer !important;
        pointer-events: auto !important;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background: linear-gradient(135deg, rgba(2, 132, 199, 0.5), rgba(30, 58, 138, 0.45)) !important;
        border-color: #38bdf8 !important;
        color: #ffffff !important;
        box-shadow: 0 0 22px rgba(56, 189, 248, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.25) !important;
        transform: translateY(-2px) !important;
    }

    /* Sidebar Glassmorphic File Uploader */
    [data-testid="stSidebar"] [data-testid="stFileUploader"] {
        background: rgba(15, 23, 42, 0.75) !important;
        border: 1px dashed rgba(56, 189, 248, 0.45) !important;
        border-radius: 12px !important;
        padding: 10px !important;
        backdrop-filter: blur(14px) !important;
        -webkit-backdrop-filter: blur(14px) !important;
        box-shadow: inset 0 0 20px rgba(56, 189, 248, 0.08) !important;
        transition: all 0.25s ease !important;
        cursor: pointer !important;
    }

    /* ========================================================
       📂 UNIVERSAL EXPANDERS / SLIDE BARS (GUARANTEES OPEN/CLOSE)
       ======================================================== */
    [data-testid="stExpander"] {
        background: rgba(15, 23, 42, 0.85) !important;
        backdrop-filter: blur(18px) !important;
        -webkit-backdrop-filter: blur(18px) !important;
        border: 1px solid rgba(56, 189, 248, 0.35) !important;
        border-radius: 12px !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35) !important;
        margin-bottom: 14px !important;
        overflow: hidden !important;
        pointer-events: auto !important;
    }

    [data-testid="stExpander"] summary {
        color: #f8fafc !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        padding: 12px 16px !important;
        background: rgba(30, 41, 59, 0.6) !important;
        border-radius: 10px !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        transition: all 0.2s ease !important;
        user-select: none !important;
        pointer-events: auto !important;
    }

    [data-testid="stExpander"] summary:hover {
        background: rgba(2, 132, 199, 0.25) !important;
        color: #38bdf8 !important;
    }

    [data-testid="stExpander"] summary svg {
        fill: #38bdf8 !important;
        color: #38bdf8 !important;
        width: 18px !important;
        height: 18px !important;
    }

    [data-testid="stExpander"] [data-testid="stExpanderDetails"] {
        background: rgba(10, 15, 29, 0.92) !important;
        padding: 16px !important;
        border-top: 1px solid rgba(56, 189, 248, 0.2) !important;
        color: #cbd5e1 !important;
    }

    /* Sidebar Dividers */
    [data-testid="stSidebar"] hr {
        border-color: rgba(56, 189, 248, 0.25) !important;
        box-shadow: 0 0 10px rgba(56, 189, 248, 0.18) !important;
        margin: 14px 0 !important;
    }

    /* Main View Styling - High Contrast Commercial Typography */
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #f8fafc !important;
        text-shadow: 0 2px 14px rgba(56, 189, 248, 0.3) !important;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #94a3b8 !important;
        margin-bottom: 1.5rem;
    }
    .urgent-box {
        background: rgba(239, 68, 68, 0.15) !important;
        border: 1px solid rgba(239, 68, 68, 0.45) !important;
        border-left: 6px solid #EF4444 !important;
        padding: 16px !important;
        border-radius: 8px !important;
        margin-bottom: 20px !important;
        color: #fecaca !important;
    }
    .urgent-title {
        color: #fca5a5 !important;
        font-weight: 800;
        font-size: 1.15rem;
        margin-bottom: 6px;
    }
    .safe-box {
        background: rgba(16, 185, 129, 0.15) !important;
        border: 1px solid rgba(16, 185, 129, 0.45) !important;
        border-left: 6px solid #22C55E !important;
        padding: 14px !important;
        border-radius: 8px !important;
        margin-bottom: 20px !important;
        color: #a7f3d0 !important;
    }
    .metric-card {
        background: rgba(15, 23, 42, 0.85) !important;
        border: 1px solid rgba(56, 189, 248, 0.25) !important;
        border-radius: 10px !important;
        padding: 14px !important;
        margin-bottom: 10px !important;
        color: #f1f5f9 !important;
    }
    .status-badge-urgent {
        background-color: rgba(239, 68, 68, 0.25) !important;
        color: #fca5a5 !important;
        border: 1px solid #ef4444 !important;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .status-badge-active {
        background-color: #DCFCE7;
        color: #15803D;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .status-badge-final {
        background-color: #F3F4F6;
        color: #4B5563;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.85rem;
    }

    /* Universal 5.6 Tera ChartGPT Cockpit Styling */
    .search-cockpit-box {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9), rgba(30, 41, 59, 0.85)) !important;
        border: 1px solid rgba(56, 189, 248, 0.35) !important;
        border-radius: 14px !important;
        padding: 16px 20px !important;
        margin-bottom: 18px !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.12) !important;
    }
    .search-result-card {
        background: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(56, 189, 248, 0.22) !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
        margin-bottom: 10px !important;
        backdrop-filter: blur(12px) !important;
        transition: all 0.2s ease !important;
    }
    .search-result-card:hover {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 16px rgba(56, 189, 248, 0.25) !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Database
init_orders_db()

# Session State Initialization & Auto Startup
if "session_data" not in st.session_state:
    st.session_state["session_data"] = None
if "current_receipt_source" not in st.session_state:
    st.session_state["current_receipt_source"] = None
if "chat_messages" not in st.session_state:
    st.session_state["chat_messages"] = []
if "search_result" not in st.session_state:
    st.session_state["search_result"] = None
if "search_query" not in st.session_state:
    st.session_state["search_query"] = ""
if "active_source_mode" not in st.session_state:
    st.session_state["active_source_mode"] = "sample"
if "uploaded_file_fingerprint" not in st.session_state:
    st.session_state["uploaded_file_fingerprint"] = None

# Auto Startup: Default to Sample 1 on initial load so the agent and 3D twin are immediately active
if st.session_state.get("receipt_content") is None and st.session_state.get("session_data") is None:
    sample_path = SAMPLE_RECEIPTS_DIR / "receipt_urgent_electronics.txt"
    if sample_path.exists():
        st.session_state["receipt_content"] = sample_path.read_text(encoding="utf-8")
        st.session_state["receipt_name"] = "Sample 1: Urgent Electronics (REC-2026-8891)"
        st.session_state["active_source_mode"] = "sample"

# 🎬 Full-Screen 3D Cinematic Ambient Background Engine
components.html(render_cinematic_3d_background(), height=0)

# Spatial Banner
st.markdown("""
<div style="background:linear-gradient(90deg, #0f172a, #1e293b);border:1px solid #334155;border-radius:10px;padding:8px 14px;margin-bottom:14px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
    <div style="display:flex;align-items:center;gap:8px;">
        <span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#38bdf8;box-shadow:0 0 8px #38bdf8;"></span>
        <span style="font-family:'DM Mono',monospace;font-size:11px;font-weight:700;color:#38bdf8;">SPATIAL DIGITAL TWIN NODE · VISION OS</span>
    </div>
    <div style="display:flex;gap:10px;align-items:center;">
        <span style="background:rgba(56, 189, 248, 0.15);border:1px solid rgba(56, 189, 248, 0.35);color:#7dd3fc;padding:3px 10px;border-radius:6px;font-size:11px;font-weight:700;font-family:'DM Mono',monospace;">STREAMLIT PORT 8501</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Top Header
col_title, col_status = st.columns([3, 1])
with col_title:
    st.markdown('<div class="main-header">⚡ CODEX Order & Warranty Agent</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Autonomous Ingestion, Deterministic Date Math & Grounded ReAct Assistant</div>', unsafe_allow_html=True)
with col_status:
    st.caption("⚡ **Provider:** Groq")
    st.caption(f"🤖 **Model:** `{GROQ_MODEL}`")
    st.caption(f"📅 **Ref Date:** `{CURRENT_DATE.isoformat()}`")

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.75), rgba(15, 23, 42, 0.9)); border: 1px solid rgba(56, 189, 248, 0.35); border-radius: 12px; padding: 12px 14px; margin-bottom: 16px; box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.12); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px;">
            <div style="font-family: 'DM Mono', monospace; font-size: 11px; font-weight: 800; color: #38bdf8; letter-spacing: 0.08em; display: flex; align-items: center; gap: 6px;">
                <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #38bdf8; box-shadow: 0 0 10px #38bdf8;"></span>
                3D DIGITAL COCKPIT
            </div>
            <span style="background: rgba(56, 189, 248, 0.15); border: 1px solid rgba(56, 189, 248, 0.35); color: #7dd3fc; font-family: 'DM Mono', monospace; font-size: 9px; font-weight: 700; padding: 2px 7px; border-radius: 999px;">PORT 8501</span>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px; font-family: 'DM Mono', monospace; font-size: 9px; margin-top: 8px;">
            <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(56, 189, 248, 0.15); border-radius: 7px; padding: 5px 7px;">
                <div style="color: #64748b; font-size: 8px;">RENDER ENGINE</div>
                <div style="color: #38bdf8; font-weight: 700;">Three.js WebGL</div>
            </div>
            <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(56, 189, 248, 0.15); border-radius: 7px; padding: 5px 7px;">
                <div style="color: #64748b; font-size: 8px;">COCKPIT STATUS</div>
                <div style="color: #4ade80; font-weight: 700;">● OPERATIONAL</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.header("📄 Shopper Receipt Upload")
    st.write("Upload your receipt, shopkeeper invoice, or POS ticket to trigger automatic ingestion:")

    uploaded_file = st.file_uploader(
        "Choose receipt file (.txt, .md, .csv, .json)", 
        type=["txt", "md", "csv", "json", "log", "text"],
        key="file_uploader"
    )

    if uploaded_file is not None:
        file_bytes = uploaded_file.getvalue()
        content_str = None
        for enc in ["utf-8", "utf-8-sig", "latin-1", "cp1252"]:
            try:
                content_str = file_bytes.decode(enc)
                break
            except Exception:
                pass

        if content_str:
            file_id = f"{uploaded_file.name}_{len(file_bytes)}"
            if st.session_state.get("uploaded_file_fingerprint") != file_id:
                st.session_state["uploaded_file_fingerprint"] = file_id
                st.session_state["receipt_content"] = content_str
                st.session_state["receipt_name"] = f"📄 {uploaded_file.name}"
                st.session_state["active_source_mode"] = "upload"
                st.session_state["current_receipt_source"] = None
                st.session_state["search_result"] = None
                st.session_state["search_query"] = ""
                st.session_state["cockpit_query_val"] = ""
                st.rerun()

    st.markdown("---")
    st.subheader("⚡ Quick Load Sample Receipts")
    st.caption("Click any sample to start up proactive ingestion & 3D twin:")

    if st.button("🚨 Sample 1: Urgent Electronics (5 days left!)", use_container_width=True):
        sample_path = SAMPLE_RECEIPTS_DIR / "receipt_urgent_electronics.txt"
        st.session_state["receipt_content"] = sample_path.read_text(encoding="utf-8")
        st.session_state["receipt_name"] = "Sample 1: Urgent Electronics (REC-2026-8891)"
        st.session_state["active_source_mode"] = "sample_1"
        st.session_state["current_receipt_source"] = None
        st.session_state["search_result"] = None
        st.session_state["search_query"] = ""
        st.session_state["cockpit_query_val"] = ""
        st.rerun()

    if st.button("🧥 Sample 2: Mixed Apparel & Outdoor Goods", use_container_width=True):
        sample_path = SAMPLE_RECEIPTS_DIR / "receipt_apparel_mixed.txt"
        st.session_state["receipt_content"] = sample_path.read_text(encoding="utf-8")
        st.session_state["receipt_name"] = "Sample 2: Mixed Apparel & Goods (REC-2026-9042)"
        st.session_state["active_source_mode"] = "sample_2"
        st.session_state["current_receipt_source"] = None
        st.session_state["search_result"] = None
        st.session_state["search_query"] = ""
        st.session_state["cockpit_query_val"] = ""
        st.rerun()

    if st.button("⏳ Sample 3: Expiring Winter Apparel (3 days left!)", use_container_width=True):
        sample_path = SAMPLE_RECEIPTS_DIR / "receipt_expiring_apparel.txt"
        st.session_state["receipt_content"] = sample_path.read_text(encoding="utf-8")
        st.session_state["receipt_name"] = "Sample 3: Expiring Winter Apparel (REC-2026-7731)"
        st.session_state["active_source_mode"] = "sample_3"
        st.session_state["current_receipt_source"] = None
        st.session_state["search_result"] = None
        st.session_state["search_query"] = ""
        st.session_state["cockpit_query_val"] = ""
        st.rerun()

    sample_shopkeeper = SAMPLE_RECEIPTS_DIR / "sample_shopkeeper_bill.txt"
    if sample_shopkeeper.exists():
        if st.button("🛒 Sample 4: Shopkeeper Store Invoice (Tabish)", use_container_width=True):
            st.session_state["receipt_content"] = sample_shopkeeper.read_text(encoding="utf-8")
            st.session_state["receipt_name"] = "Sample 4: Shopkeeper Store Invoice (ORD-9912)"
            st.session_state["active_source_mode"] = "sample_4"
            st.session_state["current_receipt_source"] = None
            st.session_state["search_result"] = None
            st.session_state["search_query"] = ""
            st.session_state["cockpit_query_val"] = ""
            st.rerun()

    sample_corex = SAMPLE_RECEIPTS_DIR / "corex_sample_receipt.txt"
    if not sample_corex.exists():
        sample_corex = BASE_DIR / "corex sample reciept.txt"
    if sample_corex.exists():
        if st.button("🏪 Sample 5: ABC Mart Shopper Receipt (Table/POS)", use_container_width=True):
            st.session_state["receipt_content"] = sample_corex.read_text(encoding="utf-8")
            st.session_state["receipt_name"] = "Sample 5: ABC Mart POS Invoice (20230922-001234)"
            st.session_state["active_source_mode"] = "sample_5"
            st.session_state["current_receipt_source"] = None
            st.session_state["search_result"] = None
            st.session_state["search_query"] = ""
            st.session_state["cockpit_query_val"] = ""
            st.rerun()

    with st.expander("✍️ Or Paste Receipt Text Directly"):
        pasted_text = st.text_area("Paste receipt or shopkeeper bill text:", height=130, key="sidebar_paste_receipt", placeholder="e.g. ABC Mart\nOrder: 1234\nItem: Wireless Mouse Price: 24.99...")
        if st.button("🚀 Ingest & Start Up Pasted Receipt", use_container_width=True):
            if pasted_text and pasted_text.strip():
                st.session_state["receipt_content"] = pasted_text.strip()
                st.session_state["receipt_name"] = "📄 Pasted Shopper Receipt"
                st.session_state["active_source_mode"] = "pasted"
                st.session_state["current_receipt_source"] = None
                st.session_state["search_result"] = None
                st.session_state["search_query"] = ""
                st.session_state["cockpit_query_val"] = ""
                st.rerun()
            else:
                st.warning("Please paste receipt text before submitting.")

    # Active Ingested Receipt HUD in Sidebar
    if st.session_state.get("session_data"):
        s_meta = st.session_state["session_data"]["receipt_data"]
        s_items = s_meta.get("items", [])
        st.markdown(f"""
        <div style="background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(56, 189, 248, 0.4); border-radius: 10px; padding: 10px 12px; margin: 12px 0; font-family: 'DM Mono', monospace;">
            <div style="color: #38bdf8; font-size: 10px; font-weight: 700; margin-bottom: 4px;">● ACTIVE INGESTED RECEIPT</div>
            <div style="color: #f1f5f9; font-size: 11px; font-weight: 700; word-break: break-all;">{st.session_state.get("receipt_name", "Shopkeeper Receipt")}</div>
            <div style="color: #94a3b8; font-size: 10px; margin-top: 4px;">Order: <span style="color: #cbd5e1;">{s_meta.get('order_id', 'N/A')}</span> | Items: <span style="color: #38bdf8;">{len(s_items)}</span></div>
            <div style="color: #94a3b8; font-size: 10px;">Customer: <span style="color: #cbd5e1;">{s_meta.get('customer', 'Valued Shopper')}</span></div>
        </div>
        """, unsafe_allow_html=True)

    if st.session_state.get("receipt_content") or st.session_state.get("session_data"):
        if st.button("🔄 Clear Active Receipt & Reset", use_container_width=True):
            st.session_state["receipt_content"] = None
            st.session_state["receipt_name"] = None
            st.session_state["active_source_mode"] = None
            st.session_state["uploaded_file_fingerprint"] = None
            st.session_state["session_data"] = None
            st.session_state["current_receipt_source"] = None
            st.session_state["chat_messages"] = []
            st.session_state["search_result"] = None
            st.rerun()

    st.markdown("---")
    with st.expander("📦 Mock Orders Database (Live Table)"):
        conn = sqlite3.connect(str(ORDERS_DB_PATH))
        df_orders = pd.read_sql_query("SELECT order_id, customer_name, status, carrier, tracking_number FROM orders", conn)
        st.dataframe(df_orders, use_container_width=True)

    with st.expander("📜 CODEX Store Policy"):
        policy_text = load_policy(POLICY_PATH)
        st.markdown(policy_text)

# Determine receipt content to process
receipt_to_process = st.session_state.get("receipt_content")

# Trigger Ingestion if receipt changed or not yet ingested
if receipt_to_process and (st.session_state.get("current_receipt_source") != receipt_to_process):
    with st.spinner("🔄 Ingesting receipt: parsing items, building scoped Chroma vector store, and running window calculator..."):
        ingest_res = ingest_receipt_proactively(receipt_to_process, current_date_str=CURRENT_DATE.isoformat())
        st.session_state["session_data"] = ingest_res
        shared_state.active_session = ingest_res["session"]
        st.session_state["current_receipt_source"] = receipt_to_process
        # Seed chat with the proactive summary so it is immediately visible
        st.session_state["chat_messages"] = [
            {"role": "assistant", "content": ingest_res["proactive_summary"]}
        ]
    st.rerun()

# ========================================================
# ✦ GOOGLE & GEMINI AI SEARCH & REASONING COCKPIT
# ========================================================
st.markdown("""
<div class="search-cockpit-box" style="background:linear-gradient(135deg, rgba(15,23,42,0.95), rgba(30,41,59,0.9), rgba(66,133,244,0.14));border:1px solid rgba(66,133,244,0.45);box-shadow:0 8px 32px rgba(0,0,0,0.5), 0 0 25px rgba(66,133,244,0.2);">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;flex-wrap:wrap;gap:8px;">
        <div style="display:flex;align-items:center;gap:10px;">
            <span style="font-size:1.35rem;font-weight:900;">
                <span style="color:#4285f4;">G</span><span style="color:#ea4335;">o</span><span style="color:#fbbc05;">o</span><span style="color:#4285f4;">g</span><span style="color:#34a853;">l</span><span style="color:#ea4335;">e</span>
            </span>
            <span style="font-size:1.35rem;background:linear-gradient(135deg, #38bdf8, #818cf8, #f472b6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-weight:900;">✦</span>
            <span style="font-family:'DM Mono',monospace;font-size:1.05rem;font-weight:800;background:linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;letter-spacing:0.04em;">
                GEMINI AI SEARCH & REASONING COCKPIT
            </span>
            <span style="background:rgba(66,133,244,0.18);border:1px solid rgba(66,133,244,0.45);color:#93c5fd;font-size:0.75rem;font-family:'DM Mono',monospace;padding:2px 8px;border-radius:999px;font-weight:700;">
                ✦ GOOGLE & GEMINI 2.5 ACTIVE
            </span>
        </div>
        <div style="font-size:0.82rem;color:#94a3b8;font-family:'DM Sans',sans-serif;">
            Instant Google AI Overviews, web citations, grounded retail reasoning & multi-modal charts
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

engine_cols, mode_info_col = st.columns([3, 1])
with engine_cols:
    search_engine_mode = st.radio(
        "Intelligence Engine:",
        ["✨ Google ✦ Gemini AI Overview (Conversational & Search)", "📊 5.6 Tera ChartGPT (Visual & Charts)"],
        index=0,
        horizontal=True,
        key="cockpit_search_mode"
    )
with mode_info_col:
    if "Google" in search_engine_mode or "Gemini" in search_engine_mode:
        st.caption("✨ **Mode:** Google AI Overview & Gemini Reasoning")
    else:
        st.caption("📊 **Mode:** 5.6T Visual Chart & Forecast")

if "cockpit_query_val" not in st.session_state:
    st.session_state["cockpit_query_val"] = ""
if "run_search_action" not in st.session_state:
    st.session_state["run_search_action"] = False

# Quick Google & Gemini Suggestion Chips (placed above form so clicks set query and trigger immediately)
st.caption("⚡ **Trending Google & Gemini Searches (Click to Run):**")
chip1, chip2, chip3, chip4, chip5 = st.columns(5)

if chip1.button("📦 Product Details & Prices", use_container_width=True, key="chip_products"):
    st.session_state["cockpit_query_val"] = "Show complete product details, prices, SKUs, and items on my uploaded receipt"
    st.session_state["run_search_action"] = True
    st.rerun()

if chip2.button("⏳ Return Window Policy", use_container_width=True, key="chip_returns"):
    st.session_state["cockpit_query_val"] = "What is the return window and deadline for items on my receipt?"
    st.session_state["run_search_action"] = True
    st.rerun()

if chip3.button("🛡️ Warranty Coverage", use_container_width=True, key="chip_warranty"):
    st.session_state["cockpit_query_val"] = "What is the warranty coverage for products on my receipt?"
    st.session_state["run_search_action"] = True
    st.rerun()

if chip4.button("🚚 Track Order ORD-1002", use_container_width=True, key="chip_orders"):
    st.session_state["cockpit_query_val"] = "Check live status and tracking for ORD-1002"
    st.session_state["run_search_action"] = True
    st.rerun()

if chip5.button("📊 5.6T Sales & Velocity", use_container_width=True, key="chip_sales"):
    st.session_state["cockpit_query_val"] = "Plot 7-day sales velocity and revenue trends"
    st.session_state["run_search_action"] = True
    st.rerun()

with st.form(key="gemini_search_form", clear_on_submit=False):
    col_search_bar, col_search_go = st.columns([5, 1])
    with col_search_bar:
        user_search_text = st.text_input(
            "Google & Gemini Search Query:",
            value=st.session_state.get("cockpit_query_val", ""),
            placeholder="✦ Search receipt products, item details, prices, return policies, order tracking (ORD-1001), or plot charts...",
            label_visibility="collapsed",
            key="gemini_search_text_input"
        )
    with col_search_go:
        trigger_search = st.form_submit_button("Google ✦ Gemini", use_container_width=True, type="primary")

active_query = None
if trigger_search:
    q_cand = user_search_text.strip() if user_search_text else ""
    if q_cand:
        active_query = q_cand
        st.session_state["cockpit_query_val"] = q_cand
elif st.session_state.get("run_search_action") and st.session_state.get("cockpit_query_val"):
    active_query = st.session_state["cockpit_query_val"].strip()
    st.session_state["run_search_action"] = False

if active_query:
    st.session_state["search_query"] = active_query
    with st.spinner(f"✦ Google & Gemini AI are searching & reasoning about '{active_query}'..."):
        current_sess = st.session_state["session_data"]["session"] if st.session_state.get("session_data") else None
        current_rec = st.session_state["session_data"]["receipt_data"] if st.session_state.get("session_data") else None
        chart_res = run_chartgpt_or_ai_engine(active_query, mode=search_engine_mode, session=current_sess, receipt_data=current_rec)
        st.session_state["search_result"] = chart_res
    st.rerun()

# Render Google & Gemini AI Results Panel
if st.session_state.get("search_result"):
    s_res = st.session_state["search_result"]
    res_mode = s_res.get("mode", "Google ✦ Gemini AI Overview")
    res_query = s_res.get("query", "")
    chart_title = s_res.get("chart_title")

    st.markdown(f"""
    <div style="background:linear-gradient(135deg, rgba(15,23,42,0.95), rgba(30,41,59,0.92), rgba(66,133,244,0.12));border:1px solid rgba(66,133,244,0.45);border-radius:14px;padding:16px 20px;margin-bottom:14px;box-shadow:0 8px 30px rgba(0,0,0,0.5), 0 0 20px rgba(66,133,244,0.15);">
        <div style="display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid rgba(66,133,244,0.22);padding-bottom:10px;flex-wrap:wrap;gap:8px;">
            <div style="display:flex;align-items:center;gap:8px;">
                <span style="font-weight:900;font-size:1.1rem;">
                    <span style="color:#4285f4;">G</span><span style="color:#ea4335;">o</span><span style="color:#fbbc05;">o</span><span style="color:#4285f4;">g</span><span style="color:#34a853;">l</span><span style="color:#ea4335;">e</span>
                </span>
                <span style="color:#818cf8;font-size:1.1rem;font-weight:900;">✦</span>
                <span style="font-family:'DM Mono',monospace;font-size:0.88rem;font-weight:700;color:#c7d2fe;letter-spacing:0.06em;">
                    AI OVERVIEW
                </span>
                <span style="font-size:0.88rem;color:#94a3b8;margin-left:6px;"><em>"{res_query}"</em></span>
            </div>
            <span style="background:rgba(66,133,244,0.18);color:#93c5fd;font-family:'DM Mono',monospace;font-size:0.75rem;padding:3px 10px;border-radius:999px;font-weight:700;border:1px solid rgba(66,133,244,0.3);">
                {s_res.get('engine', 'Google Search + Gemini 2.5 Multi-Modal Engine')}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 1. Google Verified Source Cards (Citations Carousel)
    if s_res.get("sources"):
        st.markdown("<div style='font-size:0.8rem;color:#94a3b8;font-weight:700;margin:6px 0 6px;'>🌐 GOOGLE KNOWLEDGE & STORE CITATIONS:</div>", unsafe_allow_html=True)
        src_cols = st.columns(len(s_res["sources"]))
        for col, s in zip(src_cols, s_res["sources"]):
            col.markdown(f"""
            <div style="background:rgba(30,41,59,0.7);border:1px solid rgba(255,255,255,0.12);border-radius:10px;padding:9px 12px;height:100%;">
                <div style="font-size:0.75rem;color:#94a3b8;display:flex;align-items:center;gap:4px;">
                    <span>{s.get('icon', '🌐')}</span> <strong>{s.get('domain', 'source')}</strong>
                </div>
                <div style="font-size:0.82rem;font-weight:700;color:#f8fafc;margin:3px 0 4px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;" title="{s.get('title')}">
                    {s.get('title')}
                </div>
                <div style="font-size:0.72rem;color:#cbd5e1;line-height:1.25;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;">
                    {s.get('snippet')}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # 2. Gemini Multi-Step Thought Chain
    if s_res.get("thought_steps"):
        with st.expander("✦ View Gemini Multi-Step Thought Process & Retrieval", expanded=False):
            for step in s_res["thought_steps"]:
                st.markdown(f"- {step}")

    # 3. Quantitative Telemetry Metrics Bar (if present)
    if s_res.get("metrics"):
        m_items = list(s_res["metrics"].items())
        cols = st.columns(len(m_items))
        for col, (label, val) in zip(cols, m_items):
            col.metric(label, str(val))

    # 4. Interactive Chart Rendering (if multi-modal chart data is generated)
    if s_res.get("series_data") and s_res.get("labels"):
        st.markdown(f"#### {chart_title or '✦ Gemini Multi-Modal Visual Analytics'}")
        df_chart = pd.DataFrame(s_res["series_data"], index=s_res["labels"])
        
        c_mode_col1, c_mode_col2 = st.columns([2, 4])
        with c_mode_col1:
            chart_view = st.radio(
                "Display Chart Style:",
                ["📊 Interactive Bar", "📈 Smooth Line", "🌊 Area Fill"],
                horizontal=True,
                key="gemini_chart_style_selector"
            )
        
        if "Bar" in chart_view:
            st.bar_chart(df_chart, use_container_width=True)
        elif "Line" in chart_view:
            st.line_chart(df_chart, use_container_width=True)
        else:
            st.area_chart(df_chart, use_container_width=True)

        if s_res.get("table_rows"):
            with st.expander("📋 View Underlying 5.6 Tera Data Table"):
                st.dataframe(pd.DataFrame(s_res["table_rows"]), use_container_width=True)

    # 4b. Verified Product Details Cards & Telemetry (Rendered when product inquiry or products in payload)
    if s_res.get("products"):
        prods = s_res["products"]
        with st.expander(f"📦 Verified Ingested Products & Coverage ({len(prods)} Items Scoped)", expanded=True):
            for p_idx, p in enumerate(prods, 1):
                p_col1, p_col2, p_col3 = st.columns([3, 2, 2])
                with p_col1:
                    st.markdown(f"**{p_idx}. {p.get('name')}**")
                    st.caption(f"🏷️ **SKU:** `{p.get('sku')}` | 📁 **Category:** `{p.get('category')}`")
                    st.caption(f"🔢 **Qty:** {p.get('qty', 1)} | 💵 **Unit Price:** ${p.get('unit_price', 0):.2f} | 💰 **Total:** ${p.get('total_price', 0):.2f}")
                with p_col2:
                    p_ret_status = p.get("return_status", "ACTIVE")
                    p_days = p.get("return_days_remaining", "N/A")
                    p_deadline = p.get("return_deadline", "N/A")
                    st.markdown("**Return Window:**")
                    if p_ret_status == "EXPIRING_SOON":
                        st.markdown(f'<span class="status-badge-urgent">⚠️ Expiring Soon ({p_days}d left)</span>', unsafe_allow_html=True)
                    elif "FINAL" in str(p_ret_status).upper() or p_days == 0:
                        st.markdown('<span class="status-badge-final">❌ Final Sale (Non-Returnable)</span>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<span class="status-badge-active">✅ Active ({p_days}d left)</span>', unsafe_allow_html=True)
                    st.caption(f"Deadline: `{p_deadline}`")
                with p_col3:
                    st.markdown(f"**Warranty:** `{p.get('warranty_status', 'ACTIVE')}`")
                    st.caption(f"Expires: `{p.get('warranty_deadline', 'N/A')}`")
                if p_idx < len(prods):
                    st.divider()

    # 5. Google AI Overview Main Answer
    if s_res.get("summary"):
        st.markdown("""
        <div style="font-family:'DM Mono',monospace;font-size:0.82rem;font-weight:700;color:#93c5fd;margin:12px 0 6px;">
            ✦ GOOGLE AI OVERVIEW RESPONSE:
        </div>
        """, unsafe_allow_html=True)
        st.markdown(s_res["summary"])

    # 6. People Also Ask (Google-Style Clickable Questions)
    paa_items = s_res.get("people_also_ask") or s_res.get("followups")
    if paa_items:
        st.markdown("<div style='font-size:0.82rem;color:#93c5fd;margin-top:14px;font-weight:700;'>🔍 People Also Ask (Google Searches):</div>", unsafe_allow_html=True)
        f_cols = st.columns(len(paa_items))
        for idx, (col, f_q) in enumerate(zip(f_cols, paa_items)):
            if col.button(f"✦ {f_q}", key=f"paa_{idx}_{abs(hash(f_q))%1000000}", use_container_width=True):
                st.session_state["cockpit_query_val"] = f_q
                st.session_state["run_search_action"] = True
                st.rerun()

    # Action buttons
    res_btn_col1, res_btn_col2 = st.columns([1, 4])
    with res_btn_col1:
        if st.button("Clear Response ✖", key="btn_clear_cockpit_search"):
            st.session_state["search_result"] = None
            st.session_state["search_query"] = ""
            st.session_state["cockpit_query_val"] = ""
            st.rerun()
    with res_btn_col2:
        if st.session_state.get("session_data"):
            if st.button("💬 Send Overview to Copilot Chat", key="btn_send_cockpit_to_chat"):
                chat_content = f"**✦ Google & Gemini AI Overview on '{res_query}':**\n\n"
                if s_res.get("metrics"):
                    chat_content += " | ".join([f"**{k}:** {v}" for k, v in s_res['metrics'].items()]) + "\n\n"
                if s_res.get("summary"):
                    chat_content += s_res["summary"]
                st.session_state["chat_messages"].append({"role": "assistant", "content": chat_content})
                st.success("Sent Google AI Overview to Agent Chat history below! 👇")
                st.rerun()

st.markdown("---")

# Main Screen Display
if st.session_state["session_data"] is None:
    st.info("👈 **Please upload a receipt or select one of the Quick Load Sample Receipts in the sidebar to begin.**")
    
    # 3D Standby Animation
    st.markdown("##### 📦 CODEX 4D Spacetime & Digital Twin Hub")
    components.html(
        render_3d_order_animation(
            order_id="CODEX-STANDBY",
            customer_name="Awaiting Receipt Ingestion",
            is_urgent=False,
            urgent_count=0,
            total_items=0,
            height=380
        ),
        height=395
    )
    
    st.markdown("""
    ### What this Order & Warranty Agent does:
    1. **Immediate Proactive Ingestion**: The instant you upload your receipt, the agent parses the line items, scopes a Chroma vector database to your order, and runs deterministic date math.
    2. **Expiring Window Alerts**: If any return or warranty window has **< 7 days remaining**, it proactively flags it before you type any question.
    3. **Interactive 4D Spacetime Digital Twin**: Visualizes the shipment with real-time 4D Tesseract rotation, Riemannian curvature wave grid, warranty status illumination, and orbit controls.
    4. **Grounded QA**: You can ask follow-up questions about exchange policies, return conditions, or warranty claim procedures.
    5. **Mock Order Lookup**: Query live order statuses (e.g. `ORD-1001` or `ORD-1002`) with graceful handling for unknown orders.
    """)
else:
    session_data = st.session_state["session_data"]
    analysis = session_data["analysis"]
    receipt_meta = session_data["receipt_data"]
    urgent_items = analysis.get("urgent_items", [])

    # 1. Proactive Alerts Section (Immediate on Ingestion)
    if urgent_items:
        st.markdown(f"""
        <div class="urgent-box">
            <div class="urgent-title">🚨 PROACTIVE ALERT: {len(urgent_items)} ITEM(S) EXPIRING SOON (&lt; 7 DAYS REMAINING)</div>
            The return window for these items is closing rapidly. Deterministic Python calculation verified from purchase date:
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="safe-box">
            ✅ <strong>All Return Windows Active:</strong> No items on this receipt have return windows expiring within 7 days.
        </div>
        """, unsafe_allow_html=True)

    # 2. Interactive 3D/4D Digital Twin Section
    with st.expander("📦 Interactive 4D Spacetime & Warranty Digital Twin", expanded=True):
        components.html(
            render_3d_order_animation(
                order_id=receipt_meta.get("order_id", "ORD-UNKNOWN"),
                customer_name=receipt_meta.get("customer", "Valued Shopper"),
                is_urgent=bool(urgent_items),
                urgent_count=len(urgent_items),
                total_items=len(analysis.get("items_analysis", [])),
                height=400
            ),
            height=415
        )

    # 3. Key Metrics Row
    m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)
    with m_col1:
        st.metric("Order ID", receipt_meta.get("order_id", "N/A"))
    with m_col2:
        st.metric("Customer", receipt_meta.get("customer", "N/A"))
    with m_col3:
        st.metric("Store", receipt_meta.get("store_name", "CODEX Store")[:22])
    with m_col4:
        st.metric("Purchase Date", receipt_meta.get("purchase_date", "N/A"))
    with m_col5:
        total_val = receipt_meta.get("total")
        st.metric("Total Charged", f"${total_val:.2f}" if total_val is not None else "N/A")

    # 4. Itemized Coverage Cards
    with st.expander("🔍 Complete Itemized Return & Warranty Breakdown", expanded=True):
        items_analysis = analysis.get("items_analysis", [])
        parsed_items_map = {it.get("name"): it for it in receipt_meta.get("items", [])}

        for idx, item in enumerate(items_analysis, start=1):
            matching_raw_item = parsed_items_map.get(item.get("item_name"), {})
            qty = matching_raw_item.get("qty", 1)
            u_price = matching_raw_item.get("unit_price", 0.0)
            t_price = matching_raw_item.get("total_price", 0.0)
            sku = matching_raw_item.get("sku", "N/A")
            cond = matching_raw_item.get("condition", "Standard")

            c1, c2, c3 = st.columns([3, 2, 2])
            with c1:
                st.markdown(f"**{idx}. {item.get('item_name')}**")
                st.caption(f"📁 **Category:** `{item.get('category')}` | 🏷️ **SKU:** `{sku}`")
                st.caption(f"🔢 **Qty:** {qty} | 💵 **Unit Price:** ${u_price:.2f} | 💰 **Total:** ${t_price:.2f}")
                if cond and cond != "Standard":
                    st.caption(f"📦 **Condition:** {cond}")
            with c2:
                status = item.get("return_status")
                days_left = item.get("return_days_remaining")
                deadline = item.get("return_deadline")
                ret_days_policy = item.get("return_policy_days", 30)

                st.markdown("**Return Window:**")
                if status == "EXPIRING_SOON":
                    st.markdown(f'<span class="status-badge-urgent">⚠️ Expiring Soon ({days_left}d left)</span>', unsafe_allow_html=True)
                elif status == "NON_RETURNABLE_FINAL_SALE":
                    st.markdown('<span class="status-badge-final">❌ Final Sale (Non-Returnable)</span>', unsafe_allow_html=True)
                elif status == "EXPIRED":
                    st.markdown('<span class="status-badge-final">❌ Expired</span>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<span class="status-badge-active">✅ Active ({days_left}d left)</span>', unsafe_allow_html=True)
                st.caption(f"Policy: {ret_days_policy} days | Deadline: `{deadline}`")
            with c3:
                w_status = item.get("warranty_status")
                w_days = item.get("warranty_days_remaining")
                w_deadline = item.get("warranty_deadline")
                w_policy_days = item.get("warranty_policy_days", 365)

                st.markdown(f"**Warranty Coverage:** `{w_status}`")
                st.caption(f"Policy: {w_policy_days} days | Remaining: {w_days}d")
                st.caption(f"Warranty Expiry: `{w_deadline}`")
            st.divider()

    # 5. Raw Shopkeeper Receipt Document View
    with st.expander("📄 Original Ingested Receipt Document (Raw Text View)", expanded=False):
        raw_text_content = receipt_meta.get("raw_text", "")
        st.caption("Verbatim text extracted from the uploaded file / receipt slip:")
        st.code(raw_text_content, language="markdown")

    st.markdown("---")
    st.subheader("💬 Ask CODEX Follow-up Questions or Request 5.6 Tera Charts")
    st.caption("Ask questions like *'When can I return the jacket?'*, *'Check status for ORD-1002'*, or *'Plot return countdown with 5.6 Tera ChartGPT'*:")

    # Dedicated 5.6 Tera ChartGPT Quick Plotting Box
    with st.expander("📊 5.6 Tera ChartGPT Quick Plotting Box", expanded=False):
        with st.form(key="chat_quick_plot_form", clear_on_submit=False):
            chart_col1, chart_col2 = st.columns([4, 1])
            with chart_col1:
                chart_q = st.text_input(
                    "Enter chart query or analytics prompt:", 
                    placeholder="e.g. Plot 7-day sales velocity or chart return window countdown", 
                    key="app_chartgpt_box",
                    label_visibility="collapsed"
                )
            with chart_col2:
                chart_btn = st.form_submit_button("Plot 📊", use_container_width=True, type="primary")
            
        if chart_btn and chart_q:
            st.session_state["chat_messages"].append({"role": "user", "content": f"5.6 Tera ChartGPT: {chart_q}"})
            with st.spinner("Computing 5.6 Tera visual analytics & forecast..."):
                c_res = run_chartgpt_or_ai_engine(chart_q, mode="📊 5.6 Tera ChartGPT", session=session_data["session"], receipt_data=receipt_meta)
                chat_summary = f"**{c_res.get('chart_title', '5.6 Tera ChartGPT')}**\n\n"
                if c_res.get("metrics"):
                    chat_summary += " | ".join([f"**{k}:** {v}" for k, v in c_res['metrics'].items()]) + "\n\n"
                chat_summary += c_res.get("summary", "")
                st.session_state["chat_messages"].append({"role": "assistant", "content": chat_summary})
            st.rerun()

    # Display Chat History
    for msg in st.session_state["chat_messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User Input
    if user_prompt := st.chat_input("Ask a question, enter an Order ID (e.g. ORD-1002), or type 'Plot chart with 5.6T ChartGPT'"):
        # Append User Message
        st.session_state["chat_messages"].append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        # Generate Assistant Answer
        with st.chat_message("assistant"):
            with st.spinner("Thinking & consulting scoped vector store and tools..."):
                response_text = answer_shopper_query(session_data["session"], user_prompt)
                st.markdown(response_text)
        
        # Append Assistant Response
        st.session_state["chat_messages"].append({"role": "assistant", "content": response_text})

    # Inspection Expander for Judges / Developers
    with st.expander("🛠️ Under the Hood: Pipeline & Scoped Vector Store Inspection"):
        st.write("**Receipt Chunks in Chroma Vector Store:**")
        docs = session_data["vectorstore"].similarity_search("return policy and item details", k=4)
        for i, d in enumerate(docs, 1):
            st.text(f"Chunk #{i} [{d.metadata.get('doc_type')}]:\n{d.page_content}\n")
        st.write("**Raw Deterministic Calculation JSON:**")
        st.json(analysis)
