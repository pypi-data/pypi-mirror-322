import streamlit as st
from streamlit_cookies_controller import CookieController

from constant import Constant
from data.quizwiz_session import QuizwizSession
from utils import Http, ImageElem, TextElem, PageManager


def display_intro_message():
    word_user_name = QuizwizSession.get().user_name()
    msg_name_and_suffix = (
        word_user_name
        + " "
        + QuizwizSession.get().i18n_instance().translate("word_name_suffix")
    )
    # Gil-dong.Hong 님,
    TextElem.translate_message(
        msg_name_and_suffix, focus_words=[(word_user_name, "green")], use_key=False
    )

    TextElem.translate_message(
        "msg_intro_ready_to_solve",
        focus_words=[("word_solve_problem", "blue")],
    )

    TextElem.translate_message(
        "msg_intro_time_to_start",
        focus_words=[("word_start_time", "red")],
    )

    TextElem.translate_message(
        "msg_intro_lucky_draw",
        focus_words=[("word_lucky_draw", "violet")],
    )


def init_cookie():
    controller = CookieController()
    controller.set(
        Constant.COOKIE_KEY_EVENT_CODE, QuizwizSession.get().event["event_code"]
    )


PageManager.check_state_validity(Constant.APP_STATE_INTRO)
ImageElem.show_title_image(Constant.APP_STATE_INTRO)
PageManager.show_event_status_message(QuizwizSession.get().event)
display_intro_message()

init_cookie()

if st.button(
    QuizwizSession.get().i18n_instance().translate("word_solve_problem"),
    type="primary",
    use_container_width=True,
):
    Http.update_ticket_info(state=Constant.APP_STATE_PROBLEM)
    if QuizwizSession.get().event["problem_mode"] == Constant.PROBLEM_MODE_STEP:
        st.switch_page("problem_step.py")

    st.switch_page("problem.py")

TextElem.display_github_voc()
