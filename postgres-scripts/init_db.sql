CREATE TABLE regional_state_administrations (
    id SERIAL PRIMARY KEY,
    rsa_name TEXT,
    rsa_edrpou TEXT UNIQUE,
    rsa_address TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);


CREATE TABLE admin_service_centers (
    id SERIAL PRIMARY KEY,
    rs_admin_id INT REFERENCES regional_state_administrations(id),
    center_idf VARCHAR(50) UNIQUE,
    name TEXT,
    address TEXT,
    locality_name TEXT,
    postal_code TEXT,
    latitude FLOAT,
    longitude FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);


CREATE TABLE admin_service_centers_details (
    id SERIAL PRIMARY KEY,
    admin_sc_id INT UNIQUE REFERENCES admin_service_centers(id),
    num_total_services INT,
    num_e_services INT,
    num_rsa_services INT,
    num_dsa_services INT,
    num_city_services INT,
    num_asc_services INT,
    num_special_services INT,
    is_all_asc_services_via_center BOOLEAN,
    num_from_this_year_start INT,
    accessibility_options JSONB,
    admin_service_data JSONB,
    resp_person_data JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP
);
