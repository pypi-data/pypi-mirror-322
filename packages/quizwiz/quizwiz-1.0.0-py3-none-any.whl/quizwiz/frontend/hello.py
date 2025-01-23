import uuid
from urllib.parse import urlencode
import pandas as pd
import streamlit as st
from datetime import datetime
from streamlit_extras.grid import grid
from streamlit_option_menu import option_menu
from streamlit_cookies_controller import CookieController
import streamlit.components.v1 as components


from config import Config
from constant import Constant
from data.quizwiz_session import QuizwizSession
from i18n import I18n
from utils import Log, Http, ImageElem, TextElem

# 세션 상태에서 I18n 인스턴스를 유지하거나 새로 생성
QuizwizSession.get().ensure_i18n_initialized(I18n())


def login():  # AD FS에 인증 요청을 보내는 URL 생성 함수
    nonce_val = uuid.uuid4().urn
    nonce_val = nonce_val[9:]

    idp_url = Config.IDP_CONFIG["Idp.EntityID"]

    auth_param = "?client_id=" + Config.IDP_CONFIG["Idp.ClientID"]
    auth_param += "&redirect_uri=" + Config.SP_CONFIG["SP.RedirectUrl"]
    auth_param += "&response_mode=form_post"
    auth_param += "&response_type=id_token"
    auth_param += "&scope=openid+profile"
    auth_param += "&nonce=" + nonce_val
    url = idp_url + auth_param
    return url


def verify_auth_info(user_id, name, stamp, target_token):
    query_dict = {
        "loginid": user_id,
        "username": name,
        "timestamp": stamp,
        "token": target_token,
    }

    # get 요청으로 streamlit에 전달하기 위해 query string으로 변환
    api_url = f"{Config.AUTH_URL}/auth/status?{urlencode(query_dict)}"
    response = Http.send_request_url(api_url, "GET", verify=False)
    if not response:
        return False

    Log.ui_debug(f"Success to verify_auth_info {api_url} {response.json()}")
    return True


def create_custom_button_style():
    st.html(
        """<style>
                        button.login {
                            font: inherit;
                            background-color: #f0f0f0;
                            border: 0;
                            color: #242424;
                            border-radius: 0.5em;
                            font-size: 0.8rem;
                            padding: 0.00em 0.8em;
                            font-weight: 1000;
                            text-shadow: 0 0.0625em 0 #fff;
                            box-shadow: inset 0 0.0625em 0 0 #f4f4f4, 0 0.0625em 0 0 #efefef, 0 0.125em 0 0 #ececec, 0 0.25em 0 0 #e0e0e0, 0 0.3125em 0 0 #dedede, 0 0.375em 0 0 #dcdcdc, 0 0.425em 0 0 #cacaca, 0 0.425em 0.5em 0 #cecece;
                            transition: 0.15s ease;
                            pointer: cursor;
                        }

                        button.login:active, button.login:hover {
                            translate: 0 0.225em;
                            box-shadow: inset 0 0.03em 0 0 #f4f4f4, 0 0.03em 0 0 #efefef, 0 0.0625em 0 0 #ececec, 0 0.125em 0 0 #e0e0e0, 0 0.125em 0 0 #dedede, 0 0.2em 0 0 #dcdcdc, 0 0.225em 0 0 #cacaca, 0 0.225em 0.375em 0 #cecece;
                            cursor: pointer;
                        }

                        .parent {
                            text-align: right;
                        }

                        .child {
                            display: inline-block;
                        }
                   </style>
                """
    )


def display_home_menu():
    menu_obj = option_menu(
        None,
        ["Home", "Settings"],
        icons=["house", "gear"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "orange", "font-size": "25px"},
            "nav-link": {
                "font-size": "20px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#eee",
            },
            "nav-link-selected": {"background-color": "#08c7cc"},
        },
        key="home_menu",
    )
    return menu_obj


STATUS_ONGOING = "💦 Ongoing"
STATUS_UPCOMING = "👁‍🗨 Upcoming"
STATUS_EXPIRED = "💥 Expired"


def get_status(row):
    now = datetime.now()
    if now < row["started_at"]:
        return STATUS_UPCOMING  # 시작 시간이 현재 시간보다 나중인 경우
    elif now > row["expired_at"]:
        return STATUS_EXPIRED  # 만료 시간이 현재 시간보다 이전인 경우
    else:
        return STATUS_ONGOING  # 현재 시간이 시작 시간과 만료 시간 사이인 경우


