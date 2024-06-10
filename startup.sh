#!/bin/bash

service mysql stop
service mysql start

mysql -u "$DB_USER" -p"$DB_PASSWORD" < mysqlsampledatabase.sql
python3 app.py