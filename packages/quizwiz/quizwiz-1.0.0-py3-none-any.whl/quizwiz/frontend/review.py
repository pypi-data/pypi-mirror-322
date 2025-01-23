import time

import pandas as pd
import streamlit as st

from data.quiz_status import QuizStatus
from data.quizwiz_session import QuizwizSession
from i18n import I18n
from utils import Http, ImageElem, TextElem, GraphElem, PageManager
from constant import Constant


def get_statistics_data(evt_code):
    return {
        "current_rank": get_current_rank(evt_code),
        "best_rank": get_best_rank(evt_code),
    }


def read_ticket(evt_code):
    param = {
        "event_code": evt_code,
        "method": QuizStatus.get_value(QuizStatus.READ_TICKET_CODE),
    }
    response = Http.send_request_json_response("ticket", "GET", params=param)
    if not response:
        return None

    return get_ticket_table_with_event_code(evt_code, response)


def get_current_rank(evt_code):
    param = {
        "event_code": evt_code,
        "ticket_id": QuizwizSession.get().ticket["id"],
    }
    return get_ranking(param)


def get_best_rank(evt_code):
    param = {
        "event_code": evt_code,
        "knox_id": QuizwizSession.get().ticket["knox_id"],
    }
    return get_ranking(param)


def get_ticket_table_with_event_code(evt_code, tickets) -> pd.DataFrame:
    df = pd.DataFrame(tickets)
    df = df[df["event_code"] == evt_code]
    # created_at AND finished_at이 NULL이 아닌 행만 선택
    filtered_df = df[
        (df["created_at"].notnull()) & (df["finished_at"].notnull())
    ].copy()
    return filtered_df


def display_ticket_statistics_description(df: pd.DataFrame):
    # 1. 총 몇명이 몇번 이벤트에 참여한 정보
    total_unique_users = df["knox_id"].nunique()

    # 2. 현재 사용자는 몇번 이벤트에 참여했고, max, min, avg 정보
    df_mine = df[df["knox_id"] == QuizwizSession.get().ticket["knox_id"]]["grade"]

    # 3. show summary
    TextElem.md_colored(
        QuizwizSession.get()
        .i18n_instance()
        .translate("msg_review_get_grade")
        .format(grade=round(QuizwizSession.get().ticket["grade"]))
    )
    TextElem.md_colored(
        QuizwizSession.get()
        .i18n_instance()
        .translate("msg_review_count_max_min_avg")
        .format(
            count=len(df_mine),
            max=round(df_mine.max()),
            min=round(df_mine.min()),
            avg=round(df_mine.mean()),
        )
    )
    TextElem.md_colored(
        QuizwizSession.get()
        .i18n_instance()
        .translate("msg_review_total_user_count")
        .format(total_user=total_unique_users, count=len(df))
    )
    TextElem.md_colored(
        QuizwizSession.get()
        .i18n_instance()
        .translate("msg_review_1st_grade_avg")
        .format(max_grade=round(df["grade"].max()), avg=round(df["grade"].mean()))
    )


def display_ticket_statistics_header(df: pd.DataFrame, stats):
    score = round(QuizwizSession.get().ticket["grade"])
    current_ranking = stats["current_rank"]
    df_mine = df[df["knox_id"] == QuizwizSession.get().ticket["knox_id"]]["grade"]
    TextElem.md_colored(
        QuizwizSession.get()
        .i18n_instance()
        .translate("msg_review_final_result")
        .format(score=score, ranking=current_ranking)
    )
    TextElem.md_colored(
        QuizwizSession.get()
        .i18n_instance()
        .translate("msg_review_your_grade_ranking")
        .format(
            user=QuizwizSession.get().user_name(),
            grade=round(df_mine.max()),
            ranking=stats["best_rank"],
        )
    )


def get_ranking(param):
    response = Http.send_request_json_response("ranking", "GET", params=param)
    data = response if response else []
    return data