def notify_empty_event():
    TextElem.translate_message(
        "msg_event_empty", focus_words=[("word_event_empty", "red")]
    )


def show_event_list():
    msg_past_event = QuizwizSession.get().i18n_instance().translate("msg_past_event")

    with st.expander(msg_past_event):
        is_exist, events = Http.get_event_list()

        if not is_exist:
            notify_empty_event()
            return

        # JSON 데이터를 DataFrame 형식으로 변환한 후, index를 제거합니다.
        df = pd.json_normalize(events)
        df["started_at"] = pd.to_datetime(
            df["started_at"], format="%Y-%m-%d %H:%M:%S", errors="coerce"
        )
        df["expired_at"] = pd.to_datetime(
            df["expired_at"], format="%Y-%m-%d %H:%M:%S", errors="coerce"
        )

        df = df.query("started_at.notna() and expired_at.notna() and is_visible").loc[
            :,
            [
                "event_code",
                "promotion_url",
                "winner_announcement_url",
                "started_at",
                "expired_at",
            ],
        ]

        if df.empty:
            notify_empty_event()
            return

        TextElem.translate_message(
            "msg_event_history",
            focus_words=[("word_event_code", "green")],
        )

        # url 열을 마크다운 링크 형식으로 변환합니다.
        df["promotion_url"] = df["promotion_url"].apply(
            lambda url: (
                f'<a href="{url}" target="_blank">💫 promotion</a>' if url else ""
            )
        )
        df["winner_announcement_url"] = df["winner_announcement_url"].apply(
            lambda url: (
                # fmt: off
                f'<a href="{url}" target="_blank">🎉 lucky_draw</a>' if url else ""
                # fmt: on
            )
        )
        df["status"] = df.apply(get_status, axis=1)

        # status 열의 정렬 우선순위 설정
        status_order = [STATUS_ONGOING, STATUS_UPCOMING, STATUS_EXPIRED]
        df["status_order"] = pd.Categorical(
            df["status"], categories=status_order, ordered=True
        )
        # 정렬 수행: 먼저 status_order로, 그다음 expired_at으로 오름차순
        df = df.sort_values(by=["status_order", "expired_at"])
        # status_order 열 제거 후 결과 출력
        df = df.drop(columns=["status_order"])

        # 새로운 형식으로 변환하여 'period' 열 생성
        df["period"] = (
            df["started_at"].dt.strftime("%y/%m/%d")
            + " - "
            + df["expired_at"].dt.strftime("%m/%d")
        )

        df = df[
            [
                "status",
                "event_code",
                "promotion_url",
                "winner_announcement_url",
                "period",
            ]
        ]

        df.columns = [
            QuizwizSession.get().i18n_instance().translate("column_status"),
            QuizwizSession.get().i18n_instance().translate("column_event_code"),
            QuizwizSession.get().i18n_instance().translate("column_promote"),
            QuizwizSession.get().i18n_instance().translate("column_winners"),
            QuizwizSession.get().i18n_instance().translate("column_schedule"),
        ]

        # 테이블 헤더를 center 정렬하기 위해 스타일 추가
        html_table = df.to_html(escape=False, index=False)
        styled_table = (
            """
            <style>
                body {
                    font-family: Arial, sans-serif;
                    font-size: 12px;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                }
                th, td {
                    border: 1px solid #ddd;
                    padding: 8px;
                    text-align: center;
                }
                th {
                    background-color: #f2f2f2;
                }
                tr:nth-child(even) {
                    background-color: #f9f9f9;
                }
            </style>
            """
            + html_table
        )
        # 더 확실하게(강제적으로) 렌더링
        components.html(styled_table, height=200, scrolling=True)


def select_box_i18n():
    language_list = ["ko", "en", "zh"]
    choose_language_label = (
        QuizwizSession.get().i18n_instance().translate("msg_choose_language")
    )

    selected_language = st.selectbox(
        choose_language_label,
        label_visibility="visible",
        options=language_list,
        index=language_list.index(QuizwizSession.get().get_language()),
    )

    # 언어 변경 기능 (사용자가 선택할 때마다 갱신)
    if selected_language != QuizwizSession.get().get_language():
        QuizwizSession.get().set_language(selected_language)
        QuizwizSession.get().i18n_instance().update_language(selected_language)
        st.rerun()


def check_am_i_admin(knox_id):
    """
    Check am_i_admin via transferring knox_id to backend server
    """
    admins = Http.get_admin_info(knox_id)
    QuizwizSession.get().set_you_are_admin(admins[0])


