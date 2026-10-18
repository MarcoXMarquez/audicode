---
name: consent-validator
description: "Auditoría de obtención, registro probatorio y revocación del consentimiento (ISO/IEC 27701:2025 A.1.2.4, CMPs y opt-out)."

status: published
category: ISO/IEC 27701:2025
---

# Consent Validator: Auditoría del Ciclo de Vida del Consentimiento (ISO/IEC 27701:2025)

Esta skill proporciona las directrices operativas y metodológicas para auditar de forma integral la captación, registro probatorio, trazabilidad técnica y canales de revocación del consentimiento en sistemas de gestión de privacidad (PIMS).

---

## 1. Controles Normativos Auditados

- **Control A.1.2.4 (Guía B.1.2.4)**: *Determine when and how consent is to be obtained* (Validez jurídica, consentimiento no condicionado, granularidad por propósito y reglas para menores).
- **Control A.1.2.5 (Guía B.1.2.5)**: *Obtain and record consent* (Acción afirmativa inequívoca, prohibición de casillas premarcadas y registro probatorio inmutable - *Consent Ledger*).
- **Control A.1.3.5 (Guía B.1.3.5)**: *Providing mechanism to modify or withdraw consent* (Simetría de canales, revocación sin fricción y propagación de la baja a sistemas y terceros).
- **Control A.2.2.4 (Guía B.2.2.4)**: *Marketing and advertising use* (Restricciones y prohibición estricta de mercadotecnia para encargados del tratamiento sin consentimiento válido).
- **Equivalencias ISO/IEC 27701:2019**: Cláusulas 7.2.4, 7.2.5, 7.3.4 y 8.2.3.

---

## 2. Activación y Descarte (Fronteras Operativas)

### Cuándo Usar Esta Skill (Triggers)
- Evaluación de formularios de registro, checkout o suscripción en aplicaciones web o móviles.
- Auditoría de banners CMP de cookies y selectores de preferencias de rastreo.
- Verificación del estado por defecto de casillas de verificación (*pre-ticked boxes*).
- Inspección de esquemas de bases de datos, tablas de logs o eventos de consentimiento (*Consent Ledger*).
- Análisis de la simetría y facilidad técnica en flujos de baja (*opt-out*) y desuscripción.
- Auditoría de restricciones a encargados respecto al uso publicitario de datos de clientes.

### Qué Delegar a Otras Skills (Límites Estrictos)
- **Textos completos de avisos de privacidad y políticas de privacidad internas**: Delegar a `privacy-policy-reviewer` (Cláusula 5.2, A.1.3.3, A.1.3.4).
- **Atención de solicitudes formales de derechos ARCO (acceso, rectificación, cancelación/supresión, oposición)**: Delegar a `pii-rights-manager` (A.1.3.1, A.1.3.2, A.1.3.6).
- **Contratos marco de encargo de tratamiento (DPA) con proveedores**: Delegar a `processor-contract-validator` (A.1.5.1, A.2.2.2).

---

## 3. Flujo de Trabajo de Auditoría (Paso a Paso)

```
[Entrada: UI / Formulario / CMP / DB Logs]
                  │
                  ▼
   Paso 1: Clasificación de Rol y Ámbito (A.1 Responsable vs A.2 Encargado)
                  │
                  ▼
   Paso 2: Evaluación de Libre Elección y No Condicionamiento (A.1.2.4)
                  │
                  ▼
   Paso 3: Verificación de Especificidad y Vínculo Informativo (A.1.2.4, A.1.3.3)
                  │
                  ▼
   Paso 4: Validación de Acción Inequívoca y Patrones Oscuros (A.1.2.5)
                  │
                  ▼
   Paso 5: Auditoría de Logs y Trazabilidad Probatoria - Ledger (A.1.2.5)
                  │
                  ▼
   Paso 6: Verificación de Simetría en Revocación y Propagación (A.1.3.5, A.2.2.4)
                  │
                  ▼
   Paso 7: Calificación de Severidad y Generación del Informe de Auditoría
```

### Paso 1: Clasificación de Rol y Ámbito
Determinar si la organización auditada actúa como:
1. **Responsable (*PII Controller*)**: Aplican los controles A.1.2.4, A.1.2.5 y A.1.3.5.
2. **Encargado (*PII Processor*)**: Aplica el control A.2.2.4 (verificar que no realice mercadotecnia con datos del cliente sin autorización documentada).

