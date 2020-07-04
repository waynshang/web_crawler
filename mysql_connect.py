import mysql.connector
from secret import mysql_secret
def connect(table_name):
	try:
		db = mysql.connector.connect(
		  host = mysql_secret["host"],
		  user = mysql_secret["user"],
		  password = mysql_secret["password"],
		  database = table_name,
		  )
	except mysql.connector.Error as error:
		print("Failed to insert record into Laptop table {}".format(error))
	return db
