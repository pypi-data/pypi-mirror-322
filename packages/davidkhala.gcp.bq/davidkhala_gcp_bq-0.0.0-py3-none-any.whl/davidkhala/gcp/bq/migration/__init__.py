from enum import auto

from google.cloud.bigquery_migration import TeradataDialect, Dialect


class SourceDialect:
    Teradata = Dialect({
        "teradata_dialect": TeradataDialect({
            "mode": TeradataDialect.Mode.SQL
        }),
    })
    Bteq = Dialect({
        "teradata_dialect": TeradataDialect({
            "mode": TeradataDialect.Mode.BTEQ
        }),
    })
    Redshift = auto(),
    Oracle = auto()
    HiveQL = auto()
    SparkSQL = auto()
    Snowflake = auto()
    Netezza = auto()
    AzureSynapse = auto()
    Vertica = auto()
    SQLServer = auto()
    Presto = auto()
    MySQL = auto()
    Postgresql = auto()
    # TODO we also need self.dialect.value