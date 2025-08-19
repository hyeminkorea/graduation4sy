# app.py — Streamlit guestbook stored in Google Sheets + image rotation
import streamlit as st
from datetime import datetime
from PIL import Image, ImageOps
import gspread
from gspread.exceptions import WorksheetNotFound

st.set_page_config(page_title="서영 졸업 축하 🎓", page_icon="🎉", layout="wide")

# ===== Google Sheets helpers =====
def get_ws():
    """Authorize from st.secrets and return the guestbook worksheet (create if missing)."""
    sa_info = st.secrets["gcp_service_account"]
    client = gspread.service_account_from_dict(sa_info)
    sh = client.open_by_key(st.secrets["gsheets"]["guestbook_id"])
    ws_name = st.secrets["gsheets"].get("worksheet_name", "guestbook")
    try:
        ws = sh.worksheet(ws_name)
    except WorksheetNotFound:
        ws = sh.add_worksheet(title=ws_name, rows=1000, cols=3)
        ws.append_row(["ts", "name", "msg"], value_input_option="USER_ENTERED")
    return ws

@st.cache_data(ttl=5)
def load_messages():
    """Read all records from the sheet (cached for a few seconds)."""
    ws = get_ws()
    records = ws.get_all_records()  # [{'ts':..., 'name':..., 'msg':...}, ...]
    return records

def append_message(name: str, msg: str):
    ws = get_ws()
    ws.append_row(
        [datetime.now().isoformat(timespec="minutes"), name, msg],
        value_input_option="USER_ENTERED",
    )
    load_messages.clear()  # bust cache so the new item appears immediately

# ===== Hero =====
st.title("🎓 한서영 졸업 축하 페이지")
st.subheader("그동안의 노력과 열정에 박수를 보내요 👏")
st.write("새로운 시작도 우리가 함께 응원할게요! 🌱")

colA, colB = st.columns(2)
with colA:
    if st.button("축하 풍선 🎈", use_container_width=True):
        st.balloons()

st.divider()

# ===== Info =====
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

# ===== Photo Gallery with rotation =====
st.markdown("### 📸 사진 갤러리 (선택택 가능)")
files = st.file_uploader(
    "졸업식 사진을 업로드해보세요 (여러 장 가능, jpg/png)", type=["jpg", "jpeg", "png"], accept_multiple_files=True
)

if files:
    st.caption("각 사진 아래 버튼으로 90° 단위 회전/리셋이 가능합니다.")
    cols = st.columns(3)
    for i, f in enumerate(files):
        key_base = f"{f.name}-{i}"
        rot_key = f"rot_{key_base}"
        if rot_key not in st.session_state:
            st.session_state[rot_key] = 0

        img = Image.open(f)
        img = ImageOps.exif_transpose(img)  # auto-fix orientation

        rot = st.session_state[rot_key]
        shown = img.rotate(-rot, expand=True)  # clockwise +90 => -90 here

        with cols[i % 3]:
            st.image(shown, use_column_width=True, caption=f"{f.name} ({rot}°)")
            b1, b2, b3 = st.columns(3)
            if b1.button("⟲ -90°", key=f"left_{key_base}"):
                st.session_state[rot_key] = (rot - 90) % 360
                st.experimental_rerun()
            if b2.button("↻ +90°", key=f"right_{key_base}"):
                st.session_state[rot_key] = (rot + 90) % 360
                st.experimental_rerun()
            if b3.button("Reset", key=f"reset_{key_base}"):
                st.session_state[rot_key] = 0
                st.experimental_rerun()

st.divider()

# ===== Guestbook (Google Sheets) =====
st.markdown("### 💌 축하 메시지 방명록 (모든 방문자에게 공유)")

if "name" not in st.session_state:
    st.session_state.name = ""
if "msg" not in st.session_state:
    st.session_state.msg = ""

st.text_input("이름 (선택)", key="name")
st.text_area("축하 메시지를 입력해주세요", key="msg")

g1, g2 = st.columns(2)
with g1:
    if st.button("메시지 남기기"):
        n = (st.session_state.name or "익명").strip()
        m = (st.session_state.msg or "").strip()
        if m:
            try:
                append_message(n, m)
                st.session_state.msg = ""
                st.success("메시지가 등록되었습니다! 🎉")
            except Exception as e:
                st.error(f"저장 오류: {e}")
        else:
            st.warning("메시지를 입력해주세요!")
with g2:
    if st.button("새로고침"):
        load_messages.clear()
        st.experimental_rerun()

st.write("---")

try:
    rows = load_messages()
    if rows:
        for row in reversed(rows):  # latest first
            st.markdown(f"**{row['name']}** ({row['ts']})  \n{row['msg']}")
    else:
        st.caption("아직 메시지가 없어요. 첫 메시지를 남겨보세요! 😊")
except Exception as e:
    st.error(f"읽기 오류: {e}\nSecrets 설정 및 시트 공유 상태를 확인해주세요.")

st.divider()
st.caption("© 2025 Made with ❤️ for Han Seo-young — hyemingway")


