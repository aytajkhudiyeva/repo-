import streamlit as st
from duffel_api import Duffel
from datetime import datetime, timedelta

# TOKENİN
DUFFEL_TOKEN = "duffel_test_4MOrL_5hbu8p20N2V8_oMl3VyFWlx_4HiYFvqnoEKdL"
client = Duffel(access_token=DUFFEL_TOKEN)

st.set_page_config(page_title="Travel Agent Pro", layout="wide")
st.title("✈️ Uçuş Arama Paneli")

# Sol Panel (Sidebar)
with st.sidebar:
    st.header("Arama Ayarları")
    origin = st.text_input("Nereden? (IATA)", value="LHR").upper()
    dest1 = st.text_input("1. Şehir", value="JFK").upper()
    dest2 = st.text_input("2. Şehir", value="DXB").upper()
    
    start_date = st.date_input("Arama Başlangıç", datetime.now() + timedelta(days=14))
    end_date = st.date_input("Arama Bitiş", datetime.now() + timedelta(days=21))
    duration = st.number_input("Kalınacak Gün", min_value=1, value=7)

if st.button("En Ucuz Bileti Ara"):
    st.info("Sistem taranıyor, lütfen bekleyin...")
    
    all_results = []
    current_date = start_date
    
    while current_date <= end_date:
        # Tarihi tam olarak Duffel'ın istediği formatta yazıyoruz (YYYY-MM-DD)
        go_date = current_date.strftime("%Y-%m-%d")
        back_date = (current_date + timedelta(days=duration)).strftime("%Y-%m-%d")
        
        # Test modunda her iki şehri de kontrol ediyoruz
        for destination in [dest1, dest2]:
            try:
                # Duffel API'ye en basit sorguyu gönderiyoruz
                offer_request = client.offer_requests.create().slices([
                    {"origin": origin, "destination": destination, "departure_date": go_date},
                    {"origin": destination, "destination": origin, "departure_date": back_date}
                ]).passengers([{"type": "adult"}]).execute()

                if offer_request.offers:
                    best = min(offer_request.offers, key=lambda x: float(x.total_amount))
                    all_results.append({
                        "Tarih": go_date,
                        "Dönüş": back_date,
                        "Ruta": f"{origin} ➔ {destination}",
                        "Fiyat": f"{best.total_amount} {best.total_currency}",
                        "Havayolu": best.owner.name
                    })
            except Exception as e:
                continue
        
        current_date += timedelta(days=1)

    if all_results:
        st.success(f"{len(all_results)} adet seçenek bulundu!")
        st.table(all_results)
    else:
        st.error("Hala bilet bulunamadı. Lütfen Duffel Dashboard'dan 'Test Mode'un açık olduğundan emin ol.")

st.warning("Not: Eğer bilet çıkmazsa, Duffel Dashboard'da 'Duffel Airways'in aktif olup olmadığını kontrol et.")
