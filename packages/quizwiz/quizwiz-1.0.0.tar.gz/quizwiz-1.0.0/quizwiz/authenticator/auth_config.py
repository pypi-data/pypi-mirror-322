import os
from dotenv import load_dotenv

load_dotenv()


class AuthConfig:
    SALT = os.environ.get("SALT", "salt for quizwiz")
    PORT = int(os.environ.get("PORT", 8080))
    MODE = os.environ.get("MODE", "DEV")

    if MODE == "DEV":
        IDP_CERT_FILE = f"{os.getcwd()}/authenticator/cert/stsds-dev.secsso.net.cer"
        IDP_LOGOUT_URL = "https://stsds-dev.secsso.net/adfs/ls/?wa=wsignoutcleanup1.0"
    else:
        IDP_CERT_FILE = f"{os.getcwd()}/authenticator/cert/stsds.secsso.net.cer"
        IDP_LOGOUT_URL = "https://stsds.secsso.net/adfs/ls/?wa=wsignoutcleanup1.0"

    SERVICE_URL = os.environ.get("SERVICE_URL", "localhost:8501")
