"""
Global constant config variable
"""

import os
from dotenv import load_dotenv  # pip install python-dotenv
from constant import Constant

load_dotenv()


class Config:
    """Global config variable"""

    IMAGE_URL = {
        "title": "https://github.samsungds.net/pages/SLSISE/QuizWiz/images/quizwiz.jpg",
        Constant.APP_STATE_HELLO: "https://github.samsungds.net/pages/SLSISE/QuizWiz/images/hello.jpg",
        Constant.APP_STATE_INTRO: "https://github.samsungds.net/pages/SLSISE/QuizWiz/images/intro.jpg",
        Constant.APP_STATE_PROBLEM: "https://github.samsungds.net/pages/SLSISE/QuizWiz/images/problem.jpg",
        Constant.APP_STATE_ANSWER: "https://github.samsungds.net/pages/SLSISE/QuizWiz/images/answer.jpg",
        Constant.APP_STATE_REVIEW: "https://github.samsungds.net/pages/SLSISE/QuizWiz/images/review.jpg",
    }

    # BE(Backend) Server
    API_HOST = os.environ.get("API_HOST", "127.0.0.1")
    API_PORT = int(os.environ.get("API_PORT", 8000))
    MODE = os.environ.get("MODE", "DEV")

    if MODE == "DEV":
        IDP_CONFIG = {
            "Idp.EntityID": "https://stsds-dev.secsso.net/adfs/oauth2/authorize/",
            "Idp.SignoutUrl": "https://stsds-dev.secsso.net/adfs/ls/?wa=wsignoutcleanup1.0",
            "Idp.ClientID": "23e379fe-9639-4c93-9041-ad5dfa68146e",
        }
    else:
        IDP_CONFIG = {
            "Idp.EntityID": "https://stsds.secsso.net/adfs/oauth2/authorize/",
            "Idp.SignoutUrl": "https://stsds.secsso.net/adfs/ls/?wa=wsignoutcleanup1.0",
            "Idp.ClientID": "9120ce40-8146-4e4b-a027-a805e98fca19",
        }

    AUTH_URL = os.environ.get("AUTH_URL", "")
    SP_CONFIG = {"SP.RedirectUrl": f"{AUTH_URL}/auth"}

    DEBUG_PRINT = False  # for UX 개발 디버깅
    DEBUG_ID = os.environ.get("DEBUG_ID", None)

    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return "Config class"

    @classmethod
    def is_prod_auth(cls):
        return Config.AUTH_URL == "https://pando.samsungds.net/auth"

    @classmethod
    def get_backend_url(cls):
        """
        return url of backend server
        """
        return f"http://{Config.API_HOST}:{Config.API_PORT}/"
