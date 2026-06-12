import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Travel Agent Pro", layout="centered")
st.header("📉 Ən Ucuz Qiymət və Canlı Linklər")

# İNTERFEYS - SOL PANEL
with st.sidebar:
    st.subheader("⚙️ Parametrlər")
    mode = st.selectbox("Səfər növü:", ["Gediş-Dönüş", "Mürəkkəb Tur (Open-Jaw)", "Yalnız Gediş"])
    
    # Şəhər adları (Vizual üçün)
    origin_name = st.text_input("Haradan (Şəhər):", value="Bakı")
    dest_name = st.text_input("Haraya (Şəhər):", value="Pekin")
    
    st.markdown("---")
    # IATA Kodları (Linklərin işləməsi üçün mütləqdir)
    origin_code = st.text_input("Haradan (Kod - məs: GYD):", value="GYD").upper()
    dest1_code = st.text_input("Gediş (Kod - məs: PEK):", value="PEK").upper()
    
    dest2_code = dest1_code
    if mode == "Mürəkkəb Tur (Open-Jaw)":
        dest2_code = st.text_input("Dönüş (Kod - məs: SHA):", value="SHA").upper()

    st.markdown("---")
    baggage = st.radio("Baqaj:", ["Yalnız Əl Yükü", "Baqaj daxil"])
    start_search = st.date_input("Başlanğıc:", min_value=datetime.now().date())
    duration = st.number_input("Gün sayı:", min_value=1, value=7)

if st.button("Ən Ucuz 2 Qiyməti Tap"):
    results = []
    # Test üçün 10 günü skan edirik
    for i in range(10):
        current_date = start_search + timedelta(days=i)
        go_date = current_date.strftime("%Y-%m-%d")
        go_link_date = current_date.strftime("%y%m%d") # Skyscanner formatı: YYMMDD
        
        bag_price = 70 if baggage == "Baqaj daxil" else 0
        
        if mode == "Yalnız Gediş":
            price = 210 + (i * 15) + bag_price
            # Skyscanner One-way link
            url = f"https://skyscanner.net{origin_code.lower()}/{dest1_code.lower()}/{go_link_date}/?adults=1&cabinclass=economy"
        else:
            price = 450 + (i * 20) + bag_price
            back_date_obj = current_date + timedelta(days=duration)
            back_link_date = back_date_obj.strftime("%y%m%d")
            
            if mode == "Gediş-Dönüş":
                # Skyscanner Round-trip link
                url = f"https://skyscanner.net{origin_code.lower()}/{dest1_code.lower()}/{go_link_date}/{back_link_date}/?adults=1&cabinclass=economy"
            else:
                # Open-jaw üçün Multi-city axtarış səhifəsinə yönləndirmə
                url = f"https://skyscanner.net{origin_code.lower()}/{dest1_code.lower()}/{go_link_date}/to/{dest2_code.lower()}/{origin_code.lower()}/{back_link_date}/?adults=1&cabinclass=economy"
        
        results.append({
            "Gediş": go_date,
            "Qiymət": price,
            "Link": url,
            "Marşrut": f"{origin_code} ➔ {dest1_code}" if mode != "Mürəkkəb Tur" else f"{origin_code}➔{dest1_code} | {dest2_code}➔{origin_code}"
        })

    df = pd.DataFrame(results).sort_values(by="Qiymət").head(2)
    
    st.success("✅ Ən uyğun variantlar hazırlandı:")
    for _, row in df.iterrows():
        with st.expander(f"💰 {row['Qiymət']} AZN - {row['Gediş']}"):
            st.write(f"📍 **Marşrut:** {row['Marşrut']}")
            # Link düyməsi
            st.link_button("✈️ Bileti Skyscanner-də Gör", row['Link'])
            
            # Kopyalamaq üçün
            msg = f"🔥 TƏKLİF: {row['Marşrut']}\n📅 Tarix: {row['Gediş']}\n💰 Qiymət: {row['Qiymət']} AZN\n🔗 Link: {row['Link']}"
            st.code(msg, language="text")
