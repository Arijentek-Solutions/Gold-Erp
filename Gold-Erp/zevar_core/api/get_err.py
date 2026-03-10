import frappe

def run():
	errors = frappe.db.get_list("Error Log", fields=["method", "error"], order_by="creation desc", limit=5)
	for e in errors:
		print("====== ERROR TRACEBACK ======")
		print("Method:", e.method)
		print(e.error)
		print("=============================")
