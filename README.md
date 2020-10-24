# Movie Web Application

## Description

A Movie web!

## Installation

**Installation via requirements.txt**

First clone this project from the GitHub repository using a Git Bash 
shell as follows 
```shell
$ git init
$ git clone https://github.com/Ryen-LTC/CS235-A2.git
```
Then,
```shell
$ cd CS235-A2
$ py -3 -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```

When using PyCharm, set the virtual environment using 'File'->'Settings' and select 
'Project:CS235-A2' from the left menu. Select 'Project Interpreter', click on the 
gearwheel button and select 'Add'. Click the 'Existing environment' radio button 
to select the virtual environment. 

## Execution

**Running the application**

From the *CS235-A2* directory, and within the activated virtual environment 
(see *venv\Scripts\activate* above):

````shell
$ flask run
```` 

## Configuration

The *CS235-A2/.env* file contains variable settings. They are set with appropriate values.

* `FLASK_APP`: Entry point of the application (should always be `wsgi.py`).
* `FLASK_ENV`: The environment in which to run the application (either `development` or `production`).
* `SECRET_KEY`: Secret key used to encrypt session data.
* `TESTING`: Set to False for running the application. Overridden and set to True automatically when testing the application.
* `WTF_CSRF_SECRET_KEY`: Secret key used by the WTForm library.

## Testing

Testing requires that file *CS235-A2/tests/conftest.py* be edited to set the value of `TEST_DATA_PATH`. 
You should set this to the absolute path of the *CS235-A2/tests/data* directory. 

E.g. 

`TEST_DATA_PATH = os.path.join('C:', os.sep, 'Users', 'CI GE', 'Desktop',
                              'CS235-A2', 'tests', 'data')`

assigns TEST_DATA_PATH with the following value (the use of os.path.join and os.sep ensures use of the correct platform path separator):

`C:\Users\CI GE\Desktop\CS235-A2\tests\data`

You can then run tests from within PyCharm or by typing 

 ````shell
$ python -m pytest
```` 
from within the virtual environment in a terminal.