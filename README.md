# Enterprise Continuous Cycle Count & Shrinkage Dashboard

## Overview
This repository contains a full-stack data analytics solution designed to track warehouse cycle counts, quantify financial shrinkage, and expose systemic inventory errors. It features a Python-based synthetic data generator that simulates realistic logistics environments and a robust Power BI dashboard built on a Star Schema data model.

The goal of this project is to move beyond standard "net-variance" reporting—which often hides cross-picking errors—by utilizing advanced DAX measures to calculate Absolute Variance and track "Ghost Inventory" over time.

## Architecture & Data Flow
1. **Data Engineering (Python):**
   - A Python script (`generate_audit_data.py`) engineers synthetic warehouse audit drops.
   - It utilizes a binomial distribution model to simulate a realistic ~85% exact match rate across multiple industrial SKUs, injecting organic variances (surpluses and shortages).
2. **Data Modeling (Power BI):**
   - Structured using a classic Star Schema with `Fact_CycleCounts` for transactional audit logs and `Dim_Product` for SKU-level financial metrics.
3. **Data Visualization (Power BI):**
   - An industrial-themed dashboard UI designed for executive reporting.

## Key Features & DAX Implementation
* **Absolute Variance Tracking:** Standard net-variance cancels out surpluses and shortages (+5 and -5 equals 0). This model calculates the absolute variance using `ABS()` to expose the true volume of mis-picks and stock movement errors.
* **Directional Financial Shrinkage:** Distinct measures for *Recovered Asset Value* and *Shortage Value* accurately quantify the financial impact of discrepancies based on exact unit costs.
* **Longitudinal Variance Matrix:** A custom visualization that tracks individual SKUs across multiple audit numbers to identify chronic bottlenecks, delayed receiving, and recovered assets.
* **Dynamic Top N Filtering:** Automatically isolates and ranks the top 5 SKUs contributing to operational shrinkage.

## Tech Stack
* **Languages:** Python (pandas, numpy), DAX
* **Tools:** Power BI, Power Query

## How to Use
1. Run `generate_audit_data.py` to generate a fresh batch of simulated cycle count CSV files in the `WMS_Audit_Drops` directory.
2. Open the Power BI `.pbix` file.
3. Refresh the data model to automatically ingest the new audit drops and update the dashboard visuals.
