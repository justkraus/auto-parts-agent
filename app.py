import streamlit as st
import pandas as pd

st.set_page_config(page_title="Auto Parts Agent", layout="wide")
st.title("🚗 Auto Parts Agent")
st.caption("Find parts for any vehicle • Local + Online pricing")

# User Profile
if "profile" not in st.session_state:
    st.session_state.profile = None

if st.session_state.profile is None:
    st.info("### Set up your vehicle profile")
    col1, col2 = st.columns(2)
    with col1:
        year = st.text_input("Year", placeholder="1996")
        make = st.text_input("Make", placeholder="Chevrolet")
    with col2:
        model = st.text_input("Model", placeholder="Suburban K2500")
        zip_code = st.text_input("ZIP Code", placeholder="28205")
    
    if st.button("Save Profile", type="primary"):
        if year and make and model and zip_code:
            st.session_state.profile = {
                "year": year.strip(),
                "make": make.strip(),
                "model": model.strip(),
                "zip": zip_code.strip()
            }
            st.success("✅ Profile saved! Now search for parts.")
            st.rerun()
else:
    profile = st.session_state.profile
    with st.sidebar:
        st.success(f"✅ {profile['year']} {profile['make']} {profile['model']}")
        st.write(f"📍 {profile['zip']}")
        if st.button("Change Vehicle"):
            st.session_state.profile = None
            st.rerun()

    query = st.text_input("What part do you need?", placeholder="brake vacuum check valve")
    
    if st.button("🔍 Search", type="primary") and query:
        with st.spinner("Searching..."):
            st.subheader(f"Results for: **{query}**")
            
            data = [
                ["RockAuto", "Dorman 80189", "$3.77", "2-5 days", "$10-16", "Cheapest"],
                ["Amazon", "ACDelco 179-1266", "$28.50", "1-2 days", "$28.50", "Fast delivery"],
                ["AutoZone", "ACDelco 179-1266", "$39.99", "Same day pickup", "$39.99", "Local"],
                ["Advance", "ACDelco 179-1266", "$39.99", "Same day pickup", "$39.99", "Local"]
            ]
            
            df = pd.DataFrame(data, columns=["Source", "Part", "Price", "Delivery", "Total", "Notes"])
            st.dataframe(df, use_container_width=True, hide_index=True)
