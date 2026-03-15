-- =============================================================
-- Neon Database Setup for MCP Lab
-- =============================================================
-- This script creates and populates the VARIANCE_BASELINE_V table
-- used by the Model Context Protocol (MCP) lab exercise.
--
-- Instructions:
-- 1. Go to your Neon project's SQL Editor
-- 2. Copy and paste this entire script
-- 3. Click "Run"
-- =============================================================

-- Drop the table if it already exists (safe to re-run)
DROP TABLE IF EXISTS "VARIANCE_BASELINE_V";

-- Create the table
CREATE TABLE "VARIANCE_BASELINE_V" (
    id                  SERIAL PRIMARY KEY,
    actual_amount_usd   INTEGER NOT NULL,
    baseline_amount_usd INTEGER NOT NULL,
    variance            INTEGER NOT NULL,
    variance_pct        DOUBLE PRECISION NOT NULL,
    cost_center         VARCHAR(50) NOT NULL,
    fiscal_year         INTEGER NOT NULL,
    forecast_source     VARCHAR(100) NOT NULL,
    gl_account          INTEGER NOT NULL,
    last_updated        TIMESTAMP NOT NULL,
    period              VARCHAR(20) NOT NULL
);

-- Insert seed data (24 rows)
INSERT INTO "VARIANCE_BASELINE_V" (actual_amount_usd, baseline_amount_usd, variance, variance_pct, cost_center, fiscal_year, forecast_source, gl_account, last_updated, period) VALUES
(190200, 190000, -200, -0.11, 'BIZD-IT-01', 2025, 'ML Model V3', 610000, '2025-12-26 00:00:00', '2025-FY'),
(220033, 220000, -33, -0.02, 'BIZD-JP-01', 2025, 'ML Model V3', 610100, '2025-12-26 00:00:00', '2025-FY'),
(350400, 350000, -400, -0.11, 'CC_FIN_002', 2025, 'Manual', 620500, '2025-12-26 00:00:00', '2025-FY'),
(400001, 400000, -1, 0, 'CC_IT_001', 2025, 'ML Model V2', 620510, '2025-12-26 00:00:00', '2025-FY'),
(150550, 150000, -550, -0.37, 'CC_IT_002', 2025, 'Budget FY25', 630000, '2025-12-26 00:00:00', '2025-FY'),
(151300, 160000, 8700, 5.44, 'CLIN-BR-A', 2025, 'Budget FY25', 631200, '2025-12-26 00:00:00', '2025-FY'),
(500100, 500000, -100, -0.02, 'CLIN-BR-M', 2025, 'ML Model V3', 640200, '2025-12-26 00:00:00', '2025-FY'),
(554167, 550000, -4167, -0.76, 'CLIN-DE-01', 2025, 'ML Model V3', 640300, '2025-12-26 00:00:00', '2025-FY'),
(441900, 450000, 8100, 1.8, 'EHS-DE-SA', 2025, 'Budget FY25', 640400, '2025-12-26 00:00:00', '2025-FY'),
(272900, 275000, 2100, 0.76, 'HR-AU-TR', 2025, 'Manual', 650200, '2025-12-26 00:00:00', '2025-FY'),
(874800, 800000, -74800, -9.35, 'HR-IN-RC', 2025, 'ML Model V4', 660500, '2025-12-26 00:00:00', '2025-FY'),
(958400, 900000, -58400, -6.49, 'LEGAL-NL-C', 2025, 'ML Model V4', 660510, '2025-12-26 00:00:00', '2025-FY'),
(611467, 550000, -61467, -11.18, 'MKTG-FR-PR', 2025, 'ML Model V3', 670100, '2025-12-26 00:00:00', '2025-FY'),
(435233, 400000, -35233, -8.81, 'MKTG-US-DM', 2025, 'ML Model V3', 670200, '2025-12-26 00:00:00', '2025-FY'),
(313900, 320000, 6100, 1.91, 'PROD-DE-1', 2025, 'Budget FY25', 670300, '2025-12-26 00:00:00', '2025-FY'),
(105000, 120000, 15000, 12.5, 'PROD-DE-2', 2025, 'Budget FY25', 680000, '2025-12-26 00:00:00', '2025-FY'),
(763000, 700000, -63000, -9, 'PROD-ES-01', 2025, 'ML Model V2', 690100, '2025-12-26 00:00:00', '2025-FY'),
(827000, 760000, -67000, -8.82, 'PROD-IT-01', 2025, 'ML Model V2', 690200, '2025-12-26 00:00:00', '2025-FY'),
(724000, 720000, -4000, -0.56, 'PVG-EU-01', 2025, 'ML Model V3', 700100, '2025-12-26 00:00:00', '2025-FY'),
(648000, 648000, 0, 0, 'QC-CH-01', 2025, 'Budget FY25', 710100, '2025-12-26 00:00:00', '2025-FY'),
(901200, 900000, -1200, -0.13, 'SCM-UK-PL', 2025, 'Budget FY25', 750100, '2025-12-26 00:00:00', '2025-FY'),
(970000, 960000, -10000, -1.04, 'SCM-UK-WH', 2025, 'Budget FY25', 750200, '2025-12-26 00:00:00', '2025-FY'),
(1100000, 1100000, 0, 0, 'REG-US-01', 2025, 'ML Model V3', 730300, '2025-12-26 00:00:00', '2025-FY'),
(1491000, 1450000, -41000, -2.83, 'SALES-US-IN', 2025, 'ML Model V2', 740200, '2025-12-26 00:00:00', '2025-FY');

-- Verify the data
SELECT count(*) AS total_rows FROM "VARIANCE_BASELINE_V";
SELECT * FROM "VARIANCE_BASELINE_V" WHERE cost_center = 'CC_IT_001' LIMIT 1;
