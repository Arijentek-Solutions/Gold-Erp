// Copyright (c) 2026, Zevar and contributors
// For license information, please see license.txt

frappe.ui.form.on("Layaway Contract", {
    contract_date(frm) {
        set_target_completion(frm);
    },
    maximum_duration_months(frm) {
        set_target_completion(frm);
    },
});

function set_target_completion(frm) {
    const contractDate = frm.doc.contract_date;
    const months = frm.doc.maximum_duration_months;

    if (contractDate && months) {
        const target = frappe.datetime.add_months(contractDate, parseInt(months));
        frm.set_value("target_completion_date", target);
    }
}
