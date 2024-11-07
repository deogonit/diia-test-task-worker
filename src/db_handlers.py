import os

import psycopg
from psycopg import rows as psycopg_rows

from transformers import (
    transform_admin_service_center_detail_to_tuple,
    transform_admin_services_centers_to_tuples,
)

INSERT_RS_ADMINS_STATEMENT = """
INSERT INTO regional_state_administrations (rsa_name, rsa_edrpou, rsa_address)
VALUES (%s, %s, %s)
ON CONFLICT (rsa_edrpou) DO NOTHING
"""
SELECT_RS_ADMIN_STATEMENT = """
SELECT id, rsa_edrpou from regional_state_administrations ORDER BY rsa_edrpou;
"""

INSERT_ADMIN_CENTERS_STATEMENT = """
INSERT INTO admin_service_centers (
    rs_admin_id,
    center_idf,
    name,
    address,
    locality_name,
    postal_code,
    latitude,
    longitude
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (center_idf) DO NOTHING;
"""
SELECT_ADMIN_CENTERS_STATEMENTS = """
SELECT id, center_idf from admin_service_centers ORDER BY center_idf;
"""

INSERT_SC_DETAILS_STATEMENT = """
INSERT INTO admin_service_centers_details (
    admin_sc_id, num_total_services,
    num_e_services, num_rsa_services,
    num_dsa_services, num_city_services,
    num_asc_services, num_special_services,
    is_all_asc_services_via_center,
    num_from_this_year_start, accessibility_options,
    admin_service_data, resp_person_data, updated_at
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (admin_sc_id) DO UPDATE
SET
    num_total_services = EXCLUDED.num_total_services,
    num_e_services = EXCLUDED.num_e_services,
    num_rsa_services = EXCLUDED.num_rsa_services,
    num_dsa_services = EXCLUDED.num_dsa_services,
    num_city_services = EXCLUDED.num_city_services,
    num_asc_services = EXCLUDED.num_asc_services,
    num_special_services = EXCLUDED.num_special_services,
    is_all_asc_services_via_center = EXCLUDED.is_all_asc_services_via_center,
    num_from_this_year_start = EXCLUDED.num_from_this_year_start,
    accessibility_options = EXCLUDED.accessibility_options,
    admin_service_data = EXCLUDED.admin_service_data,
    resp_person_data = EXCLUDED.resp_person_data,
    updated_at = EXCLUDED.updated_at;
"""


DB_PARAMS = {
    "dbname": os.environ.get("POSTGRES_DB", "app"),
    "user": os.environ.get("POSTGRES_USER", "app"),
    "password": os.environ.get("POSTGRES_PASSWORD", "app"),
    "host": os.environ.get("POSTGRES_HOST", "localhost"),
    "port": os.environ.get("POSTGRES_PORT", 15432),
}


def db_factory_connection():
    return psycopg.connect(**DB_PARAMS)


def insert_regional_state_admin_data(
    conn: psycopg.Connection, state_administrations: list[dict]
):
    with conn.cursor() as cursor:
        data_to_insert = [
            (
                state_admin["rsa"]["name"],
                state_admin["rsa"]["edrpou"],
                state_admin["rsa"]["address"],
            )
            for state_admin in state_administrations
        ]

        cursor.executemany(
            INSERT_RS_ADMINS_STATEMENT,
            data_to_insert,
        )
        conn.commit()

    with conn.cursor(row_factory=psycopg_rows.dict_row) as cursor:
        cursor.execute(SELECT_RS_ADMIN_STATEMENT)
        db_rs_administrations = cursor.fetchall()

    rsa_edrpou_to_id = {
        rs_admin["rsa_edrpou"]: rs_admin["id"]
        for rs_admin in db_rs_administrations
    }

    for state_admin in state_administrations:
        state_admin["rs_admin_id"] = rsa_edrpou_to_id[
            state_admin["rsa"]["edrpou"]
        ]

    return state_administrations


def insert_admin_service_centers_data(
    conn: psycopg.Connection, admin_service_centers: list[dict]
):
    with conn.cursor() as cursor:
        data_to_insert = [
            transform_admin_services_centers_to_tuples(asc_obj)
            for asc_obj in admin_service_centers
        ]

        cursor.executemany(
            INSERT_ADMIN_CENTERS_STATEMENT,
            data_to_insert,
        )
        conn.commit()

    with conn.cursor(row_factory=psycopg_rows.dict_row) as cursor:
        cursor.execute(SELECT_ADMIN_CENTERS_STATEMENTS)
        db_admin_centers = cursor.fetchall()

    center_idf_to_id = {
        asc_obj["center_idf"]: asc_obj["id"] for asc_obj in db_admin_centers
    }

    for admin_center in admin_service_centers:
        admin_center["db_admin_sc_id"] = center_idf_to_id[
            admin_center["asc_org"]["idf"]
        ]

    return admin_service_centers


def update_admin_service_centers_detailed_data(
    conn: psycopg.Connection, details: list[dict]
):
    with conn.cursor() as cursor:
        data_to_update = [
            transform_admin_service_center_detail_to_tuple(detail_obj)
            for detail_obj in details
        ]

        cursor.executemany(
            INSERT_SC_DETAILS_STATEMENT,
            data_to_update,
        )
        conn.commit()
