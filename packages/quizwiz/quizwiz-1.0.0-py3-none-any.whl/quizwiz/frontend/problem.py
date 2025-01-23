import streamlit as st

from data.quiz_status import QuizStatus
from data.quizwiz_session import QuizwizSession
from utils import Log, Http, ImageElem, TextElem, PageManager, Common
from constant import Constant


def get_quizzes():
    param = {
        "label": QuizwizSession.get().event["label"],
        "method": Common.get_method_from_label(),
    }
    Log.ui_debug(f"get_quizzes: {param=}")

    quizzes = Http.send_request_json_response("quiz", "GET", params=param)
    if quizzes and len(quizzes):
        Log.ui_debug(f"Received {len(quizzes)} quiz from the server.")
        for quiz in quizzes:
            QuizwizSession.get().add_quiz(quiz)
        return True

    st.error(f"None quiz for label={QuizwizSession.get().event['label']}")
    st.warning(
        QuizwizSession.get().i18n_instance().translate("msg_problem_pre_check_quiz")
    )
    return False


def show_quizzes_batch():
    choices = [None] * len(QuizwizSession.get().quiz)
    for idx, quiz in enumerate(QuizwizSession.get().quiz):
        TextElem.draw_headerline()
        choices[idx] = show_quiz_with_option(idx, quiz)
    TextElem.draw_headerline()
    return choices


def show_quiz_with_option(idx, quiz):
    TextElem.show_question_field(idx + 1, quiz)
    options = quiz["contents"]
    # if multiple choices, label_visibility='visible'
    selected_option = st.radio(
        QuizwizSession.get()
        .i18n_instance()
        .translate("label_option_select_contents")
        .format(count=len(options)),
        label_visibility="collapsed",
        options=options,
        index=None,
        key=quiz["id"],
    )
    return selected_option


def submit_choices(choices):
    Log.ui_debug(f"submit_choices: len={len(choices)}, choices={choices}")
    for idx, choice in enumerate(choices):
        submit_answer(choice, idx)


def submit_answer(choice, idx: int):
    Log.ui_debug(f"quiz[{idx}]={QuizwizSession.get().quiz[idx]}")
    param = {
        "quiz_id": QuizwizSession.get().quiz[idx]["id"],  # quiz_id
        "knox_id": QuizwizSession.get().user_id(),
        "ticket_id": QuizwizSession.get().ticket["id"],
        "choice": choice,
        "method": QuizStatus.get_value(QuizStatus.READ_QUIZ_ID),
    }

    answer = Http.send_request_json_response("answer", "POST", params=param)
    if answer and len(answer):
        Log.ui_debug(f"Received {answer=}")
        QuizwizSession.get().add_answer(answer, idx)
        return True

    st.error(
        f"Can't submit_answer for event_code={QuizwizSession.get().event['event_code']} knox_id={QuizwizSession.get().user_id()}"
    )
    return False


def display_problem_message():
    word_user_name = QuizwizSession.get().user_name()
    msg_name_and_suffix = (
        "#### "
        + word_user_name
        + " "
        + QuizwizSession.get().i18n_instance().translate("word_name_suffix")
    )
    # Gil-dong.Hong 님,
    TextElem.translate_message(
        msg_name_and_suffix, focus_words=[(word_user_name, "green")], use_key=False
    )

    TextElem.translate_message(
        "msg_problem_submit_to_answer",
        focus_words=[("word_submit_answer", "blue")],
    )

    TextElem.translate_message(
        "msg_problem_time_to_end",
        focus_words=[("word_submit_answer", "blue"), ("word_end_time", "red")],
    )

    TextElem.translate_message(
        "msg_problem_lucky_draw",
        focus_words=[("word_lucky_draw", "violet")],
    )


PageManager.check_state_validity(Constant.APP_STATE_PROBLEM)
# problem 페이지 진입시, 상태를 다시 업데이트해야 backend에서 attempt_count 증가
Http.update_ticket_info(state=Constant.APP_STATE_PROBLEM)
# 여기부터 UX 표시
ImageElem.show_title_image(Constant.APP_STATE_PROBLEM)
display_problem_message()

if not QuizwizSession.get().is_quiz_valid():
    get_quizzes()

st.subheader("")  # 줄간격이 필요해보여서...

# 문제 출제
with st.form("problem_form"):
    if not QuizwizSession.get().choices_submitted:
        choice_items = show_quizzes_batch()

        if st.form_submit_button(
            QuizwizSession.get().i18n_instance().translate("word_submit_answer"),
            type="primary",
            use_container_width=True,
        ):
            if all(answer is not None for answer in choice_items):
                # 서버에서 정답 기록 및 사용자의 이벤트 참여 정보를 업데이트
                submit_choices(choice_items)
                Http.update_ticket_info(state=Constant.APP_STATE_ANSWER)
                QuizwizSession.get().choices_submitted = True
                st.switch_page("answer.py")
            else:
                Log.ui_debug(f"{choice_items=}")
                st.warning(
                    QuizwizSession.get()
                    .i18n_instance()
                    .translate("msg_problem_notice_all_selection")
                )
    else:
        st.write(
            QuizwizSession.get()
            .i18n_instance()
            .translate("msg_problem_notice_already_submit_answer")
        )
        if st.form_submit_button(
            QuizwizSession.get().i18n_instance().translate("word_submit_answer"),
            type="primary",
            use_container_width=True,
        ):
            st.switch_page("answer.py")

TextElem.display_github_voc()
