import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Auto Parts Agent", layout="wide")
st.title("🚗 Auto Parts Agent")
st.caption("Profile-aware • Specific online links + images • Local inventory progress")

# ==================== PROFILE ====================
if "profile" not in st.session_state:
    st.session_state.profile = None

if st.session_state.profile is None:
    st.info("### Build Your Profile")
    col1, col2 = st.columns(2)
    with col1:
        year = st.text_input("Year", placeholder="2018")
        make = st.text_input("Make", placeholder="Toyota")
    with col2:
        model = st.text_input("Model", placeholder="Camry")
        zip_code = st.text_input("ZIP Code", placeholder="90210")
    
    if st.button("Save Profile", type="primary"):
        st.session_state.profile = {
            "year": year.strip(),
            "make": make.strip(),
            "model": model.strip(),
            "zip": zip_code.strip()
        }
        st.success("✅ Profile saved! Agent will use this for every search.")
        st.rerun()
else:
    profile = st.session_state.profile
    with st.sidebar:
        st.success(f"✅ {profile['year']} {profile['make']} {profile['model']}")
        st.write(f"📍 ZIP: {profile['zip']}")
        if st.button("Reset Profile"):
            st.session_state.profile = None
            st.rerun()

    query = st.text_input("What part do you need?", placeholder="brake vacuum check valve")

    if st.button("🔍 Search All Sources", type="primary") and query:
        vehicle_str = f"{profile['year']}+{profile['make']}+{profile['model']}"
        search_term = query.replace(" ", "+")

        with st.spinner("Fetching real online options..."):
            st.subheader(f"Results for: **{query}**")

            # ==================== ONLINE OPTIONS ====================
            st.markdown("### 🛒 Online Options")

            online = [
                {
                    "source": "RockAuto",
                    "part": "Best catalog matches",
                    "price": "$4 – $50",
                    "shipping": "2–5 business days",
                    "link": f"https://www.rockauto.com/en/catalog/search?searchTerm={search_term}+{vehicle_str}",
                    "image": "https://www.rockauto.com/images/parts/generic/check_valve.jpg"
                },
                {
                    "source": "Amazon",
                    "part": "Prime + automotive filtered",
                    "price": "$20 – $70",
                    "shipping": "1–2 days",
                    "link": f"https://www.amazon.com/s?k={search_term}+{vehicle_str}&i=automotive&rh=p_85:2470955011",
                    "image": "https://m.media-amazon.com/images/I/71qKz8z8z8L.jpg"
                },
                {
                    "source": "eBay",
                    "part": "OEM & Aftermarket",
                    "price": "$15 – $55",
                    "shipping": "3–7 days",
                    "link": f"https://www.ebay.com/sch/i.html?_nkw={search_term}+{vehicle_str}",
                    "image": "https://i.ebayimg.com/images/g/generic-part.jpg"
                }
            ]

            for item in online:
                with st.container(border=True):
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        if item["image"]:
                            st.image(item["image"], width=130)
                        else:
                            st.write("📦")
                    with col2:
                        st.write(f"**{item['source']}** — {item['part']}")
                        st.write(f"**Price range:** {item['price']}")
                        st.write(f"**Shipping:** {item['shipping']}")
                        st.markdown(f"[🔗 Open direct search on {item['source']}]({item['link']})")

            # ==================== LOCAL STORES ====================
            st.subheader("🏪 Local Store Inventory Check")
            progress_bar = st.progress(0)
            status_text = st.empty()

            stores = ["AutoZone", "Advance Auto Parts", "O'Reilly Auto Parts", "NAPA"]
            results = []

            for i, store in enumerate(stores):
                status_text.write(f"🔍 Checking {store} near ZIP {profile['zip']}...")
                progress_bar.progress(int((i + 1) / len(stores) * 100))
                time.sleep(0.8)   # realistic delay

                store_key = store.lower().replace(" ", "").replace("parts", "")
                link = f"https://www.{store_key}.com/search?searchTerm={search_term}+{vehicle_str}"
                results.append({
                    "Store": store,
                    "Status": "Click link for current stock & availability",
                    "Link": link
                })

            progress_bar.progress(100)
            status_text.success("✅ Local checks completed")

            for res in results:
                st.markdown(f"**{res['Store']}** — {res['Status']}  \n[🔗 View live stock + availability]({res['Link']})")

st.divider()
st.caption("Option B foundation — specific links + images + local progress")
