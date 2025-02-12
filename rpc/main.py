from pylon.core.tools import web, log

from tools import rpc_tools, worker_client, this

from ..models.integration_pd import AIModel


class RPC:
    integration_name = 'hugging_face'

    @web.rpc(f'{integration_name}_set_models', 'set_models')
    @rpc_tools.wrap_exceptions(RuntimeError)
    def set_models(self, payload: dict):
        api_key = payload['settings'].get('api_token', {})
        #
        if api_key:
            api_key = api_key.unsecret(payload.get('project_id'))
        else:
            api_key = None
        #
        settings = {
            "token": api_key,
        }
        #
        raw_models = worker_client.ai_get_models(
            integration_name=this.module_name,
            settings=settings,
        )
        #
        return [AIModel(**model).dict() for model in raw_models]
