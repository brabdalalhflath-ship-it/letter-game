import streamlit as st
import random
import time
import streamlit.components.v1 as components

st.set_page_config(page_title="لعبة الحروف الجماعية", page_icon="🎮", layout="centered")

# --- كود تحويل الموقع إلى تطبيق للجوال (PWA Injection) ---
pwa_code = """
<script>
  // إضافة ملف الـ Manifest ديناميكياً لتشغيل التطبيق ملء الشاشة
  const manifest = {
    "name": "لعبة الحروف الجماعية",
    "short_name": "لعبة الحروف",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#ffffff",
    "theme_color": "#ff4b4b",
    "icons": [
      {
        "src": "https://em-content.zobj.net/source/microsoft-teams/337/video-game_1f3ae.png",
        "sizes": "192x192",
        "type": "image/png"
      }
    ]
  };
  const stringManifest = JSON.stringify(manifest);
  const blob = new Blob([stringManifest], {type: 'application/json'});
  const manifestURL = URL.createObjectURL(blob);
  
  let link = document.createElement('link');
  link.rel = 'manifest';
  link.href = manifestURL;
  document.head.appendChild(link);
</script>
"""
components.html(pwa_code, height=0)

# --- واجهة اللعبة الأساسية ---
st.title("🎮 لعبة إنسان حيوان جماد")

ALPHABET = ['أ', 'ب', 'ت', 'ث', 'ج', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ك', 'ل', 'م', 'ن', 'هـ', 'و', 'ي']
CATEGORIES = ["إنسان", "حيوان", "جماد", "بلاد"]

if "letter" not in st.session_state:
    st.session_state.letter = random.choice(ALPHABET)
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

TIME_LIMIT = 60
elapsed_time = int(time.time() - st.session_state.start_time)
remaining_time = max(0, TIME_LIMIT - elapsed_time)

def reset_round():
    st.session_state.letter = random.choice(ALPHABET)
    st.session_state.start_time = time.time()

col1, col2 = st.columns(2)
with col1:
    st.subheader(f"الحرف المطلوب: :red[{st.session_state.letter}]")
with col2:
    if remaining_time > 0:
        st.metric("⏳ الوقت المتبقي", f"{remaining_time} ثانية")
    else:
        st.error("⏰ انتهى الوقت!")

if st.button("🔄 جولة جديدة"):
    reset_round()
    st.rerun()

answers = {}
for cat in CATEGORIES:
    answers[cat] = st.text_input(f"أدخل {cat}:", key=cat, disabled=(remaining_time == 0))

if st.button("✅ التحقق من الإجابات", type="primary"):
    if remaining_time == 0:
        st.warning("⚠️ انتهى الوقت قبل إرسال الإجابات!")
    else:
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
                
        st.markdown("---")
        if score >= 30:
            st.balloons()
            st.success(f"🎉 **مبروك! فوز ساحق!** المجموع الكلي: {score} من 40")
        elif score >= 10:
            st.info(f"👍 **محاولة جيدة!** المجموع الكلي: {score} من 40")
        else:
            st.error(f"❌ **خسارة!** المجموع الكلي: {score} من 40. حاول مرة أخرى!")
