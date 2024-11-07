import logging
import os
import time

import psutil

from data_source_handlers import (
    fetch_data_regional_state_administrations,
    get_data_admin_sc_details,
    get_data_admin_service_centers,
)
from date_helper import get_previous_quarter
from db_handlers import (
    db_factory_connection,
    insert_admin_service_centers_data,
    insert_regional_state_admin_data,
    update_admin_service_centers_detailed_data,
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def run_worker():
    process = psutil.Process(os.getpid())
    start_time = time.time()
    logging.info("Worker started")

    year, quarter = get_previous_quarter()
    logging.info("Worker started for %d year and %d quarter", year, quarter)

    state_administrations = fetch_data_regional_state_administrations(
        year, quarter
    )
    if not state_administrations:
        return

    conn = db_factory_connection()
    enhanced_state_admins = insert_regional_state_admin_data(
        conn, state_administrations
    )

    admin_service_centers = get_data_admin_service_centers(
        enhanced_state_admins
    )
    if not admin_service_centers:
        return

    enhanced_service_centers = insert_admin_service_centers_data(
        conn, admin_service_centers
    )

    admin_sc_details = get_data_admin_sc_details(enhanced_service_centers)
    if not admin_sc_details:
        return

    update_admin_service_centers_detailed_data(conn, admin_sc_details)

    conn.close()
    end_time = time.time()
    total_time = end_time - start_time

    mem_info = process.memory_info()
    cpu_usage = process.cpu_percent()

    logging.info("Memory usage: %.2f MB", mem_info.rss / 1024**2)
    logging.info("CPU usage: %.1f%%", cpu_usage)
    logging.info("Worker finished; total time: %.3f seconds", total_time)


if __name__ == "__main__":
    run_worker()
