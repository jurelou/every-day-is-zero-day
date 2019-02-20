# Requirements
*	python3.5
# Install

On Debian/Ubuntu:

	$ sudo apt-get install git gcc make libpcap-dev python3-pip
	$ git clone https://github.com/jurelou/every-day-is-zero-day.git --recurse-submodules
	$ cd every-day-is-zero-day
	$ ./setup.sh
# Usage

Run with default parameters

	$ ./main.py

Run with a custom plugin 
	
	$ ./main.py --plugin <PLUGIN_NAME>

Run with a custom plugin  on a single IP

	$ ./main.py -p <PLUGIN_NAME> -d <IP>


# Create new plugin

Adding a custom module is as simple as the following !!

	$ chmod+x ./scripts/new_plugin.sh && ./scripts/new_plugin.sh my_super_module
	$ ./main.py my_super_module
