/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class ListaUsuariosAction extends Component {
    static template = 'mi_modulo_owl.lista_usuarios_accion';
    
    setup() {
        // Servicio ORM para consultas
        this.orm = useService('orm');
        this.notification = useService('notification');
        
        // Estado reactivo
        this.state = useState({
            usuarios: [],
            cargando: true,
            error: null
        });

        // Cargar usuarios
        this.cargarUsuarios();
    }

    async cargarUsuarios() {
        try {
            // Buscar usuarios
            const usuarios = await this.orm.searchRead(
                'res.users', 
                [['active', '=', true]], 
                ['id', 'name', 'login', 'email']
            );

            this.state.usuarios = usuarios;
            this.state.cargando = false;
        } catch (error) {
            console.error('Error al cargar usuarios:', error);
            this.state.error = 'No se pudieron cargar los usuarios';
            this.state.cargando = false;
        }
    }

    mostrarEmail(email) {
        this.notification.add(`Email: ${email}`, {
            title: 'Correo Electrónico',
            type: 'info'
        });
    }
}

// Función global para uso en templates web
window.mostrarEmail = function(email) {
    const toast = document.createElement('div');
    toast.className = 'toast show position-fixed';
    toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    toast.innerHTML = `
        <div class="toast-header bg-primary text-white">
            <i class="fa fa-envelope me-2"></i>
            <strong class="me-auto">Correo Electrónico</strong>
            <button type="button" class="btn-close btn-close-white" onclick="this.parentElement.parentElement.remove()"></button>
        </div>
        <div class="toast-body">
            <strong>Email:</strong> ${email}
        </div>
    `;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        if (toast.parentNode) {
            toast.remove();
        }
    }, 5000);
};

// Registrar la acción
registry.category("actions").add("lista_usuarios", ListaUsuariosAction);