### Paso 2: Análisis de Libre Elección (*Freely Given*)
1. Verificar que el acceso a las funcionalidades esenciales del servicio o contrato principal **no esté condicionado** a la aceptación de finalidades accesorias (ej. publicidad, analítica de terceros).
2. Constatar la ausencia de coerción económica, penalización o desbalance manifiesto de poder.
3. Comprobar que negarse a consentir no conlleva la degradación indebida de prestaciones básicas.

### Paso 3: Verificación de Especificidad e Información Previa
1. **Granularidad**: Cada propósito de tratamiento diferenciado debe contar con un mecanismo de selección independiente. Queda terminantemente prohibido el consentimiento empaquetado (*bundled consent*).
2. **Identificación**: La identidad del responsable debe ser visible en el punto de captura.
3. **Enlace al Aviso de Privacidad**: Debe existir un enlace directo, accesible y funcional al aviso de privacidad íntegro antes de que el titular emita su consentimiento.

### Paso 4: Validación de Acción Inequívoca (*Unambiguous Action*)
1. **Prohibición de casillas premarcadas**: Toda casilla o selector debe venir desmarcado por defecto (*opt-in* puro).
2. **Prohibición de consentimiento por inacción**: El silencio, la continuación de la navegación o el scroll no constituyen consentimiento válido.
3. **Detección de patrones oscuros (*dark patterns*)**:
   - Desbalance visual o cromático entre "Aceptar" y "Rechazar" / "Configurar".
   - *Confirmshaming* (textos de rechazo humillantes o disuasorios).
   - Opciones preseleccionadas encubiertas en submenús o ventanas modales.

### Paso 5: Auditoría de Logs y Registro Probatorio (*Consent Ledger*)
Para verificar el cumplimiento probatorio de **A.1.2.5**, auditar la estructura de base de datos o logs del CMP. Consultar [consent_matrix.md](references/consent_matrix.md) para la especificación completa:
- Identificador unívoco del evento (`consent_id`).
- Identificador del titular (`subject_identifier`).
- Marca de tiempo exacta en formato ISO 8601 UTC (`timestamp_utc`).
- Finalidad(es) consentida(s) de forma desglosada (`purpose_id`).
- Versión exacta del texto legal aceptado (`legal_text_version`) o hash criptográfico (`legal_text_hash`).
- Canal de recolección (`capture_channel`).

> **Regla de Auditoría**: Si el sistema solo almacena una bandera booleana (`consent = 1`) sin timestamp ni versión del texto legal aceptado, se emitirá una **No Conformidad Mayor**.

### Paso 6: Verificación de Mecanismo de Revocación y Simetría
Conforme a **A.1.3.5**:
1. **Regla de simetría de canales**: Retirar el consentimiento debe ser tan fácil como otorgarlo (*same effort rule*). Si se otorgó mediante un clic web, debe poder retirarse mediante un centro de preferencias web o enlace directo de baja.
2. **Prohibición de fricción asimétrica**: No se permite exigir llamadas telefónicas, envío de formularios impresos o comparecencias presenciales para revocar consentimientos otorgados digitalmente.
3. **Propagación técnica**: Constatar que el evento de revocación actualice de forma sincronizada los sistemas internos y se notifique a terceros/encargados en un plazo máximo razonable (24-72 horas).

### Paso 7: Calificación de Severidad y Emisión de Informe
Clasificar cada discrepancia detectada en una de las cuatro categorías de severidad:
- **Crítica**: Casillas premarcadas, consentimiento forzado para uso publicitario, o ausencia total de mecanismo de revocación.
- **Mayor**: Empaquetamiento de finalidades dispares en una sola casilla, logs sin versión de política/timestamp, o fricción asimétrica desproporcionada.
- **Menor**: Formato de timestamp no estandarizado (falta zona UTC), o demora técnica de propagación que no supera el umbral regulatorio pero carece de confirmación formal al usuario.
- **Oportunidad de Mejora**: Integración de sellado criptográfico (*proof_token*) en los registros o redacción optimizada de microtextos legales informativos.

---

## 4. Formato Estándar de Hallazgos

Todo informe emitido bajo esta skill debe tabular los hallazgos con la siguiente estructura:

