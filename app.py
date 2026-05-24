import streamlit as st
import pandas as pd
import asyncio
from playwright.async_api import async_playwright

st.set_page_config(page_title="Auto Parts Agent", layout="wide")
st.title("🚗 Auto Parts Agent")
st.caption("Vehicle-aware • Real online prices + shipping • Local inventory attempts")

# Persistent user profile
if "profile" not in st.session_state:
    st.session_state.profile = None

if st.session_state.profile is None:
    st.info("### Build Your Profile")
    col1, col2 = st.columns(2)
    with col1:
        year = st.text_input("Year", placeholder="2015")
        make = st.text_input("Make", placeholder="Ford")
    with col2:
        model = st.text_input("Model", placeholder="F-150")
        zip_code = st.text_input("ZIP Code", placeholder="10001")
    
    if st.button("Save Profile", type="primary"):
        st.session_state.profile = {
            "year": year.strip(),
            "make": make.strip(),
            "model": model.strip(),
            "zip": zip_code.strip()
        }
        st.success("Profile saved. The agent will use this going forward.")
        st.rerun()
else:
    profile = st.session_state.profile
    with st.sidebar:
        st.success(f"✅ {profile['year']} {profile['make']} {profile['model']}")
        st.write(f"📍 {profile['zip']}")
        if st.button("Reset Profile"):
            st.session_state.profile = None
            st.rerun()

    query = st.text_input("What part do you need?", placeholder="oil filter")

    if st.button("🔍 Search All Sources", type="primary") and query:
        with st.spinner("Searching RockAuto + attempting local stores..."):
            st.subheader(f"Results for **{query}**")

            # Online results placeholder (we'll add real RockAuto next)
            online_data = [
                ["RockAuto", "$8.50", "2-5 days", "$15", "Usually cheapest"],
                ["Amazon", "$22.99", "1-2 days Prime", "$22.99", "Fast"],
                ["eBay", "$18-35", "3-7 days", "$25", "Good deals"]
            ]
            df_online = pd.DataFrame(online_data, columns=["Source", "Price", "Shipping", "Est Total", "Notes"])
            st.dataframe(df_online, use_container_width=True)

            # Local attempt with Playwright
            st.subheader("Local Store Attempts")
            st.info(f"Attempting to check stores near ZIP {profile['zip']}... (this can be flaky)")
            
            # We can expand this with real Playwright logic in next iteration

st.caption("Core agent foundation — ready for deeper scraping")
