# Matriz de Plazos Legales y Plantillas de Respuesta Formal para Derechos PII (ARCO / DSAR)

Este documento constituye la guía de referencia regulatoria y documental para la skill `pii-rights-manager` conforme a **ISO/IEC 27701:2025 (A.1.3, A.1.3.6, A.1.3.7, A.1.3.8, A.1.3.9, A.1.3.10, A.2.3.2)**.

---

## 1. Matriz Comparativa de Plazos por Jurisdicción

| Jurisdicción / Ley | Ámbito Territorial | Derecho Ejercido | Plazo Ordinario de Respuesta | Plazo de Prórroga Máxima | Cómputo de Días | Notificación de Prórroga |
|---|---|---|---|---|---|---|
| **RGPD / GDPR** (Reglamento UE 2016/679, Art. 12) | Unión Europea / EEE | Acceso, Rectificación, Supresión, Limitación, Oposición, Portabilidad | **1 mes** (fecha a fecha) | **+2 meses** (máximo 3 meses totales) | Días naturales / Mes calendario | Obligatoria dentro del 1.er mes, motivando complejidad o volumen. |
| **CCPA / CPRA** (Cal. Civ. Code § 1798.130) | California, EE.UU. | Right to Know (Acceso), Delete, Correct, Opt-out | **45 días** | **+45 días** (máximo 90 días totales) | Días naturales | Obligatoria dentro de los primeros 45 días con explicación de causa. |
| **LGPD** (Lei 13.709/2018, Art. 19) | Brasil | Acceso simplificado<br>Acceso completo / Demás derechos | **Inmediato** (simplificado)<br>**15 días** (declaración completa) | Sin previsión expresa de prórroga ordinaria | Días naturales (corridos) | Debe justificarse ante la ANPD cualquier retraso por complejidad. |
| **LFPDPPP** (Ley Federal de México, Art. 32) | México | Acceso, Rectificación, Cancelación (Supresión), Oposición | **20 días** para emitir resolución de procedencia | **+20 días** prórroga de resolución | Días hábiles | Dentro de los primeros 20 días hábiles. Si procede, **15 días hábiles** adicionales para hacerla efectiva (+15 prorrogable). |
| **Ley 1581 / Dcto 1377** (Arts. 14 y 15) | Colombia | **Consultas** (Acceso a datos)<br>**Reclamos** (Rectificación, Supresión) | **10 días** (Consultas)<br>**15 días** (Reclamos) | **+5 días** (Consultas)<br>**+8 días** (Reclamos) | Días hábiles | Obligatoria antes del vencimiento inicial, expresando motivos y nueva fecha. |
| **Ley 29733 / D.S. 003-2013-JUS** (Arts. 55-58) | Perú | **Acceso / Información**<br>**Rectificación, Supresión, Oposición** | **20 días** (Acceso)<br>**10 días** (Rectificación, Supresión, Oposición) | **+20 días** (Acceso)<br>**+10 días** (Demás derechos) | Días hábiles | Notificación motivada al titular antes de vencer el plazo ordinario. |
| **Ley 25.326** (Arts. 14 y 16) | Argentina | **Información / Acceso**<br>**Rectificación, Actualización, Supresión** | **10 días** (Acceso)<br>**5 días** (Rectificación / Supresión) | Sin prórroga ordinaria legal automática | Días corridos (Acceso)<br>Días hábiles (Rectificación / Supresión) | Cualquier retardo habilita de inmediato la acción judicial de *Habeas Data*. |
| **Ley 19.628** (Chile - Régimen General) | Chile | Modificación, Cancelación, Bloqueo | **2 días** (régimen vigente formal)<br>*15 días hábiles* (estándar en proyecto de ley modernizado) | Prórroga sujeta a justificación judicial | Días hábiles | Notificación formal requerida. |

---

## 2. Reglas Jurídicas y Criterios Operativos de Cómputo

