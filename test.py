import pyodbc

conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=cafe-test.database.windows.net;DATABASE=cafe;UID=indrajeet;PWD=Redwings@2022')
cursor = conn.cursor()

print("Connected")