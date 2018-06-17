[![bPortal documentation](https://img.shields.io/badge/docs-passing-brightgreen.svg?style=flat-square)](https://sanchezfauste.github.io/bPortal)
[![GitHub (pre-)release](https://img.shields.io/github/release/sanchezfauste/bPortal/all.svg?style=flat-square)](https://github.com/sanchezfauste/bPortal/releases/latest)


# bPortal
bPortal is a SuiteCRM portal written using django project.

## Clone the repository
To clone the repository and all submodules simply run:
```
git clone --recursive https://github.com/sanchezfauste/bPortal.git
```
## Getting the development environment ready
In this section is described how to get the development environment ready on Debian based systems.

It's recommended to use `virtualenv` and `pip` packages. You can install this two dependencies runnig:
```
sudo apt-get update
sudo apt-get install virtualenv python-pip
```

Once you have `virtualenv` and `pip` tools ready it's time to prepare the virtual environment to run the application.  
Following we create a virtual environment and install all Python dependencies:
```
cd bPortal
virtualenv env
source env/bin/activate
pip install -r requirements.txt
pip install -r suitepy/requirements.txt
python manage.py migrate
```

Our development environment it's ready. Now we can create an admin account with:
```
python manage.py createsuperuser
```

To deactivate our Python virtual environment simply run:
```
deactivate
```

### Configuring SuiteCRM server
Edit conveniently `suitepy.ini` file.

### How to run the application using development environment
First of all we have to activate our virtual environment.  
Enter to root directory of the application (normally `bPortal`) and run:
```
source env/bin/activate
```

Now we can start `bPortal` on development mode running:
```
python manage.py runserver 0.0.0.0:8080
```

Once we have run the previous command, the application is listening on `http://localhost:8080`.

To stop the application press `CTRL-C` and run the command `deactivate` to deactivate the Python virtual environment.
