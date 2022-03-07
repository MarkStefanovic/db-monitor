import pytest

from src import domain


def test_query_rejects_empty_datasource_name():
    with pytest.raises(domain.exceptions.InvalidJobSpecException):
        domain.Job(
            report_name="Customers",
            sql_file="/tmp/test.sql",
            datasource_name="",
            height=200,
            seconds_between_refreshes=100,
        )


def test_query_rejects_missing_sql_file():
    with pytest.raises(domain.exceptions.InvalidJobSpecException):
        domain.Job(
            report_name="Customers",
            sql_file="",
            datasource_name="test",
            height=200,
            seconds_between_refreshes=100,
        )


def test_query_rejects_negative_seconds_between_refreshes():
    with pytest.raises(domain.exceptions.InvalidJobSpecException):
        domain.Job(
            report_name="Customers",
            sql_file="/tmp/test.sql",
            datasource_name="test",
            height=200,
            seconds_between_refreshes=-100,
        )