def display_table_with_markdown(data, columns_names=None, columns=None):
    # 헤더 생성
    markdown_table = " | ".join(columns_names) + "\n"
    markdown_table += " | ".join(["---"] * len(columns)) + "\n"

    # 각 행에 대한 데이터 추가
    for dic in data:
        markdown_table += " | ".join([str(dic[key]) for key in columns]) + "\n"
    st.markdown(markdown_table, unsafe_allow_html=True)


def create_custom_ranking_table_style():
    st.html(
        """<style>
                table {
                    width: 100%;
                    margin-bottom: 1rem;
                    vertical-align: top;
                    border-color: var(--bs-table-border-color);
                }
                table>:not(caption)>*>* {
                    border-bottom-width: 1px !important;
                }
                table>thead {
                    vertical-align: bottom;
                }
                tbody, td, tfoot, th, thead, tr {
                    border-color: inherit;
                    border-style: solid;
                    border-width: 0 !important;
                }
            </style>
        """
    )


def show_statistics(evt_code, df_tickets):
    stats = get_statistics_data(evt_code)
    display_ticket_statistics_header(df_tickets, stats)
    display_ticket_statistics_description(df_tickets)
    st.plotly_chart(GraphElem.display_ticket_statistics_bubble_chart(df_tickets))


def show_ranking(user_rank_info, df_tickets):
    create_custom_ranking_table_style()

    st.subheader("🏆Ranking")
    display_table_with_markdown(
        data=user_rank_info,
        columns_names=["순위", "이름", "Knox ID", "점수", "풀이 시간(초)"],
        columns=[
            "rank",
            "encrypted_user_name",
            "encrypted_knox_id",
            "grade",
            "seconds_time",
        ],
    )
    st.subheader("")
    st.subheader(
        QuizwizSession.get().i18n_instance().translate("msg_review_grade_ratio")
    )
    if df_tickets is not None:
        st.plotly_chart(
            GraphElem.display_pie(df_tickets, "count", "grade"),
            theme="streamlit",
            use_container_width=True,
        )


def get_rank_data(evt_code):
    param = {
        "event_code": evt_code,
        "count": 15,
    }
    data = get_ranking(param)
    data = [{**x, "seconds_time": x["time"] / 1000000} for x in data]
    return data


def handle_spinner_invalid_event_code(evt_code):
    if not evt_code:
        st.switch_page("hello.py")

    with st.spinner(
        QuizwizSession.get().i18n_instance().translate("msg_review_invalid_event_code")
    ):
        time.sleep(2)
        st.switch_page("hello.py")


def handle_spinner_no_participants():
    with st.spinner(
        QuizwizSession.get().i18n_instance().translate("msg_review_no_participant")
    ):
        time.sleep(2)
        st.switch_page("hello.py")


# 이벤트 유효성 및 코드 가져오기
event_data = None
if QuizwizSession.get().is_event_valid():
    ranking_only = False
    event_code = QuizwizSession.get().event["event_code"]
else:
    ranking_only = True
    QuizwizSession.get().ensure_i18n_initialized(I18n())
    QuizwizSession.get().i18n_instance().update_language("ko")
    event_code = st.query_params.get("event")
    is_event_valid_flag, event_data = Http.get_event(event_code)
    if not is_event_valid_flag:
        handle_spinner_invalid_event_code(event_code)

# Get data, Make dataframes
rank_data = get_rank_data(event_code)
if not rank_data:
    handle_spinner_no_participants()

df_ticket_list = read_ticket(event_code)
st.balloons()


ImageElem.show_title_image(Constant.APP_STATE_REVIEW)

if not ranking_only:
    PageManager.check_state_validity(Constant.APP_STATE_REVIEW)
    show_statistics(event_code, df_ticket_list)
else:
    PageManager.show_event_status_message(event_data)

show_ranking(rank_data, df_ticket_list)

if not ranking_only:
    if st.button(
        QuizwizSession.get().i18n_instance().translate("btn_retry"),
        type="primary",
        use_container_width=True,
    ):
        Http.update_ticket_info(is_expired=True)
        QuizwizSession.reset_except_login()
        st.switch_page("hello.py")

TextElem.display_github_voc()
