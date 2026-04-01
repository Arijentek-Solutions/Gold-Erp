import os
import unittest

try:
	import pandas as pd
	from dbfread import DBF
except ImportError:
	pd = None
	DBF = None

pandas_missing = unittest.skipIf(pd is None or DBF is None, "pandas or dbfread not installed")


@pandas_missing
def test_dbf_reading():
	"""Test reading DBF files and show data structure"""

	# Define the source directory for legacy DBF files
	legacy_dir = "/workspace/development/Zevar_URMS/Zevar_HIPmall_MD_1/"

	# List of DBF files to test
	test_files = [
		"customer.DBF",
		"inventor.DBF",
		"EMPLOYEE.DBF",
		"invoice.dbf",
		"SUPPLIER.DBF",
		"REPAIR.dbf",
		"GOLD$.dbf",
	]

	for dbf_file in test_files:
		dbf_path = os.path.join(legacy_dir, dbf_file)

		if not os.path.exists(dbf_path):
			continue

		try:
			# Read the DBF file
			table = DBF(dbf_path, load=True)
			df = pd.DataFrame(iter(table))

			# Show sample data
			if len(df) > 0:
				print(f"Sample data from {dbf_file}:")
				print(df.head())

		except Exception:
			continue


if __name__ == "__main__":
	test_dbf_reading()
