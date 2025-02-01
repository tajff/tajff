# Copyright (c) 2025, Maged BAjandooh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import date_diff,getdate, today


class Licenses(Document):
	def on_update(self):
		update_status('Licenses', filters={'name':self.name})
		self.reload()

	def befor_save(self):
		update_status('Licenses', filters={'name':self.name})
		self.reload()

def	scheduled_status_update(doctype, filters=None):
	update_status('Licenses')

def	update_status(doctype, filters=None):
	today_date = getdate(today())
	docs = frappe.get_all(doctype, filters=filters, fields=['name','expiry_date','status'])
	for doc in docs:
		if not doc.get("expiry_date"):
			continue

		expiry_date = getdate(doc["expiry_date"])
		days_difference = date_diff(expiry_date, today_date)
		if days_difference < 0:
			new_status = 'Expired'
		elif days_difference <= 30:
			new_status = 'Renew'
		elif days_difference > 30:
			new_status = 'Active'

		frappe.db.set_value(doctype, doc["name"], "status", new_status)
		
		frappe.db.commit()