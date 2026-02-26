import subprocess
import sys


def main():
	try:
		print("Running ruff check --fix...")
		result_check = subprocess.run(
			[
				sys.executable,
				"-m",
				"ruff",
				"check",
				"zevar_core/",
				"--fix",
				"--output-format=concise",
				"--no-cache",
			],
			cwd="/workspace/development/frappe-bench/apps/zevar_core",
			capture_output=True,
			text=True,
			timeout=30,
		)
		print("Ruff Check Output:")
		print(result_check.stdout)
		if result_check.stderr:
			print("Ruff Check Errors:")
			print(result_check.stderr)

		print("\nRunning ruff format...")
		result_fmt = subprocess.run(
			[sys.executable, "-m", "ruff", "format", "zevar_core/"],
			cwd="/workspace/development/frappe-bench/apps/zevar_core",
			capture_output=True,
			text=True,
			timeout=30,
		)
		print("Ruff Format Output:")
		print(result_fmt.stdout)
		if result_fmt.stderr:
			print("Ruff Format Errors:")
			print(result_fmt.stderr)

	except Exception as e:
		print(f"Error: {e}")


if __name__ == "__main__":
	main()
