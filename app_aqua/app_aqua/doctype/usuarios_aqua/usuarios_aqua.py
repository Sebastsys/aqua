# Copyright (c) 2021, Francisco Adame and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class UsuariosAqua(Document):
	def after_insert(self):
		clie = frappe.new_doc("Customer")
		clie.tipo_de_identificacion = self.tipo_identificación
		clie.ruc = self.ruc
		clie.customer_name = self.nombres
		clie.correo = self.correo
		clie.telefono = self.telefono
		clie.direccion = self.direccion
		clie.customer_type = "Individual"
		clie.customer_group = "Individual"
		clie.territory = "Ecuador"

	def on_update(self):
		if not frappe.db.exists("Customer", self.name):
			clie = frappe.new_doc("Customer")
		else:
			clie = frappe.get_doc('Customer',self.name)
				
		clie.tipo_de_identificacion = self.tipo_identificación
		clie.ruc = self.ruc
		clie.customer_name = self.nombres
		clie.correo = self.correo
		clie.telefono = self.telefono
		clie.direccion = self.direccion
		clie.customer_type = "Individual"
		clie.customer_group = "Individual"
		clie.territory = "Ecuador"
		clie.save()
