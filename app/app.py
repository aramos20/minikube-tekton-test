import os
import psycopg2
from flask_cors import CORS
from flask import Flask, jsonify

app = Flask(__name__)
CORS(app)

# Configuración de la base de datos
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'database')
DB_USER = os.getenv('DB_USER', 'user')
DB_PASS = os.getenv('DB_PASS', 'password')

# Conexión a la DB
def get_db_conn():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn

# Primeras configuraciones DB
def init_db():
    try:
        conn = get_db_conn()
        cursor = conn.cursor()

        # Tabla para contar visitas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS visits (
                id SERIAL PRIMARY KEY,
                count BIGINT
            )
        ''')

        # Tabla para indicar el modo (develop o release)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS config (
                id SERIAL PRIMARY KEY,
                environment VARCHAR(20)
            )
        ''')

        # Colocar registro en la tabla visits
        cursor.execute("SELECT COUNT(*) FROM visits")
        row_count = cursor.fetchone()[0]
        if row_count == 0:
            cursor.execute("INSERT INTO visits (count) VALUES (0)")

        # Insertar registro en la tabla config
        cursor.execute("SELECT COUNT(*) FROM config")
        row_count = cursor.fetchone()[0]
        if row_count == 0:
            cursor.execute("INSERT INTO config (environment) VALUES ('release')")

        conn.commit()
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error al inicializar la db: {e}")

init_db()

# Endpoint /visits
@app.route('/visits', methods=['GET'])
def visits():
    conn = get_db_conn()
    cursor = conn.cursor()

    # Incremento del contador de visitas
    cursor.execute('UPDATE visits SET count = count + 1 WHERE id = 1')
    conn.commit()

    # Obtener número de visitas
    cursor.execute('SELECT count FROM visits WHERE id = 1')
    visit_count = cursor.fetchone()[0]

    # Modo del sistema
    cursor.execute('SELECT environment FROM config WHERE id = 1')
    mode = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return jsonify({
        'message': 'Hola, mundo',
        'visits': visit_count,
        'mode': mode
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
