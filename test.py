# import mysql.connector
# maxdb = mysql.connector.connect(
#   host = "localhost",
#   user = "joadmin",
#   password = "Qiok5432!",
#   database = "Ptt_Web_Crawler",
#   )
# cursor=maxdb.cursor()

# # Create db
# # cursor.execute("CREATE DATABASE Ptt_Web_Crawler")

# # Create table
# # cursor.execute("CREATE TABLE MacBook_Pro (name VARCHAR(255), type VARCHAR(255), spec VARCHAR(255), location VARCHAR(255), price INTEGER(99), post_at DATE,  article_id INTEGER AUTO_INCREMENT PRIMARY Key)")
# # cursor.execute("CREATE TABLE Apple_Watch (name VARCHAR(255), type VARCHAR(255), spec VARCHAR(255), location VARCHAR(255), price INTEGER(99), post_at DATE,  article_id INTEGER AUTO_INCREMENT PRIMARY Key)")
# cursor.execute("ALTER TABLE MacBook_Pro CHANGE post_at DATETIME")

# cursor.execute("ALTER TABLE Apple_Watch CHANGE post_at DATETIME")

# # # Insert Multiple Records
# # sqlStuff = "INSERT INTO users (name, age) VALUES (%s,%s)"
# # records = [("Steve", 24),
# #            ("Max", 25),
# #            ("Chang" ,26),]
# # cursor.executemany(sqlStuff, records)
# maxdb.commit()


a = [1,2,3,4,55]
b= a[1:4]
print('\n'.join(str(e) for e in b))