# Introduction
This is another version of code to extract content from PDF which has not been deployed. This version can automatically extract all the content from a PDF in the given format. We mainly use the titles in the PDF to locate the information that we want and store the content in the MySQL Database. 

# Setup
## Download XAMPP
1.	download XAMPP: https://www.apachefriends.org/download.html
2.	in XAMPP: Manage Servers -> start MySQL Database
3.	To view database: http://localhost/phpmyadmin/


## Install all the packages required to run this project use the code:
**pip install -r requirements.txt**

# Run
1.	open the XAMPP and start both Apache and MySQL.
 
2.	get into folder dbControlByFlask and use the command **python app.py** to run the project.
 

3.	Open the browser and enter the url: http://127.0.0.1:5000/login
Enter a username and a email to login.

4.	Choose a PDF that has the same format as the PDFs in the folder dbControlByFlask and click submit.

5.	We can see the browser will automatically jump to http://localhost:5000/process2 which shows the content in the PDF just submitted in the form of JSON.

6.	Then we can check whether the data has been stored correctly in the database by entering http://localhost/phpmyadmin/. The data is stored in the database called users.
 
