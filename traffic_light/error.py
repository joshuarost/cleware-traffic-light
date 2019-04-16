class TrafficLightError(Exception):
    """Exception raiesed for errors in the traffic light

    Attributes:
        message -- error message
    """

    def __init__(self, message):
        self.message = message


class MultipleTrafficLightsError(Exception):
    """Exception raised if multiple traffic lights are connected but no address
    is specified

    Attributes:
        message -- error message
    """

    def __init__(self, message):
        self.message = message
