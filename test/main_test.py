from traffic_light.__main__ import main
from unittest import mock
import pytest


@mock.patch("usb.core.find")
@pytest.mark.parametrize("test_input,expected", [
    (['--all', 'on'], 0),
    (['--all', 'off'], 0),
    (['-a', 'off'], 0),
])
def test_set_all_leds(usb_find_mock, test_input, expected):
    assert main(test_input) == expected


@pytest.mark.parametrize("test_input", [
    (['--all', 'foo']),
    (['--blue', 'on'])
])
def test_should_fail_for_wrong_argument_and_value(test_input):
    with pytest.raises(SystemExit):
        main(test_input)


@mock.patch("usb.core.find")
@pytest.mark.parametrize("test_input,expected", [
    (['--red', 'on'], 0),
    (['--red', 'off'], 0),
    (['-r', 'off'], 0),
    (['--yellow', 'on'], 0),
    (['--yellow', 'off'], 0),
    (['-y', 'off'], 0),
    (['--green', 'on'], 0),
    (['--green', 'off'], 0),
    (['-g', 'off'], 0),
])
def test_set_diffrent_color_leds(usb_find_mock, test_input, expected):
    assert main(test_input) == expected


@pytest.mark.parametrize("test_input,expected", [
    (['-adr', "2"], 1),
    (['--address', "2"], 1),
])
def test_should_fail_for_no_given_color(test_input, expected):
    assert main(test_input) == expected


@mock.patch("usb.core.find")
def test_should_fail_for_multiple_lights_whitout_given_address(usb_find_mock):
    # given
    usb_find_mock.return_value = [mock.MagicMock(), mock.MagicMock()]
    # then
    assert main(["--red", "on"]) == 1


@mock.patch("usb.core.find")
def test_should_fail_for_no_connected_light(usb_find_mock):
    # given
    usb_find_mock.return_value = None

    # then
    assert main(["--red", "on"]) == 1
