import pyodbc

conn = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=BEAST;DATABASE=cafe;')
cursor = conn.cursor()