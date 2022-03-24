from grove.grove_relay import GroveRelay


def switchOn(digitalPortId):
    relay = GroveRelay(digitalPortId)
    relay.on()
    print("relay D{} on".format(digitalPortId))
    return


def switchOff(digitalPortId):
    relay = GroveRelay(digitalPortId)
    relay.off()
    print("relay D{} off".format(digitalPortId))
    return