import streamlit as st
import streamlit.components.v1 as components
import random

# 1. Page Configuration
st.set_page_config(page_title="لعبة الحروف الجماعية", page_icon="🏆", layout="centered")

# PWA Code Injection
pwa_code = """
<script>
  const manifest = {
    "name": "لعبة الحروف الجماعية",
    "short_name": "لعبة الحروف",
    "start_url": ".",
    "display": "standalone",
    "background_color": "#000000",
    "theme_color": "#d4af37",
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

# 2. Header Style
st.markdown("""
    <style>
    .main-container {
        background-color: #000000;
        color: #ffffff;
    }
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

# 3. Game Settings
st.sidebar.title("⚙️ إعدادات اللعبة")
game_mode = st.sidebar.radio("اختر طريقة اللعب:", ["لعب فردي (لاعبين)", "لعب جماعي (فرق)"])

if "scores" not in st.session_state:
    st.session_state.scores = {}

if game_mode == "لعب فردي (لاعبين)":
    players_count = st.sidebar.number_input("عدد اللاعبين:", min_value=1, max_value=8, value=2)
    players = []
    st.sidebar.markdown("### أسماء اللاعبين:")
    for i in range(int(players_count)):
        p_name = st.sidebar.text_input(f"اللاعب {i+1}:", value=f"لاعب {i+1}", key=f"player_{i}")
        players.append(p_name)
        if p_name not in st.session_state.scores:
            st.session_state.scores[p_name] = 0

    current_turn = st.sidebar.selectbox("اللاعب الحالي:", players)

else:
    teams_count = st.sidebar.number_input("عدد الفرق:", min_value=2, max_value=4, value=2)
    teams = []
    st.sidebar.markdown("### أسماء الفرق:")
    for i in range(int(teams_count)):
        t_name = st.sidebar.text_input(f"الفريق {i+1}:", value=f"فريق {i+1}", key=f"team_{i}")
        teams.append(t_name)
        if t_name not in st.session_state.scores:
            st.session_state.scores[t_name] = 0

    current_turn = st.sidebar.selectbox("الفريق الحالي:", teams)

# 4. Main Game Logic State
ALPHABET = ['أ', 'ب', 'ت', 'ث', 'ج', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ك', 'ل', 'م', 'ن', 'هـ', 'و', 'ي']
CATEGORIES = ["إنسان", "حيوان", "نبات", "جماد", "بلاد"]

if "letter" not in st.session_state:
    st.session_state.letter = None

if "game_started" not in st.session_state:
    st.session_state.game_started = False

if "timer_id" not in st.session_state:
    st.session_state.timer_id = 0

# 5. Timer Function
def show_timer(seconds=60, unique_id=0):
    timer_html = f"""
    <div style="text-align: center; background: #0d0d0d; padding: 15px; border-radius: 15px; border: 2px solid #d4af37; max-width: 320px; margin: 0 auto 20px auto;">
        <div style="color: #d4af37; font-size: 16px; font-weight: bold;">⏳ الوقت المتبقي</div>
        <div id="time" style="font-size: 48px; font-weight: bold; color: #ffffff;">{seconds}</div>
        <div style="width: 100%; background: #333; height: 8px; border-radius: 5px; margin-top: 8px; overflow: hidden;">
            <div id="bar" style="width: 100%; height: 100%; background: #d4af37; transition: width 1s linear;"></div>
        </div>
    </div>
    <script>
        var t = {seconds}, total = {seconds};
        var timer = setInterval(function(){{
            if(t <= 0){{
                clearInterval(timer);
                document.getElementById("time").innerHTML = "انتهى الوقت!";
                document.getElementById("time").style.color = "#ff4d4d";
                document.getElementById("bar").style.width = "0%";
            }} else {{
                t--;
                document.getElementById("time").innerHTML = t;
                document.getElementById("bar").style.width = ((t/total)*100) + "%";
                if(t <= 10) {{
                    document.getElementById("time").style.color = "#ff4d4d";
                    document.getElementById("bar").style.background = "#ff4d4d";
                }}
            }}
        }}, 1000);
    </script>
    """
    components.html(timer_html, height=160, key=f"timer_comp_{unique_id}")

st.markdown(f"<h3 style='text-align: center;'>الدور الحالي: <span style='color: #d4af37;'>{current_turn}</span></h3>", unsafe_allow_html=True)

# أزرار تحكم اللعبة
col_btn1, col_btn2 = st.columns([1, 1])

with col_btn1:
    if st.button("🏁 بدء الجولة والوقت", type="primary", use_container_width=True):
        st.session_state.letter = random.choice(ALPHABET)
        st.session_state.game_started = True
        st.session_state.timer_id += 1
        st.rerun()

with col_btn2:
    if st.button("🔄 تغيير الحرف فقط", use_container_width=True):
        st.session_state.letter = random.choice(ALPHABET)
        st.rerun()

# عرض الحرف والمؤقت
if st.session_state.game_started and st.session_state.letter:
    st.markdown(f"<h2 style='text-align: center; margin-top: 15px;'>الحرف المطلوب: <span style='color: #ff4d4d;'>{st.session_state.letter}</span></h2>", unsafe_allow_html=True)
    show_timer(60, unique_id=st.session_state.timer_id)
else:
    st.info("💡 اضغط على زر **'🏁 بدء الجولة والوقت'** لبدء الوقت وتحديد الحرف المطلوب!")

# إدخال الإجابات
answers = {}
col_inputs = st.columns(len(CATEGORIES))
for idx, cat in enumerate(CATEGORIES):
    with col_inputs[idx % len(CATEGORIES)]:
        answers[cat] = st.text_input(f"{cat}:", key=f"input_{cat}")

# الاحتساب والتحقق
if st.button("✅ التحقق والاحتساب", type="primary", use_container_width=True):
    if not st.session_state.letter:
        st.warning("⚠️ يرجى بدء الجولة أولاً بالضغط على زر 'بدء الجولة والوقت'!")
    else:
        round_score = 0
        current_l = st.session_state.letter
        
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

# 6. Leaderboard
st.markdown("---")
st.subheader("📊 جدول النقاط الإجمالي")
for entity, score in st.session_state.scores.items():
    st.write(f"🏆 **{entity}**: {score} نقطة")
