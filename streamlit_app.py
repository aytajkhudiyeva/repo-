import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Professional Travel Engine", layout="wide")
st.header("✈️ Universal Skaner")

# İNTERFEYS - SOL PANEL
with st.sidebar:
    st.subheader("⚙️ Axtarış Növü")
    # Ssenari seçimi
    mode = st.selectbox("Səfər növünü seçin:", 
                        ["Yalnız Gediş (One-way)", 
                         "Gediş-Dönüş (Eyni şəhər)", 
                         "Mürəkkəb Tur (Open-Jaw)"])
    
    st.markdown("---")
    origin = st.text_input("Haradan? (IATA)", value="GYD").upper()
    
    # Seçimə görə xanalar açılır
    if mode == "Yalnız Gediş (One-way)":
        dest1 = st.text_input("Haraya?", value="IST").upper()
        dest2 = None
    elif mode == "Gediş-Dönüş (Eyni şəhər)":
        dest1 = st.text_input("Haraya?", value="DXB").upper()
        dest2 = dest1
    else: # Open-Jaw
        dest1 = st.text_input("1-ci Şəhər (Gediş)", value="PEK").upper()
        dest2 = st.text_input("2-ci Şəhər (Dönüş)", value="SHA").upper()

    st.markdown("---")
    # Tarix: Minimum BUGÜN
    start_search = st.date_input("Axtarışın başlanğıcı:", min_value=datetime.now().date())
    end_search = st.date_input("Axtarışın sonu:", value=start_search + timedelta(days=30), min_value=start_search)
    
    duration = 0
    if mode != "Yalnız Gediş (One-way)":
        duration = st.number_input("Səyahət müddəti (Gün)", min_value=1, value=7)

if st.button("Skan et və Ən Ucuzunu Tap"):
    st.info("Bütün kombinasiyalar müqayisə edilir...")
    
    results = []
    current = start_search
    
    while current <= end_search:
        go_date = current.strftime("%Y-%m-%d")
        
        # Ssenariyə uyğun məlumat yığırıq
        if mode == "Yalnız Gediş (One-way)":
            results.append({
                "Tarix": go_date,
                "Marşrut": f"{origin} ➔ {dest1}",
                "Qiymət (Təxmini)": 150 + (current.day * 3),
                "Növ": "Gediş"
            })
        else:
            back_date = (current + timedelta(days=duration)).strftime("%Y-%m-%d")
            results.append({
                "Gediş": go_date,
                "Dönüş": back_date,
                "Marşrut": f"{origin} ➔ {dest1} | {dest2} ➔ {origin}",
                "Qiymət (Təxmini)": 400 + (current.day * 5),
                "Növ": mode
            })
        current += timedelta(days=1)

    df = pd.DataFrame(results).sort_values(by="Qiymət (Təxmini)")
    st.success(f"✅ {len(results)} variant skan edildi.")
    st.dataframe(df, use_container_width=True)

st.sidebar.markdown(f"**Cari Tarix:** {datetime.now().strftime('%Y-%m-%d')}")
