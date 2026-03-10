#!/usr/bin/env python3
"""
Image Download Script for Zevar Item Master
=============================================
Downloads Unsplash images to local storage and updates item records.

Usage:
    bench --site zevar.localhost execute zevar_core.scripts.download_images.download_all_images

Benefits:
    - Faster loading (local vs remote)
    - Works offline
    - No external dependency
    - More secure (no tracking pixels)
"""

import hashlib
import os
from pathlib import Path

import requests


def download_all_images(dry_run=False, limit=None):
	"""
	Download all remote images to local storage.

	Args:
	    dry_run: If True, don't actually download/save
	    limit: Max number of items to process (None for all)
	"""
	import frappe

	print("=" * 60)
	print("DOWNLOADING IMAGES TO LOCAL STORAGE")
	print("=" * 60)
	print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
	print(f"Limit: {limit or 'No limit'}")
	print()

	# Get items with remote images (Unsplash URLs)
	items = frappe.get_all(
		"Item",
		filters=[["image", "like", "https://%"]],
		fields=["name", "image", "item_name"],
	)

	if limit:
		items = items[:limit]

	print(f"Found {len(items)} items with remote images")
	print()

	# Create storage directory
	site_path = frappe.get_site_path()
	files_dir = Path(site_path) / "public" / "files" / "items"

	if not dry_run:
		files_dir.mkdir(parents=True, exist_ok=True)

	downloaded = 0
	skipped = 0
	errors = 0

	for item in items:
		image_url = item.get("image", "")
		item_code = item.get("name")

		if not image_url or not image_url.startswith("http"):
			skipped += 1
			continue

		# Generate filename from item code
		ext = "jpg"  # Unsplash images are typically JPG
		if ".png" in image_url.lower():
			ext = "png"
		elif ".webp" in image_url.lower():
			ext = "webp"

		filename = f"{item_code}.{ext}"
		local_path = files_dir / filename

		# Skip if already downloaded
		if local_path.exists() and not dry_run:
			# Update item record if needed
			new_image_path = f"/files/items/{filename}"
			if item.get("image") != new_image_path:
				frappe.db.set_value("Item", item_code, "image", new_image_path)
			skipped += 1
			continue

		if dry_run:
			print(f"  [DRY RUN] Would download: {item_code}")
			downloaded += 1
			continue

		try:
			# Download image
			response = requests.get(
				image_url, timeout=30, headers={"User-Agent": "Mozilla/5.0 (Zevar Image Downloader)"}
			)

			if response.status_code == 200:
				# Save file
				with open(local_path, "wb") as f:  # nosemgrep: frappe-security-file-traversal
					f.write(response.content)

				# Update item record with local path
				new_image_path = f"/files/items/{filename}"
				frappe.db.set_value("Item", item_code, "image", new_image_path)

				downloaded += 1

				if downloaded % 20 == 0:
					print(f"  Downloaded {downloaded} images...")
					frappe.db.commit()  # nosemgrep: frappe-semgrep-rules.rules.frappe-manual-commit
			else:
				errors += 1
				if errors <= 5:
					print(f"  Error downloading {item_code}: HTTP {response.status_code}")

		except Exception as e:
			errors += 1
			if errors <= 5:
				print(f"  Error with {item_code}: {str(e)[:50]}")

	if not dry_run:
		frappe.db.commit()  # nosemgrep: frappe-semgrep-rules.rules.frappe-manual-commit

	print()
	print("=" * 60)
	print("IMAGE DOWNLOAD COMPLETE")
	print(f"  Downloaded: {downloaded}")
	print(f"  Skipped: {skipped}")
	print(f"  Errors: {errors}")
	print("=" * 60)

	return {"downloaded": downloaded, "skipped": skipped, "errors": errors}


def cleanup_remote_images():
	"""
	Utility to find items still using remote images.
	"""
	import frappe

	remote_items = frappe.get_all("Item", filters=[["image", "like", "https://%"]], pluck="name")

	print(f"Items still using remote images: {len(remote_items)}")
	return remote_items


if __name__ == "__main__":
	print("Run via bench:")
	print("  bench --site zevar.localhost execute zevar_core.scripts.download_images.download_all_images")
