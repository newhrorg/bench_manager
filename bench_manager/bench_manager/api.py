import frappe
from datetime import datetime, timedelta
@frappe.whitelist()
def call_backub_methode():
    bench_settings_doc  = frappe.get_doc('Bench Settings')
    if bench_settings_doc.auto_backup and bench_settings_doc.cron_job:
        key = datetime.now()
        site_list = frappe.get_list("Site")
        if site_list:
            for i in site_list:
                site_doc = frappe.get_doc("Site",i.name)
                key += timedelta(seconds=1)
                frappe.enqueue(
                    "bench_manager.bench_manager.utils.run_command",
                    commands=["bench --site {site_name} backup --with-files".format(site_name=i.name)],
                    doctype=site_doc.doctype,
                    key=str(key),
                    docname=site_doc.name,
                )
            return "executed"
