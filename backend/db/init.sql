CREATE TABLE IF NOT EXISTS stations (
    station_number INTEGER PRIMARY KEY,
    station_name TEXT NOT NULL,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION
);
-- Fictional records only; demonstration coordinates are not station locations.
INSERT INTO stations (station_number, station_name, latitude, longitude) VALUES
    (1, 'Demo station — example coordinates only', 0.0, 0.0),
    (2, 'Demo station — awaiting coordinates', NULL, NULL),
    (3, 'Sample pump site — awaiting coordinates', NULL, NULL)
ON CONFLICT (station_number) DO NOTHING;
