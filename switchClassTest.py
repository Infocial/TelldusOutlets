from switches import TelldusSwitch

from time import sleep

# WiringPi pin number is 0 and button press is repeated 5 times.
switchTest = TelldusSwitch(0,5)

# Turn on switch 1 (also used to program the switch)
switchTest.switchOutlet(1,1)

sleep(2)

# Turn off switch 1
switchTest.switchOutlet(1,0)

sleep(2)

# Turn on every switch for this remote
switchTest.switchAll(1)

sleep(2)

# Turn off every switch for this remote
switchTest.switchAll(0)