# Start Page -----
create_custom_button_style()

known_event_code = ""
controller = CookieController()

if "event" in st.query_params:
    known_event_code = st.query_params["event"]
    controller.set(Constant.COOKIE_KEY_EVENT_CODE, known_event_code)

if (
    "loginid" in st.query_params
    and "username" in st.query_params
    and "timestamp" in st.query_params
    and "token" in st.query_params
):
    loginid = st.query_params["loginid"]
    username = st.query_params["username"]
    timestamp = st.query_params["timestamp"]
    token = st.query_params["token"]
    if verify_auth_info(loginid, username, timestamp, token) is True:
        QuizwizSession.get().login["knox_id"] = loginid
        QuizwizSession.get().login["user_name"] = username
    st.query_params.clear()
elif Config.DEBUG_ID is not None:  # for dev
    QuizwizSession.get().login["knox_id"] = Config.DEBUG_ID
    QuizwizSession.get().login["user_name"] = Config.DEBUG_ID
    if Config.DEBUG_ID == "admin":
        QuizwizSession.get().set_you_are_admin(True)

check_am_i_admin(QuizwizSession.get().login["knox_id"])

# CSS style definitions
if QuizwizSession.get().is_admin():
    menus = display_home_menu()
    if menus == "Settings":
        st.switch_page("admins/setup.py")

ImageElem.show_title_image(Constant.APP_STATE_HELLO)
col1, col2 = st.columns([7, 2])
with col1:
    TextElem.draw_headerline(
        label=": Where Knowledge Meets Fun!",
        description="🎆Have a good time with QuizWiz🎆",
        color="blue-green-70",
    )
with col2:
    select_box_i18n()


# Get a cookie
cookie = controller.get(Constant.COOKIE_KEY_EVENT_CODE)
if cookie is not None:
    known_event_code = cookie


if not QuizwizSession.get().is_login_valid():
    # <a> tag로 AD FS Site에 인증 요청하는 버튼 생성
    st.markdown(
        f"""
        #### To access QuizWiz services, DS AD login is required.
        <button class="login"><a href="{login()}" target="_self"> Login </a></button>
        """,
        unsafe_allow_html=True,
    )
    TextElem.translate_message(
        "msg_quiz_wiz_intro1",
        focus_words=[("word_QuizWiz", "blue")],
    )
    TextElem.translate_message(
        "msg_quiz_wiz_intro2a",
        focus_words=[("word_event_code", "green")],
    )
else:
    menu_grid = grid([6, 1], vertical_align="bottom")
    menu_grid.write(
        QuizwizSession.get().i18n_instance().translate("msg_hello_to_user")
        + QuizwizSession.get().login["user_name"]
    )
    word_logout = QuizwizSession.get().i18n_instance().translate("logout")
    menu_grid.markdown(
        f"""
        <button class="login"><a href="{Config.IDP_CONFIG["Idp.SignoutUrl"]}" target="_self"> {word_logout} </a></button>
        """,
        unsafe_allow_html=True,
    )

    TextElem.translate_message(
        "msg_quiz_wiz_intro1",
        focus_words=[("word_QuizWiz", "blue")],
    )
    TextElem.translate_message(
        "msg_quiz_wiz_intro2",
        focus_words=[("word_event_code", "green")],
    )

    with st.form("hello_form"):
        event_code = st.text_input(
            label=QuizwizSession.get().i18n_instance().translate("txt_event_input"),
            value=known_event_code,
        )

        if st.form_submit_button(
            QuizwizSession.get().i18n_instance().translate("btn_event_participation"),
            type="primary",
            use_container_width=True,
        ):
            QuizwizSession.reset_except_login()
            is_event_valid_flag, event_data = Http.get_event(event_code)
            if event_code and is_event_valid_flag:
                QuizwizSession.get().init_event(event_data)
                st.switch_page("intro.py")
            else:
                st.warning(
                    QuizwizSession.get()
                    .i18n_instance()
                    .translate("msg_invalid_event_code_warning")
                )

    show_event_list()
    TextElem.display_github_voc()


if Config.is_prod_auth():
    st.html(
        '<img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=quizwiz-prod"/>'
    )
    st.html(
        '<img referrerpolicy="no-referrer-when-downgrade" src="https://pando.samsungds.net:8008/matomo.php?idsite=5&amp;rec=1" style="border:0" alt="" />'
    )
