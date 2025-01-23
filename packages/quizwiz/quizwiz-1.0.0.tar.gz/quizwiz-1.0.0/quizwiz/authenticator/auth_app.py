import time
import hashlib
import jwt
import json
from urllib.parse import urlencode

from cryptography import x509
from cryptography.hazmat.backends import default_backend

from fastapi import FastAPI, Form, Depends, status, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from http import HTTPStatus

from dataclasses import dataclass
from .auth_config import AuthConfig

app = FastAPI()


@dataclass
class SSOModel:
    id_token: str = Form(...)


# DS AD login POST 요청으로 전달 된 Token 처리하는 함수
@app.post("/auth", response_class=HTMLResponse)
async def auth(form_data: SSOModel = Depends(SSOModel)):
    is_error = False
    error_msg = ""
    claim_val = {}

    # 복호화 : Token으로 부터 claim value 추출
    cert_str = open(
        AuthConfig.IDP_CERT_FILE, "rb"
    ).read()  # Token 복호화에 필요한 key 값

    cert_obj = x509.load_pem_x509_certificate(cert_str, default_backend())
    public_key = cert_obj.public_key()
    id_token_val = form_data.id_token
    b_token = id_token_val.encode()

    try:
        decode = jwt.decode(
            jwt=b_token,
            key=public_key,
            verify=True,
            algorithms="RS256",
            options={"verify_signature": True, "verify_exp": True, "verify_aud": False},
        )

        json_str = json.dumps(decode)
        claim_val = json.loads(json_str)

    except jwt.ExpiredSignatureError:
        is_error = True
        error_msg = "Authentication Token has expired."

    except jwt.InvalidTokenError:
        is_error = True
        error_msg = "Authentication Token is not valid."

    claim_val["isLoad"] = False
    claim_val["isError"] = is_error
    claim_val["Error_MSG"] = error_msg

    if is_error:
        return RedirectResponse(url=AuthConfig.SERVICE_URL)

    # claim value 중 필요한 부분만 필터링
    login_id = claim_val.get("loginid")
    username = claim_val.get("username")
    timestamp = get_timestamp_ms()
    query_dict = {
        "loginid": login_id,
        "username": username,
        "timestamp": timestamp,
        "token": get_hash(login_id, username, timestamp),
    }

    # get 요청으로 streamlit에 전달하기 위해 query string으로 변환
    query_string = "?" + urlencode(query_dict)

    # fastapi 서버에 "/auth" endpoint로 접근 시 설정한 url로 redirection
    return RedirectResponse(
        url=f"{AuthConfig.SERVICE_URL}{query_string}", status_code=status.HTTP_302_FOUND
    )


def get_hash(
    loginid: str = None,
    username: str = None,
    timestamp: str = None,
):
    query_dict = {
        "loginid": loginid,
        "username": username,
        "timestamp": timestamp,
    }

    data = f"{str(query_dict)}{AuthConfig.SALT}".encode()
    sha256_hash = hashlib.sha256()
    sha256_hash.update(data)
    return sha256_hash.hexdigest()


@app.get("/auth/status")
def get_auth_status(
    loginid: str = "",
    username: str = "",
    timestamp: str = "",
    token: str = "",
):
    if token != get_hash(loginid, username, timestamp):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Invalid Request"
        )
    return "OK"


# 로그아웃
@app.get("/logout")
async def logout():
    idp_url = AuthConfig.IDP_LOGOUT_URL
    return RedirectResponse(url=idp_url)


def get_timestamp_ms():
    return str(int(time.time() * 1000))
