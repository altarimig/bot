from psycopg2 import connect, Error
from logger import write_errors

class ConnectionDB:
    
    bd = None
    cursor = None

    def __init__(self, **param):

        try:
            self.db = connect(
                host = '127.0.0.1',
                user = 'postgres',
                password = '/1(Iwasborn)*84',
                database = 'storage_messages'
            )
            self.cursor = self.db.cursor()
        except Error as e:
            write_errors(e, 'Tenemos problemas para acceder a la BD, verificar problema')

    def ejecutar_sql(
        self, 
        sentencia_sql, 
        param=None, 
        escribir_en_db=True
    ):
        
        try:
            execute = self.cursor.execute(sentencia_sql, param)
            if escribir_en_db:
                result =  self.db.commit()
            return self.cursor.rowcount
        except Exception as e:
            write_errors(e, f"Ocurrió un error al ejecutar la sentencia SQL:\n\n{sentencia_sql}\n")
            if escribir_en_db:
                self.db.rollback()

class Tabla(ConnectionDB):
    
    def crear_tabla(self):
        
        self.ejecutar_sql(
            """
            CREATE TABLE IF NOT EXISTS messages(
                id SERIAL,
                hour_date TIMESTAMP,
                user_id INT NOT NULL,
                name VARCHAR(50) NOT NULL,
                PRIMARY KEY (id)
            )
            """
        )

        # TABLA USUARIOS
        self.ejecutar_sql(
            """
            CREATE TABLE IF NOT EXISTS user(
                user_id SERIAL,
                name VARCHAR(50) NOT NULL,
                PRIMARY KEY (user_id)
            )
            """
        )

class Model():

    table_name = None
    connection = ConnectionDB()

    def create(self):
        table_name = self.table_name
        keys = ", ".join(self.__dict__.keys()) 
        values_placeholders = ", ".join(["%s" for i in range(len(self.__dict__.keys()))])
        values = self.__dict__.values()
        sql = f"INSERT INTO {table_name} ({keys}) VALUES ({values_placeholders})"
        
        return self.connection.ejecutar_sql(sql, tuple(values))
    