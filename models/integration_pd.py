from typing import List, Optional

from pydantic import BaseModel

from tools import session_project, rpc_tools, VaultClient, worker_client, this
from pylon.core.tools import log
from ...integrations.models.pd.integration import SecretField


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
        #
        settings = {}
        #
        if self.api_token:
            settings["token"] = self.api_token.unsecret(project_id)
        else:
            settings["token"] = None
        #
        return worker_client.ai_check_settings(
            integration_name=this.module_name,
            settings=settings,
        )

    def refresh_models(self, project_id):
        integration_name = 'hugging_face'
        payload = {
            'name': integration_name,
            'settings': self.dict(),
            'project_id': project_id
        }
        return getattr(rpc_tools.RpcMixin().rpc.call, f'{integration_name}_set_models')(payload)
