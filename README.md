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
	
	$ ./main.py <plugin_name>

Run with a custom plugin on a single IP

	$ ./main.py <plugin_name> <ip_address>
