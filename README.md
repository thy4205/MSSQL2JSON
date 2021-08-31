<h1>MSSQL2JSON</h1>
This is a Python script to create JSON files from Microsoft SQL Server, if whatever reason you need to export database tables to any other platform (e.g. MySQL), and the version you are using is too old to export JSON natively.

This script creates the JSON file for data only.


## Requirement
* Software to create the SQL table structure (E.g. Online SQL convertor like SQLines)
* Basic knowlege for SQL
* Python 3
* OBDC Driver from Mircosoft that is suitable for your verison, the script defaults to MSSQL8, which do not support JSON export

### Instructions
1. Download or git clone the script
1. Change the required parameters in the script
  * Database IP address
  * Database Table Name
  * User Name
  * Password
  * OBDC Driver Name (if Required)