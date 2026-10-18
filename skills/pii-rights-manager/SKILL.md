---
name: pii-rights-manager
description: >
  Audita y gestiona el cumplimiento de las obligaciones hacia los titulares de PII
  y el ejercicio de sus derechos ARCO/DSAR (A.1.3, A.1.3.7, A.1.3.8, A.1.3.6, A.1.3.9, A.1.3.10, A.2.3.2)
  bajo ISO/IEC 27701:2025. Use when user says "auditar atencion de derechos ARCO", "gestionar solicitud de supresion de datos",
  "revisar plazo de respuesta DSAR", "exportar datos para portabilidad", o "notificar borrado a terceros receptores".
  No gestiona revocaciones simples de consentimiento publicitario ni bajas de newsletter (use consent-validator).
---

# PII Rights Manager

Guía operacional para la auditoría, estructuración y gestión técnica del ejercicio de derechos de los titulares de datos personales (*PII Principals*) conforme al estándar internacional **ISO/IEC 27701:2025** y las principales legislaciones de protección de datos (RGPD, LGPD, CCPA/CPRA, normativas ARCO de América Latina).

---

## 1. Disparadores y Límites Operativos

### 1.1 Cuándo usar esta Skill (Triggers)
Activa esta skill cuando se presenten situaciones tales como:
- Auditoría o diseño del procedimiento interno de gestión de solicitudes de derechos ARCO / DSAR (*Data Subject Access Requests*).
- Tramitación de solicitudes de **acceso** a PII, detalle de finalidades y destinatarios (A.1.3.7).
- Solicitudes de **rectificación** o actualización de datos erróneos o incompletos (A.1.3.7).
- Solicitudes de **supresión** (*erasure* o derecho al olvido) y bloqueo de datos en sistemas y copias de seguridad (A.1.3.7).
- Solicitudes de **oposición** (*objection*) al tratamiento basado en interés legítimo o mercadotecnia directa (A.1.3.6).
- Requerimientos de **portabilidad de datos** y entrega de copias estructuradas en formatos interoperables (A.1.3.9).
- Evaluación de los mecanismos de **verificación de identidad** para evitar recopilación excesiva (A.1.3.10).
- Orquestación de la **notificación en cascada a terceros cesionarios** y subencargados tras una modificación o borrado (A.1.3.8).
- Supervisión del cumplimiento de encargados de tratamiento (*PII Processors*) para asistir al responsable (A.2.3.2).

### 1.2 Límites Estrictos y Descarte (Qué NO atiende esta Skill)
- **Revocación ordinaria de consentimiento**: Si el usuario simplemente hace clic en "darme de baja" de un correo comercial, retira permisos en un banner de cookies o modifica preferencias de UI/UX, delega a `consent-validator` (A.1.3.5 / A.1.2.5).
- **Redacción de avisos informativos generales**: Para el análisis estático de las cláusulas informativas de políticas de privacidad web o apps móviles, delega a `privacy-policy-reviewer` (Cláusula 5.2 / A.1.3.3 / A.1.3.4).
- **Inspección general de esquemas de bases de datos**: Para auditar la minimización estructural de tablas SQL, índices y payloads de APIs independientes de un caso ARCO concreto, delega a `data-minimization-checker` (A.1.4.2 / A.1.4.5).
- **Contratos B2B marco con proveedores**: Para la revisión contractual integral de DPAs y cláusulas de confidencialidad, delega a `processor-contract-validator` (A.1.2.7 / Tabla A.2).

---

## 2. Mapa Normativo ISO/IEC 27701:2025