### 2.1 Cómputo de Días Naturales vs Días Hábiles
1. **Días Naturales / Calendario (RGPD, CCPA, LGPD, Argentina Acceso)**:
   - Se computan todos los días de la semana, incluyendo sábados, domingos y días feriados.
   - Si el día de vencimiento coincide con un sábado, domingo o día inhábil en la jurisdicción del responsable, el plazo expira el siguiente día hábil disponible.
   - En cómputo por meses (RGPD): expira el mismo día numérico del mes siguiente. Si el mes de vencimiento carece de dicho día (ej. recepción 31 de enero en año no bisiesto), vence el último día de dicho mes (28 de febrero).
2. **Días Hábiles (México, Colombia, Perú, Argentina Rectificación)**:
   - Se excluyen del cómputo los sábados, los domingos y los días festivos oficiales reconocidos por el calendario laboral local de la sede u operación.

### 2.2 Requisitos Sustantivos para Aplicar Prórrogas Legales
Toda prórroga legal exige estricta justificación formal. Constituyen causales legítimas:
- **Volumen inusitado de datos solicitados**: El titular requiere el historial íntegro de interacciones de más de 5 años disperso en sistemas heredados.
- **Complejidad técnica de desvinculación**: Necesidad de anonimizar registros cruzados que contienen datos de terceras personas físicas que no pueden ser revelados.
- **Dispersión geográfica o arquitectónica**: Los datos están alojados en múltiples sistemas descentralizados o involucran encargados internacionales en diferentes husos horarios.

> [!WARNING]
> La falta de personal interno, las vacaciones del responsable de seguridad o la acumulación ordinaria de trabajo administrativo **NO constituyen causa legítima de prórroga** ante las autoridades de protección de datos (AEPD, INAI, SIC, ANPD, etc.).

---

## 3. Protocolo de Bloqueo Lógico de PII (*Data Freezing*)

Cuando un titular solicita la **supresión** de sus datos pero la organización está legalmente obligada a conservarlos (ej. obligaciones tributarias durante 5 años, prevención de blanqueo de capitales durante 10 años, o posibles responsabilidades civiles/laborales):

1. **Aislamiento Funcional**: Desactivar el registro de las bases de datos transaccionales, CRMs y plataformas operativas cotidianas.
2. **Restricción de Acceso (Bloqueo)**: La información permanece cifrada y custodiada exclusivamente por el Oficial de Protección de Datos (DPO) o el área jurídica.
3. **Prohibición de Uso**: Queda terminantemente prohibido utilizar los datos bloqueados para fines comerciales, estadísticos, analíticos o perfilado.
4. **Destrucción Definitiva**: Al prescribir las obligaciones legales de retención, los datos deben ser purgados físicamente de forma automática o mediante borrado criptográfico según los estándares de descarte seguro.

---

## 4. Plantillas de Respuesta Formal Estructurada

A continuación se disponen las plantillas maestras normalizadas para la emisión de comunicaciones formales a los titulares de datos y terceros receptores.

---

### Plantilla 1: Acuse de Recibo y Verificación Proporcional de Identidad
*Uso: Enviar dentro de las 48 horas siguientes a la recepción de una solicitud de derechos no autenticada previamente.*

```markdown
ASUNTO: Acuse de recibo de solicitud de derechos de protección de datos personales - Ref: [REQUEST_ID]

Estimado/a [NOMBRE_DEL_TITULAR]:

Acusamos formalmente recibo de su solicitud recibida con fecha [FECHA_RECEPCIÓN_UTC], mediante la cual ejerce el derecho de [TIPO_DE_DERECHO: Acceso / Rectificación / Supresión / Oposición / Limitación / Portabilidad] respecto de sus datos personales tratados por [NOMBRE_ORGANIZACIÓN].

Su solicitud ha sido registrada en nuestro sistema bajo el número de expediente: [REQUEST_ID].

Para dar curso a su petición y salvaguardar la confidencialidad de su información frente a posibles accesos no autorizados por parte de terceros (Control ISO/IEC 27701:2025 A.1.3.10), requerimos confirmar su identidad de manera proporcional:

[OPCIÓN A - Confirmación por código OTP/Token]:
Le solicitamos ingresar al siguiente enlace seguro [ENLACE_SEGURO_OTP] e introducir el código temporal de un solo uso que le hemos enviado vía SMS/Email al número/correo previamente registrado en su cuenta.

[OPCIÓN B - Duda razonable no autenticable por medios automáticos]:
Le solicitamos responder a este correo aportando copia digitalizada de un documento de identidad oficial, pudiendo tachar o enmascarar datos no estrictamente necesarios para su identificación (fotografía, firma o datos no requeridos).

Le informamos que el cómputo del plazo legal de resolución de [PLAZO_ORDINARIO_DIAS] días comenzará a contar a partir de la confirmación efectiva de su identidad.

Atentamente,

Oficina de Protección de Datos Personales / Delegado de Protección de Datos (DPO)
[NOMBRE_ORGANIZACIÓN]
Correo: [CORREO_DPO]
```

