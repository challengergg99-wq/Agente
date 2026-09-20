#conexion a postgresql 
import psycopg2
connection = psycopg2.connect(
        user="postgres",
        password="1234",
        host="localhost",
        database="prueba"
    )
print("conexion exitosa")
   
