# Estándares de Portabilidad y Entrega Segura de Copias de PII

- **Norma de Referencia**: ISO/IEC 27701:2025, Controles **A.1.3.9** y **A.3.7**.
- **Objetivo**: Establecer los requisitos técnicos para la generación de copias estructuradas de datos y los protocolos de entrega segura que eviten la interceptación o fuga de información.

---

## 1. Requisitos de Formato para Portabilidad (Control A.1.3.9)

El control A.1.3.9 exige que la copia entregada al titular sea:
1. **Estructurada**: Datos organizados conforme a esquemas lógicos comprensibles.
2. **De uso común e interoperable**: Formatos no propietarios ampliamente soportados por la industria.
3. **De lectura mecánica (*machine-readable*)**: Procesables directamente por programas informáticos sin intervención humana manual.

### Formatos Aceptables vs Formatos Rechazados

| Formato | Estado | Justificación Técnica |
|---|---|---|
| **JSON** (`application/json`) | **Óptimo** | Esquema jerárquico abierto, ampliamente compatible, estándar de facto para APIs web. |
| **CSV** (`text/csv` normalizado UTF-8) | **Aceptable** | Ideal para datos tabulares (ej. historial de transacciones o registros de llamadas). |
| **XML** (`application/xml` con XSD) | **Aceptable** | Estructurado y validable, comúnmente usado en banca y sistemas tributarios. |
| **PDF con texto seleccionable** | **Limitado** (Solo para Acceso visual) | Válido para el derecho de Acceso general, pero **insuficiente para Portabilidad técnica**. |
| **Imágenes escaneadas / Capturas de pantalla** | **PROHIBIDO** | Viola A.1.3.9 al no permitir lectura mecánica ni interoperabilidad. |
| **Formatos propietarios binarios cerrados** | **PROHIBIDO** | Bloquea la libre transferencia a otro responsable de tratamiento. |

---

## 2. Protocolo de Entrega Segura de la Copia de Datos

La entrega de la copia personal no debe crear un nuevo vector de vulnerabilidad ni exponer los datos a interceptaciones:

1. **Prohibición de Adjuntos por Correo Ordinario sin Cifrar**:
   - Está prohibido remitir archivos con datos personales sensibles o identificativos directos como adjuntos sin contraseña mediante correos SMTP abiertos.
2. **Repositorio Protegido con Enlace Temporal**:
   - Alojar el archivo en un portal seguro con cifrado TLS 1.3 en tránsito y cifrado en reposo (AES-256).
   - Generar un enlace temporal con caducidad estricta (máximo 7 días naturales).
   - Limitar el número de descargas permitidas (ej. 3 intentos).
3. **Autenticación Fuera de Banda (Out-of-Band Auth)**:
   - Proteger el archivo mediante una clave de descifrado o código temporal enviado por un canal de comunicación diferente al usado para enviar el enlace (ej. enlace por correo electrónico, PIN por SMS/WhatsApp o aplicación autenticadora).
