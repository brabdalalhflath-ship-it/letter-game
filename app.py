import streamlit as st

# 1. Page Configuration
st.set_page_config(page_title="لعبة إنسان حيوان", page_icon="🏆", layout="centered")

# 2. Header Style
st.markdown("""
    <style>
    .header-box {
        text-align: center;
        background-color: #0d0d0d;
        padding: 20px;
        border-radius: 20px;
        border: 2px solid #d4af37;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);
    }
    .game-title {
        color: #d4af37;
        text-align: center;
        font-family: 'Arial', sans-serif;
        font-size: 26px;
        font-weight: bold;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Header with Image
st.markdown('<div class="header-box">', unsafe_allow_html=True)
st.image("RF.jpeg", width=180) 
st.markdown('<div class="game-title">🎮 لعبة إنسان حيوان نبات جماد بلاد</div></div>', unsafe_allow_html=True)

# 3. Game Settings (Scores & Players)
if "scores" not in st.session_state:
    st.session_state.scores = {}

st.sidebar.title("⚙️ إعدادات اللاعبين")
players_count = st.sidebar.number_input("عدد اللاعبين:", min_value=1, max_value=8, value=2)
players = []
st.sidebar.markdown("### أسماء اللاعبين:")
for i in range(int(players_count)):
    p_name = st.sidebar.text_input(f"اللاعب {i+1}:", value=f"لاعب {i+1}", key=f"player_{i}")
    players.append(p_name)
    if p_name not in st.session_state.scores:
        st.session_state.scores[p_name] = 0

current_turn = st.sidebar.selectbox("دور اللاعب الحالي:", players)

st.markdown(f"<h3 style='text-align: center;'>دور اللاعب: <span style='color: #d4af37;'>{current_turn}</span></h3>", unsafe_allow_html=Type if 'Type' in globals() else str)

# 4. Input for the Real-life chosen letter & Timer Button
col_l1, col_l2 = st.columns([1, 1])

with col_l1:
    # إدخال الحرف الذي اخترتوه في الواقع شفوياً
    current_letter = st.text_input("✍️ أدخل الحرف المتفق عليه (في الواقع):", max_chars=2, placeholder="مثال: ب")

with col_l2:
    st.markdown("<br>", unsafe_allow_html=True)
    start_timer = st.button("⏳ بدء المؤقت (60 ثانية)", type="primary", use_container_width=True)

# عرض المؤقت المرئي إذا تم الضغط عليه
if start_timer:
    st.markdown(
        """
        <div style="text-align: center; background: #0d0d0d; padding: 15px; border-radius: 15px; border: 2px solid #d4af37; max-width: 320px; margin: 10px auto 20px auto;">
            <div style="color: #d4af37; font-size: 16px; font-weight: bold;">⏳ الوقت قيد العد التنازلي</div>
            <div style="font-size: 32px; font-weight: bold; color: #ff4d4d; margin-top: 5px;">مفعل (60 ثانية)</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# 5. Categories Inputs
CATEGORIES = ["إنسان", "حيوان", "نبات", "جماد", "بلاد"]
answers = {}

st.markdown(f"<h4 style='text-align: center; color: #ffffff;'>الحرف الحالي: <span style='color: #ff4d4d;'>{current_letter if current_letter else 'لم يتم إدخاله بعد'}</span></h4>", unsafe_allow_html=True)

col_inputs = st.columns(len(CATEGORIES))
for idx, cat in enumerate(CATEGORIES):
    with col_inputs[idx % len(CATEGORIES)]:
        answers[cat] = st.text_input(f"{cat}:", key=f"input_{cat}")

# 6. Check and Calculate Scores
if st.button("✅ التحقق واحتساب النقاط", type="primary", use_container_width=True):
    if not current_letter:
        st.warning("⚠️ يرجى كتابة الحرف المتفق عليه في الأعلى أولاً!")
    else:
        round_score = 0
        current_l = current_letter.strip()
        
        st.markdown("---")
        for cat, ans in answers.items():
            word = ans.strip()
            cleaned = word[2:] if word.startswith("ال") else word
            
            if cleaned and (cleaned.startswith(current_l) or (current_l == 'أ' and cleaned[0] in ['أ', 'إ', 'آ', 'ا'])):
                round_score += 10
                st.success(f"✓ {cat}: {word} (+10)")
            else:
                st.error(f"✗ {cat}: {word if word else 'فارغ'} (0)")
                
        st.session_state.scores[current_turn] += round_score
        st.markdown("---")
        
        if round_score >= 50:
            st.balloons()
            st.success(f"🎉 **ممتاز يا {current_turn}!** حصلت على العلامة الكاملة {round_score} نقطة!")
        else:
            st.info(f"👍 **جولة جيدة يا {current_turn}!** حصلت على {round_score} نقطة.")

# 7. Leaderboard
st.markdown("---")
st.subheader("📊 جدول النقاط الإجمالي")
for entity, score in st.session_state.scores.items():
    st.write(f"🏆 **{entity}**: {score} نقطة")
