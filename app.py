import time
import random
import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="لعبة إنسان حيوان نبات", page_icon="🎮", layout="centered")

CATEGORIES = ["إنسان", "حيوان", "نبات", "جماد", "بلاد"]
ALPHABET = ['أ', 'ب', 'ت', 'ث', 'ج', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ك', 'ل', 'م', 'ن', 'هـ', 'و', 'ي']
DURATION = 15  # مدة العداد بالثواني

# تهيئة الـ Session State
if "timer_running" not in st.session_state:
    st.session_state.timer_running = False
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "current_letter" not in st.session_state:
    st.session_state.current_letter = "ح"
if "score" not in st.session_state:
    st.session_state.score = 0

st.title("🎮 لعبة إنسان حيوان نبات جماد بلاد")

# إدخال اسم اللاعب
player_name = st.text_input("اسم اللاعب الحالي:", value="براء")
st.markdown(f"### دور اللاعب: :gold[{player_name}]")

st.divider()

# قسم اختيار الحرف
col1, col2 = st.columns([3, 1])
with col1:
    custom_letter = st.text_input("أدخل الحرف المتفق عليه (أو اتركه للاختيار العشوائي):", value=st.session_state.current_letter)
with col2:
    st.write("")
    st.write("")
    if st.button("🎲 حرف عشوائي"):
        st.session_state.current_letter = random.choice(ALPHABET)
        st.rerun()

if custom_letter:
    st.session_state.current_letter = custom_letter.strip()[0] if len(custom_letter.strip()) > 0 else "ح"

# زر بدء المؤقت
if st.button("⏳ بدء المؤقت (15 ثانية)", use_container_width=True, type="primary"):
    st.session_state.timer_running = True
    st.session_state.start_time = time.time()
    st.rerun()

# منطقة عرض العداد التنازلي المتحرك
if st.session_state.timer_running:
    elapsed = time.time() - st.session_state.start_time
    remaining = int(DURATION - elapsed)

    if remaining > 0:
        st.markdown(
            f"""
            <div style="border: 2px solid #d4af37; padding: 15px; border-radius: 10px; text-align: center; background-color: #1a1a1a; margin: 15px 0;">
                <h4 style="color: #ffffff; margin: 0;">⏳ الوقت قيد العد التنازلي</h4>
                <h1 style="color: #ff4d4d; font-size: 42px; margin: 5px 0;">مفعل ({remaining} ثانية)</h1>
            </div>
            """,
            unsafe_allow_html=True,
        )
        time.sleep(1)
        st.rerun()
    else:
        st.session_state.timer_running = False
        st.error("⏰ انتهى الوقت!")
else:
    st.info("اضغط على 'بدء المؤقت' لتفعيل العد التنازلي.")

st.markdown(f"### 🎯 الحرف الحالي: :red[{st.session_state.current_letter}]")

# نموذج إدخال الكلمات
with st.form("game_form"):
    user_inputs = {}
    for cat in CATEGORIES:
        user_inputs[cat] = st.text_input(f"{cat}:", key=cat)
    
    submitted = st.form_submit_button("✅ التحقق واحتساب النقاط", use_container_width=True)

if submitted:
    letter = st.session_state.current_letter
    round_score = 0
    details = []

    for cat, word in user_inputs.items():
        cleaned = word.strip()
        if cleaned.startswith("ال"):
            cleaned = cleaned[2:]

        is_correct = False
        if cleaned:
            if letter == 'أ' and cleaned[0] in ['أ', 'إ', 'آ', 'ا']:
                is_correct = True
            elif cleaned.startswith(letter):
                is_correct = True

        if is_correct:
            round_score += 10
            details.append(f"✅ **{cat}**: {word} (+10)")
        else:
            details.append(f"❌ **{cat}**: {word if word else 'فارغ'} (0)")

    st.session_state.score += round_score
    st.session_state.timer_running = False
    st.success(f"نقاط هذه الجولة لـ {player_name}: {round_score}")
    st.metric("مجموع النقاط الكلي", st.session_state.score)
    for item in details:
        st.write(item)
