from fastapi import FastAPI
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        database=os.getenv("DB_NAME", "liftstations_data"),
        user=os.getenv("DB_USER", "lift_mechanic"),
        password=os.environ["DB_PASS"]
    )

@app.get("/api/stations")
def get_stations():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    # Fetch all records sorted numerically
    cursor.execute("SELECT station_number, station_name, latitude, longitude FROM stations ORDER BY station_number ASC;")
    stations = cursor.fetchall()
    cursor.close()
    conn.close()
    return stations
