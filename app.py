import streamlit as st
import time

# إعداد الصفحة وتفعيل تصميم الموبايل
st.set_page_config(
    page_title="Eli - Tech English",
    page_icon="👦",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# تصميم مخصص وتأثيرات حركية (Custom CSS)
st.markdown("""
<style>
    /* خلفية التطبيق والخطوط */
    .stApp {
        background: linear-gradient(180deg, #F8FAFC 0%, #EEF2F6 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* بطاقة Eli التفاعلية */
    .eli-card {
        background: white;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.06);
        border: 2px solid #E2E8F0;
        margin-bottom: 20px;
        text-align: center;
        animation: fadeIn 0.8s ease-in-out;
    }
    
    /* بالون التحدث */
    .chat-bubble {
        background: #EBF4FF;
        color: #1E3A8A;
        padding: 14px 18px;
        border-radius: 18px 18px 18px 4px;
        font-weight: 600;
        font-size: 1.05rem;
        margin-top: 10px;
        display: inline-block;
        border: 1px solid #BFDBFE;
    }
    
    /* شريط النقاط والإنجاز */
    .stats-container {
        display: flex;
        justify-content: space-around;
        background: white;
        padding: 12px;
        border-radius: 16px;
        border: 1px solid #E2E8F0;
        margin-bottom: 15px;
    }
    
    .stat-item {
        font-weight: bold;
        font-size: 1.1rem;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# إدارة الحالة (State Management)
if "xp" not in st.session_state:
    st.session_state.xp = 50
if "streak" not in st.session_state:
    st.session_state.streak = 1
if "track" not in st.session_state:
    st.session_state.track = None
if "current_step" not in st.session_state:
    st.session_state.current_step = 0

# شريط الحالة العلوي (النقاط والـ Streak)
st.markdown(f"""
<div class="stats-container">
    <div class="stat-item" style="color: #D97706;">🔥 {st.session_state.streak} Day Streak</div>
    <div class="stat-item" style="color: #2563EB;">⚡ {st.session_state.xp} XP</div>
</div>
""", unsafe_allow_html=True)

# بنك الأسئلة والمصطلحات التقنية
DATA = {
    "الذكاء الاصطناعي وعلم البيانات 🤖": [
        {
            "term": "Overfitting",
            "meaning": "فرط التخصيص / الحفظ المفرط للبيانات",
            "context": "The model has high accuracy on training data but fails on new data due to Overfitting.",
            "question": "ماذا يعني أن النموذج يعاني من 'Overfitting'؟",
            "options": ["حفظ بيانات التدريب بدلاً من التعلم منها", "النموذج سريع جداً في الحسابات", "نقص في حجم البيانات"],
            "answer": "حفظ بيانات التدريب بدلاً من التعلم منها"
        },
        {
            "term": "Epoch",
            "meaning": "دورة تدريبية كاملة على كل البيانات",
            "context": "We trained the neural network for 50 epochs.",
            "question": "في تدريب الشبكات العصبية، ماذا يمثل الـ 'Epoch'؟",
            "options": ["دورة تدريب واحدة عبر كامل البيانات", "معدل سرعة المعالج", "نوع من دوال التنشيط"],
            "answer": "دورة تدريب واحدة عبر كامل البيانات"
        }
    ],
    "تطوير الويب وهندسة البرمجيات 💻": [
        {
            "term": "API (Application Programming Interface)",
            "meaning": "واجهة برمجة التطبيقات لتبادل البيانات",
            "context": "The frontend communicates with the backend through a REST API.",
            "question": "ما هو الدور الأساسي للـ API في الأنظمة؟",
            "options": ["جسر وسيط لنقل وتبادل البيانات بين الأنظمة", "تصميم الواجهات الرسومية", "حفظ البيانات في القرص الصلب"],
            "answer": "جسر وسيط لنقل وتبادل البيانات بين الأنظمة"
        }
    ]
}

# 1. شاشة اختيار المسار والترحيب
if st.session_state.track is None:
    st.markdown("""
    <div class="eli-card">
        <div style="font-size: 50px;">👦</div>
        <div class="chat-bubble">
            مرحباً بك! أنا <b>Eli</b> 👋<br>
            سأكون رفيقك اليومي لإتقان المصطلحات البرمجية والإنجليزية التقنية بسهولة وبدون تعقيد.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("🎯 اختر مسارك التقني للبدء:")
    chosen_track = st.selectbox(
        "المجال التدريبي:",
        list(DATA.keys()),
        label_visibility="collapsed"
    )
    
    if st.button("🚀 ابدأ المسار الآن", use_container_width=True):
        st.session_state.track = chosen_track
        st.session_state.current_step = 0
        st.rerun()

# 2. شاشة الدرس التفاعلي
else:
    lessons = DATA[st.session_state.track]
    step = st.session_state.current_step
    
    if step < len(lessons):
        item = lessons[step]
        
        st.progress((step + 1) / len(lessons))
        
        st.markdown(f"""
        <div class="eli-card">
            <h2 style="color: #1E40AF; margin-bottom: 5px;">{item['term']}</h2>
            <p style="color: #475569; font-size: 1.1rem;"><b>المعنى:</b> {item['meaning']}</p>
            <hr style="border: 0; border-top: 1px solid #E2E8F0; margin: 15px 0;">
            <p style="font-style: italic; color: #334155; direction: ltr; text-align: center;">
                "{item['context']}"
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write(f"**سؤال سريع:** {item['question']}")
        user_choice = st.radio("اختر الإجابة الصحيحة:", item['options'], key=f"q_{step}", label_visibility="collapsed")
        
        if st.button("تحقق من الإجابة ✔️", use_container_width=True):
            if user_choice == item['answer']:
                st.session_state.xp += 15
                st.balloons()
                st.success("🎉 إجابة صحيحة ومتقنة! +15 نقطة XP")
                time.sleep(1)
                st.session_state.current_step += 1
                st.rerun()
            else:
                st.error("💡 ليست الإجابة الدقيقة، حاول مجدداً أو راجع سياق الجملة أعلاه!")
    else:
        st.markdown("""
        <div class="eli-card">
            <div style="font-size: 55px;">🏆</div>
            <h2 style="color: #059669;">أحسنت! أكملت درس اليوم بنجاح</h2>
            <p>أصبحت أكثر جاهزية لمقابلات العمل وقراءة التوثيقات التقنية باللغة الإنجليزية.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 بدء مسار جديد", use_container_width=True):
            st.session_state.track = None
            st.session_state.current_step = 0
            st.rerun()
