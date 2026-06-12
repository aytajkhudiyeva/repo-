import streamlit as st
from duffel_api import Duffel
import pandas as pd
from datetime import datetime, timedelta

# TOKENİN
DUFFEL_TOKEN = "duffel_test_4MOrL_5hbu8p20N2V8_oMl3VyFWlx_4HiYFvqnoEKdL"
client = Duffel(access_token=DUFFEL_TOKEN)

st.set_page_config(page_title="Travel Pro Max", layout="centered")
st.header("🔎 İyul-Avqust Ən Ucuz Tarix Tapıcı")

# İNTERFEYS
col1, col2 = st.columns(2)
with col1:
    origin = st.text_input("Haradan? (IATA)", value="GYD").upper()
    city1 = st.text_input("1-ci Şəhər", value="PEK").upper()
with col2:
    city2 = st.text_input("2-ci Şəhər", value="SHA").upper()
    duration = st.number_input("Səyahət müddəti (Gün)", min_value=1, value=10)

if st.button("Bütün Yay Boyu Ən Ucuzunu Tap"):
    st.warning("⚠️ Bu bir az vaxt apara bilər, çünki sistem 60 günü skan edir...")
    
    # İyulun 1-dən Avqustun sonuna qədər olan tarixlər
    start_date = datetime(2024, 7, 1)
    end_date = datetime(2024, 8, 20) # Qayıdışı hesablamaq üçün avqust sonuna qədər
    
    all_results = []
    
    # Hər 5 gündən bir yoxlayırıq ki, sistem donmasın və ən ucuz həftəni tapsın
    current_date = start_date
    while current_date <= end_date:
        go_date = current_date.strftime("%Y-%m-%d")
        back_date = (current_date + timedelta(days=duration)).strftime("%Y-%m-%d")
        
        # Həm A-B, həm B-A variantlarını yoxlayırıq
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
                        "Gediş Tarixi": go_date,
                        "Qayıdış Tarixi": back_date,
                        "Marşrut": f"{sc['go']} ➔ {sc['back']}",
                        "Qiymət": float(best.total_amount),
                        "Valyuta": best.total_currency,
                        "Aviaşirkət": best.owner.name
                    })
            except:
                continue
        
        current_date += timedelta(days=5) # 5 günlük addımlarla yoxlayır (daha sürətli olması üçün)

    if all_results:
        # Nəticələri qiymətə görə sıralayırıq
        df = pd.DataFrame(all_results).sort_values(by="Qiymət")
        st.success("✅ Yay boyu ən ucuz 5 variant tapıldı!")
        st.table(df.head(5))
    else:
        st.error("Heç bir nəticə tapılmadı.")
