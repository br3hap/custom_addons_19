from odoo import http
from odoo.http import request, route


class Main(http.Controller):
    @http.route('/public-component', type='http', auth='public', website=True, method=['GET'], csrf=False)
    def render_simple_controller(self):
        values = {
            'partner_name': request.env.user.partner_id.name if not request.env.user._is_internal() else f"Usuario {request.env.user.partner_id.name}",
        }

        return request.render('component_public.my_template_simple_component', values)


    @http.route('/partner-resume/<int:partner_id>', type='json', auth='user', website=True, methods=['POST'], csrf=False)
    def get_partner_resume(self, partner_id):
        SaleOrder = request.env['sale.order']
        PurchaseOrder = request.env['purchase.order']
        sales_sumary = SaleOrder.read_group(
            [('partner_id', '=', partner_id)],
            ['amount_total:sum'],
            ['state']
        )
        purchases_sumary = PurchaseOrder.read_group(
            [('partner_id', '=', partner_id)],
            ['amount_total:sum'],
            ['state']
        )

        result = {
            "sales": [
                {
                    "state": record['state'] or 'undefined',
                    "total_amount": record['amount_total'],
                    "count": record['__count', 0]
                }
                for record in sales_sumary
            ],
            "purchases": [
                {
                    "state": record['state'] or 'undefined',
                    "total_amount": record['amount_total'],
                    "count": record['__count', 0]
                }
                for record in purchases_sumary
            ],
        }

        return result