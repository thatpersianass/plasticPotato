import psycopg2
from psycopg2 import Error

def get_connection():
    try:
        connection = psycopg2.connect(
            user="aed_user",
            password="aed_pass",
            host="localhost",
            port="5432",
            database="aed_db"
        )
        return connection
    except (Exception, Error) as error:
        print(f"Error conectando a la BD: {error}")
        return None