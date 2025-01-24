import datetime
import inspect
import pytest

import pandas as pd
import polars


from src.flodger.flodger import (
    _get_function_call_str,
    _coerce_value,
    _coerce_str,
    _coerce_basic_iterable,
    _coerce_dataframe,
    _coerce_series
)


def execute() -> bool:
    """A function with no arguments."""
    return True


def add(a: int, b: int) -> int:
    """A function with two positional arguments."""
    return a + b


def stringagg(*strings: str) -> str:
    """A function that takes strings and aggregates them."""
    return ''.join(strings)


def flex(*args, **kwargs):
    return args


class TestGetFunctionCallStr:
    def test_execute(self):
        """
        GIVEN the `execute` function
        THEN we get back the simple function_call_str 
        """
        expected_output = 'test_flodger:execute()'
        output = _get_function_call_str(
            execute, 
            args=(), 
            kwargs={}
        )
        assert expected_output == output

    def test_add_with_params(self):
        """
        GIVEN the `add` function
        THEN the params are included in the logged output
        """
        expected_output = 'test_flodger:add(1, 2)'
        output = _get_function_call_str(
            add, 
            args=(1, 2), 
            kwargs={}
        )
        assert expected_output == output

    def test_add_with_keyword_params(self):
        """
        GIVEN the `add` function
        WHEN we pass `b` as a keyword argument
        THEN the params are included in the logged output as expected
        """
        expected_output = 'test_flodger:add(1, b=2)'
        output = _get_function_call_str(
            add, 
            args=(1,), 
            kwargs={'b': 2}
        )
        assert expected_output == output

    def test_stringagg_small(self):
        """
        GIVEN the `stringagg` function
        WHEN we pass two strings small enough to not be coerced
        THEN both are included in the function_call_str in full 
        """
        expected_output = "test_flodger:stringagg('hello', 'world')"
        output = _get_function_call_str(
            stringagg,
            args=('hello', 'world'),
            kwargs={}
        )
        assert expected_output == output

    def test_stringagg_mix(self):
        """
        GIVEN the `stringagg` function
        WHEN we pass one string small enough to not be coerced and one big
            enough to be coerced
        THEN both are included in the function_call_str as expected
        """
        expected_output = "test_flodger:stringagg('hello', 'worldworldworldworldworldworldworldworldworldwo...')"
        output = _get_function_call_str(
            stringagg,
            args=('hello', 'world'*11),
            kwargs={}
        )
        assert expected_output == output

    def test_flex(self):
        """
        GIVEN the `flex` function
        WHEN we pass a DataFrame and a big list
        THEN the params are rendered as expected 
        """
        expected_output = 'test_flodger:flex(df=pandas.DataFrame<shape=(50, 3)>, names=list<len=30>)'
        output = _get_function_call_str(
            flex,
            args=(),
            kwargs={
                'df': pd.DataFrame({'a': range(50), 'b': range(50), 'c': range(50)}),
                'names': ['abcde']*30
            }
        )
        assert expected_output == output

    def test_polars(self): 
        """
        GIVEN we pass a `polars.DataFrame` to the `flex` function
        THEN the params are rendered as expected 
        """
        expected_output = 'test_flodger:flex(polars.DataFrame<shape=(50, 2)>)'
        output = _get_function_call_str(
            flex,
            args=(polars.DataFrame({'a': range(50), 'b': range(50)}), ),
            kwargs={}
        )
        assert expected_output == output


class TestCoerceValue:
    def test_none(self):
        assert _coerce_value(None) == 'None'

    def test_datetime(self):
        """
        GIVEN a datetime
        THEN we see the full repr
        """
        case = datetime.datetime(2024, 10, 14, 10, 58, 32, 535480)
        expected_output = case.__repr__()
        assert _coerce_value(case) == expected_output


