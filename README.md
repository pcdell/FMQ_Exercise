# **Software Developer exercise interview - FMQ**

This project is a Flask application developed as an exercise to analyze office, employee, product, and customer data the data base mysqlsampledatabase.sql. Below is the documentation for setting up and running the application.


## **Project Structure**

app.py: Flask application entry point containing route definitions.
models.py: Database models using SQLAlchemy ORM.
templates/: HTML templates for rendering pages.
static/: Static files (CSS).

## **Functionality Overview**

 - **Offices:** 
	 - Analyze office details including number of employees and number of customers sortable in ascending or descending order and alphabetical order. 
 - **Products:**
	 -  View top 5 low stock products and top 5 best-selling products.
		 - Click on the arrow to reveal more details about each of these products.
	 - Display information for all products.
 -  **Employees:** 
	 - Insights into employee data including sales volume and purchase frequency.
	 - Determinate the `Promotion scores` by multiplying `Purchase Frequency` and `Sales Volume` to identify employees eligible for promotion.
 - **Customers:** 
	 - Identify top 20% customers by total spent for potential discounts.

## **Download and Execution**
Clone the repository `git clone <link>` or download the files to your machine.
This project was conceived to be run in a docker container to avoid dependency issues. Therefore make sure you have `docker` and `docker compose` in your machine.
Make sure you have a `.env` file with the following variables setup:

```
DB_USER = <your_user>
DB_PASSWORD = <your_password>
DB_HOSTNAME = <your_db_host>
DB_NAME = 'classicmodels'
SQLALCHEMY_TRACK_MODIFICATIONS = False
```
If you're running this in your local machine, your `.env`should look like this: 
```
DB_USER = 'root'
DB_PASSWORD = 'root123'
DB_HOSTNAME = 'localhost'
DB_NAME = 'classicmodels'
SQLALCHEMY_TRACK_MODIFICATIONS = False
```
***Note:*** By default MySQL server runs on Port 3306, therefore you should make sure no services are running on this Port when you execute this project.
If you have a different MySQL service running, please stop it using `sudo service mysql stop`.

Run `docker compose up` on the root of the repository.
Open the link output by the command and browse the website. If you ran it using the `.env` provided previously access it at `127.0.0.1:5000`.