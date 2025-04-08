from google.cloud import spanner

# Configuraciones
project_id = "TU_PROJECT_ID"
instance_id = "TU_INSTANCE_ID"
database_id = "maik_memoria"

spanner_client = spanner.Client(project=project_id)
instance = spanner_client.instance(instance_id)
database = instance.database(database_id)

def guardar_memoria(usuario, mensaje, respuesta):
    with database.batch() as batch:
        batch.insert(
            table='memoria',
            columns=('usuario', 'mensaje', 'respuesta'),
            values=[(usuario, mensaje, respuesta)]
        )

def obtener_historial(usuario):
    historial = []
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(
            f"SELECT mensaje, respuesta FROM memoria WHERE usuario='{usuario}'"
        )
        for row in results:
            historial.append({'mensaje': row[0], 'respuesta': row[1]})
    return historial
