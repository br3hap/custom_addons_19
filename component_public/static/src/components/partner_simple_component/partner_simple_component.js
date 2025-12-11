/** @odoo-module **/

import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { rpc } from "@web/core/network/rpc";
import { _t } from "@web/core/l10n/translation";

class PartnerPublicComponent extends Component {
      static template = "component_public.PartnerPublicComponent";
      // static components = {};
      static props = {
        partnerName: { type: String, optional: true },
      };

      setup() {
        this.notification = useService("notification");
        this.orm = useService("orm");
        this.state = useState({
          partners: [],
        });

        onWillStart(async () => {
          this.state.partners = await this.orm.searchRead("res.partner", [], ["id","name"], { limit: 10 });
          console.log(this.state.partnerName);          
        });
      }

      async showPartnerInfo(partner) {
        try{
          const partnerInfo = await rpc(`/partner-resume/${partner.id}`, {});
          const infoText = `
            Sales:
            ${partnerInfo.sales.map(s => `${s.state}: $${s.total_amount}`).join('\n')}
            
            Purchases:
            ${partnerInfo.purchases.map(p => `${p.state}: $${p.total_amount}`).join('\n')}
          `;
          this.notification.add(infoText, { type: "info" });
        } catch(err){
          this.notification.add(`Error fetching partner info: ${err.message}`, { type: "danger" });
        }
      }
  }

registry.category("public_components").add("@component_public/components/partner_simple_component/partner_simple_component", {
  Component: PartnerPublicComponent,
});

export default PartnerPublicComponent;
  