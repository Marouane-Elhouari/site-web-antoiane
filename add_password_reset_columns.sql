-- SQL Commands to add password reset columns to existing user table
-- Run these commands in your MySQL database to update the table structure

-- Add reset_code column (6-digit code for password reset)
ALTER TABLE user 
ADD COLUMN reset_code VARCHAR(6) NULL 
AFTER verification_code;

-- Add reset_expiration column (timestamp for code expiration)
ALTER TABLE user 
ADD COLUMN reset_expiration DATETIME NULL 
AFTER reset_code;

-- Optional: Add index for faster queries on reset codes
CREATE INDEX idx_user_reset_code ON user(reset_code);

-- Optional: Add index for combined reset code and expiration queries
CREATE INDEX idx_user_reset_code_expiration ON user(reset_code, reset_expiration);

-- Explanation:
-- VARCHAR(6): 6-digit reset code format
-- DATETIME: Stores expiration timestamp (10 minutes from generation)
-- NULL: Allows NULL values when no reset is in progress
-- AFTER clauses: Place columns logically after verification_code for organization
DROP DATABASE IF EXISTS railway;
CREATE DATABASE railway;
