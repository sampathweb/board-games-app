# Building an Tic Tac Toe App using Tornado and WebSockets

## Tic Tac Toe

Tic-Tac-Toe game (https://en.wikipedia.org/wiki/Tic-tac-toe) is a classic two player game that I love playing with my kids.  

I built this app using Python 3.5, but tested in Python 2.7 as well.

The Comamnd line version does not require any packages.  The Web version requires Tornado 4 as specified in the requirements.txt

### Command Line App (Play with Computer)

Navigate to board_games folder, then run from your terminal -

`python run_tic_tac_toe.py`

### Two Player version over WebSockets

1. Create a Virtual Environment - `pyvenv venv`.  For Python2, install `virtualenv venv`

2. Activate Virtual Environment - `source venv/bin/activate`.  For Windows, you may need `venv/scripts/activate`.

3. Install Requirments - `pip install -r requirements.txt`.  This will install Tornado Web Framework.

4. Run the App - `python run.py`

5. Open two browser Tabs for `http://localhost:9000` and Play the game.


## Deploy Steps Performed on AWS Ubuntu 14.04 LTS EC2 Instance

### Login to AWS Instance:

`ssh -i <your AWS Pem key file> ubuntu@<aws ip>`


### Install Python / Git

```
# Update Ubuntu

sudo apt-get update
sudo apt-get upgrade
sudo apt-get install libssl-dev openssl

# Install GIT
sudo apt-get install git

# Install Make
sudo apt-get install make


# Install Python 3
# Go to https://www.python.org/downloads/ and copy link to Python3

wget https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tgz

tar zxvf Python-3.5.2.tgz
cd Python-3.5.2
./configure
make
sudo make install

# Now test to make sure python3 is installed.
python3 <enter>

# Once that's confirmed, we don't need the installers anymore.  We can delete them.
cd ..
rm Python-3.5.2.tgz
sudo rm -rf Python-3.5.2/
```

### Run Tests

TODO

### Download App Source Code:

```
# Go to home directory
cd ~

# Create Projects folder where we will clone our app
mkdir projects
cd projects

git clone https://github.com/sampathweb/board-games-app.git
cd board-games-app

# Create Virtual Environment
pyvenv venv
source venv/bin/activate

# Install required packages for the app
pip install -r requirements.txt

# Test by running the app at command line
python run.py (Confirm that App is running)
```

### Run in Supervisor Process:

We want to serve the App under a Supervisor process so that we can Start / Stop and log errors in the app.

Let's install and configure Supervisor.

```
sudo apt-get install supervisor
sudo vi /etc/supervisor/conf.d/board-games-app.conf
<press i insert mode>


[program:board-games-app]
autostart = true
autorestart = true
command = /home/ubuntu/projects/board-games-app/venv/bin/python /home/ubuntu/projects/board-games-app/run.py --debug=False --port=80
numprocs = 1
startsecs = 10
stderr_logfile = /var/log/supervisor/board-games-app-err.log
stdout_logfile = /var/log/supervisor/board-games-app.log
environment = PYTHONPATH="/home/ubuntu/projects/board-games-app/venv/bin/"

<escape :wq>

sudo supervisorctl reload

# Verify that App is running under Supervisor.
# You may need to wait to few seconds for it go from Starting to Running

sudo supervisorctl status


<Your APP is live now>
```

### Test the App

Open Browser:  `http://<AWS IP>` (App is Live!)


### Updating App

Each time you update the App via a git pull on your ubuntu instance, restart Supervisor to update the running app process.

```
sudo supervisorctl restart all  
# You could also just say - restart board-games-app if you have multiple apps running

# Check if the restart has been successful.
sudo supervisorctl status
```

### The End