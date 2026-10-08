import streamlit as st
import datetime
import random
import pandas as pd
from PIL import Image

# ----------------- Page Configuration -----------------
st.set_page_config(
    page_title="Waste2Worth - Smart Waste Management",
    page_icon="♻️",
    layout="wide"
)

# ----------------- High-Contrast Theme, Sidebar & File Uploader CSS -----------------
st.markdown(
    """
    <style>
    /* Full App Background */
    .stApp {
        background: linear-gradient(135deg, #f4faf6 0%, #e8f5ec 50%, #d8ebd9 100%);
        background-attachment: fixed;
    }

    /* Main Area Typography */
    .stApp, .stApp p, .stApp span, .stApp label {
        color: #172a1e !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #0d381e !important;
        font-weight: 700 !important;
    }

    /* Cards / Containers in Main Screen */
    [data-testid="stForm"], [data-testid="stMetric"], .stTable {
        background-color: rgba(255, 255, 255, 0.95) !important;
        padding: 18px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.05) !important;
        border: 1px solid #c9e4d1 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #1b6338 !important;
        font-weight: 800 !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #31533d !important;
        font-weight: 600 !important;
    }

    /* ---------------------------------------------------- */
    /* FILE UPLOADER VISIBILITY FIX                         */
    /* ---------------------------------------------------- */
    [data-testid="stFileUploader"] {
        background-color: #ffffff !important;
        border: 2px dashed #246d41 !important;
        border-radius: 12px !important;
        padding: 16px !important;
    }

    [data-testid="stFileUploaderDropzone"] {
        background-color: #ffffff !important;
    }

    /* File uploader internal text (Drag and drop / file limit) */
    [data-testid="stFileUploaderDropzone"] * {
        color: #1b4332 !important;
        font-weight: 600 !important;
    }

    /* File uploader button ("Browse files") */
    [data-testid="stFileUploaderDropzone"] button {
        background-color: #246d41 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: bold !important;
        padding: 8px 16px !important;
    }

    [data-testid="stFileUploaderDropzone"] button:hover {
        background-color: #1b4332 !important;
        color: #ffffff !important;
    }

    /* ---------------------------------------------------- */
    /* LEFT SIDEBAR HIGH-SPECIFICITY OVERRIDES             */
    /* ---------------------------------------------------- */
    [data-testid="stSidebar"] {
        background-color: #0c2819 !important;
    }

    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
        font-weight: 800 !important;
    }

    [data-testid="stSidebar"] div[role="radiogroup"] label {
        background: rgba(255, 255, 255, 0.12) !important;
        padding: 10px 14px !important;
        border-radius: 8px !important;
        margin-bottom: 8px !important;
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
        display: flex !important;
        align-items: center !important;
    }

    [data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background: rgba(255, 255, 255, 0.22) !important;
    }

    [data-testid="stSidebar"] div[role="radiogroup"] label p,
    [data-testid="stSidebar"] div[role="radiogroup"] label span,
    [data-testid="stSidebar"] div[role="radiogroup"] label div {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 15px !important;
    }

    [data-testid="stSidebar"] [data-testid="stMetric"] {
        background-color: #ffffff !important;
        border-radius: 12px !important;
        padding: 14px !important;
    }
    [data-testid="stSidebar"] [data-testid="stMetric"] [data-testid="stMetricLabel"] * {
        color: #2d3748 !important;
        font-weight: 600 !important;
    }
    [data-testid="stSidebar"] [data-testid="stMetric"] [data-testid="stMetricValue"] * {
        color: #0f4d2a !important;
        font-weight: 800 !important;
        font-size: 32px !important;
    }
