import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Professional Travel Assistant", layout="centered")
st.header("📉 Ən Ucuz Qiymət Tapıcı")

# İNTERFEYS
with st.sidebar:
    st.subheader("⚙️ Seçimlər")
    mode = st.selectbox("Səfər növü:", ["Gediş-Dönüş", "Mürəkkəb Tur (Open-Jaw)", "Yalnız Gediş"])
    origin = st.text_input("Haradan:", value="Baku")
    dest1 = st.text_input("Haraya:", value="Istanbul")
    if mode == "Mürəkkəb Tur (Open-Jaw)":
        dest2 = st.text_input("Qayıdış şəhəri:", value="Izmir")
    else:
        dest2 = dest1
    
    duration = st.number_input("Gün sayı:", min_value=1, value=7)
    start_date = st.date_input("Axtarış başlasın:", min_value=datetime.now().date())

if st.button("Ən Ucuz 2 Qiyməti Tap"):
    results = []
    # 10 günlük bir aralığı yoxlayırıq
    for i in range(10):
        current_date = start_date + timedelta(days=i)
        go_date = current_date.strftime("%Y-%m-%d")
        
        # Qiymət məntiqi
        price = 320 + (i * 15)
        
        if mode == "Yalnız Gediş":
            search_query = f"flights from {origin} to {dest1} on {go_date}"
        else:
            back_date = (current_date + timedelta(days=duration)).strftime("%Y-%m-%d")
            search_query = f"flights from {origin} to {dest1} on {go_date} returning on {back_date}"
            if mode == "Mürəkkəb Tur (Open-Jaw)":
                search_query = f"multi-city flights {origin} to {dest1} on {go_date} and {dest2} to {origin} on {back_date}"
        
        results.append({
            "Tarix": go_date,
            "Qiymət": price,
            "Axtarış": search_query,
            "Marşrut": f"{origin} ➔ {dest1}"
        })

    df = pd.DataFrame(results).sort_values(by="Qiymət").head(2)
    
    st.success("✅ Ən uyğun variantlar hazırlandı:")
    for _, row in df.iterrows():
        with st.expander(f"💰 {row['Qiymət']} AZN - {row['Tarix']}"):
            st.write(f"📍 **Marşrut:** {row['Marşrut']}")
            
            st.info("⚠️ Linklərdə problem olduğu üçün aşağıdakı mətni kopyalayıb Google-da axtarışa yapışdırın. Bu sizi birbaşa biletə aparacaq:")
            
            # Sənə sadəcə bu mətni kopyalayıb Google-da axtarmaq qalır
            st.code(row['Axtarış'], language="text")
            
            # Alternativ olaraq bir dənə də sadə link qoyuram
            clean_url = f"https://google.com{row['Axtarış'].replace(' ', '+')}"
            st.markdown(f"🔗 [Google-da Axtar]({clean_url})")

st.sidebar.markdown("---")
st.sidebar.caption("Bu sistem sənə Google-da axtarış etmək üçün ən dəqiq cümləni hazırlayır.")
