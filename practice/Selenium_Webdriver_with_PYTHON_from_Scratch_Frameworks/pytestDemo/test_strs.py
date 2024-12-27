import pytest



# @pytest.mark.xfail # Run it but not 'reported' the result
def test_same_strs(setup):
    expected_str = "Hello"
    actual_str = "Hello"
    err_msg = "Both str are not equal"
    assert expected_str	== actual_str, err_msg

