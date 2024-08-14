#!/usr/bin/python3
# coding=utf-8

#   Copyright 2021 getcarrier.io
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

""" Module """
from pylon.core.tools import log  # pylint: disable=E0611,E0401
from pylon.core.tools import module  # pylint: disable=E0611,E0401

from tools import worker_client  # pylint: disable=E0611,E0401

from .models.integration_pd import IntegrationModel


class Module(module.ModuleModel):
    """ Task module """

    def __init__(self, context, descriptor):
        self.context = context
        self.descriptor = descriptor

    def init(self):
        """ Init module """
        log.info('Initializing AI module')
        SECTION_NAME = 'ai'
        #
        self.descriptor.init_all()
        #
        self.context.rpc_manager.call.integrations_register_section(
            name=SECTION_NAME,
            integration_description='Manage ai integrations',
        )
        self.context.rpc_manager.call.integrations_register(
            name=self.descriptor.name,
            section=SECTION_NAME,
            settings_model=IntegrationModel,
        )
        #
        worker_client.register_integration(
            integration_name=self.descriptor.name,
            #
            ai_check_settings_callback=self.ai_check_settings,
            ai_get_models_callback=self.ai_get_models,
            ai_count_tokens_callback=None,
            #
            llm_invoke_callback=None,
            llm_stream_callback=None,
            #
            chat_model_invoke_callback=None,
            chat_model_stream_callback=None,
            #
            embed_documents_callback=None,
            embed_query_callback=None,
            #
            indexer_config_callback=self.indexer_config,
        )

    def deinit(self):  # pylint: disable=R0201
        """ De-init module """
        log.info('De-initializing')
        #
        self.descriptor.deinit_all()