class TestCoerceStr:
    def test_shorter_than_fifty(self):
        """
        GIVEN a string shorter than fifty characters 
        THEN the entire string is passed back exactly as it was
        """
        case = 'A string shorter than fifty characters'
        assert _coerce_str(case) == "'A string shorter than fifty characters'"

    def test_longer_than_fifty(self):
        """
        GIVEN a string longer than fifty characters
        THEN the string is passed back, coerced as expected 
        """
        case = 'x'*55
        expected_output = "'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx...'"
        assert _coerce_str(case) == expected_output

    def test_empty(self):
        """
        GIVEN an empty string
        THEN we get an empty string back 
        """
        case = ''
        expected_output = "''"
        assert _coerce_str(case) == expected_output


class TestCoerceBasicIterable:
    def test_list_small(self):
        """
        GIVEN a list that is small enough to display
        THEN a stringified version is returned 
        """
        case = [1, 2, 3]
        expected_output = '[1, 2, 3]'
        assert _coerce_basic_iterable(case) == expected_output

    def test_list_long(self):
        """
        GIVEN a list that is too big to display  
        THEN the summary is displayed in the expected format
        """
        case = ['x']*100
        expected_output = 'list<len=100>'
        assert _coerce_basic_iterable(case) == expected_output

    def test_list_empty(self):
        """
        GIVEN an empty list
        THEN the empty list is displayed 
        """
        assert _coerce_basic_iterable([]) == '[]'
    
    def test_set_small(self):
        """
        GIVEN a set that is small enough to display
        THEN a stringified version is returned 
        """
        case = {1, 2, 3}
        expected_output = '{1, 2, 3}'
        assert _coerce_basic_iterable(case) == expected_output

    def test_set_long(self):
        """
        GIVEN a set that is too big to display  
        THEN the summary is displayed in the expected format
        """
        case = set(range(200))
        expected_output = 'set<len=200>'
        assert _coerce_basic_iterable(case) == expected_output

    def test_dict_small(self):
        """
        GIVEN a dict that is small enough to display
        THEN a stringified version is returned 
        """
        case = {'a': 1, 'b': 2, 'c': 3}
        expected_output = "{'a': 1, 'b': 2, 'c': 3}"
        assert _coerce_basic_iterable(case) == expected_output

    def test_dict_long(self):
        """
        GIVEN a dict that is too big to display  
        THEN the summary is displayed in the expected format
        """
        case = {x: 'a' for x in range(200)}
        expected_output = 'dict<len=200>'
        assert _coerce_basic_iterable(case) == expected_output

    def test_tuple_small(self):
        """
        GIVEN a tuple that is small enough to display
        THEN a stringified version is returned 
        """
        case = (1, 2, 3)
        expected_output = '(1, 2, 3)'
        assert _coerce_basic_iterable(case) == expected_output

    def test_tuple_long(self):
        """
        GIVEN a tuple that is too big to display  
        THEN the summary is displayed in the expected format
        """
        case = tuple(['x']*100)
        expected_output = 'tuple<len=100>'
        assert _coerce_basic_iterable(case) == expected_output


class TestCoerceDataFrame:
    def test_pandas(self):
        df = pd.DataFrame({'a': [1, 2, 3], 'b': ['yes', 'no', 'maybe']})
        expected_output = 'pandas.DataFrame<shape=(3, 2)>'
        assert _coerce_dataframe(df, 'pandas') == expected_output

    def test_polars(self):
        df = pd.DataFrame({'a': [1, 2, 3], 'b': ['yes', 'no', 'maybe']})
        expected_output = 'polars.DataFrame<shape=(3, 2)>'
        assert _coerce_dataframe(df, 'polars') == expected_output

    def test_empty(self):
        df = pd.DataFrame()
        expected_output = 'pandas.DataFrame<shape=(0, 0)>'
        assert _coerce_dataframe(df, 'pandas') == expected_output


class TestCoerceSeries:
    def test_pandas(self):
        series = pd.Series([1, 2, 3])
        expected_output = 'pandas.Series<len=3>'
        assert _coerce_series(series, 'pandas') == expected_output

    def test_polars(self):
        series = polars.Series(name='test_series', values=[1, 2, 3])
        expected_output = 'polars.Series<len=3>'
        assert _coerce_series(series, 'polars') == expected_output

    def test_empty(self):
        series = pd.Series()
        expected_output = 'pandas.Series<len=0>'
        assert _coerce_series(series, 'pandas') == expected_output

