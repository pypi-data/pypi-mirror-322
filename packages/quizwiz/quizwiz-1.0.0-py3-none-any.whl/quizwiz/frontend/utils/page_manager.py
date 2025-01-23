from datetime import datetime
import time
import streamlit as st

from constant import Constant
from data.quiz_status import QuizStatus
from data.quizwiz_session import QuizwizSession
from utils import Http, TextElem


class PageManager:
    @classmethod
    def check_state_validity(cls, current_state):
        if not QuizwizSession.get().is_event_valid():
            cls._goto_valid_page(current_state, "hello")
            return

        is_ticket, ticket = Http.get_ticket()
        if not is_ticket:
            # only intro page can create new ticket
            if current_state == "intro":
                Http.create_ticket()
                Http.update_ticket_info(is_expired=False)
            next_state = "intro"
        else:
            next_state = ticket["state"]
        cls._goto_valid_page(current_state, next_state)

    @classmethod
    def _goto_valid_page(cls, current_state, next_state):
        if not next_state or current_state == next_state:
            return
        st.switch_page(cls._get_page_from_state(next_state))

    @classmethod
    def _get_page_from_state(cls, state):
        if (
            state == "problem"
            and QuizwizSession.get().event["problem_mode"] == Constant.PROBLEM_MODE_STEP
        ):
            return state + "_step.py"
        else:
            return state + ".py"

    @classmethod
    def show_event_status_message(cls, event):
        is_welcome_message = False
        event_status = cls._get_event_status(event)
        if event_status[0] == QuizStatus.UPCOMING_EVENT:
            TextElem.show_upcoming_event(event)
            with st.spinner("📣 5초 후, 시작 페이지 이동..."):
                time.sleep(2)
                st.switch_page("hello.py")
        elif event_status[0] == QuizStatus.ONGOING_EVENT:
            is_welcome_message = True
            TextElem.welcome_event_message(event)
            TextElem.show_ongoing_event(event)
        elif event_status[0] == QuizStatus.EXPIRED_EVENT:
            TextElem.show_expired_event(event)
        else:
            TextElem.show_unknown_event()

        if not is_welcome_message:
            TextElem.welcome_event_message(event)

    @classmethod
    def _check_event_status(cls, started_at, expired_at, current_datetime=None):
        current_datetime = (
            datetime.now() if current_datetime is None else current_datetime
        )
        # return (STATUS, STRING)
        return (
            (QuizStatus.UPCOMING_EVENT, "이벤트 시작 전")
            if current_datetime < started_at
            else (
                (QuizStatus.EXPIRED_EVENT, "이벤트 종료")
                if current_datetime > expired_at
                else (QuizStatus.ONGOING_EVENT, "이벤트 진행 중")
            )
        )

    @classmethod
    def _parse_datetime(cls, datetime_str):
        try:
            # 방법 1: 마이크로초 있는 경우
            return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
            # 방법 2: 마이크로초 없는 경우
            return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")

    @classmethod
    def _get_event_status(cls, event):
        if not event:
            return (QuizStatus.UNKNOWN_EVENT, "Unknown event")

        started_at = cls._parse_datetime(event["started_at"])
        expired_at = cls._parse_datetime(event["expired_at"])
        return cls._check_event_status(started_at, expired_at)
