from pydantic import BaseModel

from tools import session_project
from pylon.core.tools import log
from ...integrations.models.pd.integration import SecretField
from huggingface_hub import login, logout


class IntegrationModel(BaseModel):
    api_token: SecretField | str

    def check_connection(self):
        token = self.api_token.unsecret(session_project.get())
        log.info(f"Checking connection with token {token}")
        try:
            login(token=token, new_session=True)
        except ValueError:
            log.error("Invalid token")
            return "Invalid token"
        finally:
            logout()
        return True
