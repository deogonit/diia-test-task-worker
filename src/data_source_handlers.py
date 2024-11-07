import concurrent
import logging

import requests

STATIC_REPORTS_BASE_URL = "https://guide.diia.gov.ua/api/v1/static_reports"
TIMEOUT = 10
THREAD_POOL_EXECUTOR_MAX_WORKERS = None


def fetch_data_regional_state_administrations(
    year: int, quarter: int
) -> list[dict] | None:
    state_administrations_reports_url = (
        f"{STATIC_REPORTS_BASE_URL}/list/{year}/{quarter}/?format=json"
    )
    response = requests.get(state_administrations_reports_url, timeout=TIMEOUT)
    results = response.json().get("results", [])
    if not results:
        logging.warning(
            "There are no data about administrations by %s",
            state_administrations_reports_url,
        )
        return

    return results


def fetch_data_admin_service_centers(
    state_admin_obj: dict,
) -> list[dict] | None:
    admin_service_centers_url = (
        f"{STATIC_REPORTS_BASE_URL}/entries/{state_admin_obj['id']}?format=json"
    )

    response = requests.get(admin_service_centers_url, timeout=TIMEOUT)
    results = response.json().get("results", [])
    if not results:
        logging.warning(
            "There are no data about SC by %s", admin_service_centers_url
        )
        return

    return [
        result_obj | {"rs_admin_id": state_admin_obj["rs_admin_id"]}
        for result_obj in results
    ]


def get_data_admin_service_centers(state_administrations: list[dict]):
    admin_service_centers = []
    exceptions: list[Exception] = []

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=THREAD_POOL_EXECUTOR_MAX_WORKERS
    ) as executor:
        get_admin_service_centers_futures = {
            executor.submit(
                fetch_data_admin_service_centers, state_adminitration_obj
            )
            for state_adminitration_obj in state_administrations
        }

        for future in concurrent.futures.as_completed(
            get_admin_service_centers_futures
        ):
            try:
                admin_service_centers.extend(future.result())
            except Exception as exc:
                exceptions.append(exc)

    if exceptions:
        logging.warning(
            "Multiple exceptions occurred when "
            "retrieve data about admin service centers"
        )
        return

    return admin_service_centers


def fetch_data_admin_sc_details(
    service_center: dict,
) -> dict | None:
    service_center_details_url = (
        f"{STATIC_REPORTS_BASE_URL}/detail/{service_center['id']}?format=json"
    )

    response = requests.get(service_center_details_url, timeout=TIMEOUT)
    results = response.json().get("results", [])
    if not results:
        logging.warning(
            "There are no data about SC details by %s",
            service_center_details_url,
        )
        return

    # Endpoint api/v1/static_reports/detail/<report_entries_id>
    # returns only one element
    return results[0] | {"service_center_id": service_center["db_admin_sc_id"]}


def get_data_admin_sc_details(
    admin_service_centers: list[dict],
) -> list[dict] | None:
    admin_sc_details = []
    exceptions: list[Exception] = []

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=THREAD_POOL_EXECUTOR_MAX_WORKERS
    ) as executor:
        get_service_center_details_futures = {
            executor.submit(fetch_data_admin_sc_details, admin_service_obj)
            for admin_service_obj in admin_service_centers
        }

        for future in concurrent.futures.as_completed(
            get_service_center_details_futures
        ):
            try:
                admin_sc_details.append(future.result())
            except Exception as exc:
                exceptions.append(exc)

    if exceptions:
        logging.warning(
            "Multiple exceptions occurred when "
            "retrieve data about admin sc details"
        )
        return

    return admin_sc_details
