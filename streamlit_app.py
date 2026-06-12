import streamlit as st
import webbrowser

st.set_page_config(page_title="Travel Finder Pro", layout="centered")
st.title("✈️ Sürətli Tur Planlayıcı")

st.markdown("""
Bu panel sənə **İyul və Avqust** ayları üçün ən ucuz kombinasiyaları tapan platformalara birbaşa keçid verir. 
API qeydiyyatı ilə vaxt itirmədən, müştərin üçün ən ucuz 10 günü belə tapa bilərsən:
""")

col1, col2 = st.columns(2)
with col1:
    origin = st.text_input("Haradan? (Məs: GYD)", value="GYD").upper()
    dest1 = st.text_input("1-ci Şəhər (Məs: PEK)", value="PEK").upper()
with col2:
    days = st.number_input("Səyahət müddəti (Gün)", min_value=1, value=10)
    dest2 = st.text_input("2-ci Şəhər (Məs: SHA)", value="SHA").upper()

st.markdown("---")
st.subheader("Hansı ayda axtarış edək?")

def link_yarat(ay_kodu):
    # Bu funksiya avtomatik olaraq Google Flights-da 'Multi-city' və 'Flexible dates' linki yaradır
    url = f"https://google.com{dest1}%20from%20{origin}%20on%202024-{ay_kodu}-01%20through%202024-{ay_kodu}-20%20with%20{dest2}"
    return url

col_a, col_b = st.columns(2)
with col_a:
    if st.button("İyul Ayını Skan Et"):
        url = f"https://skyscanner.net{dest1.lower()}/240701/240731/?adults=1&children=0&infants=0&cabinclass=economy&rtn=1&preferdirects=false&outboundaltsenabled=false&inboundaltsenabled=false"
        st.write(f"🔗 [İyul üçün ən ucuz variantları burada gör]({url})")
        st.info("Açılan səhifədə 'Whole Month' (Bütün Ay) bölməsinə baxmağı unutma!")

with col_b:
    if st.button("Avqust Ayını Skan Et"):
        url = f"https://skyscanner.net{dest1.lower()}/240801/240831/?adults=1&children=0&infants=0&cabinclass=economy&rtn=1&preferdirects=false&outboundaltsenabled=false&inboundaltsenabled=false"
        st.write(f"🔗 [Avqust üçün ən ucuz variantları burada gör]({url})")

st.sidebar.warning("API Tokenləri ilə bağlı problem olduğu üçün bu 'Sürətli Keçid' sistemi sənin işini daha tez həll edəcək.")
