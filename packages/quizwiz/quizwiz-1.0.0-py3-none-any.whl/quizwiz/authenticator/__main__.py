import os
import uvicorn
from .auth_app import app
from .auth_config import AuthConfig

if __name__ == "__main__":
    key_file = os.environ.get("CERT_KEY", None)
    cert_file = os.environ.get("CERT", None)
    if key_file is not None and cert_file is not None:
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=AuthConfig.PORT,
            ssl_keyfile=key_file,
            ssl_certfile=cert_file,
        )
    else:
        uvicorn.run(app, host="0.0.0.0", port=AuthConfig.PORT)
