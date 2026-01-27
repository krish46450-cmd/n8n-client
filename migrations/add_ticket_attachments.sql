-- Migration: Add attachments column to tickets table
-- Date: 2026-01-20
-- Description: Adds support for image/screenshot attachments in support tickets

-- Add attachments column to tickets table
ALTER TABLE tickets ADD COLUMN attachments TEXT NULL;

-- Update existing records to have NULL attachments
UPDATE tickets SET attachments = NULL WHERE attachments IS NULL;

-- Note: attachments will store JSON array of file paths
-- Example: ["tickets/abc123_screenshot1.png", "tickets/def456_error2.jpg"]
