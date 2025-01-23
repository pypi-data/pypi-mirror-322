import streamlit as st
from pages import pages, admin_pages

# 사용자의 모든 진입은 이곳을 거침

# session_state는 새로고침하거나 url 이동시 삭제됨, 따라서 클라이언트에 저장되지 않고, 매번 사용자 입력 필요.

# 무조건 hello 페이지(디폴트)로 이동 후 User Ticket을 조회하고 session_state 업데이트.
# session_state 상태에 따라서 intro, problem, answer, review 페이지중 하나로 이동 st.switch_page

# icon reference - https://fonts.google.com/icons?icon.set=Material+Symbols&icon.style=Outlined

pg = st.navigation(
    {
        "pages": pages,
        "administration": admin_pages,
    },
    position="hidden",
)
pg.run()
