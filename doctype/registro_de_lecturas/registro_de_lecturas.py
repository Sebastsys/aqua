# -*- coding: utf-8 -*-
# Copyright (c) 2020, Ing. Orlando Cholota and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import datetime
import calendar
class RegistrodeLecturas(Document):
	def after_insert(self):
		 
		mesnombre = self.mes
		mes=0

		if mesnombre == 'Enero':
    			mes=2
		if mesnombre == 'Febrero':
    			mes=3
		if mesnombre == 'Marzo':
    			mes=4
		if mesnombre == 'Abril':
    			mes=5
		if mesnombre == 'Mayo':
    			mes=6
		if mesnombre == 'Junio':
    			mes=7
		if mesnombre == 'Julio':
    			mes=8
		if mesnombre == 'Agosto':
    			mes=9
		if mesnombre == 'Septiembre':
    			mes=10
		if mesnombre == 'Octubre':
    			mes=11
		if mesnombre == 'Noviembre':
    			mes=12
		if mesnombre == 'Diciembre':
    			mes=1
	 
		fecha = datetime.date(int(self.anio), mes, 1) - datetime.timedelta(days=1)

		self.fecha = fecha
		medidores = frappe.db.sql(""" select name,zona from `tabAsignar Medidor de Agua`  """  )
		for m  in medidores:
			self.append("lectura_usuarios", {"medidor":m[0] ,"lectura":0,"fecha": fecha})
		self.save()
		
		if mes > 1:
			fechaant = datetime.date(int(self.anio), mes-1, 1) - datetime.timedelta(days=1)
		else:
			fechaant = datetime.date(int(self.anio), mes, 1) - datetime.timedelta(days=1)
		
		sqlUpdate1 =""" update tablectura_usuarios a set lectura_a  =  (  select b.lectura from tablectura_usuarios b where  b.fecha ='{0}' and a.medidor = b.medidor) where   a.fecha ='{1}' """.format(fechaant,fecha)
		frappe.db.sql( sqlUpdate1,  as_dict=0)

		sqlUpdate2 ="""update tablectura_usuarios a set lectura   =   lectura_a where   a.fecha ='{0}'  """.format(fecha)
		frappe.db.sql( sqlUpdate2,  as_dict=0)
		
		 
		
	def on_update(self):
    		if self.docstatus==1:
    				comprobarLecturas(self)  

	def getMedidores(self, inusuario):
			obj  = frappe.db.sql(""" SELECT  medidor from tabUsuarioMedidor where parent =%s """,inusuario)
			return obj

def comprobarLecturas(doc):	
	sql="""select count(*)   as count  from  tablectura_usuarios where    parent = '{0}' and lectura = 0""".format(  doc.name)
	contar = frappe.db.sql( sql,  as_dict=0)[0][0]
	if contar > 1 :
    		frappe.throw("No ha Registrado la lectura(s) de : "+ str(contar) + " Usuario(s)")
	else:
    		generarFatura(doc)

def generarFatura(doc):
		parms = frappe.get_doc('Parametros Agua')
		if not parms.listaprecio:
			frappe.throw("Debe definir una lista de precios para la facturación, revisé los parámetros")
		if not parms.producto:
			frappe.throw("Debe definir una producto por defecto , revisé los parámetros")
		if not parms.almacen:
			frappe.throw("Debe definir el establecimiento (SRI) , revisé los parámetros")
		
		sql="""select precio, iva  from tablistaprecios_productos where parent='{0}' and  productos ='{1}'""".format( parms.listaprecio,parms.producto)
		retorno = frappe.db.sql( sql,  as_dict=0) 
		precio = retorno[0][0]
		iva = retorno[0][1]
		
		sql2="""select precio, iva  from tablistaprecios_productos where parent='{0}' and  productos ='{1}'""".format( parms.listaprecio,parms.producto2)
		retorno2 = frappe.db.sql( sql2,  as_dict=0) 
		precio2 = retorno2[0][0]
		iva2 = retorno2[0][1]
		
		pro = frappe.get_doc('Productos',parms.producto)
		pro2 = frappe.get_doc('Productos',parms.producto2)

		perido = doc.anio + '  ' + doc.mes

		for lect in doc.lectura_usuarios:
			cliente = frappe.get_doc("Clientes",lect.usuario);
			factura = frappe.new_doc("Factura en Ventas")
			factura.estab = parms.almacen
			factura.ptoemi = parms.puntoemision
			factura.formapago = '01-SIN UTILIZACION DEL SISTEMA FINANCIERO'
			factura.cliente = lect.usuario
			factura.listaprecios = parms.listaprecio
			factura.bajarstock = 0
			subtotal= lect.lectura * precio
			ivavalor =( subtotal * iva) /100
			total =  subtotal + ivavalor

		 
			factura.append('detalles_facventas', {
                    "producto":  parms.producto,
                    "codigoprincipal":pro.codigo ,
                    "codigoauxiliar":pro.codigo ,
                    "descripcion": pro.descripcion,
                    "cantidad":lect.lectura ,
                    "preciounitario":precio,
                    "descuento":0 ,
                    "preciototalsinimpuesto": subtotal,
                    "tarifa_iva": iva,
                    "iva_valor": ivavalor,
                    "totallinea":subtotal + ivavalor
                })
			factura.append('detalles_facventas', {
                    "producto":  parms.producto2,
                    "codigoprincipal":pro2.codigo ,
                    "codigoauxiliar":pro2.codigo ,
                    "descripcion": pro2.descripcion,\
                    "cantidad":1,
                    "preciounitario":pro2.precio,
                    "descuento":0 ,
                    "preciototalsinimpuesto": subtotal,
                    "tarifa_iva": iva,
                    "iva_valor": ivavalor,
                    "totallinea":pro2.precio
                })

			
			factura.append('infoadicional',{
				"nombre":"Periodo",
				"valor":perido,
			})
			factura.append('infoadicional',{
				"nombre":"Consumo",
				"valor":lect.lectura,
			})

			factura.append('infoadicional',{
				"nombre":"Número de Medidor",
				"valor":lect.medidor,
			})
			factura.append('infoadicional',{
				"nombre":"Correo",
				"valor":cliente.correo,
			})
			

			factura.observacion = perido + ' M:' + lect.medidor 
			factura.importetotal = total				 
			factura.totalsinimpuestos = subtotal
			factura.docstatus = 1
			factura.insert();

@frappe.whitelist()  
def registarCobro(num_fac):
		fac = frappe.get_doc('Factura en Ventas',num_fac)
		rc = frappe.new_doc("Registro de Cobros")
		rc.fecha = datetime.datetime.now()
		rc.descripcion ="Pago en EFECTIVO de la factura: " + fac.num_fac
		rc.clientes =  fac.cliente
		rc.docstatus = 1
		rc.append("detalle_pagos", {"tipo":"EFECTIVO" ,"cantidad": fac.importetotal  })
		rc.append("detallepago_fac_ventas", {"factura": num_fac ,
            "totalfactura": fac.importetotal ,
            "cantidad": fac.importetotal })

        
		rc.insert()
		 
		sql="""UPDATE `tabFactura en Ventas` SET saldo =0.0,pagoefectivo=1,registrocobro='{0}'  where name='{1}' """.format( rc.name ,num_fac)
		retorno = frappe.db.sql( sql,  as_dict=0) 
		#fac.registrocobro = rc.name		
		#fac.saldo = 0;
		#fac.pagoefectivo = 1
		#fac.save()
		return "ok"

