import streamlit as st
import pandas as pd
from rockauto_api import RockAutoClient
import asyncio

st.set_page_config(page_title="Auto Parts Agent", layout="wide")
st.title("🚗 Auto Parts Agent")
st.caption("Real RockAuto prices • Vehicle-specific search")

# User Profile
if "profile" not in st.session_state:
    st.session_state.profile = None

if st.session_state.profile is None:
    st.info("### Set up your vehicle")
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
                "make": make.strip().upper(),
                "model": model.strip().upper(),
                "zip": zip_code.strip()
            }
            st.success("✅ Profile saved!")
            st.rerun()
else:
    profile = st.session_state.profile
    with st.sidebar:
        st.success(f"✅ {profile['year']} {profile['make']} {profile['model']}")
        st.write(f"📍 ZIP: {profile['zip']}")
        if st.button("Change Profile"):
            st.session_state.profile = None
            st.rerun()

    query = st.text_input("What part do you need?", placeholder="brake vacuum check valve")
    
    if st.button("🔍 Real Search on RockAuto", type="primary") and query:
        with st.spinner("Fetching real prices from RockAuto..."):
            try:
                async def search():
                    async with RockAutoClient() as client:
                        vehicle = await client.get_vehicle(profile['make'], int(profile['year']), profile['model'])
                        parts = await vehicle.search_parts(query)
                        return parts
                
                parts = asyncio.run(search())
                
                if parts:
                    data = []
                    for part in parts[:10]:  # Limit to top 10
                        data.append([
                            part.brand,
                            part.part_number,
                            f"${part.price}",
                            part.description[:80] + "..." if len(part.description) > 80 else part.description
                        ])
                    
                    df = pd.DataFrame(data, columns=["Brand", "Part Number", "Price", "Description"])
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.warning("No results found. Try a different part name.")
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("RockAuto search is being added — it may need small tweaks.")

st.divider()
st.caption("Your live app now tries real RockAuto data")
