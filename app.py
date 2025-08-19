# app.py — Streamlit version (Python only)
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="서영 졸업 축하 🎓", page_icon="🎉", layout="wide")

# ===== Hero / Title =====
st.title("🎓 한서영 졸업 축하 페이지")
st.subheader("그동안의 노력과 열정에 박수를 보내요 👏")
st.write("새로운 시작도 우리가 함께 응원할게요! 🌱")
col_a, col_b = st.columns(2)
with col_a:
    if st.button("축하 풍선 🎈", use_container_width=True):
        st.balloons()

st.divider()

# ===== Profile / Info =====
st.markdown("### 👩‍🎓 서영 정보")
c1, c2 = st.columns(2)
with c1:
    st.write("**이름:** 한서영 (Han Seo-young)")
    st.write("**학교:** 국민대학교")
    st.write("**전공:** 산림환경시스템학과")
with c2:
    st.write("**학위:** 학사 (B.Sc.)")
    st.write("**기간/졸업:** 2020-03 ~ 2025-08")

st.divider()

# ===== Timeline =====
st.markdown("### ⏳ 여정 타임라인")
timeline = [
    {"year": "2020", "title": "입학", "desc": "코로나 학번으로 대학 생활 시작"},
    {"year": "2022", "title": "성장", "desc": "숲애의 짱이 되다"},
    {"year": "2025", "title": "졸업", "desc": "졸업장을 품에 안다 🎓"},
]
for t in timeline:
    st.markdown(f"**{t['year']}** — *{t['title']}* : {t['desc']}")

st.divider()

# ===== Photo Gallery =====
st.markdown("### 📸 사진 갤러리 (선택)")
files = st.file_uploader("졸업식 사진을 업로드해보세요 (여러 장 가능)", type=["jpg", "png"], accept_multiple_files=True)
if files:
    cols = st.columns(3)
    for i, f in enumerate(files):
        with cols[i % 3]:
            st.image(f, use_column_width=True, caption=f.name)

st.divider()

# ===== Guestbook =====
st.markdown("### 💌 축하 메시지 방명록")
if "guestbook" not in st.session_state:
    st.session_state.guestbook = []

name = st.text_input("이름 (선택)")
msg = st.text_area("축하 메시지를 입력해주세요")

g1, g2 = st.columns(2)
with g1:
    if st.button("메시지 남기기"):
        if msg.strip():
            st.session_state.guestbook.append(
                {"name": name or "익명", "msg": msg.strip(), "time": datetime.now()}
            )
            st.success("메시지가 등록되었습니다! 🎉")
        else:
            st.warning("메시지를 입력해주세요!")
with g2:
    if st.button("초기화"):
        st.session_state.guestbook = []

st.write("---")
if st.session_state.guestbook:
    for note in reversed(st.session_state.guestbook):
        st.markdown(
            f"**{note['name']}** ({note['time'].strftime('%Y-%m-%d %H:%M')})  \n{note['msg']}"
        )
else:
    st.caption("아직 메시지가 없어요. 첫 메시지를 남겨보세요! 😊")

st.divider()
st.caption("© 2025 Made by hyemingway")
