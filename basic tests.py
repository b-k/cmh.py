"""Just some rudimentary tests for the CMH calculator. Like all unit test suites,
arbitrary and incomplete."""

from warnings import catch_warnings
import pandas as pd
from cmh import _get_control_cols, cmh

if __name__ == '__main__':
    testdata = [["a", 12, 12,    8],
                ["a", 12, 33. ,9],
                ["b", 12., 123,11],
                ["a", 0, 1     ,21]]
    test_df = pd.DataFrame(testdata, columns=["a", "b", "c", "ct"])

    # Check the include/excludes. Note that 'coulmns b and c are floating-point.
    print("Check that this warning is printed: ")
    with catch_warnings(record=True) as caught_warnings:
        assert _get_control_cols(test_df, "a", "b", "ct",["∀, ∀, ∀."],[]) == []
        assert len(caught_warnings) == 1

    # Cast columns b and c to int and try again
    test_df[['b','c']] = test_df[['b', 'c']].astype('int32')


    with catch_warnings(record=True) as caught_warnings:
        no_control = _get_control_cols(test_df, "a", "b", "ct",["∀, ∀, ∀."], ["c"])
        assert no_control == []
        assert set(_get_control_cols(test_df, "a", "b", "ct",["∀, ∀, ∀."], []))== set(['c'])
        assert len(caught_warnings) == 0
    print(cmh(test_df, 'a', 'b', 'ct', indep_c=lambda x: x=='a'))

    # Test reduction and roll-up of the data set
    print(cmh(test_df, 'a', 'b', 'ct', no_control, indep_c=lambda x: x=='a'))

    print("CMH module tests passed.")
