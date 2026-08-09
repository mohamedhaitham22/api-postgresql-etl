-- ============================================================
-- FakeStore ETL - Analytics Queries
-- PostgreSQL
-- Schema: raw
-- ============================================================


-- ============================================================
-- Query 1: List all products ordered by price
-- Purpose: View products from the most expensive to the cheapest.
-- ============================================================

SELECT
    product_id,
    title,
    category,
    brand,
    price
FROM raw.products
ORDER BY price DESC;


-- ============================================================
-- Query 2: Average price by category
-- Purpose: Calculate the average product price for each category.
-- ============================================================

SELECT
    category,
    COUNT(*) AS product_count,
    ROUND(AVG(price), 2) AS average_price
FROM raw.products
GROUP BY category
ORDER BY average_price DESC;


-- ============================================================
-- Query 3: Product count by category
-- Purpose: Identify how many products are available in each category.
-- ============================================================

SELECT
    category,
    COUNT(*) AS product_count
FROM raw.products
GROUP BY category
ORDER BY product_count DESC;


-- ============================================================
-- Query 4: Products with low stock
-- Purpose: Find products where the available stock is less than 20.
-- ============================================================

SELECT
    product_id,
    title,
    category,
    stock,
    price
FROM raw.products
WHERE stock < 20
ORDER BY stock ASC;


-- ============================================================
-- Query 5: Products with high discounts
-- Purpose: Find products with a discount percentage of 20% or more.
-- ============================================================

SELECT
    product_id,
    title,
    category,
    price,
    discount_percentage
FROM raw.products
WHERE discount_percentage >= 20
ORDER BY discount_percentage DESC;


-- ============================================================
-- Query 6: Product details with dimensions
-- Purpose: Join products with their physical dimensions.
-- ============================================================

SELECT
    p.product_id,
    p.title,
    p.category,
    d.width,
    d.height,
    d.depth
FROM raw.products AS p
INNER JOIN raw.product_dimensions AS d
    ON p.product_id = d.product_id
ORDER BY p.product_id;


-- ============================================================
-- Query 7: Products with their tags
-- Purpose: Join products and tags to see the tags associated
-- with each product.
-- ============================================================

SELECT
    p.product_id,
    p.title,
    p.category,
    pt.tag
FROM raw.products AS p
INNER JOIN raw.product_tags AS pt
    ON p.product_id = pt.product_id
ORDER BY p.product_id, pt.tag;


-- ============================================================
-- Query 8: Products with review statistics
-- Purpose: Calculate the number of reviews and average review
-- rating for every product.
-- ============================================================

SELECT
    p.product_id,
    p.title,
    p.category,
    COUNT(r.review_id) AS review_count,
    ROUND(AVG(r.rating), 2) AS average_review_rating
FROM raw.products AS p
LEFT JOIN raw.product_reviews AS r
    ON p.product_id = r.product_id
GROUP BY
    p.product_id,
    p.title,
    p.category
ORDER BY average_review_rating DESC NULLS LAST;


-- ============================================================
-- Query 9: Top-rated products
-- Purpose: Find products whose product rating is above the
-- overall average product rating.
-- ============================================================

SELECT
    product_id,
    title,
    category,
    rating,
    price
FROM raw.products
WHERE rating > (
    SELECT AVG(rating)
    FROM raw.products
)
ORDER BY rating DESC;


-- ============================================================
-- Query 10: Products with metadata and discount information
-- Purpose: Combine product information with barcode and QR code
-- metadata, and show the potential selling price after discount.
-- ============================================================

SELECT
    p.product_id,
    p.title,
    p.category,
    p.price AS original_price,
    p.discount_percentage,
    ROUND(
        p.price * (1 - p.discount_percentage / 100),
        2
    ) AS discounted_price,
    m.barcode,
    m.qr_code
FROM raw.products AS p
LEFT JOIN raw.product_meta AS m
    ON p.product_id = m.product_id
ORDER BY discounted_price DESC;
