"""
main module connect Web and FastAPI
"""

from typing import Optional
from fastapi import FastAPI, Depends
from .data.database import Database
from .data.event import Event
from .data.event_ticket import EventTicket
from .data.handle_except import HandleExcept, CustomValueError
from .data.query_data import QueryData
from .data.quiz import Quiz
from .data.admin import Admin

app = FastAPI()


class DatabaseProvider:
    """
    Dependancy injection to avoid using global variables (database)
    """

    def __init__(self, db: Optional[Database] = None):
        self._db = db

    def set_database_instance(self, db: Database):
        """
        set_database_instance
        """
        self._db = db

    def get_database_instance(self) -> Optional[Database]:
        """
        get_database_instance
        """
        return self._db


db_provider = DatabaseProvider()


@app.get("/")
def read_root():
    """
    Define '/' path's test statements
    """
    return {
        "Hello": "QuizWiz(Quiz Wizard) is a platform that provides users \
with engaging quizzes to test their knowledge and skills."
    }


@app.get(
    "/healthcheck",
    responses={
        200: {
            "description": "Successful Response",
            "content": {"application/json": {"example": {"OK"}}},
        }
    },
)
async def check_health():
    """
    This path is for health check
    """
    return {"OK"}


@app.post("/default")
async def create_default_quizzes(
    db: Database = Depends(db_provider.get_database_instance),
):
    """
    To test easily, create a default quizzes
    """
    try:
        return db.put_default_quiz()
    except CustomValueError as e:
        HandleExcept.raise_http_exception(e)


@app.post("/quiz")
async def create_quiz(
    payload: Quiz, db: Database = Depends(db_provider.get_database_instance)
):
    """
    User can create quiz on web browser
    """
    try:
        return db.create_quiz(payload)
    except CustomValueError as e:
        HandleExcept.raise_http_exception(e)


@app.get("/quiz")
async def read_quiz(
    payload: QueryData = Depends(),
    db: Database = Depends(db_provider.get_database_instance),
):
    """
    User can read quiz on web browser
    """
    try:
        return db.read_quiz(payload)
    except CustomValueError as e:
        HandleExcept.raise_http_exception(e)


@app.put("/quiz")
async def update_quiz(
    payload: Quiz, db: Database = Depends(db_provider.get_database_instance)
):
    """
    User can update quiz on web browser
    """
    try:
        return db.update_quiz(payload)
    except CustomValueError as e:
        HandleExcept.raise_http_exception(e)


@app.delete("/quiz")
async def delete_quiz(
    payload: QueryData = Depends(),
    db: Database = Depends(db_provider.get_database_instance),
):
    """
    User can delete quiz on web browser
    """
    try:
        return db.delete_quiz(payload)
    except CustomValueError as e:
        HandleExcept.raise_http_exception(e)


@app.post("/answer")
async def solve_quiz(
    payload: QueryData = Depends(),
    db: Database = Depends(db_provider.get_database_instance),
):
    """
    퀴즈 풀기 Scenario:
        1) [Request] 사용자가 퀴즈를 풀어서 답안을 서버에 제출한다.
        2) [Response] 서버는 DB의 정답과 사용자의 답안을 비교하여 결과를 return
    """
    return db.solve_quiz(payload)


@app.get("/selection")
async def select_quiz(
    payload: QueryData = Depends(),
    db: Database = Depends(db_provider.get_database_instance),
):
    """
    This api support combination among quiz_count, category, label
    """
    return db.select_quiz(payload)


@app.post("/event")
async def create_event(
    payload: Event, db: Database = Depends(db_provider.get_database_instance)
):
    """
    BU-1, 이벤트 정보 조회 기능을 할 수 있는 API 제공 (Data - Event)
    - 이벤트 정보는 이벤트 이름, 이벤트 id, 구성할 문제의 label, 한 사람이 풀 문제 갯수 정보가 포함된다
    """

    try:
        return db.create_event(payload)
    except CustomValueError as e:
        HandleExcept.raise_http_exception(e)


@app.get("/event")
async def read_event(
    payload: QueryData = Depends(),
    db: Database = Depends(db_provider.get_database_instance),
):
    """
    User can read event on web browser
    """
    try:
        return db.read_event(payload)
    except CustomValueError as e:
        HandleExcept.raise_http_exception(e)


@app.put("/event")
async def update_event(
    payload: Event, db: Database = Depends(db_provider.get_database_instance)
):
    """
    User can update event on web browser
    """
    try:
        return db.update_event(payload)
    except CustomValueError as e:
        HandleExcept.raise_http_exception(e)


@app.delete("/event")
async def delete_event(
    payload: QueryData = Depends(),
    db: Database = Depends(db_provider.get_database_instance),
):
    """
    User can delete event on web browser
    """
    try:
        return db.delete_event(payload)
    except CustomValueError as e:
        HandleExcept.raise_http_exception(e)


