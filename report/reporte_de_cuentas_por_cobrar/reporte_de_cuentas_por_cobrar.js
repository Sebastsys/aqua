frappe.query_reports["Reporte de cuentas por cobrar"] = {
	"filters": [
		{
			"fieldname":"cliente",
			"label": __("Usuario"),
			"fieldtype": "Link",
            options: "Clientes",
            reqd:1
		}
	]
} 
function consoleerp_hi(data) { 
    frappe.confirm(
        __('Desea Registrar el pago del la factura?'),
        function() {
            frappe.call({
                method:
                  "next.jaap.doctype.registro_de_lecturas.registro_de_lecturas.registarCobro",
                args: {
                    num_fac: data
                },
                callback: r => {
                  
                    frappe.show_alert({
                        indicator: 'green',
                        message:r.message
                      });       
                       var w = window.open(
                        frappe.urllib.get_full_url("api/method/frappe.utils.print_format.download_pdf?"
                        +"doctype="+encodeURIComponent('Factura en Ventas')
                        +"&name="+encodeURIComponent(data)
                        +"&format="+encodeURIComponent('Recibo de Pago de Agua')
                        +"&no_letterhead=0"));
                    if(!w) {
                        frappe.msgprint(__("Please enable pop-ups")); return;
                    }

                      frappe.query_report.refresh();
                }
              });
        }
    ); 
}