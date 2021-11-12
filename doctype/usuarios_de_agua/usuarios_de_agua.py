# -*- coding: utf-8 -*-
# Copyright (c) 2020, Ing. Orlando Cholota and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class UsuariosdeAgua(Document):
	def after_insert(self):
			clie = frappe.new_doc("Clientes")
			clie.tipo_identificacion = self.tipo_identificacion
			clie.ruc = self.ruc
			clie.nombres = self.nombres
			clie.correo = self.correo
			clie.telefono = self.telefono
			clie.direccion = self.direccion
			clie.save()

	def on_update(self):
		
		if not frappe.db.exists("Clientes", self.name):
    			clie = frappe.new_doc("Clientes")
		else:
				clie = frappe.get_doc('Clientes',self.name)
				
		clie.tipo_identificacion = self.tipo_identificacion
		clie.ruc = self.ruc
		clie.nombres = self.nombres
		clie.correo = self.correo
		clie.telefono = self.telefono
		clie.direccion = self.direccion
		clie.save()
    		
