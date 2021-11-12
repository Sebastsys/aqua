// Copyright (c) 2020, Ing. Orlando Cholota and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tareas', {
	// refresh: function(frm) {

	// }
	ausuario: function(frm){
		frappe.call({
			doc: frm.doc,
			method: "copiarUsuariosAClientes",		 
			callback: r => {       
			 console.log(r)
			  alert(r.message)
			}
		  });

	}
});
