# liquibase-checks-python
Write your custom policy checks using Python! Secure your database and lock 
down your CI by running your own custom logic to evaluate the safety and security
of each database change.

### Requirements
* Python 3.10 or graalpy-24.0.0
* Liquibase 4.29.0

## Getting Started
We recommend installing `liquibase-checks-python` in a virtual environment.

### Installation
Create your virtual environment 

`python -m venv <path/to/venv>`

Install `liquibase-checks-python`

`pip install liquibase-checks-python`

You can validate the package has been successfully installed by running `pip list`

### Writing your first custom policy check
Create a file `custom.py` inside your liquibase working directory.

`touch custom.py`

Configure a new database scoped `CustomCheckTemplate` with the name `MyCustomCheck` with liquibase and set the `SCRIPT_PATH` to `custom.py`

`liquibase checks customize --check-name CustomCheckTemplate`

Open your `custom.py` in your text editor and add the following:

```python
from liquibase_checks_python import liquibase_utilities as lb
import sys

obj = lb.get_database_object()
status = lb.get_status()

if lb.is_table(obj):
	status.fired = True
	status.message = "No tables allowed!"
	sys.exit(1)
```

Run your new custom check

`liquibase --script-python-executable-path <path/to/venv>/bin/python --checks checks run --check-name MyCustomCheck --checks-scope database --checks-scripts-enabled`

If your database has any tables, you should see a warning like this:

```
DATABASE CHECKS
---------------
Validation of the database snapshot found the following issues:

Check Name:         Custom Check Template (test)
Object Type:        table
Object Name:        my_table
Object Location:    DEV.PUBLIC.my_table
Check Severity:     BLOCKER (Return code: 4)
Message:            No tables allowed!
```