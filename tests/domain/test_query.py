import pydantic
import pytest

from src import domain


def test_query_rejects_empty_datasource_name():
    with pytest.raises(pydantic.ValidationError):
        domain.Job(
            report_name="Customers",
            sql="SELECT * FROM sales.customers",
            datasource_name="",
            seconds_between_refreshes=100,
        )


def test_query_rejects_empty_sql():
    with pytest.raises(pydantic.ValidationError):
        domain.Job(
            report_name="Customers",
            sql="",
            datasource_name="test",
            seconds_between_refreshes=100,
        )


def test_query_rejects_negative_seconds_between_refreshes():
    with pytest.raises(pydantic.ValidationError):
        domain.Job(
            report_name="Customers",
            sql="SELECT * FROM sales.customers",
            datasource_name="test",
            seconds_between_refreshes=-100,
        )
