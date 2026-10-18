# Procedimiento Operativo Estándar (SOP): Verificación Proporcional y Gestión de Solicitudes DSAR / ARCO

- **Norma de Referencia**: ISO/IEC 27701:2025, Controles A.1.3.10 y A.1.3.7.
- **Objetivo**: Estandarizar la recepción, autenticación no invasiva y canalización interna de solicitudes de derechos sin imponer barreras desproporcionadas ni generar brechas de seguridad.

---

## 1. Principio de Autenticación Proporcional y No Discriminatoria

Conforme al Control **A.1.3.10**, la organización debe verificar la identidad del solicitante para garantizar que no se revelen datos a terceros no autorizados, pero evitando solicitar datos innecesarios o desmedidos.

### Matriz de Niveles de Autenticación Requerida

| Canal de Origen | Estado de Autenticación | Nivel de Riesgo del Trámite | Mecanismo de Verificación Recomendado | Prohibición Expresa |
|---|---|---|---|---|
| **Portal Web / App Móvil** | Sesión activa con credenciales y MFA | Bajo a Medio (Acceso, Rectificación, Oposición) | Validación de sesión activa + confirmación por correo de aviso. | **PROHIBIDO solicitar DNI/Pasaporte escaneado.** |
| **Portal Web / App Móvil** | Sesión activa | Alto (Supresión definitiva / Portabilidad masiva) | Re-autenticación obligatoria (Step-up Auth) mediante token OTP al móvil o email registrado. | No exigir personación física ni trámites notariales. |
| **Correo Electrónico Directo** | Correo coincide con el registrado en cuenta | Medio a Alto | Envío de enlace seguro temporal con código OTP de confirmación a dicho correo. | No solicitar datos bancarios ni contraseñas. |
| **Correo Electrónico Directo** | Correo desconocido / no registrado | Alto | Cotejo contextual de 2 datos no públicos (ej. número de cliente o fecha de último recibo) o código OTP por teléfono registrado. | No revelar la existencia o inexistencia previa de cuenta hasta verificar identidad. |
| **Ventanilla Física / Correo Postal** | Presencial / Documental | Medio a Alto | Exhibición visual del documento de identidad oficial. En copias físicas, admitir enmascaramiento de campos no indispensables. | No almacenar copias escaneadas de DNI en servidores sin cifrar ni más tiempo del necesario. |

---

## 2. Tratamiento de Solicitudes por Representante Legal

1. **Acreditación de Representación**:
   - Para personas con patria potestad o tutela: Documento oficial acreditativo (libro de familia, resolución judicial o certificado de nacimiento).
   - Para mandatarios / abogados: Poder especial bastanteado o autorización firmada por el titular acompañada de los mecanismos de verificación de la identidad del poderdante.
2. **Registro de Evidencia**: El poder o mandato debe anexarse al expediente digital de la solicitud en el sistema de tickets, con acceso restringido exclusivamente al Oficial de Protección de Datos (DPO).

---

## 3. Registro y Trazabilidad en Plataforma de Ticketing

Toda solicitud debe registrar obligatoriamente los siguientes metadatos inmutables:
- `ticket_id`: Identificador único (ej. `DSAR-2026-0042`).
- `timestamp_received_utc`: Marca temporal de recepción exacta.
- `applicant_type`: Titular directo o representante autorizado.
- `right_type`: Acceso, Rectificación, Supresión, Oposición, Limitación o Portabilidad.
- `identity_verification_status`: `PENDING`, `VERIFIED`, `REJECTED_UNVERIFIABLE`.
- `statutory_deadline`: Fecha límite calculada conforme a la jurisdicción aplicable.
- `extension_status`: `NONE`, `EXTENDED` (con justificación archivada).
- `resolution_status`: `IN_PROGRESS`, `FULFILLED`, `REFUSED_JUSTIFIED`, `CLOSED`.
- `third_party_cascade_logged`: Bandera booleana que acredita si se comunicó a terceros bajo A.1.3.8.
