import re
import os
from pathlib import Path
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import psycopg2

# 1. Connect to Postgres container
conn = psycopg2.connect(
    host=os.getenv("DB_HOST", "db"),
    database=os.getenv("DB_NAME", "liftstations_data"),
    user=os.getenv("DB_USER", "lift_mechanic"),
    password=os.environ["DB_PASS"]
)
cursor = conn.cursor()

# 2. Setup OpenStreetMap Geocoder
geolocator = Nominatim(user_agent="titusville_liftstation_mapper_v2")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1.5)

print("Starting robust background geocoding...")

# 3. Read and parse the text file
with open(Path(__file__).with_name("liftstations.txt"), "r") as file:
    for line in file:
        line = line.strip()
        # Handle matching for LS or P stations
        if not line or not (line.startswith("LS") or line.startswith("P")):
            continue
            
        try:
            # Extract prefix, number, and location string
            match = re.match(r"(LS|P)\s*(\d+):\s*(.*)", line)
            if match:
                station_num = int(match.group(2))
                address_raw = match.group(3)
                
                # Clean address: Strip out text in parentheses for clean mapping
                address_clean = re.sub(r"\(.*?\)", "", address_raw).strip()
                
                # Format intersections or loose descriptors to look cleaner
                if "Corner of" in address_clean:
                    address_clean = address_clean.replace("Corner of", "").strip()
                if "at" in address_clean:
                    address_clean = address_clean.replace(" at ", " & ").strip()
                
                full_address = f"{address_clean}, Titusville, FL"
                
                print(f"Geocoding Station {station_num}: {full_address}...")
                location = geocode(full_address)
                
                if location:
                    lat = location.latitude
                    lon = location.longitude
                    
                    cursor.execute(
                        """
                        INSERT INTO stations (station_number, station_name, latitude, longitude)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (station_number) DO UPDATE 
                        SET station_name = EXCLUDED.station_name, 
                            latitude = EXCLUDED.latitude, 
                            longitude = EXCLUDED.longitude;
                        """,
                        (station_num, address_raw, lat, lon)
                    )
                    conn.commit()
                    print(f"✅ Saved Station {station_num} ({lat}, {lon})")
                else:
                    print(f"❌ Could not find coordinates for: {full_address}")
                    
        except Exception as e:
            print(f"静态 Error on line '{line}': {e}")
            conn.rollback() # This keeps the script from freezing up on database errors

cursor.close()
conn.close()
print("Import complete. Refresh the navigator.")
