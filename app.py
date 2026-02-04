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

# --- 🎨 تصميم CSS احترافي (الزواق + العربية RTL) ---
st.markdown("""
<style>
    /* استيراد خط احترافي للعربية (Cairo) */
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');

    /* تطبيق الخط على كلشي */
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
    }

    /* 🛑 جعل العناوين والأسئلة محاذية لليمين (RTL) */
    .stTextInput label, .stTextArea label, .stSelectbox label, .stRadio label, .stFileUploader label, .stSlider label {
        width: 100%;
        text-align: right;
        direction: rtl;
        font-weight: bold;
        font-size: 18px;
        color: #FFC107; /* اللون الذهبي */
        margin-bottom: 5px;
    }

    /* النصوص التوضيحية (Help) تكون يمين */
    .stMarkdown p {
        text-align: right;
        direction: rtl;
    }

    /* ⬜ خانات الإدخال تبقى يسار (LTR) عشان الإيميلات والألمانية */
    .stTextInput input, .stTextArea textarea {
        direction: ltr;
        text-align: left;
        background-color: #1E1E1E;
        color: white;
        border: 1px solid #333;
        border-radius: 8px;
    }

    /* 🟥 زر الإرسال (تعديل الشكل) */
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #D32F2F, #B71C1C); /* تدرج أحمر */
        color: white;
        font-size: 20px;
        font-weight: bold;
        height: 60px;
        border-radius: 12px;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        transition: 0.3s;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 8px rgba(211, 47, 47, 0.4);
    }

    /* 📦 البطاقات (Cards) */
    div[data-testid="stVerticalBlock"] > div {
        background-color: #121212;
        border-radius: 15px;
        padding: 5px;
    }
    
    /* إخفاء القائمة الجانبية والقدم */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)

# --- 🟢 الهيدر (Header) مع واتساب ---
st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="color: white; font-size: 32px; margin-bottom: 5px;">Deutsch Bildung Sender Pro 🇩🇪</h1>
        <p style="color: gray; font-size: 14px; margin-bottom: 20px;">Professional Automated Email Tool</p>
        
        <a href="https://wa.me/212633991635" target="_blank" style="text-decoration: none;">
            <div style="
                background-color: #25D366; 
                color: white; 
                padding: 10px 25px; 
                border-radius: 50px; 
                display: inline-flex; 
                align-items: center; 
                gap: 10px; 
                font-family: 'Cairo', sans-serif;
                font-weight: bold;
                box-shadow: 0 4px 10px rgba(37, 211, 102, 0.3);
                transition: transform 0.2s;
            ">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="white"><path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.206-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414z"/></svg>
                تواصل معي: 0633991635
            </div>
        </a>
    </div>
    <hr style="border: 1px solid #333;">
""", unsafe_allow_html=True)

# --- 1. قسم معلومات الحساب ---
st.markdown("### 🔐 معلومات الحساب")
with st.container(border=True):
    email_user = st.text_input("بريد Gmail الخاص بك", placeholder="example@gmail.com")
    email_pass = st.text_input("كود التطبيق (App Password)", type="password", help="الكود المتكون من 16 حرف")
    
    with st.expander("❓ كيفاش تجيب App Password؟ (اضغط للمساعدة)"):
        st.markdown("""
        <div style="text-align: right; direction: rtl;">
        1. فعل التحقق بخطوتين (2FA) في جوجل.<br>
        2. ادخل للرابط لتحت.<br>
        3. اختر "Mail" و "Windows Computer".<br>
        4. اضغط Generate وانسخ الكود.
        </div>
        """, unsafe_allow_html=True)
        st.link_button("🔗 رابط Google App Passwords", "https://myaccount.google.com/apppasswords")

# --- 2. قسم الرسالة ---
st.markdown("### ✉️ تفاصيل الرسالة")
with st.container(border=True):
    subject = st.text_input("موضوع الرسالة (Betreff)")
    body = st.text_area("نص الرسالة (Anschreiben)", height=250, help="اكتب هنا النص بالألمانية")
    uploaded_files = st.file_uploader("📎 إرفاق ملفات (PDF, Lebenslauf...)", accept_multiple_files=True)

# --- 3. قسم المستلمين ---
st.markdown("### 👥 قائمة المستلمين")
with st.container(border=True):
    input_method = st.radio("كيفاش بغيتي دخل الإيميلات؟", ["كتابة يدوية", "ملف CSV"], horizontal=True)
    
    receivers_list = []
    
    if input_method == "ملف CSV":
        uploaded_csv = st.file_uploader("حط ملف CSV هنا", type=["csv"])
        if uploaded_csv:
            stringio = uploaded_csv.getvalue().decode("utf-8")
            for line in stringio.splitlines():
                if "@" in line:
                    receivers_list.append(line.strip())
            st.success(f"✅ تم تحميل {len(receivers_list)} إيميل.")
            
    else:
        manual_text = st.text_area("ألصق الإيميلات هنا (كل إيميل في سطر)", height=150, placeholder="email1@gmail.com\nemail2@gmail.com")
        for line in manual_text.splitlines():
            if "@" in line:
                receivers_list.append(line.strip())

    delay = st.slider("مدة الانتظار بين كل رسالة (ثواني)", 5, 120, 10)

# --- 4. زر الإرسال ---
st.markdown("---")
if st.button("🚀 إرسال الآن (Start Sending)"):
    if not email_user or not email_pass:
        st.error("المرجو إدخال الإيميل والباسورد!")
    elif not receivers_list:
        st.error("لم يتم العثور على أي مستقبلين!")
    else:
        # واجهة الإرسال
        progress_text = "جاري الإرسال... المرجو الانتظار"
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
                    
                    # تحديث الحالة
                    status_area.success(f"✅ تم الإرسال لـ: {receiver}")
                    my_bar.progress((i + 1) / len(receivers_list), text=f"تم إرسال {i+1} من {len(receivers_list)}")
                    
                    time.sleep(delay)
                    
                except Exception as e:
                    status_area.error(f"❌ فشل مع {receiver}: {e}")
            
            server.quit()
            my_bar.empty()
            st.balloons()
            st.success(f"🎉 انتهت المهمة! تم إرسال {success_count} رسالة بنجاح.")
            
        except Exception as e:
            st.error(f"خطأ في الاتصال: {e}")

# Footer بسيط
st.markdown("""
    <div style="text-align: center; margin-top: 50px; color: gray; font-size: 12px;">
        Develop by Oussama Kehal | Deutsch Bildung 2026
    </div>
""", unsafe_allow_html=True)
