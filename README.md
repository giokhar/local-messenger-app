# local-messenger-app
This is a messenger app for people within the same wireless network

To run the project, you need to have python3 and pip3 installed.

It is recommended to create virtual environment first by running `virtualenv -p {PYTHON PATH} {NAME}`

Default {PYTHON PATH}: `/usr/local/bin/python3`

Default {NAME} of the virtual environment: `venv`

If `virtualenv` command is not found `pip3 install virtualenv`

When the virtual environment is created, activate it using `source {NAME}/bin/activate`, where default {NAME} is `venv`

After virtualenv is active, install all the dependencies of the project by running `pip3 install -r requirements.txt`

Run the project using `python3 main.py` and enjoy chat with your friends.
