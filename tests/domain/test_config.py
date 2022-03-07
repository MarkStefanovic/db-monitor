import pytest

from src import domain


def test_empty_datasources():
    with pytest.raises(domain.exceptions.InvalidConfigurationSetting):
        domain.Config(
            datasources=[],
            jobs=[
                domain.Job(
                    report_name="Test Report",
                    sql_file="./test_report.sql",
                    datasource_name="test_datasource",
                    seconds_between_refreshes=60,
                    height=200,
                ),
            ],
            reports_per_row=3,
        )


def test_empty_jobs():
    with pytest.raises(domain.exceptions.InvalidConfigurationSetting):
        domain.Config(
            datasources=[
                domain.Datasource(
                    name="localhost",
                    uri="postgresql+psycopg2://test:mypassword@localhost/testdb",
                )
            ],
            jobs=[],
            reports_per_row=3,
        )


def test_negative_reports_per_row():
    with pytest.raises(domain.exceptions.InvalidConfigurationSetting):
        domain.Config(
            datasources=[
                domain.Datasource(
                    name="localhost",
                    uri="postgresql+psycopg2://test:mypassword@localhost/testdb",
                ),
            ],
            jobs=[
                 domain.Job(
                    report_name="Test Report",
                    sql_file="./test_report.sql",
                    datasource_name="test_datasource",
                    seconds_between_refreshes=60,
                    height=200,
                ),
            ],
            reports_per_row=-1,
        )
