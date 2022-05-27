from enum import IntEnum
from struct import pack

import functools
import usb.core
import usb.util

from traffic_light.error import TrafficLightError, MultipleTrafficLightsError

CTRL_ENDPOINT = 0x02
ID_VENDOR = 0x0d50
ID_PRODUCT_ORIGINAL = 0x0008
ID_PRODUCT_SWITCH = 0x0030
ID_PRODUCTS = (ID_PRODUCT_ORIGINAL, ID_PRODUCT_SWITCH)
INTERFACE = 0


class Color(IntEnum):
    RED = 0x10
    YELLOW = 0x11
    GREEN = 0x12


class State(IntEnum):
    OFF = 0x0
    ON = 0x1


class ClewareTrafficLight:
    def __init__(self, address=None):
        if address:
            self.address = address
            self.device = self.find_device(address=address)
        elif len(list(ClewareTrafficLight.find_devices())) > 1:
            raise MultipleTrafficLightsError(
                "No address is given and there are multiple devices conected! "
                "Use 'print_devices' to see a list of connected devices."
            )
        else:
            self.device = self.find_device()
        if self.device is None:
            raise TrafficLightError('Cleware traffic light not found!')
        self.reattach = False

    def attach(self):
        """Attaches the device back to the kernel"""
        usb.util.dispose_resources(self.device)
        if self.reattach:
            self.device.attach_kernel_driver(INTERFACE)

    def detach(self):
        """Detaches the device from to kernel so it can be used"""
        if self.device.is_kernel_driver_active(INTERFACE):
            self.device.detach_kernel_driver(INTERFACE)
            self.reattach = True

    @staticmethod
    def find_devices():
        """Returns the raw iterator of all found traffic lights"""
        devices = []

        for product_id in ID_PRODUCTS:
            if devs := usb.core.find(find_all=True, idVendor=ID_VENDOR,
                                     idProduct=product_id):
                devices.extend(devs)

        return devices

    @classmethod
    def find_device(self, address=None):
        """Returns a traffic light device, located at the specified address"""

        for product_id in ID_PRODUCTS:
            kwargs = {"idVendor": ID_VENDOR, "idProduct": product_id}
            if address is not None:
                kwargs["address"] = address

            if dev := usb.core.find(**kwargs):
                return dev

    @staticmethod
    def print_devices():
        """Prints a list of all connected traffic lights"""
        devices = ClewareTrafficLight.get_devices()
        for device in devices:
            print(device)

    @staticmethod
    def get_devices():
        """Returns a list of ClewareTrafficLight instances"""
        usb_devices = ClewareTrafficLight.find_devices()
        return [ClewareTrafficLight(d.address) for d in usb_devices]

    def _compute_led_payload(self, color, value):
        if self.device.idProduct == ID_PRODUCT_ORIGINAL:
            return [0x00, color, value]
        elif self.device.idProduct == ID_PRODUCT_SWITCH:
            # The traffic light v4 is acting like a switch. The switches' state
            # are represented as a 16-bit bitfield where bit 0 represents the
            # top-left LED, and all the following bits represent the next LED
            # anticlockwise all the way to bit 11 which represents the state of
            # the back-bottom LED.
            #
            # Updating the bitfield is done by setting every bit we
            # want to update in the mask, then setting the wanted value in the
            # value field. The final result will be equal to:
            #
            #     new_state = (state & ~mask) | value
            #
            # And here is the command one needs to set
            # - action: 8bits <-- Command 11
            # - value: 16 bits (big endian)
            # - mask: 16 bits (big endian)
            #
            color_id = color % 0x10      # Red = 0, Yellow = 1, Green = 2
            color_offset = color_id * 4  # Red = 0-3, Yellow = 4-7, Green = 8-11
            return pack(">BHH", 11, (0xf << color_offset) * value, 0xf << color_offset)
        else:
            raise TrafficLightError("Unknown product ID")

    def set_led(self, color, value, timeout=1000):
        """Sets the given state and color of the attached traffic light

        Attribute:
            color -- the to set color as the enum. E.g. Color.RED
            state -- the state to which it should be set. E.g. State.ON
            address -- the usb address of a specific traffic light
        """
        try:
            self.detach()
            payload = self._compute_led_payload(color, value)
            self.device.write(CTRL_ENDPOINT, payload, timeout=timeout)
        except Exception as exc:
            raise TrafficLightError(str(exc)) from exc
        finally:
            self.attach()

    def __getattr__(self, name):
        """Parses attribut calls in function"""
        args = name.split('_')
        try:
            color = Color[args[0].upper()]
            state = State[args[1].upper()]
        except Exception as exc:
            raise TrafficLightError("Either the given color or state could not be parsed! Exc: {}"
                                    .format(exc))
        return functools.partial(self.set_led, color, state)

    def __str__(self):
        """Converts instance into string with important imformations"""
        return ("== Cleware Traffic Light ==\n"
                "Address: {} \n"
                "IdVendor: {} \n"
                "IdProduct: {}".format(self.address, self.device.idVendor, self.device.idProduct))
