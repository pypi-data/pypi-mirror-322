import pytest

from astro_package.my_folder.myinnerfile import check_city


@pytest.mark.parametrize(
    argnames= "city_name, expected_result",
    argvalues=[('New York', True),('bengaluru',False),('chennai', False),('mumbai', False)])

def test_check_city_for_correct_city(city_name, expected_result):
    """ Test the check_city function to verify it returns the correct city.

    Args:
        city_name (str): The name of the city to check.
        expected_result (str): The expected result of the check_city function.

    Asserts:
        The result of check_city(city_name) is equal to expected_result. """
    assert check_city(city_name) == expected_result
