import sqlite3

class Connectionbd:
    """
    Clase que conecta la base de datos con la aplicación
    """

    def __init__ (self,reservasEnHotel):

        self.reservasEnHotel=reservasEnHotel

    def conectar(self):
        try:
            conn=sqlite3.connect(self.reservasEnHotel)
            return conn
        
        except sqlite3.Error as e:
            print(f"Error al conectar con la BBDD: {e}")
            return None
        
    def get_reservasSalon(self,tipoSalon):
        conn=self.conectar()
        if not conn:
            print("No se pudo conectar a la base de datos.")
            return []
        
        try:
            cursor=conn.cursor()
            query="""
            SELECT 
                r.reserva_id,
                r.fecha, 
                r.persona AS cliente, 
                r.telefono AS telefono, 
                tr.nombre AS tipo_reserva
                
            FROM 
                reservas r
            JOIN 
                tipos_reservas tr ON r.tipo_reserva_id=tr.tipo_reserva_id
            
            JOIN 
                salones s ON r.salon_id = s.salon_id
            WHERE 
                s.nombre = ?

            ORDER BY r.fecha DESC;

            """

            print(f"Ejecutando consulta para el salón: {tipoSalon}")

            cursor.execute(query,(tipoSalon,))
            resultado=cursor.fetchall()
            print(f"Resultado de la consulta: {resultado}")
            return resultado
        
        except sqlite3.Error as e:
            print(f"Error al consultar las reservas: {e}")
            return []
        
        finally:
            conn.close()

    def get_salones(self):
        conn = self.conectar()
        if not conn:
            print("No se pudo conectar a la base de datos.")
            return []
    
        try:
            cursor = conn.cursor()
            query = """
            SELECT salon_id, nombre
            FROM salones
            ORDER BY nombre;
            """
            cursor.execute(query)
            resultado = cursor.fetchall()
            return resultado
    
        except sqlite3.Error as e:
            print(f"Error al consultar los salones: {e}")
            return []
    
        finally:
            conn.close()

    def modificar_reserva(self, reserva_id, persona,telefono,fecha,salon_id, tipo_reserva_id,tipo_cocina_id, ocupacion, jornadas,habitaciones):
        conn=self.conectar()
        if not conn:
            print ("No se puede conectar a la BBDD")
            return False
        
        try:
            cursor=conn.cursor()
            query = """
            UPDATE reservas
            SET persona = ?, telefono = ?, fecha = ?, salon_id = ?, tipo_reserva_id = ?, tipo_cocina_id = ?, ocupacion = ?, jornadas = ?, habitaciones = ?
            WHERE reserva_id = ?
            """
            cursor.execute(query, (persona, telefono, fecha, salon_id, tipo_reserva_id, tipo_cocina_id, ocupacion, jornadas, habitaciones, reserva_id))
            conn.commit()
        
            if cursor.rowcount > 0:
                print(f"Reserva con ID {reserva_id} modificada correctamente.")
                return True
            else:
                print(f"No se encontró la reserva con ID {reserva_id}.")
                return False
        except sqlite3.Error as e:
            print(f"Error al modificar la reserva: {e}")
            return False
        finally:
            conn.close()
