import streamlit as st
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import time

# --- 🛑 لائحة المشتركين (VIP List) 🛑 ---
AUTHORIZED_USERS = [
    "oussama.kehal@gmail.com",
    "rajae.bertali.1997@gmail.com",
    "client1@gmail.com"
]

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Deutsch Bildung Sender Pro", page_icon="🇩🇪", layout="centered")

# --- 🎨 CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
html, body, [class*="css"] {font-family: 'Cairo', sans-serif;}
.stTextInput label, .stTextArea label, .stSelectbox label, .stRadio label, .stFileUploader label, .stSlider label {
text-align: right; direction: rtl; font-weight: bold; color: #FFC107;}
.stMarkdown p {text-align: right; direction: rtl;}
div.stButton > button {width: 100%; border-radius: 8px; height: 50px; font-weight: bold; font-size: 18px; border: none;}
div[data-testid="stButton"] button:first-child {background-color: #D32F2F; color: white;}
div[data-testid="stButton"] button:first-child:hover {background-color: #B71C1C;}
.result-card-success {background-color: #1E1E1E; border-left: 6px solid #25D366; padding: 12px; border-radius: 8px; margin-bottom: 8px; display: flex; align-items: center; box-shadow: 0 2px 4px rgba(0,0,0,0.2);}
.result-card-fail {background-color: #1E1E1E; border-left: 6px solid #FF0000; padding: 12px; border-radius: 8px; margin-bottom: 8px; display: flex; align-items: center; box-shadow: 0 2px 4px rgba(0,0,0,0.2);}
.email-text {color: white; font-family: monospace; font-size: 16px; margin-left: 15px; flex-grow: 1;}
.status-icon {font-size: 20px;}
#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 🟢 الهيدر (Header) الكامل (بدون مسافات لتفادي الخطأ) ---
st.markdown("""
<div style="text-align: center; padding-bottom: 10px;">
<h1 style="color: #333; font-size: 30px; font-weight: 800; margin-bottom: 15px;">Deutsch Bildung Sender Pro 🇩🇪</h1>
<div style="display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; margin-bottom: 20px;">
<a href="https://wa.me/212633991635" target="_blank" style="text-decoration: none;">
<div style="background-color: #25D366; color: white; padding: 8px 20px; border-radius: 50px; display: flex; align-items: center; gap: 8px; font-weight: bold; font-size: 14px; box-shadow: 0 3px 6px rgba(0,0,0,0.1);">WhatsApp 💬</div>
</a>
<a href="https://www.instagram.com/deutsch_bildung?igsh=bXQyeW9maGV0aWFp" target="_blank" style="text-decoration: none;">
<div style="background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%); color: white; padding: 8px 20px; border-radius: 50px; display: flex; align-items: center; gap: 8px; font-weight: bold; font-size: 14px; box-shadow: 0 3px 6px rgba(0,0,0,0.1);">Instagram 📸</div>
</a>
<a href="mailto:deutschbildung.de@gmail.com" target="_blank" style="text-decoration: none;">
<div style="background-color: #EA4335; color: white; padding: 8px 20px; border-radius: 50px; display: flex; align-items: center; gap: 8px; font-weight: bold; font-size: 14px; box-shadow: 0 3px 6px rgba(0,0,0,0.1);">Email 📧</div>
</a>
</div>
<div style="background-color: #fff3cd; border: 1px solid #ffeeba; border-radius: 12px; padding: 15px; margin-bottom: 20px; color: #856404;">
<p style="font-size: 16px; margin: 0; font-weight: bold; text-align: center; direction: rtl;">
⚠️ تنبيه هام: النسخة المجانية كتمكنك تصيفط لـ 3 ديال الشركات فقط للتجربة.<br>
باش تفتح النسخة الكاملة (Unlimited) تواصل معنا عبر واتساب.
</p>
</div>
<div style="background-color: #f8f9fa; border: 1px solid #e9ecef; border-radius: 12px; padding: 15px; margin-bottom: 25px; box-shadow: 0 4px 10px rgba(0,0,0,0.03);">
<p style="font-size: 16px; color: #444; margin-bottom: 10px; line-height: 1.6; text-align: right; direction: rtl;">
<b>إذا واجهتك أي مشكلة فالبوت، تواصل معنا فوراً عبر واتساب، إنستغرام أو الإيميل 🛠️</b>
</p>
<hr style="border: 0; border-top: 1px solid #ddd; margin: 10px 0;">
<ul style="list-style-type: none; padding: 0; margin: 0; color: #333; font-size: 14px; line-height: 2; text-align: right; direction: rtl;">
<li>✅ كنعاونوك كذلك فكل ما يخص اللغة الألمانية، الفيزا، وإنشاء ملف احترافي للتكوين المهني.</li>
<li>👥 فريقنا مكوّن من أكثر من 20 شخص وعندنا 5 سنوات خبرة فعلية وحلّينا مئات الملفات بنجاح.</li>
<li>🚀 خدمتنا سريعة، واضحة وبدون صداع.</li>
</ul>
</div>
</div>
""", unsafe_allow_html=True)

# --- 1. معلومات الحساب ---
with st.container(border=True):
    st.markdown("### 🔐 معلومات الحساب")
    email_user = st.text_input("بريد Gmail الخاص بك", placeholder="example@gmail.com")
    email_pass = st.text_input("كود التطبيق (App Password)", type="password")
    
    if st.button("تجربة الاتصال (Test Connection) 🔌"):
        if not email_user or not email_pass:
            st.error("المرجو إدخال الإيميل والباسورد أولاً!")
        else:
            try:
                with st.spinner("جاري التحقق..."):
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(email_user, email_pass)
                    server.quit()
                st.success("✅ متصل بنجاح! المعلومات صحيحة.")
            except Exception as e:
                st.error(f"❌ خطأ! تأكد من الإيميل أو App Password.")

    with st.expander("❓ كيفاش تجيب App Password؟"):
        st.info("سير لـ Google Account > Security > 2-Step Verification > App Passwords")
        st.link_button("🔗 رابط سريع", "https://myaccount.google.com/apppasswords")

# --- 2. الرسالة ---
with st.container(border=True):
    st.markdown("### ✉️ تفاصيل الرسالة")
    subject = st.text_input("موضوع الرسالة (Betreff)")
    body = st.text_area("نص الرسالة (Anschreiben)", height=200)
    uploaded_files = st.file_uploader("📎 إرفاق ملفات", accept_multiple_files=True)

# --- 3. المستلمين ---
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

# --- 4. الإرسال (مع منطق الحماية) ---
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🚀 إرسال الآن (Start Sending)"):
    if not email_user or not email_pass:
        st.error("المرجو إدخال المعلومات!")
    elif not receivers_list:
        st.error("ماكين حتى إيميل!")
    else:
        # 🛡️ التحقق من الاشتراك
        is_premium = email_user.strip() in AUTHORIZED_USERS
        limit = 3
        
        final_list = receivers_list
        limit_reached = False
        
        if not is_premium and len(receivers_list) > limit:
            final_list = receivers_list[:limit]
            limit_reached = True

        st.markdown("### 📡 تقرير الإرسال المباشر (Live Status)")
        progress_bar = st.progress(0)
        results_container = st.container()
        
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email_user, email_pass)
            success_count = 0
            
            for i, receiver in enumerate(final_list):
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
                    with results_container:
                        st.markdown(f"""<div class="result-card-success"><span class="status-icon">✅</span><span class="email-text">{receiver}</span></div>""", unsafe_allow_html=True)
                    progress_bar.progress((i + 1) / len(final_list))
                    time.sleep(delay)
                except Exception as e:
                    with results_container:
                        st.markdown(f"""<div class="result-card-fail"><span class="status-icon">❌</span><span class="email-text">{receiver}</span></div>""", unsafe_allow_html=True)
            
            server.quit()
            
            if limit_reached:
                st.error("🛑 توقف الإرسال! لقد تجاوزت الحد المسموح به في النسخة المجانية (3 إيميلات).")
                st.markdown(f"""
                <div style="background-color: #ffcccc; border: 2px solid #ff0000; padding: 20px; border-radius: 10px; text-align: center; direction: rtl;">
                    <h3 style="color: #cc0000;">⚠️ تفعيل النسخة الكاملة مطلوب</h3>
                    <p style="font-size: 18px; color: #333;">لقد قمت بإرسال 3 رسائل تجريبية بنجاح.</p>
                    <p style="font-size: 18px; color: #333;">لإرسال عدد غير محدود، يرجى تفعيل حسابك.</p>
                    <a href="https://wa.me/212633991635" target="_blank" style="text-decoration: none;">
                        <div style="background-color: #25D366; color: white; padding: 10px 20px; border-radius: 5px; display: inline-block; font-weight: bold; margin-top: 10px;">
                            تواصل معنا لتفعيل الحساب: 0633991635
                        </div>
                    </a>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.balloons()
                st.success(f"انتهت العملية! {success_count} / {len(final_list)} ناجح.")
                
        except Exception as e:
            st.error(f"خطأ في الاتصال: {e}")

st.markdown("""<div style="text-align: center; margin-top: 30px; color: #555; font-size: 12px;">Deutsch Bildung 2026 | By Oussama Kehal</div>""", unsafe_allow_html=True)
