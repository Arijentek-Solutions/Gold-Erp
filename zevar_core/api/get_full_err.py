import frappe
from frappe import _


def run():
    log = frappe.get_all('Error Log', order_by='creation desc', limit=1, fields=['error'])[0]
    print(log.error)

if __name__ == "__main__":
    run()
