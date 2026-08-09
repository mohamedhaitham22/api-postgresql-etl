from datetime import datetime
from typing import Any

from ..utils import get_logger


logger = get_logger(__name__)


def transform_products(products: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:

    logger.info("Starting product data transformation...")

    transformed_data = {
        "products": [],
        "product_dimensions": [],
        "product_tags": [],
        "product_reviews": [],
        "product_metadata": [],
        "product_images": [],
    }

    for product in products:
        product_id = product.get("id")

        if product_id is None:
            logger.warning("Skipping product without an ID.")
            continue

        # ------------------------------------------------------
        # Products
        # ------------------------------------------------------

        transformed_data["products"].append(
            {
                "product_id": product_id,
                "title": product.get("title"),
                "description": product.get("description"),
                "category": product.get("category"),
                "price": product.get("price"),
                "discount_percentage": product.get("discountPercentage"),
                "rating": product.get("rating"),
                "stock": product.get("stock"),
                "brand": product.get("brand"),
                "sku": product.get("sku"),
                "weight": product.get("weight"),
                "warranty_information": product.get("warrantyInformation"),
                "shipping_information": product.get("shippingInformation"),
                "availability_status": product.get("availabilityStatus"),
                "return_policy": product.get("returnPolicy"),
                "minimum_order_quantity": product.get("minimumOrderQuantity"),
                "thumbnail": product.get("thumbnail"),
            }
        )

        # ------------------------------------------------------
        # Dimensions
        # ------------------------------------------------------

        dimensions = product.get("dimensions")

        if isinstance(dimensions, dict):
            transformed_data["product_dimensions"].append(
                {
                    "product_id": product_id,
                    "width": dimensions.get("width"),
                    "height": dimensions.get("height"),
                    "depth": dimensions.get("depth"),
                }
            )

        # ------------------------------------------------------
        # Tags
        # ------------------------------------------------------

        tags = product.get("tags", [])

        if isinstance(tags, list):
            for tag in tags:
                if tag is not None:
                    transformed_data["product_tags"].append(
                        {
                            "product_id": product_id,
                            "tag": str(tag),
                        }
                    )

        # ------------------------------------------------------
        # Reviews
        # ------------------------------------------------------

        reviews = product.get("reviews", [])

        if isinstance(reviews, list):
            for review in reviews:
                if not isinstance(review, dict):
                    continue

                transformed_data["product_reviews"].append(
                    {
                        "product_id": product_id,
                        "rating": review.get("rating"),
                        "comment": review.get("comment"),
                        "review_date": _parse_datetime(review.get("date")),
                        "reviewer_name": review.get("reviewerName"),
                        "reviewer_email": review.get("reviewerEmail"),
                    }
                )

        # ------------------------------------------------------
        # Metadata
        # ------------------------------------------------------

        metadata = product.get("meta")

        if isinstance(metadata, dict):
            transformed_data["product_metadata"].append(
                {
                    "product_id": product_id,
                    "meta_created_at": _parse_datetime(
                        metadata.get("createdAt")
                    ),
                    "meta_updated_at": _parse_datetime(
                        metadata.get("updatedAt")
                    ),
                    "barcode": metadata.get("barcode"),
                    "qr_code": metadata.get("qrCode"),
                }
            )

        # ------------------------------------------------------
        # Images
        # ------------------------------------------------------

        images = product.get("images", [])

        if isinstance(images, list):
            for image_url in images:
                if image_url is not None:
                    transformed_data["product_images"].append(
                        {
                            "product_id": product_id,
                            "image_url": str(image_url),
                        }
                    )

    logger.info(
        "Product transformation completed. "
        "Products: %d, Dimensions: %d, Tags: %d, "
        "Reviews: %d, Metadata: %d, Images: %d",
        len(transformed_data["products"]),
        len(transformed_data["product_dimensions"]),
        len(transformed_data["product_tags"]),
        len(transformed_data["product_reviews"]),
        len(transformed_data["product_metadata"]),
        len(transformed_data["product_images"]),
    )

    return transformed_data


def _parse_datetime(value: Any) -> datetime | None:
    """
    Convert an ISO 8601 datetime string into a Python datetime object.

    Example:
        2025-04-30T09:41:02.053Z
    """

    if not value:
        return None

    if isinstance(value, datetime):
        return value

    if not isinstance(value, str):
        return None

    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        logger.warning("Invalid datetime value: %s", value)
        return None