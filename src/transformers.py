import datetime
import json


def transform_admin_service_center_detail_to_tuple(
    admin_service_center_detail: dict,
) -> tuple:
    now_datetime = datetime.datetime.now()

    return (
        admin_service_center_detail["service_center_id"],
        admin_service_center_detail["admin_service_data"]["num_total_services"],
        admin_service_center_detail["admin_service_data"]["num_e_services"],
        admin_service_center_detail["admin_service_data"]["num_rsa_services"],
        admin_service_center_detail["admin_service_data"]["num_dsa_services"],
        admin_service_center_detail["admin_service_data"]["num_city_services"],
        admin_service_center_detail["admin_service_data"]["num_asc_services"],
        admin_service_center_detail["admin_service_data"][
            "num_special_services"
        ],
        admin_service_center_detail["admin_service_data"][
            "is_all_asc_services_via_center"
        ],
        admin_service_center_detail["admin_service_data"][
            "num_from_this_year_start"
        ],
        json.dumps(admin_service_center_detail["info_support_data"]),
        json.dumps(admin_service_center_detail["admin_service_data"]),
        json.dumps(admin_service_center_detail["resp_person_data"]),
        now_datetime,
    )


def transform_admin_services_centers_to_tuples(
    admin_service_center: dict,
) -> tuple:
    rs_admin_id = admin_service_center["rs_admin_id"]
    center_idf = admin_service_center["asc_org"]["idf"]
    name = admin_service_center["asc_org"]["name"]

    address = admin_service_center["asc_org"].get("address")
    if address:
        address_full = address["address_full"]
        locality_name = (
            address["locality"]["name"] if address.get("locality") else None
        )
        postal_code = address["postal_code"]
        latitude = address["lat"]
        longitude = address["lon"]
    else:
        (
            address_full,
            locality_name,
            postal_code,
            latitude,
            longitude,
        ) = None, None, None, None, None

    return (
        rs_admin_id,
        center_idf,
        name,
        address_full,
        locality_name,
        postal_code,
        latitude,
        longitude,
    )
