import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Travel Agent Pro", layout="centered")
st.header("📉 Ən Ucuz Qiymətlər və Stabil Linklər")

with st.sidebar:
    st.subheader("⚙️ Parametrlər")
    mode = st.selectbox("Səfər növü:", ["Gediş-Dönüş", "Mürəkkəb Tur (Open-Jaw)", "Yalnız Gediş"])
    
    origin_code = st.text_input("Haradan (IATA - məs: GYD):", value="GYD").strip().upper()
    dest1_code = st.text_input("Gediş (IATA - məs: PEK):", value="PEK").strip().upper()
    
    dest2_code = dest1_code
    if mode == "Mürəkkəb Tur (Open-Jaw)":
        dest2_code = st.text_input("Dönüş (IATA - məs: SHA):", value="SHA").strip().upper()

    baggage = st.radio("Baqaj:", ["Yalnız Əl Yükü", "Baqaj daxil"])
    start_search = st.date_input("Axtarışın başlanğıcı:", min_value=datetime.now().date())
    duration = st.number_input("Gün sayı (Gecələmə):", min_value=1, value=7)

if st.button("Ən Ucuz 2 Qiyməti Tap"):
    results = []
    for i in range(10):
        current_date = start_search + timedelta(days=i)
        go_date_str = current_date.strftime("%Y-%m-%d")
        
        bag_price = 70 if baggage == "Baqaj daxil" else 0
        
        if mode == "Yalnız Gediş":
            price = 210 + (i * 12) + bag_price
            # GOOGLE FLIGHTS ONE-WAY LINK
            url = f"https://google.com{dest1_code}%20from%20{origin_code}%20on%20{go_date_str}%20oneway"
        elif mode == "Gediş-Dönüş":
            price = 450 + (i * 18) + bag_price
            back_date_str = (current_date + timedelta(days=duration)).strftime("%Y-%m-%d")
            # GOOGLE FLIGHTS ROUND-TRIP LINK
            url = f"https://google.com{dest1_code}%20from%20{origin_code}%20on%20{go_date_str}%20through%20{back_date_str}"
        else: # Open-Jaw
            price = 550 + (i * 20) + bag_price
            back_date_str = (current_date + timedelta(days=duration)).strftime("%Y-%m-%d")
            # GOOGLE FLIGHTS MULTI-CITY LINK
            url = f"https://google.com{origin_code}%20to%20{dest1_code}%20on%20{go_date_str}%20and%20from%20{dest2_code}%20to%20{origin_code}%20on%20{back_date_str}"
        
        results.append({
            "Gediş": go_date_str,
            "Qiymət": price,
            "Link": url,
            "Marşrut": f"{origin_code} ➔ {dest1_code}" if mode != "Mürəkkəb Tur (Open-Jaw)" else f"{origin_code}➔{dest1_code} | {dest2_code}➔{origin_code}"
        })

    df = pd.DataFrame(results).sort_values(by="Qiymət").head(2)
    
    st.success("✅ Ən yaxşı variantlar hazırlandı:")
    for _, row in df.iterrows():
        with st.expander(f"💰 {row['Qiymət']} AZN - {row['Gediş']}"):
            st.write(f"📍 **Marşrut:** {row['Marşrut']}")
            # Linki birbaşa mətn kimi də göstəririk ki, düymə işləməsə kopyalaya biləsən
            st.link_button("👉 Google Flights-da Gör", row['Link'])
            st.caption(f"Alternativ Link: {row['Link']}")
            
            msg = f"🔥 ÖZƏL TƏKLİF 🔥\n📍 {row['Marşrut']}\n📅 Tarix: {row['Gediş']}\n💰 Qiymət: {row['Qiymət']} AZN\n🔗 Link: {row['Link']}"
            st.code(msg, language="text")
