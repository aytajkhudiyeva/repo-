import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Professional Travel Scanner", layout="wide")
st.header("🚀 Xüsusi Tarix Aralığı Skaneri")

# İNTERFEYS - PARAMETRLƏR
with st.sidebar:
    st.subheader("🔍 Axtarış Seçimləri")
    origin = st.text_input("Haradan? (IATA)", value="GYD").upper()
    city1 = st.text_input("1-ci Şəhər (Məs: PEK)", value="PEK").upper()
    city2 = st.text_input("2-ci Şəhər (Məs: SHA)", value="SHA").upper()
    
    st.markdown("---")
    # BURADA ARALIĞI SƏN SEÇİRSƏN
    start_date = st.date_input("Axtarış başlasın:", datetime(2024, 7, 1))
    end_date = st.date_input("Axtarış bitsin:", datetime(2024, 8, 31))
    duration = st.number_input("Səyahət müddəti (Gün)", min_value=1, value=10)

if st.button("Seçilmiş Aralıqda Ən Ucuz Tarixləri Tap"):
    if start_date >= end_date:
        st.error("Xəta: Başlanğıc tarixi bitiş tarixindən əvvəl olmalıdır!")
    else:
        st.info(f"🔎 {start_date} və {end_date} aralığı tək-tək skan edilir...")
        
        results = []
        current = start_date
        
        # Bütün aralığı tək-tək gəzirik
        while current <= (end_date - timedelta(days=duration)):
            go_date = current.strftime("%Y-%m-%d")
            back_date = (current + timedelta(days=duration)).strftime("%Y-%m-%d")
            
            # Sənin "Open-Jaw" məntiqin burada işləyir
            results.append({
                "Gediş Tarixi": go_date,
                "Qayıdış Tarixi": back_date,
                "Marşrut": f"{city1} ➔ {city2}",
                "Qiymət (USD)": 700 + (current.day * 2), # Bura API-dən real qiymət gələcək
                "Hava Yolu": "Qatar Airways"
            })
            current += timedelta(days=1) # HƏR GÜNÜ yoxlayır

        df = pd.DataFrame(results).sort_values(by="Qiymət (USD)")
        
        st.success(f"✅ Skan tamamlandı! {len(results)} kombinasiya müqayisə edildi.")
        st.subheader(f"🏆 {duration} günlük səfər üçün ən ucuz tarixlər:")
        st.dataframe(df.head(15), use_container_width=True) # Ən ucuz 15 günü göstərir

st.sidebar.info("Məsləhət: Aralığı çox geniş seçsəniz, skan bir az vaxt apara bilər.")
