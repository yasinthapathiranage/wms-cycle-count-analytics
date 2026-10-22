import os
import glob
import random
from datetime import datetime
import pandas as pd

# Ensure the output directory exists
output_dir = "WMS_Audit_Drops"
os.makedirs(output_dir, exist_ok=True)

# 10 Products to ensure exactly 10 counted lines per audit
products = [
    {"sku": "EXC-TRACK-102", "ProductName": "Excavator Track Assembly", "UnitCost": 2500.00},
    {"sku": "HYD-VALVE-100", "ProductName": "Hydraulic Valve 2500psi", "UnitCost": 1350.00},
    {"sku": "HYD-VALVE-099", "ProductName": "Hydraulic Valve 2000psi", "UnitCost": 1350.00},
    {"sku": "FILT-AIR-205", "ProductName": "Industrial Air Filter Kit", "UnitCost": 600.00},
    {"sku": "PNEU-CYL-404", "ProductName": "Pneumatic Cylinder Heavy", "UnitCost": 1700.00},
    {"sku": "SENS-TMP-088", "ProductName": "Thermal Sensor Unit", "UnitCost": 1200.00},
    {"sku": "GEAR-BOX-773", "ProductName": "Heavy Duty Gearbox", "UnitCost": 3200.00},
    {"sku": "BEAR-RLL-012", "ProductName": "Roller Bearing Set", "UnitCost": 150.00},
    {"sku": "SEAL-K-990", "ProductName": "Master Seal Kit", "UnitCost": 85.00},
    {"sku": "PUMP-WTR-332", "ProductName": "Industrial Water Pump", "UnitCost": 950.00}
]

# Determine the next Audit Number by checking existing files
existing_files = glob.glob(os.path.join(output_dir, "*.csv"))
next_audit_id = 1

if existing_files:
    try:
        # Read all existing files to find the highest AuditNumber used so far
        df_existing = pd.concat([pd.read_csv(f) for f in existing_files])
        if 'AuditNumber' in df_existing.columns and not df_existing.empty:
            next_audit_id = int(df_existing['AuditNumber'].max()) + 1
    except Exception as e:
        print(f"Error reading existing files to find next Audit ID: {e}")

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
audit_data = []

# Generate exactly 1 audit with 10 counted lines
for product in products:
    expected_qty = random.randint(50, 200)
    
    # 85% probability of an exact match per line. 
    # This creates natural variance per file (e.g., 7/10, 9/10, 10/10) 
    # but averages ~85% over multiple generated files.
    if random.random() < 0.85:
        variance = 0
    else:
        variance = random.choice([-2, -1, 1, 2])
        
    actual_qty = max(0, expected_qty + variance)

    audit_data.append({
        "AuditNumber": next_audit_id,
        "sku": product["sku"],
        "ProductName": product["ProductName"],
        "UnitCost": product["UnitCost"],
        "ExpectedQty": expected_qty,
        "ActualQty": actual_qty
    })

# Export the single audit to its own CSV file
df = pd.DataFrame(audit_data)
file_path = os.path.join(output_dir, f"audit_{next_audit_id}_{timestamp}.csv")
df.to_csv(file_path, index=False)

# Calculate and display the specific accuracy for this run
matches = sum(1 for row in audit_data if row["ExpectedQty"] == row["ActualQty"])
current_accuracy = (matches / len(products)) * 100

print(f"Successfully generated Audit {next_audit_id} in {file_path}")
print(f"Audit {next_audit_id} Accuracy: {current_accuracy:.0f}% ({matches}/10 matches)")
