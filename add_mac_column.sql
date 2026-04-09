-- SQL Command to add mac_address column to existing user_log table
-- Run this command in your MySQL database to update the table structure

ALTER TABLE user_log 
ADD COLUMN mac_address VARCHAR(17) NULL 
AFTER ip_address;

-- Explanation:
-- VARCHAR(17): MAC address format is XX:XX:XX:XX:XX:XX (17 characters including colons)
-- NULL: Allows NULL values for cases where MAC address cannot be determined
-- AFTER ip_address: Places the column logically after ip_address for better organization

-- Optional: Add index for faster queries on MAC addresses
CREATE INDEX idx_user_log_mac_address ON user_log(mac_address);

-- Optional: Add index for combined IP and MAC queries
CREATE INDEX idx_user_log_ip_mac ON user_log(ip_address, mac_address);
