# Exceptions

class ZeroMass(Exception):
    pass


class ZeroRadius(Exception):
    pass


class NegativeMass(Exception):
    pass


class NonElectricalConductive(Exception):
    pass

# Warnings


class FasterThanSpeedLimitException(Warning):
    pass


class FurtherThanPositionLimitException(Warning):
    pass


class SamePosition(Warning):
    pass
