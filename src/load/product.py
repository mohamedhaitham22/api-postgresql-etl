from typing import Any

from sqlalchemy import text
from sqlalchemy.engine import Engine

from ..config import settings
from ..utils import get_logger


logger = get_logger(__name__)


def load_products(
    engine: Engine,
    transformed_data: dict[str, list[dict[str, Any]]],
) -> None:
    """
    Load transformed product data into PostgreSQL RAW tables.

    Args:
        engine: SQLAlchemy database engine.
        transformed_data: Transformed product data grouped by table.

    Raises:
        Exception: If the database transaction fails.
    """

    logger.info("Starting product data loading...")

    schema = settings.POSTGRES_SCHEMA

    products = transformed_data.get("products", [])
    dimensions = transformed_data.get("product_dimensions", [])
    tags = transformed_data.get("product_tags", [])
    reviews = transformed_data.get("product_reviews", [])
    metadata = transformed_data.get("product_metadata", [])
    images = transformed_data.get("product_images", [])

    try:
        with engine.begin() as connection:

            # --------------------------------------------------
            # Products
            # --------------------------------------------------

            if products:
                connection.execute(
                    text(
                        f"""
                        INSERT INTO {schema}.products (
                            product_id,
                            title,
                            description,
                            category,
                            price,
                            discount_percentage,
                            rating,
                            stock,
                            brand,
                            sku,
                            weight,
                            warranty_information,
                            shipping_information,
                            availability_status,
                            return_policy,
                            minimum_order_quantity,
                            thumbnail
                        )
                        VALUES (
                            :product_id,
                            :title,
                            :description,
                            :category,
                            :price,
                            :discount_percentage,
                            :rating,
                            :stock,
                            :brand,
                            :sku,
                            :weight,
                            :warranty_information,
                            :shipping_information,
                            :availability_status,
                            :return_policy,
                            :minimum_order_quantity,
                            :thumbnail
                        )
                        ON CONFLICT (product_id)
                        DO UPDATE SET
                            title = EXCLUDED.title,
                            description = EXCLUDED.description,
                            category = EXCLUDED.category,
                            price = EXCLUDED.price,
                            discount_percentage = EXCLUDED.discount_percentage,
                            rating = EXCLUDED.rating,
                            stock = EXCLUDED.stock,
                            brand = EXCLUDED.brand,
                            sku = EXCLUDED.sku,
                            weight = EXCLUDED.weight,
                            warranty_information = EXCLUDED.warranty_information,
                            shipping_information = EXCLUDED.shipping_information,
                            availability_status = EXCLUDED.availability_status,
                            return_policy = EXCLUDED.return_policy,
                            minimum_order_quantity = EXCLUDED.minimum_order_quantity,
                            thumbnail = EXCLUDED.thumbnail,
                            updated_at = CURRENT_TIMESTAMP
                        """
                    ),
                    products,
                )

            # --------------------------------------------------
            # Product Dimensions
            # --------------------------------------------------

            if dimensions:
                connection.execute(
                    text(
                        f"""
                        INSERT INTO {schema}.product_dimensions (
                            product_id,
                            width,
                            height,
                            depth
                        )
                        VALUES (
                            :product_id,
                            :width,
                            :height,
                            :depth
                        )
                        ON CONFLICT (product_id)
                        DO UPDATE SET
                            width = EXCLUDED.width,
                            height = EXCLUDED.height,
                            depth = EXCLUDED.depth
                        """
                    ),
                    dimensions,
                )

            # --------------------------------------------------
            # Product Tags
            # --------------------------------------------------

            if tags:
                connection.execute(
                    text(
                        f"""
                        INSERT INTO {schema}.product_tags (
                            product_id,
                            tag
                        )
                        VALUES (
                            :product_id,
                            :tag
                        )
                        ON CONFLICT (product_id, tag)
                        DO NOTHING
                        """
                    ),
                    tags,
                )

            # --------------------------------------------------
            # Product Reviews
            # --------------------------------------------------

            if reviews:
                connection.execute(
                    text(
                        f"""
                        INSERT INTO {schema}.product_reviews (
                            product_id,
                            rating,
                            comment,
                            review_date,
                            reviewer_name,
                            reviewer_email
                        )
                        VALUES (
                            :product_id,
                            :rating,
                            :comment,
                            :review_date,
                            :reviewer_name,
                            :reviewer_email
                        )
                        """
                    ),
                    reviews,
                )

            # --------------------------------------------------
            # Product Metadata
            # --------------------------------------------------

            if metadata:
                connection.execute(
                    text(
                        f"""
                        INSERT INTO {schema}.product_metadata (
                            product_id,
                            meta_created_at,
                            meta_updated_at,
                            barcode,
                            qr_code
                        )
                        VALUES (
                            :product_id,
                            :meta_created_at,
                            :meta_updated_at,
                            :barcode,
                            :qr_code
                        )
                        ON CONFLICT (product_id)
                        DO UPDATE SET
                            meta_created_at = EXCLUDED.meta_created_at,
                            meta_updated_at = EXCLUDED.meta_updated_at,
                            barcode = EXCLUDED.barcode,
                            qr_code = EXCLUDED.qr_code
                        """
                    ),
                    metadata,
                )

            # --------------------------------------------------
            # Product Images
            # --------------------------------------------------

            if images:
                connection.execute(
                    text(
                        f"""
                        INSERT INTO {schema}.product_images (
                            product_id,
                            image_url
                        )
                        VALUES (
                            :product_id,
                            :image_url
                        )
                        """
                    ),
                    images,
                )

    except Exception:
        logger.exception("Failed to load product data.")
        raise

    logger.info(
        "Product data loading completed successfully. "
        "Products: %d, Dimensions: %d, Tags: %d, "
        "Reviews: %d, Metadata: %d, Images: %d",
        len(products),
        len(dimensions),
        len(tags),
        len(reviews),
        len(metadata),
        len(images),
    )