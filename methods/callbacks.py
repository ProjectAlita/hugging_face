#!/usr/bin/python3
# coding=utf-8

#   Copyright 2024 EPAM Systems
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

""" Method """

import json

from pylon.core.tools import log  # pylint: disable=E0611,E0401,W0611
from pylon.core.tools import web  # pylint: disable=E0611,E0401,W0611


class Method:  # pylint: disable=E1101,R0903,W0201
    """
        Method Resource

        self is pointing to current Module instance

        web.method decorator takes zero or one argument: method name
        Note: web.method decorator must be the last decorator (at top)
    """

    #
    # AI
    #

    @web.method()
    def ai_check_settings(  # pylint: disable=R0913
            self, settings,
        ):
        """ Check integration settings/test connection """
        settings = json.loads(json.dumps(settings))
        #
        result = {
            "routing_key": None,
            #
            "target": "plugins.hugging_face_worker.utils.ai.Helper",
            "target_args": None,
            "target_kwargs": {
                "token": settings["token"],
            },
            "target_io_bound": True,
            #
            "method": "check_settings",
            "method_args": None,
            "method_kwargs": None,
        }
        #
        return result

    @web.method()
    def ai_get_models(  # pylint: disable=R0913
            self, settings,
        ):
        """ Get model list """
        settings = json.loads(json.dumps(settings))
        #
        result = {
            "routing_key": None,
            #
            "target": "plugins.hugging_face_worker.utils.ai.Helper",
            "target_args": None,
            "target_kwargs": {
                "token": settings["token"],
            },
            "target_io_bound": True,
            #
            "method": "get_models",
            "method_args": None,
            "method_kwargs": None,
        }
        #
        return result

    #
    # Indexer
    #

    @web.method()
    def indexer_config(  # pylint: disable=R0913
            self, settings, model,
        ):
        """ Make indexer config """
        #
        result = {
            "embedding_model": "HuggingFaceEmbeddings",
            "embedding_model_params": {
                "model_name": model,
            },
        }
        #
        if settings["settings"]["api_token"]:
            result["embedding_model_params"]["model_kwargs"]["token"] = \
                settings["settings"]["api_token"]
        #
        return result
