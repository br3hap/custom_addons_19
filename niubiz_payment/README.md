# Niubiz Payment Provider para Odoo 19

Este módulo integra Niubiz como proveedor de pagos en Odoo, permitiendo procesar pagos con tarjetas de crédito y débito Visa y Mastercard.

## Características

- Integración completa con la API de Niubiz
- Soporte para tarjetas Visa y Mastercard
- Entornos de prueba y producción
- Procesamiento seguro de pagos
- Webhooks para notificaciones automáticas

## Instalación

1. Copia este módulo en tu directorio `custom_addons`
2. Actualiza la lista de módulos en Odoo
3. Instala el módulo "Niubiz Payment Provider"

## Configuración

### 1. Obtener credenciales de Niubiz

Regístrate en el portal de desarrolladores de Niubiz y obtén:
- Merchant ID
- Access Key  
- Secret Key

### 2. Configurar el proveedor de pago

1. Ve a **Contabilidad > Configuración > Proveedores de Pago**
2. Crea un nuevo proveedor o edita uno existente
3. Selecciona "Niubiz" como proveedor
4. Completa los campos:
   - **Merchant ID**: Tu ID de comercio
   - **Access Key**: Tu clave de acceso
   - **Secret Key**: Tu clave secreta
   - **Entorno**: Selecciona "Test" para pruebas o "Live" para producción

### 3. Configurar métodos de pago

1. En la configuración del proveedor, ve a la pestaña "Métodos de Pago"
2. Agrega "Niubiz" como método disponible
3. Configura las monedas soportadas (PEN, USD)

## URLs de Webhook

Para recibir notificaciones automáticas de Niubiz, configura estas URLs en tu panel de Niubiz:

- **URL de Retorno**: `https://tu-dominio.com/payment/niubiz/return`
- **URL de Webhook**: `https://tu-dominio.com/payment/niubiz/webhook`

## Monedas Soportadas

- PEN (Soles Peruanos)
- USD (Dólares Americanos)

## Entornos

### Sandbox (Pruebas)
- URL: `https://apisandbox.vnforappstest.com`
- Usar tarjetas de prueba proporcionadas por Niubiz

### Producción
- URL: `https://apiprod.vnforapps.com`
- Usar credenciales reales de producción

## Tarjetas de Prueba

Para el entorno de pruebas, puedes usar estas tarjetas:

**Visa:**
- Número: 4444333322221111
- CVV: 123
- Fecha: Cualquier fecha futura

**Mastercard:**
- Número: 5555444433331111  
- CVV: 123
- Fecha: Cualquier fecha futura

## Soporte

Para soporte técnico, consulta la documentación oficial de Niubiz:
https://desarrolladores.niubiz.com.pe/docs/api-p2p