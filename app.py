import streamlit as st
import time

# 1. إعداد الصفحة
st.set_page_config(
    page_title="ELI - Tech English",
    page_icon="👦",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. تصميم CSS يطابق النمط الداكن المتقدم والشاشات المتعددة
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    * { font-family: 'Cairo', sans-serif; }
    
    .stApp {
        background: #0D131F !important;
        color: #F8FAFC !important;
    }
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 5rem !important;
        max-width: 480px !important;
    }
    
    /* شريط النقاط والـ Streak */
    .top-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #161F30;
        padding: 10px 16px;
        border-radius: 16px;
        border: 1px solid #23334E;
        margin-bottom: 15px;
    }
    .badge-item { font-weight: 700; font-size: 0.95rem; }
    .streak-color { color: #F59E0B; }
    .xp-color { color: #38BDF8; }

    /* بطاقة Eli الرئيسية */
    .eli-banner {
        background: linear-gradient(145deg, #17233B, #111A2C);
        border-radius: 22px;
        padding: 16px;
        border: 1px solid #2A3B5C;
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 15px;
    }
    .speech-box {
        background: #1E2E4A;
        color: #E2E8F0;
        padding: 10px 14px;
        border-radius: 16px 16px 4px 16px;
        font-size: 0.9rem;
        border: 1px solid #3B82F6;
        line-height: 1.4;
    }

    /* كروت الدروس والمفردات */
    .custom-card {
        background: #161F30;
        border-radius: 18px;
        padding: 16px;
        border: 1px solid #23334E;
        margin-bottom: 12px;
    }

    /* زر النطق الصوتي */
    .audio-btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: #1E293B;
        color: #38BDF8;
        border: 1px solid #38BDF8;
        border-radius: 50%;
        width: 36px;
        height: 36px;
        cursor: pointer;
        font-size: 1.1rem;
        margin-right: 8px;
    }

    /* تحسين الأزرار */
    div.stButton > button {
        background: linear-gradient(135deg, #4F46E5 0%, #3B82F6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 10px 20px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
    }

    /* خيارات الإجابة */
    div[data-testid="stRadio"] div[role="radiogroup"] label {
        background: #1A2438 !important;
        border: 1px solid #2A3B5C !important;
        border-radius: 12px !important;
        padding: 10px 14px !important;
        color: #F8FAFC !important;
        width: 100% !important;
        margin-bottom: 6px;
    }
</style>
""", unsafe_allow_html=True)

# 3. إدارة الحالة (Session State)
if "xp" not in st.session_state:
    st.session_state.xp = 1250
if "streak" not in st.session_state:
    st.session_state.streak = 12
if "page" not in st.session_state:
    st.session_state.page = "🏠 الرئيسية"
if "lesson_step" not in st.session_state:
    st.session_state.lesson_step = 0
if "user_selected_ans" not in st.session_state:
    st.session_state.user_selected_ans = None

# رابط صورة Eli المرفقة
ELI_IMAGE_URL = "https://raw.githubusercontent.com/eng-albatoolfathi771/Eli-App/main/eli.png"

# قاعدة بيانات المصطلحات البرمجية
LESSONS = [
    {
        "track": "English for Python Developers",
        "topic": "Variables & Memory",
        "term": "variable",
        "phonetic": "/ˈveəriəbəl/",
        "arabic": "متغير",
        "definition": "A symbolic name associated with a value and a storage location in memory.",
        "example": "name = 'Eli'\nage = 20",
        "question": "ما الوظيفة الأساسية للـ Variable في كتابة الأكواد؟",
        "options": [
            "حاوية برمجية لتخزين البيانات والقيم في الذاكرة",
            "أمر لإرسال البيانات إلى السيرفر مباشرة",
            "دالة تقوم بتنسيق واجهة المستخدم"
        ],
        "correct": "حاوية برمجية لتخزين البيانات والقيم في الذاكرة"
    },
    {
        "track": "English for Python Developers",
        "topic": "Data Structures",
        "term": "dictionary",
        "phonetic": "/ˈdɪkʃənəri/",
        "arabic": "قاموس بيانات (Key-Value)",
        "definition": "A collection of key-value pairs used to store data values.",
        "example": "user = {'name': 'Eli', 'role': 'AI Assistant'}",
        "question": "كيف يتم تخزين واسترجاع البيانات داخل الـ Dictionary؟",
        "options": [
            "عبر أزواج من المفاتيح والقيم (Key-Value pairs)",
            "عبر الترتيب الرقمي الثابت فقط",
            "من خلال الاتصال بقاعدة بيانات خارجية"
        ],
        "correct": "عبر أزواج من المفاتيح والقيم (Key-Value pairs)"
    }
]

# 4. الشريط العلوي
st.markdown(f"""
<div class="top-header">
    <div class="badge-item xp-color">⚡ {st.session_state.xp} XP</div>
    <div class="badge-item streak-color">🔥 {st.session_state.streak} Streak</div>
    <div style="font-size: 1.3rem; font-weight: 900; color: #38BDF8;">eli</div>
</div>
""", unsafe_allow_html=True)

# 5. شريط التنقل بين الواجهات
selected_tab = st.radio(
    "القائمة:",
    ["🏠 الرئيسية", "📖 الدرس التفاعلي", "🤖 مساعد Eli", "👤 الملف الشخصي"],
    horizontal=True,
    label_visibility="collapsed"
)

# ----------------- 1. الواجهة الرئيسية -----------------
if selected_tab == "🏠 الرئيسية":
    col_img, col_txt = st.columns([1, 2])
    with col_img:
        st.image("https://api.dicebear.com/7.x/bottts/svg?seed=EliHero", width=110)
    with col_txt:
        st.markdown("""
        <div style="margin-top: 5px;">
            <h3 style="margin: 0; color: #FFF;">مرحباً بك! 👋</h3>
            <div class="speech-box">
                جاهز لتعلم مصطلحات برمجية جديدة اليوم باللغة الإنجليزية؟ 🚀
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="custom-card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="background: #2563EB; padding: 3px 8px; border-radius: 8px; font-size: 0.8rem; font-weight: 700;">مسارك الحالي</span>
            <span style="color: #38BDF8; font-size: 0.85rem; font-weight: 700;">مكتمل 65%</span>
        </div>
        <h3 style="margin: 8px 0 2px 0; color: #F8FAFC;">English for Python Developers</h3>
        <p style="color: #94A3B8; font-size: 0.85rem; margin: 0;">المصطلحات الأساسية لهندسة البرمجيات والذكاء الاصطناعي</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="custom-card">
        <h4 style="margin: 0 0 8px 0; color: #E2E8F0;">📋 المهام اليومية</h4>
        <p style="color: #10B981; margin: 3px 0; font-size: 0.9rem;">✔ حفظ 10 مصطلحات هندسية (10/10)</p>
        <p style="color: #38BDF8; margin: 3px 0; font-size: 0.9rem;">⏳ اجتياز اختبار المصطلحات التفاعلي (1/2)</p>
    </div>
    """, unsafe_allow_html=True)

# ----------------- 2. واجهة الدرس التفاعلي -----------------
elif selected_tab == "📖 الدرس التفاعلي":
    curr = LESSONS[st.session_state.lesson_step]
    
    st.caption(f"مسار: {curr['track']} • {curr['topic']}")
    st.progress(0.60)

    # تشغيل الصوت تلقائياً عبر JavaScript بنقرة الزر
    audio_js = f"""
    <script>
    function speakTerm() {{
        var msg = new SpeechSynthesisUtterance("{curr['term']}");
        msg.lang = 'en-US';
        msg.rate = 0.85;
        window.speechSynthesis.speak(msg);
    }}
    </script>
    <div style="text-align: center; margin-bottom: 10px;">
        <button onclick="speakTerm()" style="background: #1E293B; border: 1px solid #38BDF8; color: #38BDF8; border-radius: 20px; padding: 6px 14px; font-weight: bold; cursor: pointer;">
            🔊 استمع للنطق الصوتي
        </button>
    </div>
    """
    st.components.v1.html(audio_js, height=45)

    st.markdown(f"""
    <div class="custom-card" style="text-align: center;">
        <span style="background: #3B82F6; padding: 2px 10px; border-radius: 10px; font-size: 0.75rem; font-weight: 700;">مصطلح اليوم</span>
        <h1 style="color: #38BDF8; margin: 8px 0 0 0; font-size: 2.2rem;">{curr['term']}</h1>
        <p style="color: #94A3B8; font-size: 0.9rem; margin-bottom: 6px;">{curr['phonetic']}</p>
        <h3 style="color: #F59E0B; margin: 4px 0;">{curr['arabic']}</h3>
        <p style="color: #E2E8F0; font-size: 0.95rem; margin-top: 6px;">{curr['definition']}</p>
        <div style="background: #0B111E; padding: 8px; border-radius: 10px; margin-top: 8px; text-align: left; font-family: monospace; color: #10B981; direction: ltr;">
            {curr['example']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write(f"**سؤال الفهم:** {curr['question']}")
    
    # اختيار فارغ افتراضياً (الطالب هو من يحدد)
    user_choice = st.radio(
        "اختر الإجابة الصحيحة:",
        curr['options'],
        index=None,
        key=f"quiz_opt_{st.session_state.lesson_step}",
        label_visibility="collapsed"
    )

    if st.button("تحقق من إجابتي ✔️", use_container_width=True):
        if user_choice is None:
            st.warning("⚠️ يرجى اختيار إجابة من القائمة أولاً.")
        elif user_choice == curr['correct']:
            st.session_state.xp += 20
            st.balloons()
            st.success("🎉 إجابة صحيحة ومتقنة! +20 نقطة XP")
            time.sleep(1.2)
            st.session_state.lesson_step = (st.session_state.lesson_step + 1) % len(LESSONS)
            st.rerun()
        else:
            st.error("💡 إجابة غير دقيقة، راجع تعريف المصطلح بالأعلى وحاول مجدداً.")

# ----------------- 3. واجهة مساعد Eli الذكي -----------------
elif selected_tab == "🤖 مساعد Eli":
    st.subheader("🤖 اسأل Eli - مساعدك اللغوي التقني")
    st.caption("يعمل بمحركات الفهم اللغوي الذكية للإجابة عن معاني وترجمة أي مصطلح برمجي.")
    
    user_query = st.text_input("اكتب أي مصطلح أو جملة برمجية تريد شرحها:", placeholder="مثال: What is asynchronous function?")
    
    if st.button("طلب الشرح من Eli ⚡", use_container_width=True):
        if user_query:
            with st.spinner("Eli يفكر ويجهز الشرح..."):
                time.sleep(1)
                st.markdown(f"""
                <div class="custom-card">
                    <h4 style="color: #38BDF8; margin: 0 0 5px 0;">شرح Eli:</h4>
                    <p style="color: #E2E8F0; line-height: 1.6; margin: 0;">
                        المصطلح <b>"{user_query}"</b> يتعلق بتنفيذ المهام البرمجية في الخلفية دون تجميد واجهة التطبيق حتى تكتمل الاستجابة.
                    </p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("يرجى كتابة المصطلح أولاً.")

# ----------------- 4. واجهة الملف الشخصي -----------------
elif selected_tab == "👤 الملف الشخصي":
    st.markdown(f"""
    <div class="custom-card" style="text-align: center;">
        <h2 style="color: #38BDF8; margin: 0;">المهندسة البتول 👩‍💻</h2>
        <p style="color: #94A3B8; font-size: 0.9rem;">المستوى 12 • متعلم تقني متميز</p>
        <hr style="border: 0; border-top: 1px solid #23334E; margin: 12px 0;">
        <div style="display: flex; justify-content: space-around;">
            <div>
                <h3 style="color: #F59E0B; margin: 0;">12</h3>
                <span style="color: #94A3B8; font-size: 0.8rem;">Streak أيام</span>
            </div>
            <div>
                <h3 style="color: #38BDF8; margin: 0;">{st.session_state.xp}</h3>
                <span style="color: #94A3B8; font-size: 0.8rem;">إجمالي الـ XP</span>
            </div>
            <div>
                <h3 style="color: #10B981; margin: 0;">8</h3>
                <span style="color: #94A3B8; font-size: 0.8rem;">الشارات المكتملة</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="custom-card">
        <h4 style="margin: 0 0 10px 0; color: #E2E8F0;">🎖️ الشارات والإنجازات</h4>
        <p>🥇 خبير بايثون للمبتدئين</p>
        <p>⚡ أسبوع كامل بدون انقطاع</p>
        <p>🎯 دقة إجابات 90% فما فوق</p>
    </div>
    """, unsafe_allow_html=True)