---

### Plantilla 2: Resolución Favorable de Acceso y Portabilidad de Datos
*Uso: Entrega estructurada de información personal al titular (A.1.3.7 y A.1.3.9).*

```markdown
ASUNTO: Resolución favorable a su solicitud de [ACCESO / PORTABILIDAD] - Ref: [REQUEST_ID]

Estimado/a [NOMBRE_DEL_TITULAR]:

En respuesta a su solicitud de fecha [FECHA_RECEPCIÓN], una vez verificada su identidad conforme a ley y concluido el análisis técnico de nuestros repositorios de información, le informamos que su solicitud ha sido ESTIMADA FAVORABLEMENTE.

1. Detalle del Tratamiento (Control ISO 27701 A.1.3.7):
- Categorías de datos personales tratados: [LISTADO_CATEGORIAS: identificativos, transaccionales, de contacto, etc.].
- Finalidades específicas del tratamiento: [DESCRIPCIÓN_FINALIDADES].
- Base jurídica legitimadora: [EJ. Ejecución contractual / Obligación legal / Consentimiento].
- Destinatarios o categorías de terceros a quienes se han comunicado sus datos: [LISTA_TERCEROS_O_ENCARGADOS].
- Plazo de conservación previsto: [PLAZO_RETENCION].

2. Entrega Segura de Copia / Portabilidad (Control ISO 27701 A.1.3.9):
Hemos preparado la copia estructurada de sus datos personales en formato abierto e interoperable (JSON y CSV). Por motivos de estricta seguridad de la información, el paquete cifrado se encuentra disponible para su descarga en la siguiente ubicación protegida:

- Enlace de descarga segura: [URL_DESCARGA_CIFRADA]
- Caducidad del enlace: [FECHA_EXPIRACION - Máximo 7 días corridos]
- Clave de descifrado / Verificación: Se ha remitido por canal seguro alternativo a su teléfono móvil registrado.

Si considera que la presente resolución vulnera sus derechos, le asiste la facultad de interponer reclamación ante la Autoridad de Control competente: [NOMBRE_AUTORIDAD_CONTROL, ej. AEPD, INAI, SIC], sin perjuicio de las acciones judiciales correspondientes.

Atentamente,

Oficina de Protección de Datos Personales
[NOMBRE_ORGANIZACIÓN]
```

---

### Plantilla 3: Resolución Favorable de Rectificación de Datos
*Uso: Notificar la corrección o actualización de PII inexacta (A.1.3.7 y A.1.3.8).*

```markdown
ASUNTO: Resolución favorable de Rectificación de Datos Personales - Ref: [REQUEST_ID]

Estimado/a [NOMBRE_DEL_TITULAR]:

Le comunicamos que su solicitud de rectificación de datos personales de fecha [FECHA_RECEPCIÓN] ha sido ESTIMADA y ejecutada exitosamente en todos nuestros sistemas de producción y gestión.

Detalle de los cambios efectuados:
| Campo / Dato Personal | Valor Anterior (Anonimizado) | Nuevo Valor Rectificado |
|---|---|---|
| [CAMPO_1, ej. Apellido] | [VALOR_ANTERIOR] | [NUEVO_VALOR] |
| [CAMPO_2, ej. Dirección Postal] | [VALOR_ANTERIOR] | [NUEVO_VALOR] |

Asimismo, en estricto cumplimiento del control **A.1.3.8 de ISO/IEC 27701:2025**, le confirmamos que hemos cursado notificación formal a todos los terceros cesionarios y encargados del tratamiento a quienes se hubiese comunicado dicha información, instruyéndoles a actualizar sus bases de datos sin dilación.

Quedamos a su disposición para cualquier aclaración y le recordamos su derecho a recurrir ante [NOMBRE_AUTORIDAD_CONTROL] en caso de disconformidad.

Atentamente,

Oficina de Protección de Datos Personales
[NOMBRE_ORGANIZACIÓN]
```

