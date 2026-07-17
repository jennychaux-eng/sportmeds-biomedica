import os
import base64
import streamlit as st

from datetime import datetime
from zoneinfo import ZoneInfo

from supabase import create_client, Client

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

LOGO_PATH = os.path.join(
    BASE_DIR,
    "assets",
    "Logo_sportmeds.png"
)


def get_fecha_local():
    return datetime.now(
        ZoneInfo("America/Bogota")
    ).date()


def get_base64_image(path):
    with open(path, "rb") as img:
        return base64.b64encode(
            img.read()
        ).decode()


@st.cache_resource
def init_supabase():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)


supabase: Client = init_supabase()