@app.post("/ticket")
async def create_ticket(
    payload: EventTicket, db: Database = Depends(db_provider.get_database_instance)
):
    """
    BU-2, 사용자의 이벤트 참여 정보 조회 및 업데이트 API 제공 (Data - Quiz, EventTicket, Answer)
    - 이벤트 참여 정보(EventTicket)에는 현재 풀고 있는 이벤트 코드, 문제 id, 남은 문제 갯수 등이 있다.
    - ...
    """
    try:
        return db.create_ticket(payload)
    except CustomValueError as e:
        HandleExcept.raise_http_exception(e)


@app.get("/ticket")
async def read_ticket(
    payload: QueryData = Depends(),
    db: Database = Depends(db_provider.get_database_instance),
):
    """
    User can read ticket on web browser
    """
    try:
        return db.read_ticket(payload)
    except CustomValueError as e:
        HandleExcept.raise_http_exception(e)


@app.put("/ticket")
async def update_ticket(
    payload: EventTicket, db: Database = Depends(db_provider.get_database_instance)
):
    """
    User can update ticket on web browser
    """
    try:
        return db.update_ticket(payload)
    except CustomValueError as e:
        HandleExcept.raise_http_exception(e)


@app.delete("/ticket")
async def delete_ticket(
    payload: QueryData = Depends(),
    db: Database = Depends(db_provider.get_database_instance),
):
    """
    User can delete ticket on web browser
    """
    try:
        return db.delete_ticket(payload)
    except CustomValueError as e:
        HandleExcept.raise_http_exception(e)


@app.get("/answer")
async def read_answer(
    payload: QueryData = Depends(),
    db: Database = Depends(db_provider.get_database_instance),
):
    """
    User can read ticket on web browser
    """
    try:
        return db.read_answer(payload)
    except CustomValueError as e:
        HandleExcept.raise_http_exception(e)


@app.delete("/answer")
async def delete_answer(
    payload: QueryData = Depends(),
    db: Database = Depends(db_provider.get_database_instance),
):
    """
    User can delete answer on web browser
    """
    try:
        return db.delete_answer(payload)
    except CustomValueError as e:
        HandleExcept.raise_http_exception(e)


@app.get("/ranking")
async def get_ranking(
    payload: QueryData = Depends(),
    db: Database = Depends(db_provider.get_database_instance),
):
    if payload.ticket_id and payload.event_code:
        return db.get_current_rank(payload)
    elif payload.knox_id and payload.event_code:
        return db.get_best_rank(payload)
    else:
        return db.get_ranking(payload)


@app.post("/winner")
async def create_winner(
    payload: QueryData,
    db: Database = Depends(db_provider.get_database_instance),
):
    """
    BU-2, 사용자의 이벤트 참여 정보 조회 및 업데이트 API 제공 (Data - Quiz, EventTicket, Answer)
    - 이벤트 참여 정보(EventTicket)에는 현재 풀고 있는 이벤트 코드, 문제 id, 남은 문제 갯수 등이 있다.
    - ...
    """
    try:
        return db.create_winner(payload)
    except CustomValueError as e:
        HandleExcept.raise_http_exception(e)


@app.get("/winner")
async def read_winner(
    payload: QueryData = Depends(),
    db: Database = Depends(db_provider.get_database_instance),
):
    """
    User can read ticket on web browser
    """
    try:
        return db.read_winner(payload)
    except CustomValueError as e:
        HandleExcept.raise_http_exception(e)


@app.post("/admin")
async def create_admin(
    payload: Admin, db: Database = Depends(db_provider.get_database_instance)
):
    """
    User can create admin on web browser
    """
    try:
        return db.create_admin(payload)
    except CustomValueError as e:
        HandleExcept.raise_http_exception(e)


@app.get("/admin")
async def read_admin(
    payload: QueryData = Depends(),
    db: Database = Depends(db_provider.get_database_instance),
):
    """
    User can read admin on web browser
    """
    try:
        return db.read_admin(payload)
    except CustomValueError as e:
        HandleExcept.raise_http_exception(e)


@app.put("/admin")
async def update_admin(
    payload: Admin, db: Database = Depends(db_provider.get_database_instance)
):
    """
    User can update admin on web browser
    """
    try:
        return db.update_admin(payload)
    except CustomValueError as e:
        HandleExcept.raise_http_exception(e)


@app.delete("/admin")
async def delete_admin(
    payload: QueryData = Depends(),
    db: Database = Depends(db_provider.get_database_instance),
):
    """
    User can delete admin on web browser
    """
    try:
        return db.delete_admin(payload)
    except CustomValueError as e:
        HandleExcept.raise_http_exception(e)
