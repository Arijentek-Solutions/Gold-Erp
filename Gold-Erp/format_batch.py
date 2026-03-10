import os
import subprocess
import sys


def format_batch(directory):
	print(f"Formatting {directory}...")
	try:
		# Run ruff check --fix
		subprocess.run(
			[
				sys.executable,
				"-m",
				"ruff",
				"check",
				directory,
				"--fix",
				"--output-format=concise",
				"--no-cache",
			],
			check=False,
		)
		# Run ruff format
		subprocess.run([sys.executable, "-m", "ruff", "format", directory, "--no-cache"], check=False)
		print(f"Successfully processed {directory}")
	except Exception as e:
		print(f"Error processing {directory}: {e}")


if __name__ == "__main__":
	if len(sys.argv) > 1:
		format_batch(sys.argv[1])
	else:
		print("Please provide a directory")