| Control ISO 27701:2025 | Ref. 2019 | Denominación Oficial | Enfoque de Auditoría |
|---|---|---|---|
| **A.1.3** | 7.3 | *Obligations to PII principals* | Marco y gobernanza general para satisfacer derechos de los titulares. |
| **A.1.3.7** | 7.3.6 | *Access, correction or erasure* | Mecanismos funcionales para consultar, rectificar y eliminar datos personales. |
| **A.1.3.8** | 7.3.7 | *PII controllers' obligations to inform third parties* | Cascada de avisos a terceros receptores ante cambios, borrados u oposiciones. |
| **A.1.3.6** | 7.3.5 | *Providing mechanism to object to PII processing* | Oposición incondicional a marketing y cese de tratamiento por interés legítimo. |
| **A.1.3.9** | 7.3.8 | *Providing copy of PII processed* | Formatos legibles por máquina (JSON, CSV) y transmisión segura cifrada. |
| **A.1.3.10** | 7.3.9 | *Handling requests* | Tramitación oportuna, gratuidad general y verificación proporcional de identidad. |
| **A.2.3.2** | 8.3.1 | *Comply with obligations to PII principals* | Obligación técnica del encargado de habilitar herramientas de gestión al responsable. |

---

## 3. Flujo Operativo de Atención de Derechos (5 Fases)

```
[Fase 1: Recepción & Tipificación] ---> [Fase 2: Autenticación Proporcional]
                 |                                      |
                 v                                      v
[Fase 5: Respuesta Formal & Cierre] <-- [Fase 4: Ejecución & Cascada] <-- [Fase 3: Análisis Jurídico]
```

### Fase 1: Recepción, Registro y Tipificación
1. **Canal de Entrada**: Recibir la solicitud por canal formal (formulario web seguro, correo DPO, ventanilla física o panel de usuario).
2. **Registro Inmutable (DSAR Log)**: Registrar inmediatamente en el sistema de tickets:
   - Identificador único de solicitud (`request_id`).
   - Fecha y hora exacta de recepción (marca temporal UTC ISO 8601).
   - Canal de ingreso y datos de contacto del solicitante.
   - Tipología del derecho ejercido:
     * **Acceso** (A.1.3.7): Qué datos se tratan, finalidades, destinatarios y plazos previstos.
     * **Rectificación** (A.1.3.7): Corrección de datos inexactos o integración de incompletos.
     * **Supresión / Olvido** (A.1.3.7): Eliminación por cese de finalidad, ilicitud o retiro de consentimiento.
     * **Oposición** (A.1.3.6): Rechazo a mercadotecnia directa (incondicional) o tratamiento de interés legítimo.
     * **Limitación** (A.1.3.7): Marcado de datos para restringir su tratamiento futuro mientras se resuelve una controversia.
     * **Portabilidad** (A.1.3.9): Entrega de datos facilitados en formato estructurado de lectura mecánica.
3. **Cálculo de Plazo Límite Legal**: Ejecutar el script `scripts/deadline_calculator.py` para fijar la fecha fatal de resolución conforme a la jurisdicción aplicable (consultar `references/rights_timeline_matrix.md`).

### Fase 2: Verificación Proporcional de Identidad (A.1.3.10)
- **Principio de Proporcionalidad**: No exigir requisitos desproporcionados que constituyan una barrera de entrada al derecho.
- **Titular Autenticado**: Si el usuario realiza la solicitud desde una sesión autenticada con credenciales y MFA (o enlace verificado por correo electrónico previo), **NO solicitar copia del DNI/Pasaporte**.
- **Duda Razonable**: Solo si no existe certeza sobre la identidad o la petición proviene de un canal abierto no autenticado:
  1. Solicitar confirmación mediante token/OTP enviado al canal de contacto previamente registrado en la base de datos (email o teléfono).
  2. En caso estricto y de datos de alto impacto, solicitar información de cotejo contextual (ej. número de cliente o fecha de última transacción).
  3. La copia de documento de identidad oficial debe ser el último recurso, exigiendo únicamente los datos necesarios y admitiendo el tachado (*redaction*) de campos irrelevantes (ej. fotografía o firma).
- **Representación Legal**: En casos de peticiones por apoderado o tutor, verificar poder notarial específico o documentación acreditativa fehaciente.

