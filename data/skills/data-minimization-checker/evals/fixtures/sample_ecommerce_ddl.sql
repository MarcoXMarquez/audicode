-- ==============================================================================
-- E-Commerce Platform Database Schema (DDL)
-- Production release v3.4 - Digital Goods & Streaming Marketplace
-- Intended Purpose: Online purchase, licensing and streaming of digital assets
-- ==============================================================================

CREATE TABLE users (
    user_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    mother_maiden_name VARCHAR(100) NOT NULL, -- Used for security questions recovery
    national_id VARCHAR(30) NOT NULL,         -- Stored for checkout verification
    birth_date DATE NOT NULL,                 -- Full date of birth to check legal majority (+18)
    blood_type VARCHAR(5) NOT NULL,           -- Profile enrichment / corporate wellness perk
    religion VARCHAR(50) NULL,                -- Optional demographic profiling
    gender VARCHAR(20) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    is_deleted BOOLEAN DEFAULT FALSE          -- Soft delete flag without scheduled hard purge
);

CREATE TABLE digital_purchases (
    purchase_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    digital_item_sku VARCHAR(64) NOT NULL,
    amount_paid DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    precise_gps_latitude DECIMAL(10, 7) NOT NULL,   -- Mobile GPS latitude at moment of purchase
    precise_gps_longitude DECIMAL(10, 7) NOT NULL,  -- Mobile GPS longitude at moment of purchase
    user_device_imei VARCHAR(20) NOT NULL,          -- Device hardware identifier for anti-fraud
    user_agent_full TEXT NOT NULL,
    purchase_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_purchase_user FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE user_payment_methods (
    payment_method_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    cardholder_name VARCHAR(150) NOT NULL,
    pan_credit_card VARCHAR(19) NOT NULL,       -- 16-19 digit Primary Account Number in clear text
    card_expiration_month INT NOT NULL,
    card_expiration_year INT NOT NULL,
    card_cvv VARCHAR(4) NOT NULL,               -- CVV/CVC persisted in table for re-billing
    bank_account_iban VARCHAR(34) NULL,         -- Bank IBAN stored for refund payouts
    billing_street_address VARCHAR(255) NOT NULL,
    billing_postal_code VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_payment_user FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE customer_service_audit_logs (
    log_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    session_id VARCHAR(128) NOT NULL,
    client_ip VARCHAR(45) NOT NULL,             -- Full IPv4 / IPv6 address unmasked
    browser_fingerprint VARCHAR(255) NOT NULL,  -- Canvas/Audio fingerprint string
    agent_notes TEXT NULL,
    temp_payload_dump LONGTEXT NULL,            -- Raw JSON snapshot of request payload for debugging
    log_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    -- No TTL or retention expiration column defined
);