| ID Hallazgo | Control ISO 27701:2025 | Severidad | Elemento Auditado | Evidencia Detectada | Recomendación Técnica / Correctiva |
|---|---|---|---|---|---|
| HALLAZGO-01 | A.1.2.5 | CRÍTICA | Checkbox de Newsletter en Checkout | La casilla de suscripción comercial está premarcada (`checked="true"` por defecto). | Desmarcar la casilla por defecto. Requerir una acción deliberada y positiva del titular para habilitar el consentimiento. |
| HALLAZGO-02 | A.1.2.4 | CRÍTICA | Formulario de Registro | Se obliga al usuario a aceptar envíos comerciales para poder crear su cuenta de servicio. | Separar los Términos de Servicio obligatorios de las finalidades accesorias opcionales (desagregación estricta). |
| HALLAZGO-03 | A.1.2.5 | MAYOR | Tabla `users` en Base de Datos | Solo se almacena el campo `newsletter_optin = 1`, sin timestamp ni versión del aviso. | Implementar un *Consent Ledger* inmutable que guarde timestamp ISO 8601 UTC, ID de usuario, finalidad y hash del texto aceptado. |
| HALLAZGO-04 | A.1.3.5 | MAYOR | Flujo de Baja de Publicidad | El email contiene un enlace que remite a un formulario que exige llamar por teléfono para confirmar la baja. | Habilitar un mecanismo de baja en 1 clic (*List-Unsubscribe* RFC 8058) o un centro de preferencias autogestionado en línea. |

---

## 5. Herramienta Determinista de Soporte

Para automatizar la verificación de configuraciones de formularios JSON o lotes de registros de consentimiento, ejecutar el script determinista:

```bash
python skills/consent-validator/scripts/consent_flow_checker.py --input <ruta_archivo.json> [--strict] [--format json]
```

El script inspecciona automáticamente el estado inicial de selectores, detecta condicionamiento o empaquetamiento y valida la integridad de metadatos del registro probatorio.

---

## 6. Qué NO Hacer (Límites y Reglas Negativas Explícitas)

1. **NO emitir asesoría legal vinculante**: Los informes de auditoría técnica reflejan conformidad con la norma ISO/IEC 27701:2025 y buenas prácticas de privacidad, pero no sustituyen el dictamen de un abogado o asesor jurídico colegiado.
2. **NO asumir información ausente**: Si no se proporciona el esquema de base de datos, las capturas de UI o los flujos de desuscripción, solicitar explícitamente los datos al usuario en lugar de suponer que el sistema es conforme.
3. **NO auditar el aviso de privacidad general completo**: No revisar la redacción exhaustiva de la política de privacidad corporativa; esa tarea corresponde a `privacy-policy-reviewer`.
4. **NO tramitar solicitudes de derechos ARCO**: No responder ni procesar peticiones formales de acceso, rectificación, cancelación u oposición del titular; transferir a `pii-rights-manager`.
5. **NO evaluar contratos mercantiles entre responsables y encargados**: Limitar la revisión del rol de encargado a las restricciones técnicas de mercadotecnia de A.2.2.4; el análisis integral de DPA corresponde a `processor-contract-validator`.
6. **NO aceptar indicadores booleanos simples como evidencia de cumplimiento**: Rechazar categóricamente afirmaciones de que una simple columna booleana en base de datos satisface el principio de rendición de cuentas (*accountability*) de A.1.2.5.

---

## 7. Divulgación Progresiva y Referencias Técnicas

Para profundizar en criterios específicos, consultar:
- [consent_matrix.md](references/consent_matrix.md): Matriz normativa de validez del consentimiento, catálogo de patrones oscuros y especificación de campos de trazabilidad del *Consent Ledger*.
- [consent_flow_checker.py](scripts/consent_flow_checker.py): Validador determinista de esquemas y registros de consentimiento en Python.

---

## Soporte Local de Documentos, Formularios e Imágenes (AudiCode Local Engine)

AudiCode procesa todos los archivos adjuntos de forma **100% local en tu CPU** antes de pasarlos a este agente:
- **Capturas de Pantalla e Imágenes (.png, .jpg, .webp)**: Formularios de registro, modales de cookies (CMP) o flujos de desuscripción se procesan mediante OCR local en CPU (
apidocr-onnxruntime). Los textos, botones ([Aceptar], [Rechazar]), enlaces y casillas ([x] Casilla marcada, [ ] Desmarcada) se extraen directamente en el prompt.
- **Documentos (.pdf, .docx)**: Políticas de consentimiento y términos legales se convierten a Markdown limpio estructurado mediante pymupdf4llm y markitdown.
- **Textos Extensos Pegados**: Los contratos o códigos extensos pegados (>12 líneas) se compactan en un snippet adjunto limpio sin saturar el campo de entrada.
