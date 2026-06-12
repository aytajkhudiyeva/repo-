import streamlit as st
from duffel_api import Duffel
import pandas as pd
from datetime import datetime, timedelta
import time

# TOKENİN
DUFFEL_TOKEN = "duffel_test_4MOrL_5hbu8p20N2V8_oMl3VyFWlx_4HiYFvqnoEKdL"
client = Duffel(access_token=DUFFEL_TOKEN)

st.set_page_config(page_title="Travel Pro Max - Full Scanner", layout="wide")
st.header("🔍 İyul-Avqust Gündəlik Tam Skaner")

# İNTERFEYS
col1, col2, col3 = st.columns(3)
with col1:
    origin = st.text_input("Haradan? (IATA)", value="GYD").upper()
with col2:
    city1 = st.text_input("1-ci Şəhər", value="PEK").upper()
    city2 = st.text_input("2-ci Şəhər", value="SHA").upper()
with col3:
    duration = st.number_input("Səyahət müddəti (Gün)", min_value=1, value=10)

if st.button("60 Günü Tək-Tək Yoxla (Tam Skan)"):
    all_results = []
    
    # İyulun 1-dən Avqustun 20-nə qədər hər günü tək-tək yoxlayırıq
    start_date = datetime(2024, 7, 1)
    end_date = datetime(2024, 8, 20)
    
    total_days = (end_date - start_date).days
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    current_date = start_date
    day_count = 0
    
    while current_date <= end_date:
        day_count += 1
        go_date = current_date.strftime("%Y-%m-%d")
        back_date = (current_date + timedelta(days=duration)).strftime("%Y-%m-%d")
        
        status_text.text(f"Yoxlanılır: {go_date} (Gediş) - {back_date} (Dönüş)")
        
        # Hər iki ssenarini yoxlayırıq
        scenarios = [{"go": city1, "back": city2}, {"go": city2, "back": city1}]
        
        for sc in scenarios:
            try:
                slices = [
                    {"origin": origin, "destination": sc["go"], "departure_date": go_date},
                    {"origin": sc["back"], "destination": origin, "departure_date": back_date}
                ]
                res = client.offer_requests.create().slices(slices).passengers([{"type": "adult"}]).execute()
                
                if res.offers:
                    best = min(res.offers, key=lambda x: float(x.total_amount))
                    all_results.append({
                        "Gediş": go_date,
                        "Dönüş": back_date,
                        "Marşrut": f"{sc['go']} ➔ {sc['back']}",
                        "Qiymət": float(best.total_amount),
                        "Valyuta": best.total_currency,
                        "Hava Yolu": best.owner.name
                    })
            except:
                continue
        
        # Proqress barı yeniləyirik
        progress_bar.progress(day_count / total_days if day_count < total_days else 1.0)
        current_date += timedelta(days=1) # HƏR GÜNÜ tək-tək yoxlayır
        
    if all_results:
        df = pd.DataFrame(all_results).sort_values(by="Qiymət")
        st.success(f"✅ Ümumi {len(all_results)} variant tapıldı!")
        
        # Ən ucuz 10 variantı böyük göstər
        st.subheader("🏆 Ən Ucuz 10 Seçim")
        st.dataframe(df.head(10), use_container_width=True)
        
        # Bütün nəticələri yükləmək üçün düymə
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Bütün siyahını yüklə (Excel/CSV)", csv, "ucuz_uclushlar.csv", "text/csv")
    else:
        st.error("Təəssüf ki, heç bir bilet tapılmadı.")