### Fase 3: Análisis de Procedencia Jurídica y Excepciones
Evaluar si la solicitud es jurídicamente procedente o si aplica alguna excepción tasada:
- **En Supresión**:
  * *Procedente*: Cuando los datos ya no son necesarios, venció el periodo de retención, o el tratamiento fue ilícito.
  * *Excepción Legítima*: Existencia de deber legal de conservación (fiscal, contable, prevención de lavado de activos), ejercicio o defensa de reclamaciones judiciales, o fines de salud pública previstos por ley. En tales casos, los datos **no se eliminan de inmediato, sino que se bloquean** (aislamiento lógico).
- **En Oposición**:
  * *Mercadotecnia directa*: Cese inmediato e incondicional (no admite ponderación).
  * *Interés legítimo*: Ponderación obligatoria entre los motivos legítimos imperiosos de la organización y los derechos del titular.
- **Carácter Infundado o Excesivo**: Solicitudes repetitivas en periodos irrazonables permiten exigir un canon compensatorio por costes administrativos o negarse a actuar, siempre motivándolo fehacientemente.

### Fase 4: Orquestación Técnica y Cascada a Terceros
1. **Localización Exhaustiva de PII**:
   - Rastrear identificadores del titular en bases de datos relacionales, NoSQL, logs transaccionales, almacenes analíticos (data warehouses/lakes) y herramientas SaaS.
2. **Ejecución de la Acción Técnica**:
   - **Acceso / Portabilidad**: Extraer los datos en formato estructurado (JSON, CSV, PDF accesible). Alojar el archivo en un repositorio seguro con enlace cifrado y caducidad temporal (ej. 7 días) protegido por token o MFA.
   - **Rectificación**: Actualizar el dato en la fuente maestra (*Master Data*) y sincronizar automáticamente réplicas.
   - **Supresión**:
     * En producción: Purga física o sobreescritura criptográfica de los registros.
     * En copias de seguridad (*backups*): Aplicar bloqueo lógico en índices de recuperación para que, en caso de restauración de desastre, el registro no vuelva a activarse y sea purgado durante la rotación natural del ciclo de backup.
3. **Notificación en Cascada a Terceros (A.1.3.8 / A.2.3.2)**:
   - Identificar encargados, proveedores y cesionarios que hayan recibido los datos en los últimos periodos.
   - Transmitir la instrucción de rectificación, borrado u oposición mediante APIs automatizadas, webhooks o comunicación formal documentada.
   - Exigir acuse de recibo técnico o confirmación escrita de cumplimiento por parte de los terceros.

### Fase 5: Resolución y Notificación Formal al Titular
1. **Redacción de Respuesta Formal**: Emitir comunicación oficial motivada utilizando las plantillas de `references/rights_timeline_matrix.md`.
2. **Prórroga Excepcional**: Si la complejidad de la solicitud o el volumen impiden resolver en el plazo ordinario, remitir **antes del vencimiento original** un aviso motivando las razones de la extensión y la fecha estimada final.
3. **Información de Tutela de Derechos**: Toda resolución (especialmente las desestimatorias o prórrogas) debe informar explícitamente al titular su derecho a presentar reclamación ante la Autoridad de Control de Protección de Datos correspondiente y a la tutela judicial efectiva.

---

## 4. Matriz Estándar de Hallazgos de Auditoría

Al auditar procesos, sistemas de tickets o políticas de gestión de derechos, clasifica los hallazgos en la siguiente tabla:

