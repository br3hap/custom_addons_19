# Culqi Payment Provider para Odoo 19

Este módulo integra Culqi como proveedor de pagos en Odoo, permitiendo procesar pagos con tarjetas de crédito y débito en Perú.

## Características

- Soporte para tarjetas de crédito y débito
- Procesamiento seguro con tokens
- Soporte para PEN y USD
- Entornos de prueba y producción
- Webhooks para notificaciones automáticas

## Instalación

1. Copia este módulo en tu carpeta `custom_addons`
2. Actualiza la lista de módulos en Odoo
3. Instala el módulo "Culqi Payment Provider"

## Configuración

### 1. Obtener credenciales de Culqi

1. Regístrate en [Culqi](https://culqi.com)
2. Obtén tus llaves públicas y secretas desde el panel de Culqi
3. Para pruebas, usa las credenciales de test
4. Para producción, usa las credenciales live

### 2. Configurar en Odoo

1. Ve a **Contabilidad > Configuración > Proveedores de Pago**
2. Crea un nuevo proveedor o edita uno existente
3. Selecciona "Culqi" como proveedor
4. Configura los siguientes campos:
   - **Public Key**: Tu llave pública de Culqi
   - **Secret Key**: Tu llave secreta de Culqi
   - **Entorno**: Test para pruebas, Live para producción
5. Configura las URLs de webhook en Culqi:
   - **Webhook URL**: `https://tu-dominio.com/payment/culqi/webhook`

### 3. Configurar Webhooks en Culqi

En tu panel de Culqi, configura los siguientes webhooks:
- **URL**: `https://tu-dominio.com/payment/culqi/webhook`
- **Eventos**: `charge.succeeded`, `charge.failed`

## Uso

Una vez configurado, Culqi aparecerá como opción de pago en:
- Checkout de eCommerce
- Facturas de cliente
- Órdenes de venta

## Monedas Soportadas

- PEN (Soles Peruanos)
- USD (Dólares Americanos)

## Seguridad

- Los datos de tarjeta nunca pasan por tu servidor
- Culqi maneja toda la información sensible
- Comunicación encriptada SSL/TLS
- Tokens seguros para transacciones

## Soporte

Para soporte técnico:
- Documentación de Culqi: https://docs.culqi.com
- API Reference: https://apidocs.culqi.com

## Licencia

LGPL-3