# Apache License 2.0, Copyright 2020 Logpickr
# https://gitlab.com/logpickr/logpickr-sdk/-/blob/master/LICENSE
import pytest
from igrafx_mining_sdk.column_mapping import ColumnType, Column, ColumnMapping


class TestColumnMapping:
    def test_create_case_id_column(self):
        column = Column('test', 0, ColumnType.CASE_ID)
        assert isinstance(column, Column)

    def test_exeption_case_id_column_with_time_format(self):
        with pytest.raises(ValueError):
            Column('test', 0, ColumnType.CASE_ID, time_format='%Y-%m-%dT%H:%M')

    def test_create_time_column(self):
        column = Column('test', 0, ColumnType.TIME, time_format='%Y-%m-%dT%H:%M')
        assert isinstance(column, Column)

    def test_exeption_time_column_without_time_format(self):
        with pytest.raises(ValueError):
            Column('test', 0, ColumnType.TIME)

    @pytest.mark.dependency()
    def test_column_mapping_creation(self):
        column_list = [
            Column('case_id', 0, ColumnType.CASE_ID),
            Column('task_name', 1, ColumnType.TASK_NAME),
            Column('time', 2, ColumnType.TIME, time_format='%Y-%m-%dT%H:%M')
        ]
        column_mapping = ColumnMapping(column_list)
        assert isinstance(column_mapping, ColumnMapping)

    def test_exception_time_column_missing(self):
        with pytest.raises(ValueError):
            ColumnMapping([
                Column('case_id', 0, ColumnType.CASE_ID),
                Column('task_name', 1, ColumnType.TASK_NAME)
            ])

    def test_exception_too_many_case_id_columns(self):
        with pytest.raises(ValueError):
            ColumnMapping([
                Column('case_id_1', 0, ColumnType.CASE_ID),
                Column('case_id_2', 1, ColumnType.CASE_ID),
                Column('task_name', 2, ColumnType.TASK_NAME),
                Column('time', 3, ColumnType.TIME, time_format='%Y-%m-%dT%H:%M')
            ])

    def test_exception_duplicate_column_indices(self):
        with pytest.raises(ValueError):
            ColumnMapping([
                Column('case_id', 0, ColumnType.CASE_ID),
                Column('task_name', 0, ColumnType.TASK_NAME),
                Column('time', 1, ColumnType.TIME, time_format='%Y-%m-%dT%H:%M')
            ])
