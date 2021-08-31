<h1>MSSQL2JSON</h1>
This is a Python script to create JSON files from Microsoft SQL Server, if whatever reason you need to export database tables to any other platform (e.g. MySQL), and the version you are using is too old to export JSON natively.

MSSQL2JSON generates a JSON file table name, colume name, colume type and rows of data.

This script creates the JSON file for data only.

This script is also only tested in Windows Enviroment

## Requirement
* Basic knowlege for SQL
* Python 3
* OBDC Driver from Mircosoft that is suitable for your verison, the script defaults to MSSQL8, which do not support JSON export

### Instructions
1. Download or git clone the project if you feel like being fancy
1. Change the required parameters as stated in the script
  * Database IP address/ Hostname 
  * Database Table Name
  * User Name
  * Password
  * OBDC Driver Name (if Required)
1. Run the script in Command Prompt, make sure python is working correctly in Windows command prompt
1. The Output JSON file is generated and placed in the script directory.

## Caution
* This script will not care about how big your table is and it will consume large amount of memory if the table is big enough. However it should work fine in most of the situations.