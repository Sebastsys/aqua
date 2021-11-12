# -*- coding: utf-8 -*-
# Copyright (c) 2020, Ing. Orlando Cholota and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Tareas(Document):
	def copiarUsuariosAClientes(self):
		sql ="""   select name from `tabUsuarios de Agua` u where u.name not in (select name from tabClientes tc) """
		retorno = frappe.db.sql( sql,  as_dict=0)
		for f in retorno:
			usu = frappe.get_doc('Usuarios de Agua',f[0])
			clie = frappe.new_doc("Clientes")
			clie.tipo_identificacion = usu.tipo_identificacion
			clie.ruc = usu.ruc
			clie.nombres = usu.nombres
			if usu.correo: 
				clie.correo = usu.correo
			else:
				clie.correo = 'sin@correo.com'	
			if  usu.telefono :
				clie.telefono = usu.telefono
			else:
				clie.telefono = '000000000'

			if  usu.direccion :
    				clie.direccion = usu.direccion
			else:
				clie.direccion = 'S/N'
    				
			
			clie.save()
		return "Datos Actualizados"