---

### Plantilla 4: Resolución Favorable de Supresión / Supresión con Bloqueo
*Uso: Atender solicitudes de cancelación/olvido y explicar bloqueo por obligaciones de retención (A.1.3.7).*

```markdown
ASUNTO: Resolución de Supresión de Datos Personales - Ref: [REQUEST_ID]

Estimado/a [NOMBRE_DEL_TITULAR]:

Nos dirigimos a usted en relación con su solicitud de supresión de datos personales radicada bajo el número [REQUEST_ID]. Cumplimos con informarle que su solicitud ha sido RESUELTA de la siguiente manera:

1. Supresión Efectiva:
Se ha procedido a la eliminación irreversible y desindexación de sus datos personales en nuestros sistemas de producción comercial, listas de distribución, perfiles analíticos y herramientas de mercadotecnia.

2. Bloqueo Legal de Información (Control A.1.3.7 / Normativa Aplicable):
[INCLUIR SI APLICA OBLIGACIÓN LEGAL]:
Le informamos que determinados datos vinculados a sus transacciones contractuales e historial contable no pueden ser destruidos materialmente en este momento, en virtud de la obligación legal de conservación establecida en [NORMA_APLICABLE: ej. Código Tributario / Ley Antilavado].
Dichos datos han sido sometidos a un **bloqueo estricto e irreversible para fines operativos**, permaneciendo bajo custodia criptográfica exclusiva de nuestro departamento legal para atender eventuales responsabilidades legales o requerimientos de autoridades judiciales durante un periodo de [AÑOS_BLOQUEO] años, tras el cual se procederá a su destrucción física definitiva.

3. Notificación a Terceros (Control A.1.3.8):
Se ha ordenado la supresión correspondiente a todos los encargados de tratamiento y plataformas externas que procesaban sus datos en nuestro nombre.

Atentamente,

Oficina de Protección de Datos Personales
[NOMBRE_ORGANIZACIÓN]
```

---

### Plantilla 5: Notificación Formal de Prórroga por Complejidad Excepcional
*Uso: Notificar ampliación justificada del plazo legal ANTES del vencimiento original.*

```markdown
ASUNTO: Notificación formal de prórroga para la atención de solicitud - Ref: [REQUEST_ID]

Estimado/a [NOMBRE_DEL_TITULAR]:

Nos ponemos en comunicación con usted en relación con su solicitud de [TIPO_DE_DERECHO] recibida el día [FECHA_RECEPCIÓN].

Conforme a lo previsto en la normativa aplicable en materia de protección de datos personales ([NORMATIVA: ej. Artículo 12.3 del RGPD / Art. 32 LFPDPPP]), le informamos que nos vemos en la necesidad justificada de ampliar el plazo de respuesta en [DÍAS_PRORROGA] días adicionales, fijándose como nueva fecha límite de resolución el día [NUEVA_FECHA_LIMITE].

Motivación de la Prórroga (Requisito Control ISO 27701 A.1.3.7 / A.1.3.10):
La ampliación obedece a la complejidad técnica y volumen de la solicitud, motivada específicamente por:
- [DETALLAR CAUSA REAL: ej. Necesidad de extraer y desidentificar información personal contenida en soportes archivísticos históricos / dispersión de registros en múltiples sistemas encargados en el exterior].

Le recordamos que puede presentar cualquier consulta sobre el estado de su expediente contactando directamente a nuestro Delegado de Protección de Datos en [CORREO_DPO], así como reclamar ante la autoridad de supervisión [NOMBRE_AUTORIDAD_CONTROL].

Atentamente,

Delegado de Protección de Datos / Dirección de Privacidad
[NOMBRE_ORGANIZACIÓN]
```

---

### Plantilla 6: Resolución de Desestimación o Rechazo Motivado
*Uso: Rechazo legalmente fundado cuando la solicitud no es procedente (A.1.3.7 / A.1.3.10).*

