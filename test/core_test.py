from unittest import mock

import pytest

import usb.core

from traffic_light.core import ClewareTrafficLight, Color, State, ID_PRODUCT_ORIGINAL
from traffic_light.error import TrafficLightError, MultipleTrafficLightsError


@mock.patch("usb.core.find")
def test_should_initialize_light_by_address(usb_find_mock):
    # when
    light = ClewareTrafficLight(address=10)

    # then
    assert light.address == 10
    assert light.device is not None


@mock.patch("usb.core.find")
def test_should_fail_for_no_connected_light(usb_find_mock):
    # given
    usb_find_mock.return_value = None

    # when & then
    with pytest.raises(TrafficLightError, match="Cleware traffic light not found!"):
        ClewareTrafficLight()


@mock.patch("usb.core.find")
def test_should_fail_for_multiple_lights_whitout_address(usb_find_mock):
    # given
    usb_find_mock.return_value = [mock.MagicMock(), mock.MagicMock()]

    # when & then
    with pytest.raises(MultipleTrafficLightsError,
                       match="No address is given and there are multiple devices conected! "
                             "Use 'print_devices' to see a list of connected devices."):
        ClewareTrafficLight()


@mock.patch("usb.core.find")
def test_should_fail_for_wrong_color_in_getattr(usb_find_mock):
    # when & then
    with pytest.raises(TrafficLightError,
                       match="Either the given color or state could not be parsed"):
        ClewareTrafficLight().blue_on()


@mock.patch("usb.core.find")
def test_should_fail_for_wrong_state_in_getattr(usb_find_mock):
    # when & then
    with pytest.raises(TrafficLightError,
                       match="Either the given color or state could not be parsed"):
        ClewareTrafficLight().red_foo()


@mock.patch("usb.core.find")
@pytest.mark.parametrize("test_input,expected", [
    ((Color.RED, State.ON), (0x10, 0x1)),
    ((Color.RED, State.OFF), (0x10, 0x0)),
    ((Color.YELLOW, State.ON), (0x11, 0x1)),
    ((Color.YELLOW, State.OFF), (0x11, 0x0)),
    ((Color.GREEN, State.ON), (0x12, 0x1)),
    ((Color.GREEN, State.OFF), (0x12, 0x0))
])
def test_should_turn_on_led(usb_find_mock, test_input, expected):
    # given
    device_mock = mock.MagicMock(idProduct=ID_PRODUCT_ORIGINAL)
    usb_find_mock.return_value = device_mock
    light = ClewareTrafficLight()

    # when
    light.set_led(test_input[0], test_input[1])

    # then
    device_mock.write.assert_called_once_with(
        0x02, [0x00, expected[0], expected[1]], timeout=1000
    )


@mock.patch("usb.core.find")
def test_should_raise_exception_when_light_is_disconneted(usb_find_mock):
    # given
    device_mock = mock.MagicMock()
    device_mock.write.side_effect = usb.core.USBError("[Errno 5] Input/Output Error")
    usb_find_mock.return_value = device_mock
    light = ClewareTrafficLight()

    # when & then
    with pytest.raises(TrafficLightError):
        light.set_led(Color.RED, State.ON)


@mock.patch("usb.core.find")
def test_should_raise_exception_when_color_and_state_invalid(usb_find_mock):
    # given
    device_mock = mock.MagicMock()
    device_mock.write.side_effect = TypeError()
    usb_find_mock.return_value = device_mock
    light = ClewareTrafficLight()

    # when & then
    with pytest.raises(TrafficLightError):
        light.set_led("foo", 1)
