import psycopg2
import csv
from datetime import datetime
import os

# PostgreSQL connection details from environment variables
host = os.environ.get("PG_HOST")
database = os.environ.get("PG_DATABASE")
user = os.environ.get("PG_USER")
password = os.environ.get("PG_PASSWORD")


csv_file = "student_data.csv"

conn = psycopg2.connect(
    host=host,
    database=database,
    user=user,
    password=password
)
cur = conn.cursor()

try:
    
    create_table_query = """
    CREATE TABLE students (
        id SERIAL PRIMARY KEY,
        Prenom VARCHAR(50),
        Nom VARCHAR(50),
        Sexe VARCHAR(10),
        Notes CHAR(1),
        Niveux INTEGER,
        Pays VARCHAR(50),
        Date_Naissance DATE
    )
    """
    cur.execute(create_table_query)
    conn.commit()

    
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            ID = row['ID']
            Prenom = row['Prenom']
            Nom = row['Nom']
            Sexe = row['Sexe']
            Notes = row['Notes']
            Niveux = int(row['Niveux'])
            Pays = row['Pays']
            Date_Naissance = datetime.strptime(row['Date_Naissance'], '%d-%m-%Y').date()

            insert_query = """
            INSERT INTO students (id, Prenom, Nom, Sexe, Niveux, Notes, Pays, Date_Naissance)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(insert_query, (ID, Prenom, Nom, Sexe, Niveux, Notes, Pays, Date_Naissance))

    conn.commit()
    print("Data inserted successfully.")

except psycopg2.Error as e:
    print("Error:", e)
    conn.rollback()

finally:
    cur.close()
    conn.close()