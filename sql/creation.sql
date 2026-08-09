-- ============================================================
-- FakeStore ETL - RAW Layer Database Schema
-- PostgreSQL
-- ============================================================

-- ============================================================
-- 1. Create RAW schema
-- ============================================================

CREATE SCHEMA raw;

-- ============================================================
-- 3. Products
-- ============================================================

CREATE TABLE raw.products (
    product_id INTEGER PRIMARY KEY,

    title VARCHAR(255) NOT NULL,

    description TEXT,

    category VARCHAR(100),

    price NUMERIC(12, 2),

    discount_percentage NUMERIC(5, 2),

    rating NUMERIC(3, 2),

    stock INTEGER,

    brand VARCHAR(150),

    sku VARCHAR(100) UNIQUE,

    weight NUMERIC(10, 2),

    warranty_information VARCHAR(255),

    shipping_information VARCHAR(255),

    availability_status VARCHAR(100),

    return_policy VARCHAR(255),

    minimum_order_quantity INTEGER,

    thumbnail TEXT,

    created_at TIMESTAMP,

    updated_at TIMESTAMP,

    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- 4. Product Dimensions
-- ============================================================

CREATE TABLE raw.product_dimensions (
    product_id INTEGER PRIMARY KEY,

    width NUMERIC(10, 2),

    height NUMERIC(10, 2),

    depth NUMERIC(10, 2),

    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_product_dimensions_product
        FOREIGN KEY (product_id)
        REFERENCES raw.products(product_id)
        ON DELETE CASCADE
);

-- ============================================================
-- 5. Product Tags
-- ============================================================

CREATE TABLE raw.product_tags (
    product_id INTEGER NOT NULL,

    tag VARCHAR(100) NOT NULL,

    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (product_id, tag),

    CONSTRAINT fk_product_tags_product
        FOREIGN KEY (product_id)
        REFERENCES raw.products(product_id)
        ON DELETE CASCADE
);

-- ============================================================
-- 6. Product Reviews
-- ============================================================

CREATE TABLE raw.product_reviews (
    review_id BIGSERIAL PRIMARY KEY,

    product_id INTEGER NOT NULL,

    rating INTEGER,

    comment TEXT,

    review_date TIMESTAMP,

    reviewer_name VARCHAR(255),

    reviewer_email VARCHAR(255),

    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_product_reviews_product
        FOREIGN KEY (product_id)
        REFERENCES raw.products(product_id)
        ON DELETE CASCADE
);

-- ============================================================
-- 7. Product Metadata
-- ============================================================

CREATE TABLE raw.product_metadata (
    product_id INTEGER PRIMARY KEY,

    meta_created_at TIMESTAMP,

    meta_updated_at TIMESTAMP,

    barcode VARCHAR(100),

    qr_code TEXT,

    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_product_metadata_product
        FOREIGN KEY (product_id)
        REFERENCES raw.products(product_id)
        ON DELETE CASCADE
);

-- ============================================================
-- 8. Product Images
-- ============================================================

CREATE TABLE raw.product_images (
    image_id BIGSERIAL PRIMARY KEY,

    product_id INTEGER NOT NULL,

    image_url TEXT NOT NULL,

    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_product_images_product
        FOREIGN KEY (product_id)
        REFERENCES raw.products(product_id)
        ON DELETE CASCADE
);

-- ============================================================
-- 9. Useful Indexes
-- ============================================================

CREATE INDEX idx_products_category
    ON raw.products(category);

CREATE INDEX idx_products_brand
    ON raw.products(brand);

CREATE INDEX idx_products_sku
    ON raw.products(sku);

CREATE INDEX idx_product_dimensions_product_id
    ON raw.product_dimensions(product_id);

CREATE INDEX idx_product_tags_product_id
    ON raw.product_tags(product_id);

CREATE INDEX idx_product_reviews_product_id
    ON raw.product_reviews(product_id);

CREATE INDEX idx_product_images_product_id
    ON raw.product_images(product_id);

CREATE INDEX idx_product_metadata_product_id
    ON raw.product_metadata(product_id);

-- ============================================================
-- 10. Verify Tables
-- ============================================================

SELECT
    table_schema,
    table_name
FROM information_schema.tables
WHERE table_schema = 'raw'
ORDER BY table_name;