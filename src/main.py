from .extract import extract_products
from .clients import APIClient
from .storage import LocalStorage
from .transform import transform_products
from .load import load_products
from .database import engine
from .utils import configure_logger, get_logger


configure_logger()
logger = get_logger(__name__)


def main() -> None:
    logger.info("ETL pipeline started.")

    client = APIClient()
    storage = LocalStorage()

    try:
        # ==========================================================
        # 1. Extract
        # ==========================================================
        products = extract_products(client)

        logger.info(
            "Extracted %d products from API.",
            len(products),
        )

        # ==========================================================
        # 2. Save Raw Data
        # ==========================================================
        raw_file = storage.save_json(
            data=products,
            directory="products",
        )

        logger.info("Raw data saved to %s", raw_file)

        # ==========================================================
        # 3. Transform
        # ==========================================================
        transformed_data = transform_products(products)

        logger.info(
            "Successfully transformed product data."
        )

        # ==========================================================
        # 4. Load
        # ==========================================================
        load_products(
            engine=engine,
            transformed_data=transformed_data,
        )

        logger.info(
            "Successfully loaded transformed data into PostgreSQL."
        )

    except Exception:
        logger.exception("ETL pipeline failed.")
        raise

    finally:
        client.close()

    logger.info("ETL pipeline completed successfully.")


if __name__ == "__main__":
    main()