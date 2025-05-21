# Softwares
PostegreSQL > 12
Python > 3.8

# Installation
Make sure you have the essential packages in your Linux distro.
If you have any error when install requirements.txt, specifically in psycopg2, run the commands below:
sudo apt-get install build-essential python3-dev libpq-dev

# PostgreSQL
If you are using WSL2, make sure you have a user with the same name you gave to the user in your Linux distro.
Example: I gave my Linux distro a name of leandro, so I need to have a user with the same name.
Code to create this user: sudo -u postgres createuser leandro