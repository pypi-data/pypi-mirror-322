"""
Global constant config variable
"""

import os
from dotenv import load_dotenv  # pip install python-dotenv

load_dotenv()


class Config:
    """Global config variable"""

    DB_PATH = os.environ.get("DB_PATH", "./quizwiz.db")

    HOST = os.environ.get("HOST", "0.0.0.0")
    PORT = int(os.environ.get("PORT", 8000))

    """
    [Use case]
        quizzes = DB로 부터 SELECT된 10개의 퀴즈가 있다.
        if SHUFFLE_QUIZZES = True:
            random.shuffle(quizzes)
            return quizzes[:count]
        else:
            # w/o shuffle, return database ordered
            return quizzes[:count]
    [Caution📌]
        test 수행하려면 default 값은 False 가 맞다.
        실제 서비스할 경우, 필요에 따라 True로 변경 예정
    """
    SHUFFLE_QUIZZES = True
    CheckDuplication_when_CreateTicket = False  # version_2 = True

    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return "Config class"

    def __repr__(self) -> str:
        return f"Config class, {self.SHUFFLE_QUIZZES=}, {self.CheckDuplication_when_CreateTicket=}"
