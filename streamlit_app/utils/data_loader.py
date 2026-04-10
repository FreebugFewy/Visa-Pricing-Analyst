import streamlit as st
import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "data" / "visa_pricing_metrics.csv"


@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH, parse_dates=["month"])
