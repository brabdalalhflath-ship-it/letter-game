import time
import streamlit as st

# 1. تهيئة الـ Session State للعداد
if "timer_running" not in st.session_state:
    st.session_state.timer_running = False
if "start_time" not in st.session_state:
    st.session_state.start_time = None

DURATION = 15  # مدة المؤقت بالثواني

# 2. زر بدء المؤقت
if st.button("⏳ بدء المؤقت (15 ثانية)"):
    st.session_state.timer_running = True
    st.session_state.start_time = time.time()
    st.rerun()

# 3. تشغيل وحساب العد التنازلي المتحرك
if st.session_state.timer_running:
    elapsed = time.time() - st.session_state.start_time
    remaining = int(DURATION - elapsed)

    if remaining > 0:
        # عرض الوقت المتحرك
        st.markdown(
            f"""
            <div style="border: 2px solid #d4af37; padding: 15px; border-radius: 10px; text-align: center; background-color: #1a1a1a;">
                <h3 style="color: #ffffff; margin: 0;">⏳ الوقت قيد العد التنازلي</h3>
                <h1 style="color: #ff4d4d; font-size: 40px; margin: 10px 0;">{remaining} ثانية</h1>
            </div>
            """,
            unsafe_allow_html=True,
        )
        # إجبار Streamlit على الانتظار ثانية واحدة ثم إعادة تحديث الواجهة
        time.sleep(1)
        st.rerun()
    else:
        st.session_state.timer_running = False
        st.error("⏰ انتهى الوقت!")
