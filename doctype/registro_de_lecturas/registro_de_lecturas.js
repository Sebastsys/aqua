// Copyright (c) 2020, Ing. Orlando Cholota and contributors
// For license information, please see license.txt

frappe.ui.form.on('Registro de Lecturas', {
	refresh: function (frm) {

	}
 

});

frappe.ui.form.on("lectura_usuarios", {
 
	usuario: function(frm, cdt, cdn) {
	  const doc = frappe.get_doc(cdt, cdn);
	  if (doc !== undefined && doc !== null) {
		 
	  }
	}
  });


  function getMedidores(frm, doc, cdt, cdn) { 
	if (doc.usuario !== undefined && doc.usuario !== null) {

		console.log(  doc.usuario);
   frappe.call({
		doc: frm.doc,
		method: "getMedidores",
		args: { inusuario: doc.usuario },
		callback: r => {     
			console.log(doc);    
			console.log(r.message); 
 
	   frappe.model.set_value(cdt, cdn, "nmedidor", r.message );
	 	frm.refresh_fields( );
		}
	  });  

	} 
  }