| ID | Control ISO 27701:2025 | Severidad | Descripción del Hallazgo / Evidencia | Recomendación de Mitigación / Acción Correctiva |
|---|---|---|---|---|
| **HAL-DSAR-01** | A.1.3.7 / A.1.3.10 | **Crítica** | Vencimiento de plazos legales de atención sin respuesta ni notificación de prórroga formal. | Implementar el script de alertas tempranas `deadline_calculator.py` y fijar SLA interno a 15 días. |
| **HAL-DSAR-02** | A.1.3.8 | **Crítica** | Se ejecuta el borrado en la base interna pero no se notifica a proveedores de email marketing ni CRMs externos. | Establecer webhook o protocolo de cascada informativa obligatoria con acuse de recibo a encargados. |
| **HAL-DSAR-03** | A.1.3.10 | **Mayor** | Exigencia sistemática de copia a color de DNI/Pasaporte a usuarios con sesión autenticada activa. | Adecuar la política de verificación al principio de proporcionalidad, empleando autenticación en sesión o MFA. |
| **HAL-DSAR-04** | A.1.3.7 | **Mayor** | Purgas de supresión no contemplan la reincorporación de datos al restaurar copias de seguridad. | Diseñar procedimiento de lista negra/bloqueo de restauración diferida en el ciclo de rotación de respaldos. |
| **HAL-DSAR-05** | A.1.3.9 | **Menor** | Entrega de datos de portabilidad mediante capturas de pantalla o volcados PDF no estructurados. | Automatizar la exportación en esquemas abiertos interoperables (JSON o CSV normalizado). |
| **HAL-DSAR-06** | A.1.3.7 | **Oportunidad de Mejora** | La respuesta formal de rectificación no desglosa con exactitud cuáles campos fueron modificados. | Actualizar la plantilla de resolución formal detallando el valor anterior anonimizado y el nuevo valor rectificado. |

---

## 5. Reglas Mandatorias de Comportamiento: Qué NO Hacer

1. **NO entregar jamás datos personales de terceros**: En solicitudes de acceso o portabilidad, es imperativo anonimizar, enmascarar o eliminar datos identificativos de terceras personas (ej. correos de otros clientes, nombres de empleados o partes litigantes) presentes en historiales o transcripciones.
2. **NO demorar plazos sin justificación legal ni aviso previo**: No esperar a que expire el plazo legal para informar al titular que la solicitud es compleja. La notificación de prórroga debe remitirse siempre dentro del plazo ordinario.
3. **NO solicitar copias de documentos oficiales de identidad cuando no sea estrictamente necesario**: Exigir DNI escaneado a un usuario autenticado vulnera el principio de minimización (A.1.4.2) y el control A.1.3.10.
4. **NO desestimar peticiones de forma verbal o informal**: Todo rechazo o limitación debe constar por escrito en resolución formal motivada con base fáctica y fundamentos jurídicos de conservación.
5. **NO destruir datos sujetos a deberes legales de retención**: Ante un pedido de supresión de datos con implicaciones fiscales, comerciales o litigiosas vigentes, los datos deben ser **bloqueados** (restringiendo su acceso a fines probatorios), no eliminados de forma imprudente.
6. **NO asumir que el borrado local concluye el trámite**: Si los datos fueron compartidos con terceros, encargados o subencargados, el trámite solo finaliza al cursar y registrar la notificación a terceros (A.1.3.8).
7. **NO brindar asesoría legal definitiva**: El agente asesora en buenas prácticas, directrices operativas y auditoría técnica; las controversias y desestimaciones complejas deben ser revisadas por el Delegado de Protección de Datos (DPO) o el asesor legal de la organización.
8. **NO hacer suposiciones sin evidencia**: Si en la auditoría faltan datos sobre plazos de respuesta, canales de entrada o acuerdos con terceros, solicitar expresamente la evidencia antes de emitir juicio de conformidad.

---

## 6. Recursos y Herramientas Complementarias

- **Matriz de Plazos y Plantillas Formales**: Consulta `references/rights_timeline_matrix.md` para ver los calendarios regulatorios por país (RGPD, CCPA, LGPD, normativas ARCO México, Colombia, Perú, Argentina, Chile) y las 6 plantillas de respuesta.
- **Calculadora Determinista de Plazos**: Ejecuta `scripts/deadline_calculator.py` para calcular fechas límite, alertas de vencimiento y plazos prorrogados considerando días hábiles o naturales.
