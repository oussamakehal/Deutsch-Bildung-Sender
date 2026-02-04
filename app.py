import streamlit as st
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import time

# --- إعدادات الصفحة ---
st.set_page_config(page_title="German Sender Pro", page_icon="🇩🇪", layout="wide")

# --- التصميم (CSS) ---
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        background-color: #D32F2F;
        color: white;
        font-weight: bold;
        height: 60px;
    }
    .stTextInput>div>div>input {
        background-color: #1E1E1E;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# --- العنوان ---
st.title("🇩🇪 German Career Sender Pro (Web Version)")
st.markdown("### 🚀 أرسل طلبات العمل (Ausbildung) من المتصفح مباشرة")

# --- تقسيم الشاشة ---
col1, col2 = st.columns([1, 1])

with col1:
    st.info("🔐 معلومات الحساب")
    email_user = st.text_input("Gmail Address", placeholder="example@gmail.com")
    email_pass = st.text_input("App Password", type="password", help="الكود ديال 16 حرف")
    
    st.warning("✉️ محتوى الرسالة")
    subject = st.text_input("موضوع الرسالة (Betreff)")
    body = st.text_area("نص الرسالة (Anschreiben)", height=250)
    
    uploaded_files = st.file_uploader("📎 إرفاق ملفات (PDF, CV...)", accept_multiple_files=True)

with col2:
    st.success("👥 قائمة المستلمين")
    
    # خيار CSV أو يدوي
    input_method = st.radio("كيفاش بغيتي دخل الإيميلات؟", ["كتابة يدوية", "ملف CSV"])
    
    receivers_list = []
    
    if input_method == "ملف CSV":
        uploaded_csv = st.file_uploader("حط ملف CSV هنا", type=["csv"])
        if uploaded_csv:
            stringio = uploaded_csv.getvalue().decode("utf-8")
            for line in stringio.splitlines():
                if "@" in line:
                    receivers_list.append(line.strip())
            st.write(f"✅ تم تحميل {len(receivers_list)} إيميل.")
            
    else:
        manual_text = st.text_area("ألصق الإيميلات هنا (واحد فكل سطر)", height=150)
        for line in manual_text.splitlines():
            if "@" in line:
                receivers_list.append(line.strip())

    delay = st.slider("مدة الانتظار بين الرسائل (ثواني)", 5, 60, 10)
    
    # زر الإرسال
    if st.button("🚀 إرسال الآن (Start Sending)"):
        if not email_user or not email_pass:
            st.error("المرجو إدخال الإيميل والباسورد!")
        elif not receivers_list:
            st.error("لم يتم العثور على أي مستقبلين!")
        else:
            # عملية الإرسال
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(email_user, email_pass)
                
                success_count = 0
                
                for i, receiver in enumerate(receivers_list):
                    try:
                        msg = MIMEMultipart()
                        msg['From'] = email_user
                        msg['To'] = receiver
                        msg['Subject'] = subject
                        msg.attach(MIMEText(body, 'plain'))
                        
                        # المرفقات
                        if uploaded_files:
                            for uploaded_file in uploaded_files:
                                part = MIMEBase('application', "octet-stream")
                                part.set_payload(uploaded_file.getvalue())
                                encoders.encode_base64(part)
                                part.add_header('Content-Disposition', f'attachment; filename="{uploaded_file.name}"')
                                msg.attach(part)
                        
                        server.sendmail(email_user, receiver, msg.as_string())
                        success_count += 1
                        status_text.write(f"✅ تم الإرسال لـ: {receiver}")
                        
                        # تحديث البار
                        progress_bar.progress((i + 1) / len(receivers_list))
                        time.sleep(delay)
                        
                    except Exception as e:
                        st.error(f"فشل مع {receiver}: {e}")
                
                server.quit()
                st.balloons() # احتفال
                st.success(f"انتهت العملية! تم إرسال {success_count} رسالة بنجاح.")
                
            except Exception as e:
                st.error(f"خطأ في الاتصال: {e}")

# Footer
st.markdown("---")
st.markdown("Develop by YourName | Deutsch Bildung 2026")
