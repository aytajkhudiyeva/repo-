import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Travel Agent Panel", layout="centered")
st.header("✈️ Peşəkar Tur Skaneri")

# İNTERFEYS - SOL PANEL
with st.sidebar:
    st.subheader("⚙️ Axtarış Parametrləri")
    mode = st.selectbox("Səfər növü:", ["Mürəkkəb Tur (Open-Jaw)", "Gediş-Dönüş", "Yalnız Gediş"])
    
    st.markdown("---")
    origin = st.text_input("Haradan? (Məs: Bakı)", value="Bakı")
    
    if mode == "Mürəkkəb Tur (Open-Jaw)":
        dest1 = st.text_input("1-ci Şəhər (Gediş):", value="Pekin")
        dest2 = st.text_input("2-ci Şəhər (Dönüş):", value="Şanxay")
    else:
        dest1 = st.text_input("Haraya? (Məs: İstanbul):", value="İstanbul")
        dest2 = dest1

    st.markdown("---")
    baggage = st.radio("Baqaj seçimi:", ["Yalnız Əl Yükü", "Baqaj daxil (23kq)"])
    
    # Tarix: Minimum BUGÜN
    start_search = st.date_input("Axtarış başlasın:", min_value=datetime.now().date())
    end_search = st.date_input("Axtarış bitsin:", value=start_search + timedelta(days=30), min_value=start_search)
    
    duration = st.number_input("Gün sayı (Gecələmə):", min_value=1, value=7) if mode != "Yalnız Gediş" else 0

if st.button("Ən Ucuz 2 Qiyməti Tap"):
    st.write(f"🔎 {origin} istiqamətindən ən uyğun biletlər axtarılır...")
    
    results = []
    current = start_search
    
    # Skaner məntiqi
    while current <= (end_search - timedelta(days=duration)):
        go_date = current.strftime("%Y-%m-%d")
        
        # Manatla qiymət simulyasiyası (Baqaj fərqi ilə)
        bag_price = 85 if baggage == "Baqaj daxil (23kq)" else 0
        base_price = 680 + (current.day * 5) + bag_price # Manatla baza qiymət
        
        if mode == "Yalnız Gediş":
            results.append({
                "Tarix": go_date,
                "Marşrut": f"{origin} ➔ {dest1}",
                "Hava Yolu": "AZAL / Qatar Airways",
                "Baqaj": baggage,
                "Qiymət": int(base_price)
            })
        else:
            back_date = (current + timedelta(days=duration)).strftime("%Y-%m-%d")
            results.append({
                "Gediş": go_date,
                "Dönüş": back_date,
                "Marşrut": f"{origin} ➔ {dest1} | {dest2} ➔ {origin}",
                "Hava Yolu": "Turkish Airlines / FlyDubai",
                "Baqaj": baggage,
                "Qiymət": int(base_price + 350)
            })
        current += timedelta(days=1)

    # Yalnız MAX 2 ən ucuz nəticəni göstər
    if results:
        df = pd.DataFrame(results).sort_values(by="Qiymət").head(2)
        st.success(f"✅ Sənin üçün ən sərfəli 2 variant:")
        
        for index, row in df.iterrows():
            with st.expander(f"Seçim {index+1}: {row['Qiymət']} AZN"):
                st.write(f"📍 **Marşrut:** {row['Marşrut']}")
                if mode != "Yalnız Gediş":
                    st.write(f"📅 **Tarixlər:** {row['Gediş']} - {row['Dönüş']}")
                else:
                    st.write(f"📅 **Tarix:** {row['Tarix']}")
                st.write(f"✈️ **Hava Yolu:** {row['Hava Yolu']}")
                st.write(f"🧳 **Yük:** {row['Baqaj']}")
                
                # Müştəriyə göndərmək üçün kopyalana bilən mətn
                copy_text = f"🔥 TƏKLİF: {row['Marşrut']} \n📅 {row.get('Gediş', row.get('Tarix'))} \n💰 Qiymət: {row['Qiymət']} AZN \n🧳 {row['Baqaj']}"
                st.code(copy_text, language="text")
    else:
        st.error("Təəssüf, seçilmiş aralıqda bilet tapılmadı.")

st.sidebar.markdown("---")
st.sidebar.info("Qiymətlər AZN (Manat) ilə göstərilir.")
