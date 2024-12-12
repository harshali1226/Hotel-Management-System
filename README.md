# CS425-Database-Organisation
Final Project for CS-425 course

Steps for instruction:

1. SQL workbench setup:
a) Open the Configuration.sql on your sql workbench and run the first two commands. This creates and sets a default schema 'Hotel_Management'.
b) Run each create statement for the table and import data for the created table from the 'Data' folder using Import Data Wizard.
c) Run the create View statement at the bottom of the file to create a view. This view is required in the python code.

2. Python code setup:
a) Open the folder in VSCode or code editor of your choice. Open the terminal and run the following command.
   pip install mysql-connector-python
b) After the successful installation of mysql-connector-python package open the file /Config/connection.py and change the username and password for your sql workbench.
c) Once you have configured this run the following command. This will start the application in the terminal.
   python main.py