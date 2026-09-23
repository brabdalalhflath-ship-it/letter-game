import streamlit as st
import random

st.set_page_config(page_title="لعبة الحروف الجماعية", page_icon="🎮")

st.title("🎮 لعبة إنسان حيوان جماد")

# الأحرف العربية
ALPHABET = ['أ', 'ب', 'ت', 'ث', 'ج', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ك', 'ل', 'م', 'ن', 'هـ', 'و', 'ي']
CATEGORIES = ["إنسان", "حيوان", "جماد", "بلاد"]

# حفظ الحرف في الجلسة
if "letter" not in st.session_state:
    st.session_state.letter = random.choice(ALPHABET)

st.subheader(f"الحرف المطلوب: :red[{st.session_state.letter}]")

if st.button("🔄 تغيير الحرف"):
    st.session_state.letter = random.choice(ALPHABET)
    st.rerun()

# حقول الإدخال
answers = {}
for cat in CATEGORIES:
    answers[cat] = st.text_input(f"أدخل {cat}:", key=cat)

if st.button("✅ التحقق من الإجابات", type="primary"):
    score = 0
    current_l = st.session_state.letter
    
    st.markdown("---")
    st.write("### النتائج:")
    
    for cat, ans in answers.items():
        word = ans.strip()
        cleaned = word[2:] if word.startswith("ال") else word
        
        is_correct = False
        if cleaned:
            if current_l == 'أ' and cleaned[0] in ['أ', 'إ', 'آ', 'ا']:
                is_correct = True
            elif cleaned.startswith(current_l):
                is_correct = True
                
        if is_correct:
            score += 10
            st.success(f"✓ {cat}: {word} (+10)")
        else:
            st.error(f"✗ {cat}: {word if word else 'فارغ'} (0)")
            
    st.info(f"**المجموع الكلي: {score} من 40**")
