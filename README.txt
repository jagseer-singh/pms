PHARMACY REAL-TIME INVENTORY/MANAGEMENT SYSTEM:

This project is made in PYTHON.
In order to run this project you will need to install the following modules:
-FLASK
-PYODBC
-NUMPY
-PANDAS
-PASSLIB
-SKLEARN
-PICKLE

Extra files:
	We could not find any datasets for our project so we had to create datasets.

	-Stock.csv and Stock.xlsx contains the list of drugs availabe at the pharmacy.
	-sql_scripts.sql contains SQL queries to create the required database and tables that are required for this project.
	-manager_order_list_random_dataset.py creates a random dataset for the table manager_order_list
	-stock_random_dataset.py  creates a random dataset which updates the manager_order_list table and updates the stock of our pharmacy.
	-selling_random_dataset.py create a random dataset which produces selling information which would be used in predicting threshold value for each product.

training_model.py: Here a model is trained to predict threshold values for each of the product.
selling_predictor.pkl: The trained model is saved in this pickle file.
predicting_threshold.py: Created Model is called to predict threshold value in this file.

main.py: This is the main file which contains all the functions required to run the website.


If you want to run these files on your own pc the order is:
-pms/extra files/sql_scripts.sql
-pms/extra files/manager_order_list_random_dataset.py
-pms/extra files/stock_random_dataset.py
-pms/extra files/selling_random_dataset.py
-pms/main.py
