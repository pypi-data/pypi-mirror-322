"""
Generates Pytest test suite dictionaries for concurrency, integer parsing,
and other parameter-validation functionalities.

These functions return dictionaries mapping test names to test callbacks,
and they are intended to be imported and run within a Pytest context.
"""

from typing import Any, Callable, Dict, List, Optional, Sequence, Union
from unittest.mock import patch
import pytest

def makeTestSuiteConcurrencyLimit(functionUnderTest: Callable[[Any], int], cpuCount: int = 8) -> Dict[str, Callable[[], None]]:
    """
    Creates a test suite for defineConcurrencyLimit-like functions.

    Parameters:
        functionUnderTest: The function to test, must return int
        cpuCount (8): Number of CPUs to simulate

    Returns:
        dictionaryTests: Dictionary of test functions to run
    """
    @patch('multiprocessing.cpu_count', return_value=cpuCount)
    def testDefaults(_mockCpu):
        for limitParameter in [None, False, 0]:
            assert functionUnderTest(limitParameter) == cpuCount

    @patch('multiprocessing.cpu_count', return_value=cpuCount)
    def testDirectIntegers(_mockCpu):
        for limitParameter in [1, 4, 16]:
            assert functionUnderTest(limitParameter) == limitParameter

    @patch('multiprocessing.cpu_count', return_value=cpuCount)
    def testFractionalFloats(_mockCpu):
        testCases = {
            0.5: cpuCount // 2,
            0.25: cpuCount // 4,
            0.75: int(cpuCount * 0.75)
        }
        for input, expected in testCases.items():
            assert functionUnderTest(input) == expected

    @patch('multiprocessing.cpu_count', return_value=cpuCount)
    def testMinimumOne(_mockCpu):
        for limitParameter in [-10, -0.99, 0.1]:
            assert functionUnderTest(limitParameter) >= 1

    @patch('multiprocessing.cpu_count', return_value=cpuCount)
    def testBooleanTrue(_mockCpu):
        assert functionUnderTest(True) == 1
        assert functionUnderTest('True') == 1
        assert functionUnderTest('TRUE') == 1
        assert functionUnderTest(' true ') == 1

    @patch('multiprocessing.cpu_count', return_value=cpuCount)
    def testInvalidStrings(_mockCpu):
        for stringInput in ["invalid", "True but not quite", "None of the above"]:
            with pytest.raises(ValueError, match="must be a number, True, False, or None"):
                functionUnderTest(stringInput)

    @patch('multiprocessing.cpu_count', return_value=cpuCount)
    def testStringNumbers(_mockCpu):
        testCases = [
            ("1.5", 1),
            ("-2.5", 6),
            ("4", 4),
            ("0.5", 4),
            ("-0.5", 4),
        ]
        for stringNumber, expectedLimit in testCases:
            assert functionUnderTest(stringNumber) == expectedLimit

    return {
        'testDefaults': testDefaults,
        'testDirectIntegers': testDirectIntegers,
        'testFractionalFloats': testFractionalFloats,
        'testMinimumOne': testMinimumOne,
        'testBooleanTrue': testBooleanTrue,
        'testInvalidStrings': testInvalidStrings,
        'testStringNumbers': testStringNumbers
    }

