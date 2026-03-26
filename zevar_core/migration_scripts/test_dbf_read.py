import os
from dbfread import DBF
import pandas as pd

def test_dbf_reading():
    """Test reading DBF files and show data structure"""

    # Define the source directory for legacy DBF files
    legacy_dir = "/workspace/development/Zevar_URMS/Zevar_HIPmall_MD_1/"

    # List of DBF files to test
    test_files = [
        'customer.DBF',
        'inventor.DBF',
        'EMPLOYEE.DBF',
        'invoice.dbf',
        'SUPPLIER.DBF',
        'REPAIR.dbf',
        'GOLD$.dbf'
    ]

    print("Testing DBF file reading...")
    print(f"Source directory: {legacy_dir}")
    print("=" * 60)

    for dbf_file in test_files:
        dbf_path = os.path.join(legacy_dir, dbf_file)

        if not os.path.exists(dbf_path):
            print(f"❌ File not found: {dbf_file}")
            continue

        try:
            print(f"\n📄 Testing: {dbf_file}")
            print("-" * 40)

            # Read the DBF file
            table = DBF(dbf_path, load=True)
            df = pd.DataFrame(iter(table))

            print(f"✅ Successfully read {len(df)} records")
            print(f"📊 Columns: {list(df.columns)}")

            # Show sample data
            if len(df) > 0:
                print("\n📋 Sample data (first 3 rows):")
                print(df.head(3).to_string())

            print("-" * 40)

        except Exception as e:
            print(f"❌ Error reading {dbf_file}: {str(e)}")
            continue

    print("\n" + "=" * 60)
    print("DBF reading test completed!")

if __name__ == "__main__":
    test_dbf_reading()