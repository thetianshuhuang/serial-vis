from serial_vis.py import *

# extend the serial_device class to add user definitions.
class my_serial_device(serial_device):

	# register commands here
	def register_user_commands(self):

		self.commands += {}

		# example command:
		# "dothis":["f","s","d","ff","ss","dd","ll"]
		# f = float, s = string, d = int, ff/ss/dd = array of float/string/int 

	# register user settings here
	def register_user_settings(self):
		
		self.colors += {}

		# example color:
		# "yellow":(255,255,0)
		# other attributes: self.scale: float, self.offset: (float,float)

	# program serial-callable user functions here
	def user_functions(self,instruction):

		if(instruction[0] = "example_opcode"):
			pass
			# perform operation
			return(True)

		else:
			return(False)


# create object
my_serial_device = my_serial_device("/dev/lm4f",115200,(800,600))

# that's it!
while(1):
	my_serial_device.update()
