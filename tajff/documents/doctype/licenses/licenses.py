# Copyright (c) 2025, Maged BAjandooh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, date_diff,getdate


class Licenses(Document):
	def before_save(self):
		update_status(self)


def schedule_status():
	docs = frappe.get_all('Licenses',fields=['name','expiry_date','status'])
	update_status([doc.name for doc in docs])

def	update_status(docs):
	if not isinstance(docs, list):
		docs = [docs]

	for doc in docs:
		if isinstance(doc, str):
			doc = frappe.get_doc('Licenses', doc)
			
		today_date = nowdate()
		between_dates = date_diff(getdate(doc.expiry_date), today_date)
		if between_dates <= 0:
			doc.status = 'Expired'
		elif between_dates <= 30:
			doc.status = 'Renew'
		elif between_dates > 30:
			doc.status = 'Active'
		doc.save()