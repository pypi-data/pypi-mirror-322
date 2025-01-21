from pandas import DataFrame
from .singleton import Singleton
from pandasql import sqldf
from os import getenv
from typing import Dict

class DatabaseFacade:
    """
        Fachada de base de datos, crea conexion con un singleton a mssql
    """
    def __init__(self, connection_string: str = getenv("MSSQL_STRING_CONNECTION")):
        self.db = Singleton(connection_string)

    def get_data(self, query) -> DataFrame:
        """
            Obtiene el resulado de una consulta de base de datos.
        """       
        return self.db.executable_query(query)

    def update_data(self, name, data: DataFrame) -> None:
        """
            Ejecuta un procedimiento almacenado en base de datos, 
            con el nombre y data que se le manden.
        """
        self.db.procedure(f"""
            EXEC {name} '{data.to_json(orient="records")}';
        """)
        
    def transaction(self, query) -> None:
        self.db.procedure(query)
        
    def modify_data(self, query: str, data: DataFrame) -> DataFrame:
        """
            Utiliza el paquete sqldf de pandasql para
            filtrar un Dataframe con consultas sql
        """
        return sqldf(query, locals())
       
    def modify_n_data(self, query: str, data: Dict[str, DataFrame]) -> DataFrame:
        """
            Utiliza el paquete sqldf de pandasql para
            filtrar n DataFrames Dataframe con 
            consultas sql
        """
        for var_name, dataframe in data.items():
        # Crear una instrucción de asignación de la forma 'var_name = dataframe'
            exec(f"{var_name} = dataframe")
            
        return sqldf(query, locals())
