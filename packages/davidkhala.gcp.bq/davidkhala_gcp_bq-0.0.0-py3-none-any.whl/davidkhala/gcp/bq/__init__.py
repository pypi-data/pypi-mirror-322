import re
from abc import abstractmethod
from typing import Dict, Iterable

from davidkhala.gcp.auth import OptionsInterface
from google.cloud.bigquery import Client, DatasetReference, DestinationFormat, ExtractJobConfig
from google.cloud.bigquery.table import Row


class BigQueryInterface:
    project: str
    dataset: str
    table: str

    def __init__(self, auth: OptionsInterface):
        self.project = auth.projectId

    @staticmethod
    def parse_table_path(path: str) -> Dict[str, str]:
        """Parses a table path into its component segments."""
        m = re.match(
            r"projects/(?P<project>.+?)/datasets/(?P<dataset>.+?)/tables/(?P<table>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @property
    @abstractmethod
    def table_path(self):
        pass

    @property
    def table_id(self):
        return f"{self.project}.{self.dataset}.{self.table}"

    def of(self, *, table_path=None, table_id=None):
        if table_path:
            data = BigQueryInterface.parse_table_path(table_path)
            self.project = data['project']
            self.dataset = data['dataset']
            self.table = data['table']
        elif table_id:
            self.project, self.dataset, self.table = table_id.split('.')
        return self


class BigQuery(BigQueryInterface):
    client: Client

    def __init__(self, auth: OptionsInterface):
        super().__init__(auth)
        self.client = Client(auth.projectId, auth.credentials)

    def query(self, query: str, **options) -> Iterable[Row]:
        return self.client.query_and_wait(query, **options)

    def export(self, data_format: DestinationFormat, *, bucket=None, gcs_uri=None):
        """
        A high latency but high throughput batch exporting
        :param data_format:
        :param bucket:
        :param gcs_uri:
        :return:
        """
        if not gcs_uri:
            gcs_uri = f"gs://{bucket}/{self.table_id}.{str(data_format).lower()}"
        job = self.client.extract_table(
            self.table_id,
            gcs_uri,
            job_config=ExtractJobConfig(destination_format=data_format)
        )
        return job.result()

    @property
    def table_path(self):
        return DatasetReference(self.project, self.dataset).table(self.table).path
