import streamlit as st
from duffel_api import Duffel
import pandas as pd

# TOKENİ DƏQİQ BU SƏTİRƏ, DIRNAQ İÇİNDƏ YAZ:
DUFFEL_TOKEN = "duffel_test_4MOrL_5hbu8p20N2V8_oMl3VyFWlx_4HiYFvqnoEKdL"
client = Duffel(access_token=DUFFEL_TOKEN)

st.set_page_config(page_title="Travel Pro Panel", layout="centered")
st.header("✈️ Multi-City Uçuş Tapıcı")

# İnterfeys
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        origin = st.text_input("Haradan? (Məs: GYD)", value="GYD").upper()
        city1 = st.text_input("1-ci Şəhər (Məs: PEK)", value="PEK").upper()
    with col2:
        days = st.number_input("Səyahət müddəti (Gün)", min_value=1, value=7)
        city2 = st.text_input("2-ci Şəhər (Məs: SHA)", value="SHA").upper()

if st.button("Ən Ucuz Marşrutu Tap"):
    st.write("🔍 Axtarılır...")
    
    scenarios = [
        {"go": city1, "back": city2},
        {"go": city2, "back": city1}
    ]
    
    found_offers = []

    for sc in scenarios:
        try:
            slices = [
                {"origin": origin, "destination": sc["go"], "departure_date": "2024-07-15"},
                {"origin": sc["back"], "destination": origin, "departure_date": "2024-07-22"}
            ]
            
            res = client.offer_requests.create().slices(slices).passengers([{"type": "adult"}]).execute()
            
            if res.offers:
                best = min(res.offers, key=lambda x: float(x.total_amount))
                found_offers.append({
                    "Marşrut": f"{origin}➔{sc['go']} | {sc['back']}➔{origin}",
                    "Qiymət": f"{best.total_amount} {best.total_currency}",
                    "Aviaşirkət": best.owner.name
                })
        except Exception as e:
            continue

    if found_offers:
        st.success("Nəticələr:")
        st.table(pd.DataFrame(found_offers))
    else:
        st.error("Təəssüf, bilet tapılmadı. Tarixləri və ya IATA kodlarını yoxlayın.")
