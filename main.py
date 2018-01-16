from serial_vis.py import *

# extend the serial_device class to add user definitions.
class my_serial_device(serial_device):

	# register commands here
	def register_user_commands(self):

		# example function prototype
		self.commands.update{"exampleuserfunction":"s"}

	# register user settings here
	def register_user_settings(self):
		
		# should update self.log_settings, self.graphics_settings
		pass

	# todo: pass user functions to graphics class


# create object
my_serial_device = my_serial_device("/dev/lm4f",115200)

# that's it!
while(1):
	my_serial_device.update()
