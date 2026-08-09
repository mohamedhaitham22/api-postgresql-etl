from requests.exceptions import RequestException

from ..utils import get_logger
from ..clients import APIClient


logger = get_logger(__name__)


def extract_products(api_client: APIClient) -> list[dict]:
    logger.info("Starting product data extraction...")

    try:
        response = api_client.get("/products")
        product_data = response.json()

        if not isinstance(product_data, dict):
            logger.error(
                "Unexpected response format: %s",
                product_data
            )
            raise ValueError(
                "Expected API response to be a dictionary"
            )

        products = product_data.get("products")

        if not isinstance(products, list):
            logger.error(
                "Missing or invalid 'products' field"
            )
            raise ValueError(
                "Expected 'products' to be a list"
            )

        logger.info(
            "Successfully extracted %d products.",
            len(products)
        )

        return products

    except RequestException:
        logger.exception(
            "Failed to extract product data."
        )
        raise

    except ValueError:
        logger.exception(
            "Invalid product data format."
        )
        raise