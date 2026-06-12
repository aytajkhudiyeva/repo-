import streamlit as st
from duffel_api import Duffel
import pandas as pd
from datetime import timedelta

# TOKENİN
DUFFEL_TOKEN = "duffel_test_4MOrL_5hbu8p20N2V8_oMl3VyFWlx_4HiYFvqnoEKdL"
client = Duffel(access_token=DUFFEL_TOKEN)

st.set_page_config(page_title="Travel Pro Panel", layout="centered")
st.header("✈️ Ağıllı Marşrut Tapıcı")

# İNTERFEYS
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        origin = st.text_input("Haradan? (IATA)", value="GYD").upper()
        city1 = st.text_input("1-ci Şəhər", value="PEK").upper()
        # TARİX SEÇİMİ BURADADIR
        departure_date = st.date_input("Gediş Tarixi")
    with col2:
        days = st.number_input("Səfər müddəti (Gün)", min_value=1, value=7)
        city2 = st.text_input("2-ci Şəhər", value="SHA").upper()
        # Qayıdış tarixini avtomatik hesablayırıq
        return_date = departure_date + timedelta(days=days)
        st.write(f"Təxmini qayıdış: **{return_date}**")

if st.button("Ən Ucuz Qiyməti Tap"):
    st.info(f"🔍 {departure_date} tarixinə axtarılır...")
    
    scenarios = [
        {"go": city1, "back": city2},
        {"go": city2, "back": city1}
    ]
    
    found_offers = []

    for sc in scenarios:
        try:
            slices = [
                {"origin": origin, "destination": sc["go"], "departure_date": str(departure_date)},
                {"origin": sc["back"], "destination": origin, "departure_date": str(return_date)}
            ]
            
            res = client.offer_requests.create().slices(slices).passengers([{"type": "adult"}]).execute()
            
            if res.offers:
                best = min(res.offers, key=lambda x: float(x.total_amount))
                found_offers.append({
                    "Marşrut": f"{origin}➔{sc['go']} | {sc['back']}➔{origin}",
                    "Qiymət": f"{best.total_amount} {best.total_currency}",
                    "Aviaşirkət": best.owner.name
                })
        except:
            continue

    if found_offers:
        st.success("Nəticələr tapıldı!")
        st.table(pd.DataFrame(found_offers))
    else:
        st.error("Bu tarixlərdə bilet tapılmadı. Zəhmət olmasa başqa tarixlə yoxla.")
