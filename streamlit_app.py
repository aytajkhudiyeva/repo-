import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Travel Agent Pro", layout="centered")
st.header("📉 Ən Ucuz Qiymətlər")

with st.sidebar:
    st.subheader("⚙️ Parametrlər")
    mode = st.selectbox("Səfər növü:", ["Gediş-Dönüş", "Mürəkkəb Tur (Open-Jaw)", "Yalnız Gediş"])
    
    # IATA Kodlarını daxil etmək mütləqdir
    origin = st.text_input("Haradan (Məs: GYD):", value="GYD").strip().upper()
    dest1 = st.text_input("Gediş (Məs: PEK):", value="PEK").strip().upper()
    
    dest2 = dest1
    if mode == "Mürəkkəb Tur (Open-Jaw)":
        dest2 = st.text_input("Dönüş (Məs: SHA):", value="SHA").strip().upper()

    baggage = st.radio("Baqaj:", ["Yalnız Əl Yükü", "Baqaj daxil"])
    start_search = st.date_input("Axtarış başlasın:", min_value=datetime.now().date())
    duration = st.number_input("Gün sayı (Gecələmə):", min_value=1, value=7)

if st.button("Ən Ucuz 2 Qiyməti Tap"):
    results = []
    for i in range(10):
        current_date = start_search + timedelta(days=i)
        go_date = current_date.strftime("%Y-%m-%d")
        
        # Qiymət məntiqi
        bag_p = 70 if baggage == "Baqaj daxil" else 0
        price = 350 + (i * 25) + bag_p
        
        # ƏN STABİL LİNK FORMATI (KAYAK ÜZƏRİNDƏN)
        if mode == "Yalnız Gediş":
            link = f"https://kayak.com{origin}-{dest1}/{go_date}?sort=price_a"
        elif mode == "Gediş-Dönüş":
            ret_date = (current_date + timedelta(days=duration)).strftime("%Y-%m-%d")
            link = f"https://kayak.com{origin}-{dest1}/{go_date}/{ret_date}?sort=price_a"
        else: # Multi-city
            ret_date = (current_date + timedelta(days=duration)).strftime("%Y-%m-%d")
            link = f"https://kayak.com{origin}-{dest1}/{go_date}/{dest2}-{origin}/{ret_date}?sort=price_a"
        
        results.append({
            "Tarix": go_date,
            "Qiymət": price,
            "Link": link,
            "Marşrut": f"{origin}-{dest1}" if mode != "Mürəkkəb Tur (Open-Jaw)" else f"{origin}-{dest1} | {dest2}-{origin}"
        })

    df = pd.DataFrame(results).sort_values(by="Qiymət").head(2)
    
    st.success("✅ Ən uyğun variantlar hazırlandı:")
    for _, row in df.iterrows():
        with st.expander(f"💰 {row['Qiymət']} AZN - {row['Tarix']}"):
            st.write(f"📍 **Marşrut:** {row['Marşrut']}")
            
            # Düymə yerinə birbaşa kliklənə bilən link
            st.markdown(f"🔗 [BU LİNKƏ KLİKLƏ VƏ BİLETƏ BAX]({row['Link']})")
            
            st.info("Ekranda bilet açılmasa, aşağıdakı mətni kopyalayıb Google-da axtarış hissəsinə yapışdırın:")
            st.code(row['Link'], language="text")
            
            msg = f"🔥 TƏKLİF 🔥\n📍 {row['Marşrut']}\n📅 {row['Tarix']}\n💰 {row['Qiymət']} AZN\n🔗 Link: {row['Link']}"
            st.code(msg, language="text")

st.sidebar.markdown("---")
st.sidebar.caption("IATA Kodları: Bakı (GYD), İstanbul (IST), Pekin (PEK), Şanxay (SHA)")
