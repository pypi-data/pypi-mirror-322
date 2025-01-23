import pandas as pd
import streamlit as st

from data.quiz_status import QuizStatus
from data.quizwiz_session import QuizwizSession
from utils import Http, ImageElem, TextElem, GraphElem, Log, PageManager
from constant import Constant


def get_answer_table():
    answers = read_all_answers()
    df = pd.DataFrame(answers)
    return df


def read_all_answers():
    param = {"method": QuizStatus.get_value(QuizStatus.ALL_ANSWER)}
    response = Http.send_request_json_response("answer", "GET", params=param)
    return response if response else []


def show_answers():
    df = get_answer_table()

    for idx, (answer, quiz) in enumerate(
        zip(QuizwizSession.get().answer, QuizwizSession.get().quiz)
    ):
        TextElem.draw_headerline()
        show_answer(idx, answer, quiz)
        st.plotly_chart(
            GraphElem.draw_barplot_quiz_pass_rate(df, idx + 1, quiz["id"]),
            config={"displayModeBar": False},
        )

    TextElem.draw_headerline()


def show_answer(idx, answer, quiz):
    TextElem.show_question_field(idx + 1, quiz)

    try:
        selected_index = quiz["contents"].index(answer["choice"])
    except ValueError:
        selected_index = None

    st.radio(
        QuizwizSession.get()
        .i18n_instance()
        .translate("label_option_user_choice")
        .format(user=QuizwizSession.get().user_name(), choice=answer["choice"]),
        label_visibility="collapsed",
        options=quiz["contents"],
        index=selected_index,
        disabled=True,
        key=quiz["id"],
    )

    result_msg = f"{'⭕' if answer['result'] == 'Pass' else '❌'} {QuizwizSession.get().i18n_instance().translate('msg_correct_answer') if answer['result'] == 'Pass' else QuizwizSession.get().i18n_instance().translate('msg_wrong_answer')}"

    # Initialize base content with only the result message
    base_content = f'<div style="border: 1px dashed #000; padding: 10px;">\n<h6>{result_msg}</h6>\n'

    # correct_answer_msg
    correct_answer_msg = (
        f"<p>{QuizwizSession.get().i18n_instance().translate('word_answer')}: {quiz['answer']}</p>\n"
        if answer["result"] == "Fail"
        else ""
    )
    # Check if commentary is present and create msg_a accordingly
    msg_a = f'<p>{quiz["commentary"]}</p>\n' if quiz["commentary"] else ""

    # Check if reference URL is present and create msg_b accordingly
    msg_b = (
        (
            f'<h6><a href="{quiz["reference_url"]}" target="_blank">{QuizwizSession.get().i18n_instance().translate("word_reference")}</a></h6>\n'
        )
        if quiz["reference_url"]
        else ""
    )

    # Combine base content with msg_a and msg_b
    full_content = base_content + correct_answer_msg + msg_a + msg_b + "</div>"

    # Display the final content
    st.markdown(full_content, unsafe_allow_html=True)


def show_summary():
    pass_count = sum(
        1 for answer in QuizwizSession.get().answer if answer.get("result") == "Pass"
    )
    total_quizzes = len(QuizwizSession.get().answer)
    if total_quizzes == pass_count:
        TextElem.display_rain_icons(
            emoji="✨", font_size=20, falling_speed=5, animation_length="1"
        )
        compliment_message = (
            QuizwizSession.get().i18n_instance().translate("msg_compliment_100")
        )
        pass_count_color = f"[green]{pass_count}[/green]"
    else:
        if pass_count == 0:
            TextElem.display_rain_icons(
                emoji="🤬", font_size=20, falling_speed=5, animation_length="1"
            )
            compliment_message = (
                QuizwizSession.get().i18n_instance().translate("msg_compliment_0")
            )
            pass_count_color = f"[red]{pass_count}[/red]"
        else:
            TextElem.display_rain_icons(
                emoji="🥉", font_size=20, falling_speed=5, animation_length="1"
            )
            compliment_message = (
                QuizwizSession.get().i18n_instance().translate("msg_compliment_50")
            )
            pass_count_color = f"[orange]{pass_count}[/orange]"

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

    TextElem.md_colored(
        # f"* 📣 총 [blue]{total_quizzes}[/blue] 문제 중 {pass_count_color}개를 맞추셨어요."
        QuizwizSession.get()
        .i18n_instance()
        .translate("msg_pass_per_total")
        .format(total_quizzes=total_quizzes, pass_count_color=pass_count_color)
    )
    TextElem.md_colored(f"* {compliment_message}")
    TextElem.translate_message(
        "msg_study_answer_referernce",
        focus_words=[("word_reference", "blue"), ("word_problem_answer", "red")],
    )


def get_ticket_grade():
    # This method is same with update_ticket_result() operation

    if QuizwizSession.get().ticket.get("state") != Constant.APP_STATE_ANSWER:
        # To avoid unnecessary overhead at backend server side
        return

    param = {
        "ticket_id": QuizwizSession.get().ticket["id"],
        "method": QuizStatus.get_value(QuizStatus.READ_TICKET_ID),
    }

    tickets = Http.send_request_json_response("ticket", "GET", params=param, debug=True)
    if not tickets or not len(tickets):
        st.error(f"Invalid Ticket Id = {param['ticket_id']}")
        return

    Log.ui_debug(f"Received {len(tickets)} ticket from the server.")
    QuizwizSession.get().update_grade(tickets[0]["grade"])


PageManager.check_state_validity(Constant.APP_STATE_ANSWER)
if not QuizwizSession.get().answer:
    Http.update_ticket_info(state=Constant.APP_STATE_REVIEW)
    st.switch_page("review.py")

ImageElem.show_title_image(Constant.APP_STATE_ANSWER)
get_ticket_grade()
show_summary()

with st.form("answer_form"):
    show_answers()
    if st.form_submit_button(
        QuizwizSession.get().i18n_instance().translate("word_confirm_result"),
        type="primary",
        use_container_width=True,
    ):
        Http.update_ticket_info(state=Constant.APP_STATE_REVIEW)
        st.switch_page("review.py")

TextElem.display_github_voc()
