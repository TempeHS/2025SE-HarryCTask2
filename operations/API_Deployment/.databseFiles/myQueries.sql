CREATE TABLE IF NOT EXISTS property_data (
    id SERIAL PRIMARY KEY,
    num_bed INT,
    num_bath INT,
    property_size FLOAT,
    value_score FLOAT,
    tot_rooms INT,
    suburb_median_income FLOAT,
    suburb_lat FLOAT,
    suburb_lng FLOAT,
    km_from_cbd FLOAT,
    ds_float FLOAT,
    num_parking INT
);