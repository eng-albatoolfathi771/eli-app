import streamlit as st
import time

# 1. إعداد الصفحة
st.set_page_config(
    page_title="ELI - Learn Tech English",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. تصميم CSS احترافي يطابق الـ Dark UI الفخم في التصميم
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    * {
        font-family: 'Cairo', sans-serif;
    }
    
    .stApp {
        background: #0B111E !important;
        color: #F8FAFC !important;
    }
    
    /* الحاوية الرئيسية */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 480px !important;
    }

    /* الشريط العلوي */
    .top-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #151D30;
        padding: 10px 18px;
        border-radius: 16px;
        border: 1px solid #1E293B;
        margin-bottom: 18px;
    }
    .badge {
        font-weight: 700;
        font-size: 0.95rem;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .streak { color: #F59E0B; }
    .xp { color: #38BDF8; }

    /* بطاقات واجهة Eli */
    .eli-hero-card {
        background: linear-gradient(145deg, #17233B, #111A2C);
        border-radius: 24px;
        padding: 20px;
        border: 1px solid #2A3B5C;
        box-shadow: 0 12px 28px rgba(0, 0, 0, 0.4);
        margin-bottom: 18px;
        text-align: right;
        position: relative;
    }
    
    .speech-bubble {
        background: #1E2E4A;
        color: #E2E8F0;
        padding: 12px 16px;
        border-radius: 18px 18px 4px 18px;
        font-size: 0.95rem;
        border: 1px solid #3B82F6;
        display: inline-block;
        margin-top: 8px;
        line-height: 1.5;
    }

    /* بطاقة الدرس الحالي */
    .lesson-card {
        background: #141C2E;
        border-radius: 20px;
        padding: 18px;
        border: 1px solid #23334E;
        margin-bottom: 15px;
    }

    /* أزرار مخصصة متدرجة */
    div.stButton > button {
        background: linear-gradient(135deg, #4F46E5 0%, #3B82F6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 12px 24px !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.35) !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.5) !important;
    }

    /* تنسيق كروت الراديو للاختيار */
    div[data-testid="stRadio"] > label {
        display: none;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] {
        gap: 10px;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] label {
        background: #162035 !important;
        border: 1px solid #22324F !important;
        border-radius: 14px !important;
        padding: 12px 16px !important;
        color: #F8FAFC !important;
        font-weight: 600 !important;
        width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. إدارة الحالة (Session State)
if "xp" not in st.session_state:
    st.session_state.xp = 1250
if "streak" not in st.session_state:
    st.session_state.streak = 12
if "step" not in st.session_state:
    st.session_state.step = "home" # onboarding, home, lesson
if "selected_track" not in st.session_state:
    st.session_state.selected_track = "English for Python Developers"
if "lesson_index" not in st.session_state:
    st.session_state.lesson_index = 0

# 4. بنك الدروس والمفردات التقنية
LESSONS_DB = [
    {
        "topic": "Variables in Python",
        "term": "variable",
        "phonetic": "/ˈveəriəbəl/",
        "arabic": "متغير",
        "definition": "A container for storing data values.",
        "example": "x = 10\nname = 'ELI'",
        "question": "ما هو دور الـ Variable في لغات البرمجة؟",
        "options": ["حاوية لتخزين القيم والبيانات في الذاكرة", "أمر لطباعة النتائج على الشاشة", "أداة لتشغيل السيرفر"],
        "correct": "حاوية لتخزين القيم والبيانات في الذاكرة"
    },
    {
        "topic": "Data Types",
        "term": "Data Type",
        "phonetic": "/ˈdeɪtə taɪp/",
        "arabic": "نوع البيانات",
        "definition": "Specifies the type of value a variable has (e.g., Integer, String, Boolean).",
        "example": "age = 22 # Integer\nstatus = True # Boolean",
        "question": "ماذا يحدد الـ Data Type في الكود؟",
        "options": ["نوع القيمة والعمليات الممكنة عليها", "سرعة تنفيذ الكود", "اسم الدالة الرئيسية"],
        "correct": "نوع القيمة والعمليات الممكنة عليها"
    }
]

# 5. الشريط العلوي المشترك
st.markdown(f"""
<div class="top-bar">
    <div class="badge xp">⚡ {st.session_state.xp} XP</div>
    <div class="badge streak">🔥 {st.session_state.streak} Streak</div>
    <div style="font-size: 1.2rem; font-weight: 900; color: #38BDF8;">eli</div>
</div>
""", unsafe_allow_html=True)

# ----------------- الشاشة الرئيسية (Home) -----------------
if st.session_state.step == "home":
    st.markdown(f"""
    <div class="eli-hero-card">
        <h3 style="margin: 0; color: #FFFFFF;">👋 مرحباً بك!</h3>
        <p style="color: #94A3B8; margin: 4px 0 10px 0;">جاهز لمواصلة رحلتك التقنية اليوم؟</p>
        <div class="speech-bubble">
            اليوم هو يوم رائع لتعلم مصطلحات برمجية جديدة ترفع مستواك التقني! 🚀
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="lesson-card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="background: #2563EB; padding: 4px 10px; border-radius: 8px; font-size: 0.8rem; font-weight: 700;">درس اليوم</span>
            <span style="color: #38BDF8; font-size: 0.85rem; font-weight: 700;">مكتمل 60%</span>
        </div>
        <h3 style="color: #F8FAFC; margin: 10px 0 4px 0;">{LESSONS_DB[st.session_state.lesson_index]['topic']}</h3>
        <p style="color: #94A3B8; font-size: 0.9rem; margin-bottom: 12px;">المتغيرات في بايثون للمطورين</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 متابعة الدرس الآن", use_container_width=True):
        st.session_state.step = "lesson"
        st.rerun()

    st.markdown("""
    <div class="lesson-card" style="margin-top: 15px;">
        <h4 style="margin: 0 0 10px 0; color: #E2E8F0;">📋 المهام اليومية</h4>
        <p style="color: #10B981; margin: 4px 0; font-size: 0.9rem;">✔ تعلم 10 كلمات ومصطلحات جديدة (10/10)</p>
        <p style="color: #38BDF8; margin: 4px 0; font-size: 0.9rem;">⏳ إكمال درس البرمجة التفاعلي (1/2)</p>
    </div>
    """, unsafe_allow_html=True)

# ----------------- شاشة الدرس التفاعلي (Lesson) -----------------
elif st.session_state.step == "lesson":
    lesson = LESSONS_DB[st.session_state.lesson_index]
    
    st.caption(f"📚 {st.session_state.selected_track} • {lesson['topic']}")
    st.progress(0.75)
    
    st.markdown(f"""
    <div class="eli-hero-card" style="text-align: center;">
        <span style="background: #3B82F6; padding: 3px 12px; border-radius: 12px; font-size: 0.8rem; font-weight: 700;">كلمة جديدة 📖</span>
        <h1 style="color: #38BDF8; margin: 10px 0 2px 0; font-size: 2.2rem;">{lesson['term']}</h1>
        <p style="color: #94A3B8; font-size: 0.95rem; margin-bottom: 10px;">{lesson['phonetic']}</p>
        <h3 style="color: #F59E0B; margin: 5px 0;">{lesson['arabic']}</h3>
        <p style="color: #E2E8F0; font-size: 1rem; margin-top: 8px;">{lesson['definition']}</p>
        <div style="background: #0B111E; padding: 10px; border-radius: 12px; margin-top: 12px; text-align: left; font-family: monospace; color: #10B981; direction: ltr;">
            {lesson['example'].replace(chr(10), '<br>')}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write(f"**سؤال الفهم:** {lesson['question']}")
    choice = st.radio("خيارات الإجابة:", lesson['options'], label_visibility="collapsed")

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("تحقق من إجابتي ✔️", use_container_width=True):
            if choice == lesson['correct']:
                st.session_state.xp += 25
                st.balloons()
                st.success("🎉 إجابة رائعة وصحيحة! +25 نقطة XP")
                time.sleep(1.2)
                st.session_state.step = "home"
                st.rerun()
            else:
                st.error("💡 حاول مجدداً، ركز في تعريف الحاوية والتخزين.")
    with col_b:
        if st.button("⬅ العودة للرئيسية", use_container_width=True):
            st.session_state.step = "home"
            st.rerun()
