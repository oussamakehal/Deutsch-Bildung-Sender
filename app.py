import streamlit as st
import smtplib
import os
import json
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import time

# --- 🛑 لائحة المشتركين (VIP List) 🛑 ---
AUTHORIZED_USERS = [
    "oussama.kehal@gmail.com",
    "deutschbildung.de@gmail.com",
    "rajae.bertali.1997@gmail.com",
    "client1@gmail.com"
]

# --- 📁 إعدادات الذاكرة (JSON) ---
LOG_FILE = "daily_limit_log.json"

def get_user_quota(email, is_vip):
    today_str = datetime.date.today().isoformat()
    limit = 300 if is_vip else 3
    if not os.path.exists(LOG_FILE):
        return 0, limit
    try:
        with open(LOG_FILE, "r") as f:
            data = json.load(f)
    except:
        return 0, limit
    user_data = data.get(email, {})
    if user_data.get("date") != today_str:
        return 0, limit
    return user_data.get("count", 0), limit

def update_user_quota(email):
    today_str = datetime.date.today().isoformat()
    data = {}
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                data = json.load(f)
        except:
            data = {}
    user_data = data.get(email, {})
    if user_data.get("date") != today_str:
        new_count = 1
    else:
        new_count = user_data.get("count", 0) + 1
    data[email] = {"date": today_str, "count": new_count}
    with open(LOG_FILE, "w") as f:
        json.dump(data, f)

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

