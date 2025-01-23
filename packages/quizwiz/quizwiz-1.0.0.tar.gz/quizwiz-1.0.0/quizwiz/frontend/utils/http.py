import requests
import streamlit as st

from config import Config
from constant import Constant
from data.quiz_status import QuizStatus
from data.quizwiz_session import QuizwizSession
from utils import Log


class Http:
    @classmethod
    def send_request_json_response(
        cls, path, method, params=None, json=None, timeout=5, debug=False
    ):
        response = cls._send_request(
            Config.get_backend_url() + path,
            method,
            params=params,
            json=json,
            timeout=timeout,
            debug=debug,
        )
        if not response:
            return None
        return response.json()

    @classmethod
    def send_request_url(cls, url, method, timeout=5, verify=True):
        return cls._send_request(url, method, timeout=timeout, verify=verify)

    @classmethod
    def update_ticket_info(cls, **kwargs):
        if QuizwizSession.get().ticket["id"] is None:
            st.error(
                f"can't update_ticket_info: invalid ticket_id={QuizwizSession.get().ticket['id']}"
            )
            return False

        param = {
            "id": QuizwizSession.get().ticket["id"],  # 📌 "id" is Ticket's field
            "knox_id": QuizwizSession.get().user_id(),
            "user_name": QuizwizSession.get().user_name(),
            "event_code": QuizwizSession.get().event["event_code"],
            "state": kwargs.get("state", QuizwizSession.get().ticket["state"]),
            "grade": QuizwizSession.get().ticket["grade"],
            "quiz_remain": 0,
            "current_quiz": 1,  # TBD for version2.0
            "is_expired": kwargs.get(
                "is_expired", QuizwizSession.get().ticket["is_expired"]
            ),
        }

        ticket = Http.send_request_json_response("ticket", "PUT", json=param)
        Log.ui_debug(f"Received ticket from the server. {ticket=}")
        if ticket is not None and len(ticket):
            QuizwizSession.get().init_ticket(ticket)
            return True

        st.error(
            f"Can't update ticket for event_code={QuizwizSession.get().event['event_code']}"
        )
        return False

    @classmethod
    def _send_request(
        cls, url, method, params=None, json=None, timeout=5, verify=True, debug=False
    ):
        methods = {
            "DELETE": requests.delete,
            "PUT": requests.put,
            "POST": requests.post,
            "GET": requests.get,
        }

        try:
            response = methods[method](
                url, params=params, json=json, timeout=timeout, verify=verify
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            Log.ui_debug(cls._handle_requests_exceptions(e), debug)
            return None

        if not isinstance(response, requests.Response):
            Log.ui_debug(response, debug)
            return None

        return response

    @classmethod
    def _handle_requests_exceptions(cls, e):
        if isinstance(e, requests.exceptions.Timeout):
            return "Timeout occurred during the request."

        if isinstance(e, requests.exceptions.HTTPError) and e.response is not None:
            # 응답을 JSON으로 파싱하여 detail 메시지를 출력
            try:
                error_response = e.response.json()
                error_msg = f"HTTP error: status={e.response.status_code}, detail={error_response.get('detail')}"
            except ValueError:  # Catch JSONDecodeError or similar errors
                error_msg = f"HTTP error: status={e.response.status_code}, but failed to decode JSON."
            return error_msg
        else:
            return f"Request exception occurred: {str(e)}"

    @classmethod
    def get_event(cls, evt_code):
        if not evt_code:
            return False, None

        param = {
            "event_code": evt_code,
            "method": QuizStatus.get_value(QuizStatus.READ_EVENT_CODE),
        }
        events = Http.send_request_json_response("event", "GET", params=param)

        if events and len(events):
            Log.ui_debug(f"Received {len(events)} events from the server.")
            return True, events[0]

        return False, None

    @classmethod
    def get_event_list(cls):
        param = {
            "method": QuizStatus.get_value(QuizStatus.ALL_EVENT),
        }
        events = Http.send_request_json_response("event", "GET", params=param)

        if events and len(events):
            Log.ui_debug(f"Received {len(events)} events from the server.")
            return True, events

        return False, None

    @classmethod
    def get_ticket(cls):
        param = {
            "method": QuizStatus.get_value(QuizStatus.READ_TICKET_CODE_KNOX),
            "event_code": QuizwizSession.get().event["event_code"],
            "knox_id": QuizwizSession.get().user_id(),
        }

        tickets = Http.send_request_json_response("ticket", "GET", params=param)
        if tickets and len(tickets):
            Log.ui_debug(f"Received {len(tickets)} tickets from the server.")
            # 사용자가 재시도할 경우, 다수의 ticket list가 전달되므로 last 추출
            QuizwizSession.get().init_ticket(tickets[-1])
            if not QuizwizSession.get().is_ticket_expired():
                return True, tickets[-1]

        return False, None

    @classmethod
    def create_ticket(cls):
        param = {
            "event_code": QuizwizSession.get().event["event_code"],
            "knox_id": QuizwizSession.get().user_id(),
            "user_name": QuizwizSession.get().user_name(),
            "state": Constant.APP_STATE_INTRO,
            "grade": 0,
            "quiz_remain": 0,
            "current_quiz": 1,  # TBD for version2.0
        }
        ticket = Http.send_request_json_response("ticket", "POST", json=param)

        if ticket is not None:
            Log.ui_debug(f"Received {ticket=}")
            QuizwizSession.get().init_ticket(ticket)
            return True

        st.error(
            f"Can't create ticket for event_code={QuizwizSession.get().event['event_code']}"
        )
        return False

    @classmethod
    def create_winner(cls, ticket_list):
        param = {
            "winner_list": ticket_list,
            "method": QuizStatus.get_value(QuizStatus.ALL_WINNER),
        }
        winners = Http.send_request_json_response("winner", "POST", json=param)

        if winners is not None:
            Log.ui_debug(f"Received {len(winners)} tickets are lucky-draw-winners")
            return True

        st.error(f"Can't create winner for lucky winners={ticket_list}")
        return False

    @classmethod
    def get_admin_info(cls, knox_id):
        param = {
            "admin_knox_id": knox_id,
            "method": QuizStatus.get_value(QuizStatus.READ_ADMIN_KNOX_ID),
        }
        admins = Http.send_request_json_response("admin", "GET", params=param)

        if admins and len(admins):
            Log.ui_debug(f"Received {len(admins)} admins from the server.")
            return True, admins

        return False, None
