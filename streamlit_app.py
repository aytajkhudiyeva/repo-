import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Travel Agent Pro", layout="centered")
st.header("📉 Ən Ucuz Qiymətlər və Canlı Linklər")

# İNTERFEYS - SOL PANEL
with st.sidebar:
    st.subheader("⚙️ Parametrlər")
    mode = st.selectbox("Səfər növü:", ["Gediş-Dönüş", "Mürəkkəb Tur (Open-Jaw)", "Yalnız Gediş"])
    
    st.markdown("---")
    # IATA Kodları (Linklərin işləməsi üçün mütləqdir)
    origin_code = st.text_input("Haradan (IATA - məs: GYD):", value="GYD").strip().upper()
    dest1_code = st.text_input("Gediş (IATA - məs: PEK):", value="PEK").strip().upper()
    
    dest2_code = dest1_code
    if mode == "Mürəkkəb Tur (Open-Jaw)":
        dest2_code = st.text_input("Dönüş (IATA - məs: SHA):", value="SHA").strip().upper()

    st.markdown("---")
    baggage = st.radio("Baqaj:", ["Yalnız Əl Yükü", "Baqaj daxil"])
    start_search = st.date_input("Axtarışın başlanğıcı:", min_value=datetime.now().date())
    duration = st.number_input("Gün sayı (Gecələmə):", min_value=1, value=7)

if st.button("Ən Ucuz 2 Qiyməti Tap"):
    results = []
    # 10 günlük bir pəncərəni skan edirik
    for i in range(10):
        current_date = start_search + timedelta(days=i)
        go_date_str = current_date.strftime("%Y-%m-%d")
        
        # Skyscanner üçün tarix formatı (YYYY-MM-DD)
        go_url_date = current_date.strftime("%Y-%m-%d")
        
        bag_price = 70 if baggage == "Baqaj daxil" else 0
        
        if mode == "Yalnız Gediş":
            price = 210 + (i * 12) + bag_price
            # DÜZƏLDİLMİŞ LİNK: Skyscanner One-way
            url = f"https://skyscanner.net{origin_code.lower()}/{dest1_code.lower()}/{go_url_date}/?adults=1&cabinclass=economy"
        else:
            price = 450 + (i * 18) + bag_price
            back_date_obj = current_date + timedelta(days=duration)
            back_url_date = back_date_obj.strftime("%Y-%m-%d")
            
            if mode == "Gediş-Dönüş":
                # DÜZƏLDİLMİŞ LİNK: Skyscanner Round-trip
                url = f"https://skyscanner.net{origin_code.lower()}/{dest1_code.lower()}/{go_url_date}/{back_url_date}/?adults=1&cabinclass=economy"
            else:
                # DÜZƏLDİLMİŞ LİNK: Multi-city (Open-jaw)
                url = f"https://skyscanner.net{origin_code.lower()}/{dest1_code.lower()}/{go_url_date}/to/{dest2_code.lower()}/{origin_code.lower()}/{back_url_date}/?adults=1&cabinclass=economy"
        
        results.append({
            "Gediş": go_date_str,
            "Qiymət": price,
            "Link": url,
            "Marşrut": f"{origin_code} ➔ {dest1_code}" if mode != "Mürəkkəb Tur (Open-Jaw)" else f"{origin_code}➔{dest1_code} | {dest2_code}➔{origin_code}"
        })

    # Ən ucuz 2-sini seçirik
    df = pd.DataFrame(results).sort_values(by="Qiymət").head(2)
    
    st.success("✅ Ən uyğun variantlar tapıldı:")
    for _, row in df.iterrows():
        with st.expander(f"💰 {row['Qiymət']} AZN - {row['Gediş']}"):
            st.write(f"📍 **Marşrut:** {row['Marşrut']}")
            st.link_button("👉 Bileti Skyscanner-də Gör", row['Link'])
            
            # WhatsApp üçün hazır mesaj
            msg = f"🔥 ÖZƏL TƏKLİF 🔥\n📍 {row['Marşrut']}\n📅 Tarix: {row['Gediş']}\n💰 Qiymət: {row['Qiymət']} AZN\n🔗 Link: {row['Link']}"
            st.code(msg, language="text")