# --- 🟢 الهيدر (Header) ---
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
    col1, col2 = st.columns([3, 1])
    with col1:
        email_user = st.text_input("بريد Gmail الخاص بك", placeholder="example@gmail.com")
        email_pass = st.text_input("كود التطبيق (App Password)", type="password")
    with col2:
        if email_user:
            is_vip = email_user.strip() in AUTHORIZED_USERS
            current_count, limit = get_user_quota(email_user.strip(), is_vip)
            color = "#28a745"
            if current_count >= limit: color = "#dc3545"
            elif current_count >= limit * 0.8: color = "#ffc107"
            st.markdown(f"""
            <div style="background-color: {color}; color: white; padding: 10px; border-radius: 10px; text-align: center; margin-top: 28px; box-shadow: 0 2px 5px rgba(0,0,0,0.2);">
                <div style="font-size: 12px;">رصيد اليوم</div>
                <div style="font-size: 24px; font-weight: bold;">{current_count}/{limit}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
             st.markdown("""
            <div style="background-color: #6c757d; color: white; padding: 10px; border-radius: 10px; text-align: center; margin-top: 28px;">
                <div style="font-size: 12px;">الرصيد</div>
                <div style="font-size: 24px; font-weight: bold;">--/--</div>
            </div>
            """, unsafe_allow_html=True)
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

# --- 4. الإرسال ---
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🚀 إرسال الآن (Start Sending)"):
    if not email_user or not email_pass:
        st.error("المرجو إدخال المعلومات!")
    elif not receivers_list:
        st.error("ماكين حتى إيميل!")
    else:
        is_premium = email_user.strip() in AUTHORIZED_USERS
        current_count, limit = get_user_quota(email_user.strip(), is_premium)
        remaining = limit - current_count
        if remaining < 0: remaining = 0
        final_list = receivers_list
        limit_reached_before_start = (remaining == 0)
        if len(receivers_list) > remaining:
            final_list = receivers_list[:remaining]

        if limit_reached_before_start:
             st.error(f"🛑 لقد استهلكت رصيدك اليومي ({limit} رسالة)!")
             if not is_premium:
                 st.markdown(f"""
                    <div style="background-color: #ffcccc; border: 2px solid #ff0000; padding: 20px; border-radius: 10px; text-align: center; direction: rtl;">
                        <h3 style="color: #cc0000;">⚠️ تفعيل النسخة الكاملة مطلوب</h3>
                        <p style="font-size: 18px; color: #333;">لقد استنفذت الـ 3 رسائل المجانية لهذا اليوم.</p>
                        <p style="font-size: 18px; color: #333;">الرصيد سيتجدد تلقائياً عند منتصف الليل، أو تواصل معنا للترقية.</p>
                        <a href="https://wa.me/212633991635" target="_blank" style="text-decoration: none;">
                            <div style="background-color: #25D366; color: white; padding: 10px 20px; border-radius: 5px; display: inline-block; font-weight: bold; margin-top: 10px;">
                                ترقية الحساب: 0633991635
                            </div>
                        </a>
                    </div>
                    """, unsafe_allow_html=True)
             else:
                 st.warning("⚠️ لقد وصلت للحد الأقصى المسموح به من Google (300 رسالة) لهذا اليوم.")
        else:
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
                        update_user_quota(email_user.strip())
                        with results_container:
                            st.markdown(f"""<div class="result-card-success"><span class="status-icon">✅</span><span class="email-text">{receiver}</span></div>""", unsafe_allow_html=True)
                        progress_bar.progress((i + 1) / len(final_list))
                        time.sleep(delay)
                    except Exception as e:
                        with results_container:
                            st.markdown(f"""<div class="result-card-fail"><span class="status-icon">❌</span><span class="email-text">{receiver}</span></div>""", unsafe_allow_html=True)
                server.quit()
                st.balloons()
                st.success(f"انتهت العملية! {success_count} / {len(final_list)} ناجح.")
                
                if len(receivers_list) > len(final_list):
                    st.error(f"⚠️ توقفت العملية لأنك وصلت للحد اليومي ({limit}). الرسائل المتبقية لم تُرسل.")
                    if not is_premium:
                        st.markdown(f"""
                        <div style="background-color: #ffcccc; border: 2px solid #ff0000; padding: 20px; border-radius: 10px; text-align: center; direction: rtl; margin-top: 10px;">
                            <h3 style="color: #cc0000;">⛔ لقد وصلت للحد الأقصى (3 رسائل)</h3>
                            <p style="font-size: 16px; color: #333;">لإكمال إرسال باقي الرسائل ({len(receivers_list) - len(final_list)} رسالة متبقية)، يجب تفعيل حسابك.</p>
                            <a href="https://wa.me/212633991635" target="_blank" style="text-decoration: none;">
                                <div style="background-color: #25D366; color: white; padding: 10px 20px; border-radius: 5px; display: inline-block; font-weight: bold; margin-top: 10px;">
                                    🚀 تفعيل النسخة الكاملة الآن (0633991635)
                                </div>
                            </a>
                        </div>
                        """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"خطأ في الاتصال: {e}")

# --- 5. فقرة "علاش تخدم بهاد البوت؟" (Marketing Section) ---
st.markdown("""
<div style="margin-top: 50px; direction: rtl; text-align: right;">
    <h3 style="color: #333; text-align: center; font-weight: bold; margin-bottom: 20px;">💡 علاش خاصك تخدم بـ Deutsch Bildung Sender؟</h3>
    <div style="background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 1px solid #eee;">
        <ul style="list-style-type: none; padding: 0; margin: 0; line-height: 2.2; color: #444; font-size: 16px;">
            <li>🚀 <b>ربح الوقت:</b> بدل ما تبقى تصيفط واحد بواحد وتضيع نهار كامل، صيفط لمئات الشركات فدقيقة وحدة.</li>
            <li>🛡️ <b>حماية من Spam:</b> البوت كيستعمل تقنيات متطورة باش يضمن أن الإيميل ديالك يوصل للـ Inbox ديال الشركة ماشي للـ Spam.</li>
            <li>🇩🇪 <b>تنسيق ألماني احترافي:</b> الرسائل كتمشي منظمة ومرتبة على الطريقة اللي كيبغيوها الألمان (Format Standard).</li>
            <li>💎 <b>زيادة حظوظ القبول:</b> فاش الشركة كتشوف إيميل منظم واحترافي، النظرة ديالهم ليك كتبدل وكتزيد فرصتك فالـ Vorstellungsgespräch.</li>
        </ul>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""<div style="text-align: center; margin-top: 30px; color: #555; font-size: 12px;">Deutsch Bildung 2026 | By Oussama Kehal</div>""", unsafe_allow_html=True)