```markdown
ASUNTO: Notificación de resolución desestimatoria de solicitud - Ref: [REQUEST_ID]

Estimado/a [NOMBRE_DEL_TITULAR]:

En respuesta a su solicitud de [TIPO_DE_DERECHO] con número de registro [REQUEST_ID], tras una rigurosa evaluación jurídica efectuada por nuestra Asesoría Legal y el Oficial de Protección de Datos, cumplimos con notificarle que su petición NO HA PODIDO SER ESTIMADA [TOTAL / PARCIALMENTE].

Fundamentos de Hecho y de Derecho de la Desestimación:
1. Base Fáctica: [DESCRIPCIÓN DETALLADA DE LA SITUACIÓN, ej. El solicitante exige la supresión de sus registros crediticios mientras mantiene un saldo deudor vencido e impagado en cobro judicial].
2. Fundamentación Jurídica (Control ISO 27701 A.1.3.7 y [ARTÍCULO_LEY]):
   - [CITAR PRECEPTO LEGAL: ej. El derecho de supresión no es aplicable cuando el tratamiento sea necesario para el ejercicio o la defensa de reclamaciones judiciales o el cumplimiento de un deber legal según el Art. 17.3 del RGPD].

Vías de Reclamación y Tutela Jurídica:
Le informamos expresamente de que si se encuentra disconforme con los fundamentos de esta resolución, tiene derecho a interponer una reclamación de tutela de derechos ante la Autoridad de Control de Protección de Datos:
- Organismo: [NOMBRE_AUTORIDAD_CONTROL, ej. Agencia Española de Protección de Datos (AEPD) / INAI / SIC]
- Sede electrónica: [URL_SEDE_ELECTRONICA]
- Plazo para interponer recurso: [PLAZO_RECURSO, ej. 1 mes].

Atentamente,

Oficina de Protección de Datos Personales
[NOMBRE_ORGANIZACIÓN]
```

---

### Plantilla 7: Notificación en Cascada a Terceros Receptores y Subencargados
*Uso: Comunicación obligatoria a proveedores y cesionarios bajo el Control A.1.3.8.*

```markdown
COMUNICACIÓN FORMAL DE CASCADA DE DERECHOS PII (ISO/IEC 27701:2025 CONTROL A.1.3.8)

DE: [NOMBRE_ORGANIZACIÓN_RESPONSABLE] (PII Controller)
PARA: [NOMBRE_EMPRESA_ENCARGADA_O_TERCERO] (PII Processor / Third Party)
ATENCIÓN: Responsable de Seguridad / Delegado de Protección de Datos
FECHA: [FECHA_EMISION_UTC]
EXPEDIENTE: [REQUEST_ID]

Estimados señores:

En cumplimiento de las obligaciones estipuladas en el Acuerdo de Procesamiento de Datos (DPA) vigente y del control normativo **A.1.3.8 de ISO/IEC 27701:2025**, les notificamos que el titular cuyos identificadores se detallan a continuación ha ejercido legítimamente su derecho de [SUPRESIÓN / RECTIFICACIÓN / OPOSICIÓN]:

- Identificador de Usuario en su Plataforma: [ID_EXTERNO / EMAIL_HASH]
- Tipo de Instrucción: [ELIMINACIÓN DEFINITIVA / MODIFICACIÓN DE DATO / CESE DE MARKETING]
- Detalle de la modificación (si aplica): [CAMPO_RECTIFICADO: NUEVO_VALOR]
- Plazo límite para ejecución en sus sistemas: [HORAS_O_DIAS, ej. 72 horas hábiles].

Requerimientos Mandatorios:
1. Proceder a la inmediata supresión, actualización o bloqueo de cualquier registro personal vinculado a este titular en sus bases de datos activas y réplicas.
2. Si han transferido estos datos a ulteriores subencargados (sub-processors), están obligados a trasladar idéntica instrucción en cascada.
3. Remitir acuse de recibo técnico o confirmación fehaciente de la ejecución a la dirección [CORREO_DPO] dentro del plazo estipulado.

Atentamente,

Oficina de Privacidad y Cumplimiento Normativo
[NOMBRE_ORGANIZACIÓN_RESPONSABLE]
```