def makeTestSuiteIntInnit(functionUnderTest: Callable[[Sequence, str], List]) -> Dict[str, Callable[[], None]]:
    """
    Creates a test suite for intInnit-like functions.

    Parameters:
        functionUnderTest: The function to test, must accept list and return list[int]

    Returns:
        dictionaryTests: Dictionary of test functions to run
    """
    def testHandlesValidIntegers():
        assert functionUnderTest([1, 2, 3], 'test') == [1, 2, 3]
        assert functionUnderTest([1.0, 2.0, 3.0], 'test') == [1, 2, 3]
        assert functionUnderTest(['1', '2', '3'], 'test') == [1, 2, 3]
        assert functionUnderTest([' 42 ', '0', '-1'], 'test') == [42, 0, -1]

    def testRejectsNonWholeNumbers():
        for invalidNumber in [1.5, '1.5', ' 1.5 ', -2.7]:
            with pytest.raises(ValueError):
                functionUnderTest([invalidNumber], 'test')

    def testRejectsBooleans():
        with pytest.raises(TypeError):
            functionUnderTest([True, False], 'test')

    def testRejectsInvalidStrings():
        for invalidString in ['abc', '', ' ', '1.2.3']:
            with pytest.raises(ValueError):
                functionUnderTest([invalidString], 'test')

    def testRejectsEmptyList():
        with pytest.raises(ValueError):
            functionUnderTest([], 'test')

    def testHandlesMixedValidTypes():
        assert functionUnderTest([1, '2', 3.0], 'test') == [1, 2, 3]

    def testHandlesSingleBytes():
        testCases = [
            ([b'\x01'], [1]),
            ([b'\xff'], [255]),
            ([bytearray(b'\x02')], [2]),
            ([memoryview(b'\x01')], [1]),
            ([memoryview(b'\xff')], [255]),
        ]
        for inputData, expected in testCases:
            assert functionUnderTest(inputData, 'test') == expected
        with pytest.raises(ValueError):
            functionUnderTest([b'\x01\x02'], 'test')

    def testRejectsMutableSequence():
        class MutableList(list):
            def __iter__(self):
                self.append(4)
                return super().__iter__()
        with pytest.raises(RuntimeError, match=".*modified during iteration.*"):
            functionUnderTest(MutableList([1, 2, 3]), 'test')

    def testHandlesComplexIntegers():
        testCases = [
            ([1+0j], [1]),
            ([2+0j, 3+0j], [2, 3])
        ]
        for inputData, expectedList in testCases:
            assert functionUnderTest(inputData, 'test') == expectedList

    def testRejectsInvalidComplex():
        for invalidComplex in [1+1j, 2+0.5j, 3.5+0j]:
            with pytest.raises(ValueError):
                functionUnderTest([invalidComplex], 'test')

    return {
        'testHandlesValidIntegers': testHandlesValidIntegers,
        'testRejectsNonWholeNumbers': testRejectsNonWholeNumbers,
        'testRejectsBooleans': testRejectsBooleans,
        'testRejectsInvalidStrings': testRejectsInvalidStrings,
        'testRejectsEmptyList': testRejectsEmptyList,
        'testHandlesMixedValidTypes': testHandlesMixedValidTypes,
        'testHandlesSingleBytes': testHandlesSingleBytes,
        'testRejectsMutableSequence': testRejectsMutableSequence,
        'testHandlesComplexIntegers': testHandlesComplexIntegers,
        'testRejectsInvalidComplex': testRejectsInvalidComplex
    }

def makeTestSuiteOopsieKwargsie(functionUnderTest: Callable[[str], Optional[Union[bool, str]]]) -> Dict[str, Callable[[], None]]:
    """
    Creates a test suite for oopsieKwargsie-like functions.

    Parameters:
        functionUnderTest: The function to test, must accept str and return bool|None|str

    Returns:
        dictionaryTests: Dictionary of test functions to run
    """
    def testHandlesTrueVariants():
        for variantTrue in ['True', 'TRUE', ' true ', 'TrUe']:
            assert functionUnderTest(variantTrue) is True

    def testHandlesFalseVariants():
        for variantFalse in ['False', 'FALSE', ' false ', 'FaLsE']:
            assert functionUnderTest(variantFalse) is False

    def testHandlesNoneVariants():
        for variantNone in ['None', 'NONE', ' none ', 'NoNe']:
            assert functionUnderTest(variantNone) is None

    def testReturnsOriginalString():
        for stringInput in ['hello', '123', 'True story', 'False alarm']:
            assert functionUnderTest(stringInput) == stringInput

    def testHandlesNonStringObjects():
        class UnStringable:
            def __str__(self):
                raise TypeError("Cannot be stringified")

        # This integer should get converted to string
        assert functionUnderTest(123) == "123" # type: ignore

        # This custom object should be returned as-is (same object) if str() fails
        unStringableObject = UnStringable()
        result = functionUnderTest(unStringableObject) # type: ignore
        assert result is unStringableObject

    return {
        'testHandlesTrueVariants': testHandlesTrueVariants,
        'testHandlesFalseVariants': testHandlesFalseVariants,
        'testHandlesNoneVariants': testHandlesNoneVariants,
        'testReturnsOriginalString': testReturnsOriginalString,
        'testHandlesNonStringObjects': testHandlesNonStringObjects
    }
