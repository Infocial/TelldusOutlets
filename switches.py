import wiringpi
class TelldusSwitch:
	'433MHz outlet control for Telldus/Proove self-learning switches'
    
	# ID for this hacked remote
	sSenderId = [2,2,1,2,2,3,2,1,3,1,3,1,2,3,1,2,2,2,3,1,3,2,1,2]
	bGroupId = [[2,3,2],[2,3,1]]
	sGroupId = [[2,2,2],[2,3,1],[3,1,2],[1,2,3],[1,3,2],[2,1,3],[3,2,1],[1,1,1],
	[1,1,2],[1,1,3],[1,2,1],[1,2,2],[1,3,1],[1,3,3],[2,1,1],[2,1,2],[2,2,1],[2,2,3],
	[2,3,2],[2,3,3],[3,1,1],[3,1,3],[3,2,2],[3,2,3],[3,3,1],[3,3,2],[3,3,3]]
	sSwitchState = [[2,1,2],[1,2,2],[3,1,2],[2,2,2]]

	# Timings in microseconds
	tSync = 2550
	tPulse = 250
	tSymbol = 1250 - tPulse
	tBlock = 10000


	def __init__(self, pinNumber, repeatTransmit):
		# Set pinnumber on rpi and repeat the transmissions
		self.nPin = pinNumber
		self.nRepeatTransmit = repeatTransmit
		wiringpi.wiringPiSetup()
		wiringpi.pinMode(self.nPin, 1)


	# setPinNumber set the wiringPi pinnumber which the transmitter is connected to
	def setPinNumber(self, pinNumber):
		self.nPin = pinNumber
		wiringpi.pinMode(self.nPin, 1)


	# Mimicks one or multiple buttonpresses
	def setRepeatTransmit(self, repeatTransmit):
		self.nRepeatTransmit = repeatTransmit


	# Switch off every outlet in a group. 
	# (groupNumber = 1..27)
	# (switchState = 0..3)
	def switchOutlet(self, groupNumber, switchState):
		if ( 0 < groupNumber and groupNumber <= len(TelldusSwitch.sGroupId[:][0]) and 0 <= switchState and switchState < 4):
			# Sender id
			if (1 < switchState):
				signal = TelldusSwitch.sSenderId + TelldusSwitch.bGroupId[1]
			else:
				signal = TelldusSwitch.sSenderId + TelldusSwitch.bGroupId[0]

		    for g in range(self.nRepeatTransmit):
       			for h in range(0,6):
		            # Signals go SYNC->SENDER->SWITCH->GROUP

					# Sync id
                	self.sendSync()
					# Sender id loop
                	for i in range(len(signal)):
						self.transmit(signal[i])
                
                	# Switch id loop (ie. on or off)
                	for j in range(len(TelldusSwitch.sSwitchState[switchState][:])):
                    	self.transmit(TelldusSwitch.sSwitchState[switchState][j])
                
                	# Group id loop 
			        for k in range(len(TelldusSwitch.sGroupId[groupNumber-1][:])):
                    	self.transmit(TelldusSwitch.sGroupId[groupNumber-1][k])
                
                	wiringpi.delayMicroseconds(TelldusSwitch.tBlock)
            
            	wiringpi.delayMicroseconds(TelldusSwitch.tBlock*2)
        
        	return 1
		else:
        	return 0
    
	# Switch all outlets on or off within this id
	def switchAll(self, switch):
		if (switch == 0):
			self.switchOutlet(1,2)
		elif (switch == 1):
			self.switchOutlet(1,3)

	# Transmits any number of pulses then pauses for tSymbol
	def transmit(self, pulses):
    	# Loop for each pulse
		for i in range(pulses):
		    wiringpi.digitalWrite(self.nPin, 1)
	        wiringpi.delayMicroseconds(TelldusSwitch.tPulse)
		    wiringpi.digitalWrite(self.nPin, 0)
		    wiringpi.delayMicroseconds(TelldusSwitch.tPulse)
    
    	# Symbol pause
		wiringpi.delayMicroseconds(TelldusSwitch.tSymbol)
    

	# Sync isn't a normal pulse so it has its own function the transmition
	# is a normal length high and a much longer low (about 10 times)
	def sendSync(self):
		wiringpi.digitalWrite(self.nPin, 1)
		wiringpi.delayMicroseconds(TelldusSwitch.tPulse)
    	wiringpi.digitalWrite(self.nPin, 0)
    	wiringpi.delayMicroseconds(TelldusSwitch.tSync)

