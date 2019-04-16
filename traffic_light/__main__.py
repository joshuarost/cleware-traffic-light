import sys
import argparse

from traffic_light.error import TrafficLightError, MultipleTrafficLightsError
from traffic_light.core import ClewareTrafficLight, State, Color


def main(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        prog="traffic_light",
        description='Turns the led of the cleware traffic light on or off'
    )
    parser.add_argument('-r', '--red',
                        choices=["on", "off"],
                        help="Controlls the red led")
    parser.add_argument('-y', '--yellow',
                        choices=["on", "off"],
                        help="Controlls the yellow led")
    parser.add_argument('-g', '--green',
                        choices=["on", "off"],
                        help="Controlls the green led")
    parser.add_argument('-a', '--all',
                        choices=["on", "off"],
                        help="Controlls all leds")
    parser.add_argument('-adr', '--address',
                        type=int,
                        help="Specifies which traffic light should be used")
    args = parser.parse_args(args)

    if not vars(args)['all']:
        all_given_colors = [(k, v) for k, v in vars(args).items()
                            if v is not None and k is not "address"]
        if not all_given_colors:
            parser.print_help()
            return 1
    else:
        all_state = vars(args)["all"]
        all_given_colors = [
            ('red', all_state), ('yellow', all_state), ('green', all_state)
        ]

    for color_name, state_name in all_given_colors:
        color = Color[color_name.upper()]
        state = State[state_name.upper()]
        address = vars(args)["address"]
        try:
            ClewareTrafficLight(address).set_led(color, state)
        except MultipleTrafficLightsError as exc:
            print(exc, file=sys.stderr)
            ClewareTrafficLight.print_devices()
            return 1
        except TrafficLightError as exc:
            print("Error -> {}".format(exc.message), file=sys.stderr)
            return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
