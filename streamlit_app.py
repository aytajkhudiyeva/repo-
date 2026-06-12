import streamlit as st
from duffel_api import Duffel
import pandas as pd
from datetime import datetime, timedelta

# TOKENİN
DUFFEL_TOKEN = "duffel_test_4MOrL_5hbu8p20N2V8_oMl3VyFWlx_4HiYFvqnoEKdL"
client = Duffel(access_token=DUFFEL_TOKEN)

st.set_page_config(page_title="Professional Travel Finder", layout="wide")
st.header("🚀 Xüsusi Tarix Aralığı Skaneri")

# İNTERFEYS - SEÇİMLƏR
with st.sidebar:
    st.subheader("🔍 Axtarış Parametrləri")
    origin = st.text_input("Haradan? (IATA)", value="GYD").upper()
    city1 = st.text_input("1-ci Təyinat", value="PEK").upper()
    city2 = st.text_input("2-ci Təyinat", value="SHA").upper()
    
    st.markdown("---")
    # BURADA TARİX ARALIĞINI SƏN SEÇİRSƏN
    start_search = st.date_input("Axtarış başlasın:", datetime(2024, 7, 1))
    end_search = st.date_input("Axtarış bitsin:", datetime(2024, 8, 31))
    
    duration = st.number_input("Səyahət müddəti (Gün)", min_value=1, value=10)

if st.button("Seçilmiş Aralıqda Ən Ucuzunu Tap"):
    if start_search >= end_search:
        st.error("Xəta: Başlanğıc tarixi bitiş tarixindən əvvəl olmalıdır!")
    else:
        all_results = []
        total_days = (end_search - start_search).days
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        current_date = start_search
        day_count = 0
        
        while current_date <= end_search:
            day_count += 1
            go_date = current_date.strftime("%Y-%m-%d")
            # Qayıdış tarixi gedişdən 'duration' qədər sonra
            back_date = (current_date + timedelta(days=duration)).strftime("%Y-%m-%d")
            
            status_text.text(f"Yoxlanılır: {go_date} - {back_date}")
            
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
            
            progress_bar.progress(day_count / (total_days + 1))
            current_date += timedelta(days=1)
            
        if all_results:
            df = pd.DataFrame(all_results).sort_values(by="Qiymət")
            st.success(f"✅ Ümumi {len(all_results)} variant yoxlanıldı və sıralandı!")
            st.subheader("🏆 Ən Ucuz 10 Variant")
            st.dataframe(df.head(10), use_container_width=True)
            
            # Siyahını yükləmək üçün
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Siyahını Excel kimi yüklə", csv, "travel_results.csv", "text/csv")
        else:
            st.error("Təəssüf, bilet tapılmadı.")
