odoo.define('pos_customer_uso_cfdi.get_customer', function(require) {
    "use strict";

    var models = require('point_of_sale.models');
    models.load_fields("res.partner", ['type_identifier']);


