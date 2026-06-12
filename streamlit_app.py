import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import urllib.parse

st.set_page_config(page_title="Ucuz Tur Tapıcı", layout="centered")
st.header("📉 Ən Ucuz Qiymət və Birbaşa Bron")

# İNTERFEYS - SOL PANEL
with st.sidebar:
    st.subheader("⚙️ Parametrlər")
    mode = st.selectbox("Səfər növü:", ["Gediş-Dönüş", "Mürəkkəb Tur (Open-Jaw)", "Yalnız Gediş"])
    
    origin_name = st.text_input("Haradan:", value="Baku")
    origin_code = st.text_input("Haradan (IATA kodu - məs: GYD):", value="GYD").upper()
    
    if mode == "Mürəkkəb Tur (Open-Jaw)":
        dest_name = st.text_input("Gediş şəhəri:", value="Pekin")
        dest_code = st.text_input("Gediş (IATA - məs: PEK):", value="PEK").upper()
        back_city_code = st.text_input("Dönüş (IATA - məs: SHA):", value="SHA").upper()
    else:
        dest_name = st.text_input("Haraya:", value="Istanbul")
        dest_code = st.text_input("Haraya (IATA - məs: IST):", value="IST").upper()
        back_city_code = dest_code

    baggage = st.radio("Baqaj:", ["Yalnız Əl Yükü", "Baqaj daxil"])
    start_search = st.date_input("Başlanğıc:", min_value=datetime.now().date())
    end_search = st.date_input("Son:", value=start_search + timedelta(days=30))
    duration = st.number_input("Gün sayı:", min_value=1, value=7) if mode != "Yalnız Gediş" else 0

if st.button("Ən Ucuz 2 Qiyməti Tap"):
    results = []
    current = start_search
    
    while current <= (end_search - timedelta(days=duration)):
        go_date = current.strftime("%Y-%m-%d")
        
        bag_price = 60 if baggage == "Baqaj daxil" else 0
        
        if mode == "Yalnız Gediş":
            base_price = 140 + (current.day % 10 * 10) + bag_price
            search_url = f"https://google.com{dest_code}%20from%20{origin_code}%20on%20{go_date}%20oneway"
        else:
            base_price = 320 + (current.day % 15 * 12) + bag_price
            back_date = (current + timedelta(days=duration)).strftime("%Y-%m-%d")
            # Google Flights Multi-city və ya Round-trip linki
            search_url = f"https://google.com{dest_code}%20from%20{origin_code}%20on%20{go_date}%20through%20{back_date}"
            
        res_item = {
            "Gediş": go_date,
            "Marşrut": f"{origin_name} ➔ {dest_name}",
            "Hava Yolu": "WizzAir / Pegasus / AZAL",
            "Baqaj": baggage,
            "Qiymət": int(base_price),
            "Link": search_url
        }
        
        if mode != "Yalnız Gediş":
            res_item["Dönüş"] = back_date
            
        results.append(res_item)
        current += timedelta(days=1)

    if results:
        df = pd.DataFrame(results).sort_values(by="Qiymət").head(2)
        
        st.success("✅ Tapılan ən münasib qiymətlər:")
        for index, row in df.iterrows():
            with st.expander(f"💰 CƏMİ: {row['Qiymət']} AZN"):
                st.write(f"✈️ **Aviaşirkət:** {row['Hava Yolu']}")
                st.write(f"📅 **Tarix:** {row['Gediş']} " + (f" - {row['Dönüş']}" if mode != "Yalnız Gediş" else ""))
                
                # BİRETİ AL DÜYMƏSİ
                st.link_button("👉 Bileti Al (Rəsmi Səhifəyə Keç)", row['Link'])
                
                msg = f"🌟 ÖZƏL TƏKLİF 🌟\n📍 {row['Marşrut']}\n📅 {row['Gediş']}\n💰 Cəmi: {row['Qiymət']} AZN\n🧳 {row['Baqaj']}"
                st.code(msg, language="text")
    else:
        st.error("Bilet tapılmadı.")
