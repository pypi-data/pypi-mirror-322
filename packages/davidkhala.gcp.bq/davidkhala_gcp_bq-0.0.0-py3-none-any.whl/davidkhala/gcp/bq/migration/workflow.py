# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from davidkhala.gcp.auth import OptionsInterface
from google.cloud.bigquery_migration import Dialect, MigrationServiceClient, BigQueryDialect, TranslationConfigDetails
from google.cloud.bigquery_migration import MigrationTask, MigrationWorkflow

from davidkhala.gcp.bq import BigQuery


class Workflow(BigQuery):
    name: str
    dialect: Dialect
    client: MigrationServiceClient
    location: str

    def __init__(self, auth: OptionsInterface):
        super().__init__(auth)
        self.client = MigrationServiceClient(credentials=auth.credentials)

    def create(self, gcs_input_path: str, gcs_output_path: str) -> str:
        """
        Creates a migration workflow of a Batch SQL Translation
        :param gcs_input_path:
        :param gcs_output_path:
        :return: workflow id
        """
        parent = f"projects/{self.project}/locations/{self.location}"

        # Prepare the config proto.
        translation_config = TranslationConfigDetails({
            "gcs_source_path": "gs://" + gcs_input_path,
            "gcs_target_path": "gs://" + gcs_output_path,
            "source_dialect": self.dialect,
            "target_dialect": Dialect({
                "bigquery_dialect": BigQueryDialect()
            }),
        })

        # Prepare the workflow.
        workflow = MigrationWorkflow({
            "display_name": self.name,
            "tasks": {
                "translation-task": MigrationTask({
                    "type_": f"Translation_{self.dialect.value}2BQ",
                    "translation_config_details": translation_config,
                })
            }
        })

        _migrationWorkflow = self.client.create_migration_workflow(
            parent=parent,
            migration_workflow=workflow,
        )

        return _migrationWorkflow.name
