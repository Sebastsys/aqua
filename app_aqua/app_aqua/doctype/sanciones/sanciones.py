# Copyright (c) 2021, Francisco Adame and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Sanciones(Document):
	def before_save(self):
		listaprecio = frappe.db.get_single_value("Parametros Agua","listaprecio")
		#precio = frappe.get_doc("Item Price",{'item_name':self.multa,'parent':listaprecio})
		precio = frappe.get_doc("Item Price",{'item_code':self.multa})
		self.valor =  precio.price_list_rate
		medidor = frappe.get_doc("Asignar Medidor de Agua",{'usuario':self.usuario})
		self.medidor =  medidor.medidor
