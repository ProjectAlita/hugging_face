from typing import List, Optional

from pydantic import BaseModel

from tools import session_project, rpc_tools, VaultClient
from pylon.core.tools import log
from ...integrations.models.pd.integration import SecretField
from huggingface_hub import login, logout


class CapabilitiesModel(BaseModel):
    completion: bool = False
    chat_completion: bool = False
    embeddings: bool = True


class AIModel(BaseModel):
    id: str
    name: str
    capabilities: Optional[CapabilitiesModel] = CapabilitiesModel()


class IntegrationModel(BaseModel):
    api_token: Optional[SecretField | str]
    model_name: str = 'sentence-transformers/all-mpnet-base-v2'
    models: List[AIModel] = []

    def check_connection(self, project_id=None):
        if not project_id:
            project_id = session_project.get()
        token = self.api_token.unsecret(project_id)
        log.info(f"Checking connection with token {token}")
        try:
            login(token=token, new_session=True)
        except ValueError:
            log.error("Invalid token")
            return "Invalid token"
        finally:
            logout()
        return True

    def refresh_models(self, project_id):
        integration_name = 'hugging_face'
        payload = {
            'name': integration_name,
            'settings': self.dict(),
            'project_id': project_id
        }
        return getattr(rpc_tools.RpcMixin().rpc.call, f'{integration_name}_set_models')(payload)
