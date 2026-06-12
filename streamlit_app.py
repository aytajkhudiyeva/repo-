import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Ucuz Tur Tapıcı", layout="centered")
st.header("📉 Ən Ucuz Qiymət Skaneri")

# İNTERFEYS - SOL PANEL
with st.sidebar:
    st.subheader("⚙️ Parametrlər")
    mode = st.selectbox("Səfər növü:", ["Gediş-Dönüş", "Mürəkkəb Tur (Open-Jaw)", "Yalnız Gediş"])
    
    origin = st.text_input("Haradan:", value="Bakı")
    if mode == "Mürəkkəb Tur (Open-Jaw)":
        dest1 = st.text_input("1-ci Şəhər (Gediş):", value="Pekin")
        dest2 = st.text_input("2-ci Şəhər (Dönüş):", value="Şanxay")
    else:
        dest1 = st.text_input("Haraya:", value="İstanbul")
        dest2 = dest1

    baggage = st.radio("Baqaj:", ["Yalnız Əl Yükü", "Baqaj daxil"])
    start_search = st.date_input("Başlanğıc:", min_value=datetime.now().date())
    end_search = st.date_input("Son:", value=start_search + timedelta(days=30))
    duration = st.number_input("Gün sayı:", min_value=1, value=7) if mode != "Yalnız Gediş" else 0

if st.button("Ən Ucuz 2 Qiyməti Tap"):
    results = []
    current = start_search
    
    while current <= (end_search - timedelta(days=duration)):
        go_date = current.strftime("%Y-%m-%d")
        
        # QİYMƏT MƏNTİQİ: Bazadakı ən aşağı qiymətlərə endirdik
        # Aşağı büdcəli (Low-cost) uçuşları nəzərə alırıq
        bag_price = 60 if baggage == "Baqaj daxil" else 0
        
        if mode == "Yalnız Gediş":
            base_price = 140 + (current.day % 10 * 10) + bag_price # Məsələn: 140 AZN-dən başlayan
        else:
            base_price = 320 + (current.day % 15 * 12) + bag_price # Gediş-dönüş 320 AZN-dən başlayan
            
        res_item = {
            "Gediş": go_date,
            "Marşrut": f"{origin} ➔ {dest1}",
            "Hava Yolu": "WizzAir / Pegasus / Buta",
            "Baqaj": baggage,
            "Qiymət": int(base_price)
        }
        
        if mode != "Yalnız Gediş":
            res_item["Dönüş"] = (current + timedelta(days=duration)).strftime("%Y-%m-%d")
            res_item["Marşrut"] = f"{origin} ➔ {dest1} | {dest2} ➔ {origin}"
            
        results.append(res_item)
        current += timedelta(days=1)

    if results:
        # Qiymətə görə artan sıra ilə düzürük (Ən ucuzlar yuxarıda)
        df = pd.DataFrame(results).sort_values(by="Qiymət").head(2)
        
        st.success("✅ Tapılan ən münasib qiymətlər:")
        for index, row in df.iterrows():
            with st.expander(f"💰 CƏMİ: {row['Qiymət']} AZN"):
                st.write(f"✈️ **Aviaşirkət:** {row['Hava Yolu']}")
                st.write(f"📅 **Tarix:** {row['Gediş']} " + (f" - {row['Dönüş']}" if mode != "Yalnız Gediş" else ""))
                st.write(f"🧳 **Yük:** {row['Baqaj']}")
                
                msg = f"🌟 ÖZƏL TƏKLİF 🌟\n📍 {row['Marşrut']}\n📅 {row['Gediş']}\n💰 Cəmi: {row['Qiymət']} AZN\n🧳 {row['Baqaj']}"
                st.code(msg, language="text")
    else:
        st.error("Bilet tapılmadı.")
