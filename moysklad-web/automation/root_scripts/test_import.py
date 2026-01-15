
import sys
import os

sys.path.append(os.path.join(os.getcwd(), 'moysklad-automation'))

try:
    from moysklad_automation import parse_wb_top
    print("Import successful (package style)")
except ImportError as e:
    print(f"Package import failed: {e}")

try:
    import parse_wb_top
    print("Import successful (direct)")
except Exception as e:
    print(f"Direct import failed: {e}")
    import traceback
    traceback.print_exc()
