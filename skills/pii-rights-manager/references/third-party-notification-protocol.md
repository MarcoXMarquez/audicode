# Protocolo Técnico de Notificación en Cascada a Terceros Receptores

- **Norma de Referencia**: ISO/IEC 27701:2025, Controles **A.1.3.8** y **A.2.3.2**.
- **Objetivo**: Garantizar que toda rectificación, supresión u oposición ejercida por un titular se propague y ejecute de forma verificable en toda la cadena de valor de terceros, encargados (*PII processors*) y subencargados.

---

## 1. Obligación Normativa (Control A.1.3.8)

El responsable del tratamiento (*PII controller*) debe implementar medidas razonables y proporcionales para informar a los terceros con quienes haya compartido o transferido datos personales sobre:
1. Cualquier **rectificación** de datos inexactos.
2. Cualquier **supresión** o borrado de datos.
3. Cualquier **oposición** legítima al tratamiento o revocación de consentimiento relevante.

---

## 2. Mecanismos Técnicos de Comunicación en Cascada

### 2.1 Enfoque Automatizado (Sistemas Integrados / SaaS Modernos)
- **Webhooks de Privacidad**: Disparador HTTP POST seguro (`https`) hacia el endpoint de privacidad del tercero con carga útil cifrada:
  ```json
  {
    "event_type": "PII_ERASURE_INSTRUCTION",
    "event_id": "EVT-2026-9921",
    "timestamp_utc": "2026-10-01T14:30:00Z",
    "subject_identifier": {
      "type": "USER_UUID",
      "value": "e4b9a112-882f-4c55-9011-aa9b23f81e3a"
    },
    "action": "ERASE_AND_BLOCK",
    "scope": ["MARKETING_CRM", "BILLING_ARCHIVE_EXCLUDED"]
  }
  ```
- **Bus de Mensajería (Event-Driven Architecture)**: Tópico dedicado en Kafka/RabbitMQ (`privacy-dsar-events`) consumido por microservicios y conectores a terceros.
- **Acuse de Recibo Técnico (ACK)**: El sistema tercero debe responder con código HTTP 200/202 y un token de confirmación de recepción en un SLA menor a 24 horas.

### 2.2 Enfoque Formal Documental (Proveedores Tradicionales / B2B)
- Envío de la **Plantilla 7** de `rights_timeline_matrix.md` por canal seguro o correo electrónico oficial del Delegado de Protección de Datos del proveedor.
- Exigencia de respuesta escrita confirmando la ejecución dentro del plazo estipulado en el contrato DPA (máximo 72 horas a 5 días hábiles).

---

## 3. Matriz de Auditoría y Verificación de Cascada

| Pregunta de Auditoría | Evidencia Esperada | Criterio de No Conformidad |
|---|---|---|
| ¿Se dispone de un inventario actualizado de terceros que reciben PII? | Registro de Actividades de Tratamiento (ROPA) y matriz de transferencias (A.1.5.3). | Desconocimiento de qué proveedores tienen copias del titular. (NC Mayor) |
| ¿Existen registros de las notificaciones enviadas a terceros tras un borrado? | Logs de webhooks o acuses de recibo en el ticket de la solicitud. | El ticket se cierra sin constancia de comunicación a terceros. (NC Crítica) |
| ¿Los contratos DPA incluyen la obligación de atender estas notificaciones? | Cláusula de asistencia obligatoria según el control A.2.3.2 y Tabla A.2. | Contratos de encargo que no contemplan deber de borrado a solicitud. (NC Mayor) |
