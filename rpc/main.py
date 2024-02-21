from pylon.core.tools import web, log

from tools import rpc_tools

from ..models.integration_pd import AIModel
from ...integrations.models.pd.integration import SecretField


class RPC:
    integration_name = 'hugging_face'

    @web.rpc(f'{integration_name}_set_models', 'set_models')
    @rpc_tools.wrap_exceptions(RuntimeError)
    def set_models(self, payload: dict):
        from huggingface_hub import HfApi, logout
        api_key = payload['settings'].get('api_token', {})
        try:
            api = HfApi() if not api_key else HfApi(
                token=SecretField.parse_obj(api_key).unsecret(payload.get('project_id'))
            )
            models = list(api.list_models(
                search='sentence-transformers',
                sort="downloads",
                direction=-1,
                limit=10,
            ))
        except Exception as e:
            log.error(str(e))
            models = []
        finally:
            logout()
        if models:
            models = [AIModel(id=model.id, name=model.id).dict() for model in models]
        return models
