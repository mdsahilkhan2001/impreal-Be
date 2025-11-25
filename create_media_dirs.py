# Create media directories
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Create media directories if they don't exist
media_dirs = [
    'media/avatars',
    'media/documents/pi',
    'media/documents/invoices',
    'media/documents/packing',
    'media/documents/awb',
    'media/uploads',
    'media/qc_reports',
    'media/shipment/invoices',
    'media/shipment/packing',
    'media/shipment/awb',
    'media/po_payments',
]

for media_dir in media_dirs:
    os.makedirs(BASE_DIR / media_dir, exist_ok=True)

print("Media directories created successfully!")
