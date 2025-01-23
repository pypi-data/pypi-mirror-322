import streamlit as st
import random

from data.quiz_status import QuizStatus
from data.quizwiz_session import QuizwizSession
from utils import Log, Http, ImageElem, TextElem, PageManager, Common
from constant import Constant


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
        "msg_problem_notice_next_problem",
        focus_words=[("word_next_problem", "blue")],
    )

    TextElem.translate_message(
        "msg_problem_cheer_up",
        focus_words=[("word_until_end", "red")],
    )


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


def submit_answer(choice, quiz_index):
    Log.ui_debug(f"quiz[{quiz_index}]={QuizwizSession.get().quiz[quiz_index]}")
    param = {
        "quiz_id": QuizwizSession.get().quiz[quiz_index]["id"],  # quiz_id
        "knox_id": QuizwizSession.get().user_id(),
        "ticket_id": QuizwizSession.get().ticket["id"],
        "choice": choice,
        "method": QuizStatus.get_value(QuizStatus.READ_QUIZ_ID),
    }

    answer = Http.send_request_json_response("answer", "POST", params=param)
    if answer and len(answer):
        Log.ui_debug(f"Received {answer=}")
        QuizwizSession.get().add_answer(answer, quiz_index)
        QuizwizSession.get().increase_quiz_index(quiz_index)  # To display next quiz
        return True

    st.error(
        f"Can't submit_answer for event_code={QuizwizSession.get().event['event_code']} knox_id={QuizwizSession.get().user_id()}"
    )
    return False


def show_quiz_ox():
    quiz_index = QuizwizSession.get().get_quiz_index()
    quiz = QuizwizSession.get().quiz[quiz_index]

    TextElem.show_question_field(quiz_index + 1, quiz)

    st.html(
        """
        <style>
        [data-testid="stButton"]:has([data-testid="stBaseButton-primary"],[data-testid="stBaseButton-secondary"]) {
            display: flex;
            justify-content: center;
            :hover {
                color: rgb(255, 255, 255);
            }
        }
        [data-testid="stBaseButton-primary"],[data-testid="stBaseButton-secondary"] {
            height: 12.0rem;
            width: 12.0rem;
            color: rgb(255, 255, 255);
            div p {
                font-size: 10.0rem;
            }
        }
        [data-testid="stBaseButton-primary"] {
            background-color: rgb(0, 255, 0) !important;
            border: 1px solid rgb(0, 255, 0) !important;
            color: rgb(0, 100, 0);
        }
        [data-testid="stBaseButton-secondary"] {
            background-color: rgb(255, 50, 50) !important;
            border: 1px solid rgb(255, 50, 50) !important;
            color: rgb(100, 0, 0);
        }
        </style>
        """
    )

    for col, ox, btn_type in zip(
        st.columns(2), quiz["contents"], ["primary", "secondary"]
    ):
        with col:
            if st.button(
                ox,
                type=btn_type,
                use_container_width=True,
                on_click=submit_answer,
                args=[ox, quiz_index],
            ):
                pass


def show_quiz_with_option():
    quiz_index = QuizwizSession.get().get_quiz_index()
    quiz = QuizwizSession.get().quiz[quiz_index]

    TextElem.show_question_field(quiz_index + 1, quiz)
    options = quiz["contents"]
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

    if selected_option is not None:
        submit_answer(selected_option, quiz_index)
        # without below code, can't go next quiz
        st.rerun()


def get_quiz_type() -> str:
    quiz_index = QuizwizSession.get().get_quiz_index()
    quiz = QuizwizSession.get().quiz[quiz_index]
    return "ox_style" if quiz["contents"] in (["O", "X"], ["X", "O"]) else "common"


def show_progress_bar(current_idx, total):
    if current_idx < 0 or total <= 0:
        return

    st.html(
        """
        <style>
        .stProgress > div > div > div > div {
            background-color: #007AFF; /* Deep blue */
            # background-color: #34C759; /* elegant green */            
        }
        .stProgress > div > div > div {
            background-color: #D3D3D3;  /* light silver */
            # background-color: #E0E0E0;  /* Light grey */
            height: 1.0rem;  /* Adjusts the height of the progress bar */
        }
        /* Optional styling for markdown content inside stProgress */
        .stProgress [data-testid="stMarkdownContainer"] p {
            font-size: 1rem;
            text-align: right;            
        }
        </style>
        """
    )

    progress_messages = [
        "Step {current} of {total} completed",
        "{current} out of {total} tasks done",
        "Progress: {current}/{total} steps",
        "You’ve completed {current} of {total} steps",
        "Currently on step {current} of {total}",
        "{current} steps down, {remaining} to go!",  # remaining으로 수정
    ]

    current = min(current_idx + 1, total)  # 현재 진행 중인 단계
    remaining = total - current  # 남은 단계 계산
    progress_message = random.choice(progress_messages).format(
        current=current, total=total, remaining=remaining  # remaining 추가
    )
    st.progress(current / total, text=f"{progress_message}")


def show_quizzes_step():
    current_idx = QuizwizSession.get().get_quiz_index()
    total_quiz = len(QuizwizSession.get().quiz)

    if current_idx < total_quiz:
        TextElem.draw_headerline()
        if get_quiz_type() == "ox_style":
            show_quiz_ox()
        else:
            show_quiz_with_option()
        show_progress_bar(current_idx, total_quiz)
    else:
        Http.update_ticket_info(state=Constant.APP_STATE_ANSWER)
        st.switch_page("answer.py")


PageManager.check_state_validity(Constant.APP_STATE_PROBLEM)
# problem_step 페이지 진입시, 상태를 다시 업데이트해야 backend에서 attempt_count 증가
if not QuizwizSession.get().is_ticket_info_updated():
    Http.update_ticket_info(state=Constant.APP_STATE_PROBLEM)
    # 1번만 실행 필요 (∵ problem_step은 문제 풀이할때마다 새로고침❗)
    QuizwizSession.get().set_ticket_info_updated(True)

# 여기부터 UX 표시
ImageElem.show_title_image(Constant.APP_STATE_PROBLEM)
display_problem_message()

if not QuizwizSession.get().is_quiz_valid():
    get_quizzes()

show_quizzes_step()

TextElem.display_github_voc()
