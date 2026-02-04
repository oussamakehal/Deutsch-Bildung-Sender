import streamlit as st
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import time

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Deutsch Bildung Sender Pro", page_icon="🇩🇪", layout="centered")

# --- 🎨 CSS: تصميم عصري ونظيف ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
    }

    /* توجيه العناوين لليمين (RTL) */
    .stTextInput label, .stTextArea label, .stSelectbox label, .stRadio label, .stFileUploader label, .stSlider label {
        text-align: right;
        direction: rtl;
        font-weight: bold;
        color: #FFC107;
    }
    
    .stMarkdown p {
        text-align: right;
        direction: rtl;
    }
    
    /* شكل الأزرار */
    div.stButton > button {
        width: 100%;
        background-color: #D32F2F;
        color: white;
        border-radius: 8px;
        height: 50px;
        font-weight: bold;
        font-size: 18px;
        border: none;
    }
    div.stButton > button:hover {
        background-color: #B71C1C;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 🟢 الهيدر (Header) مع واتساب و انستغرام ---
st.markdown("""
<div style="text-align: center; padding-bottom: 20px;">
    <h1 style="color: #333; font-size: 28px;">Deutsch Bildung Sender Pro 🇩🇪</h1>
    
    <a href="https://wa.me/212633991635" target="_blank" style="text-decoration: none;">
        <div style="background-color: #25D366; color: white; padding: 10px 25px; border-radius: 50px; display: inline-flex; align-items: center; gap: 10px; font-family: 'Cairo', sans-serif; font-weight: bold; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="white"><path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.206-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414z"/></svg>
            تواصل معي عبر WhatsApp
        </div>
    </a>

    <br> <a href="https://www.instagram.com/deutsch_bildung?igsh=bXQyeW9maGV0aWFp" target="_blank" style="text-decoration: none;">
        <div style="background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%); color: white; padding: 10px 25px; border-radius: 50px; display: inline-flex; align-items: center; gap: 10px; font-family: 'Cairo', sans-serif; font-weight: bold; margin-top: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="white"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.36-.2 6.78-2.618 6.98-6.98.058-1.28.072-1.689.072-4.948 0-3.259-.014-3.668-.072-4.948-.2-4.358-2.618-6.78-6.98-6.98-1.281-.059-1.689-.073-4.948-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.163 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
            تابعني على Instagram
        </div>
    </a>
</div>
""", unsafe_allow_html=True)

# --- 1. قسم معلومات الحساب ---
with st.container(border=True):
    st.markdown("### 🔐 معلومات الحساب")
    email_user = st.text_input("بريد Gmail الخاص بك", placeholder="example@gmail.com")
    email_pass = st.text_input("كود التطبيق (App Password)", type="password")
    
    with st.expander("❓ كيفاش تجيب App Password؟"):
        st.info("سير لـ Google Account > Security > 2-Step Verification > App Passwords")
        st.link_button("🔗 رابط سريع", "https://myaccount.google.com/apppasswords")

# --- 2. قسم الرسالة ---
with st.container(border=True):
    st.markdown("### ✉️ تفاصيل الرسالة")
    subject = st.text_input("موضوع الرسالة (Betreff)")
    body = st.text_area("نص الرسالة (Anschreiben)", height=200)
    uploaded_files = st.file_uploader("📎 إرفاق ملفات", accept_multiple_files=True)

# --- 3. قسم المستلمين ---
with st.container(border=True):
    st.markdown("### 👥 قائمة المستلمين")
    input_method = st.radio("طريقة الإدخال:", ["كتابة يدوية", "ملف CSV"], horizontal=True)
    
    receivers_list = []
    
    if input_method == "ملف CSV":
        uploaded_csv = st.file_uploader("حط ملف CSV هنا", type=["csv"])
        if uploaded_csv:
            stringio = uploaded_csv.getvalue().decode("utf-8")
            for line in stringio.splitlines():
                if "@" in line: receivers_list.append(line.strip())
            st.success(f"✅ {len(receivers_list)} إيميل")
    else:
        manual_text = st.text_area("الإيميلات (كل واحد فسطر)", height=100)
        for line in manual_text.splitlines():
            if "@" in line: receivers_list.append(line.strip())

    delay = st.slider("الانتظار (ثواني)", 5, 60, 10)

# --- 4. زر الإرسال ---
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🚀 إرسال الآن (Start Sending)"):
    if not email_user or not email_pass:
        st.error("المرجو إدخال المعلومات!")
    elif not receivers_list:
        st.error("ماكين حتى إيميل!")
    else:
        progress_text = "جاري الإرسال..."
        my_bar = st.progress(0, text=progress_text)
        status_area = st.empty()
        
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
                    
                    if uploaded_files:
                        for uploaded_file in uploaded_files:
                            part = MIMEBase('application', "octet-stream")
                            part.set_payload(uploaded_file.getvalue())
                            encoders.encode_base64(part)
                            part.add_header('Content-Disposition', f'attachment; filename="{uploaded_file.name}"')
                            msg.attach(part)
                    
                    server.sendmail(email_user, receiver, msg.as_string())
                    success_count += 1
                    status_area.success(f"✅ داز لـ: {receiver}")
                    my_bar.progress((i + 1) / len(receivers_list))
                    time.sleep(delay)
                    
                except Exception as e:
                    status_area.error(f"❌ مشكل مع {receiver}")
            
            server.quit()
            st.balloons()
            st.success(f"تم إرسال {success_count} رسالة!")
            
        except Exception as e:
            st.error(f"خطأ: {e}")

# Footer
st.markdown("""
    <div style="text-align: center; margin-top: 30px; color: #555; font-size: 12px;">
        Deutsch Bildung 2026 | By Oussama Kehal
    </div>
""", unsafe_allow_html=True)
