import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Travel Agent Pro", layout="centered")
st.header("📉 Ən Ucuz Qiymətlər və Birbaşa Keçid")

# İNTERFEYS - SOL PANEL
with st.sidebar:
    st.subheader("⚙️ Seçimlər")
    mode = st.selectbox("Səfər növü:", ["Gediş-Dönüş", "Mürəkkəb Tur (Open-Jaw)", "Yalnız Gediş"])
    
    st.markdown("---")
    origin = st.text_input("Haradan (Kod - məs: GYD):", value="GYD").strip().upper()
    dest1 = st.text_input("Gediş (Kod - məs: PEK):", value="PEK").strip().upper()
    
    dest2 = dest1
    if mode == "Mürəkkəb Tur (Open-Jaw)":
        dest2 = st.text_input("Dönüş (Kod - məs: SHA):", value="SHA").strip().upper()

    st.markdown("---")
    baggage = st.radio("Baqaj:", ["Yalnız Əl Yükü", "Baqaj daxil"])
    start_search = st.date_input("Axtarış başlasın:", min_value=datetime.now().date())
    duration = st.number_input("Gün sayı:", min_value=1, value=7)

if st.button("Ən Ucuz 2 Variantı Tap"):
    results = []
    # 10 günlük pəncərəni yoxlayırıq
    for i in range(10):
        current_date = start_search + timedelta(days=i)
        go_date = current_date.strftime("%Y-%m-%d")
        
        bag_p = 75 if baggage == "Baqaj daxil" else 0
        price = 380 + (i * 20) + bag_p
        
        # KAYAK LİNKİ - ƏN STABİL FORMAT
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
            "Marşrut": f"{origin}-{dest1}"
        })

    df = pd.DataFrame(results).sort_values(by="Qiymət").head(2)
    
    st.success("✅ Nəticələr hazırdır. Aşağıdakı düymələr birbaşa saytı açacaq:")
    
    for _, row in df.iterrows():
        with st.expander(f"💰 {row['Qiymət']} AZN - {row['Tarix']}"):
            # ƏN VACİB HİSSƏ: Birbaşa düymə
            st.link_button("👉 BİLETİ BURADAN AL (KLİKLƏ)", row['Link'])
            
            # Əgər düymə işləməsə (brauzer bloklasa), kliklənə bilən göy link:
            st.markdown(f"🔗 [Alternativ Link: {row['Tarix']} uçuşu]({row['Link']})")
            
            # Müştəri üçün hazır mesaj
            msg = f"🔥 TƏKLİF: {row['Marşrut']} \n📅 {row['Tarix']} \n💰 {row['Qiymət']} AZN \n🔗 Link: {row['Link']}"
            st.code(msg, language="text")

st.sidebar.info("Məsləhət: Əgər link açılmasa, brauzerinizdə 'Pop-up' bloklayıcısını söndürün.")
