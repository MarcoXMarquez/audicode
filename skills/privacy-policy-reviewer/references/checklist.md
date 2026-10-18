# Lista Exhaustiva de Verificación de Políticas y Avisos de Privacidad (ISO/IEC 27701:2025)

Este documento contiene la lista técnica de verificación para auditar la conformidad documental respecto a los controles de **ISO/IEC 27701:2025**:
- **Cláusula 5.2**: Política de privacidad del SGIP / PIMS (*Privacy policy*).
- **Control A.3.3**: Políticas para la seguridad de la información vinculadas a PII (*Policies for information security*).
- **Control A.1.3.3**: Determinación de la información para los titulares (*Determining information for PII principals*).
- **Control A.1.3.4**: Suministro de información a los titulares (*Providing information to PII principals*).

---

## 1. Verificación de la Política Interna del SGIP / PIMS (Cláusula 5.2 y A.3.3)

La política de privacidad interna es la directriz estratégica aprobada por la Alta Dirección para gobernar el tratamiento de datos personales en toda la organización.

| ID | Elemento Auditado | Requisito Mandatorio ISO/IEC 27701:2025 | Criterio de Conformidad | Evidencia Requerida | Severidad si Omite |
|---|---|---|---|---|---|
| **POL-01** | **Alineación con el Propósito** | Cláusula 5.2 a) | La política debe adaptarse expresamente a la naturaleza, escala, volumen de datos y modelo de negocio de la organización. | Sección introductoria con alcance y justificación operativa del negocio. | Mayor |
| **POL-02** | **Marco para Objetivos de Privacidad** | Cláusula 5.2 b) / Cl. 6.2 | Debe establecer las directrices y prioridades a partir de las cuales se definen las metas anuales y métricas del SGIP. | Vínculo explícito con los objetivos anuales de privacidad y KPIs de gestión. | Mayor |
| **POL-03** | **Compromiso de Cumplimiento Legal** | Cláusula 5.2 c) | Declaración formal e inequívoca de acatamiento de la legislación aplicable en materia de protección de datos (RGPD, leyes locales, contratos). | Cláusula de sometimiento normativo identificando marcos legales vigentes. | Crítica |
| **POL-04** | **Compromiso de Mejora Continua** | Cláusula 5.2 d) / Cl. 10.2 | Compromiso explícito de la dirección de perfeccionar la eficacia y conveniencia del SGIP de manera sistemática. | Compromiso formal de asignación de recursos y revisiones periódicas. | Mayor |
| **POL-05** | **Información Documentada y Aprobación** | Cláusula 5.2 e) / Cl. 7.5 | La política debe existir como información documentada formal, con código, control de versiones y firma de la Alta Dirección. | Metadatos de documento: fecha de vigencia, versión, firma de CEO / Comité de Dirección. | Crítica |
| **POL-06** | **Comunicación y Comprensión Interna** | Cláusula 5.2 f) / Cl. 7.3 | La política debe ser difundida activamente a todo el personal relevante y ser comprensible para sus funciones. | Registros de inducción, acuses de recibo firmados en intranet o evaluaciones de concienciación. | Mayor |
| **POL-07** | **Disponibilidad para Partes Interesadas** | Cláusula 5.2 g) | La política debe estar disponible, en versión pertinente, para autoridades, socios, clientes o titulares que la requieran. | Publicación en intranet o canal corporativo oficial para partes interesadas. | Menor |
| **POL-08** | **Integración de Políticas de Seguridad (A.3.3)** | Control A.3.3 / B.3.3 | Las políticas temáticas de seguridad deben incluir directrices expresas para salvaguardar PII (cifrado, copias, accesos, etc.). | Catálogo de políticas temáticas con cláusulas explícitas sobre datos personales. | Mayor |
| **POL-09** | **Periodicidad de Revisión** | Cláusula 5.2 / Cl. 9.3 | Mecanismo documentado para revisar la política al menos una vez al año o tras cambios normativos / tecnológicos relevantes. | Historial de versiones y actas de revisión por la dirección (*management review*). | Menor |

---

## 2. Verificación del Aviso de Privacidad para Titulares (A.1.3.3 y A.1.3.4)

El aviso de privacidad (*Privacy Notice*) es el instrumento público dirigido a los titulares (*PII principals*) para garantizar el principio de transparencia, lealtad y licitud.

### 2.1 Contenido Informativo Mandatorio (A.1.3.3)

| ID | Elemento Informativo | Requisito Mandatorio A.1.3.3 | Criterio de Conformidad | Severidad si Omite |
|---|---|---|---|---|
| **NOT-01** | **Identidad del Responsable** | A.1.3.3 a) | Razón social completa, CIF/NIF/RFC o identificador fiscal, y domicilio físico legal del Responsable (*PII Controller*). | Crítica |
| **NOT-02** | **Contacto del Responsable y DPO** | A.1.3.3 b) | Canales directos de contacto (correo electrónico específico, teléfono, buzón) y datos del Delegado de Protección de Datos (DPO) si aplica. | Mayor |
| **NOT-03** | **Finalidades del Tratamiento** | A.1.3.3 c) / A.1.2.2 | Finalidades explícitas, precisas y comprensibles. Prohibidas fórmulas ambiguas como *"para mejorar la experiencia"* sin mayor detalle. | Crítica |
| **NOT-04** | **Base Legal del Tratamiento** | A.1.3.3 d) / A.1.2.3 | Base jurídica aplicable a cada finalidad (consentimiento, contrato, obligación legal, interés legítimo con prueba de ponderación disponible). | Crítica |
| **NOT-05** | **Categorías de Datos Tratados** | A.1.3.3 e) | Desglose de los datos recopilados (identificativos, económicos, ubicación, navegación, datos biométricos o sensibles si procede). | Mayor |
| **NOT-06** | **Origen de los Datos (si es indirecto)** | A.1.3.3 f) | En caso de obtención no directa del titular, especificar fuentes legítimas, registros públicos o proveedores de datos. | Mayor |
| **NOT-07** | **Consecuencias de no Proporcionar Datos** | A.1.3.3 g) | Indicar claramente si la provisión de datos es obligatoria (legal/contractual) y las consecuencias prácticas de no facilitarlos. | Menor |
| **NOT-08** | **Destinatarios y Cesiones a Terceros** | A.1.3.3 h) | Identificación específica o por categorías claras de los encargados, proveedores de servicios y terceros cesionarios. | Crítica |
| **NOT-09** | **Transferencias Internacionales** | A.1.3.3 i) / A.1.5.2 / A.1.5.3 | Declarar si hay flujos transfronterizos, países de destino y la garantía legal invocada (Decisión de Adecuación, SCC, BCR). | Crítica |
| **NOT-10** | **Plazos de Conservación** | A.1.3.3 j) / A.1.4.8 | Periodos numéricos de retención o criterios objetivos determinables para el borrado/bloqueo de datos. | Mayor |
| **NOT-11** | **Catálogo de Derechos ARCO/DSAR** | A.1.3.3 k) / A.1.3.7 | Mención expresa de los derechos: Acceso, Rectificación, Supresión/Cancelación, Oposición, Limitación y Portabilidad. | Crítica |
| **NOT-12** | **Canal Gratuito de Ejercicio de Derechos** | A.1.3.3 k) / A.1.3.10 | Canal específico, ágil y sin costos indebidos para ejercitar derechos (correo, portal web, formulario). | Crítica |
| **NOT-13** | **Revocación del Consentimiento** | A.1.3.3 l) / A.1.3.5 | Derecho a retirar el consentimiento en cualquier momento con la misma facilidad con que fue otorgado. | Mayor |
| **NOT-14** | **Decisiones Automatizadas y Perfilado** | A.1.3.3 m) / A.1.3.11 | Información sobre la existencia de algoritmos o perfilado con consecuencias jurídicas o significativas, y la lógica aplicada. | Mayor |
| **NOT-15** | **Derecho de Reclamación ante Autoridad** | A.1.3.3 n) | Nombre y enlace o vía de contacto de la Autoridad de Control competente (AEPD, INAI, ANPD, etc.). | Mayor |
| **NOT-16** | **Mecanismo de Notificación de Cambios** | A.1.3.3 / A.1.3.4 | Procedimiento transparente para advertir al titular sobre modificaciones sustanciales al aviso de privacidad. | Menor |

---

### 2.2 Suministro de Información y Principio de Transparencia (A.1.3.4)

| ID | Aspecto Evaluado | Requisito Mandatorio A.1.3.4 | Criterio de Verificación | Severidad si Omite |
|---|---|---|---|---|
| **TRA-01** | **Lenguaje Claro y Comprensible** | A.1.3.4 a) | Redacción en lenguaje llano, evitando jerga jurídica oscura o cláusulas abusivas de renuncia de derechos. | Mayor |
| **TRA-02** | **Arquitectura por Capas (*Layered Notice*)** | A.1.3.4 b) | Estructura en al menos dos capas: 1ª capa informativa básica (resumen / tabla clave) y 2ª capa con el texto legal completo. | Oportunidad / Mayor |
| **TRA-03** | **Oportunidad Temporal (*Timing*)** | A.1.3.4 c) | Presentación previa o simultánea a la recolección de los datos (*just-in-time notification* en formularios). | Crítica |
| **TRA-04** | **Disponibilidad Permanente** | A.1.3.4 d) | Enlace permanente, visible y funcional en pie de página (*footer*), ajustes de perfil de usuario o menú principal. | Mayor |
| **TRA-05** | **Accesibilidad Universal** | A.1.3.4 e) | Cumplimiento de estándares de accesibilidad web (contraste, texto escalable, compatibilidad con lectores de pantalla). | Menor |
| **TRA-06** | **Adaptación a Colectivos Específicos** | A.1.3.4 f) | Si el servicio trata datos de menores o personas vulnerables, el lenguaje debe ser especialmente didáctico y adaptado. | Mayor |

---

## 3. Estructura Recomendada para Avisos por Capas

### Capa 1: Información Básica Resumida (Visible en formulario o banner)

| Elemento Clave | Contenido Síntesis Requerido |
|---|---|
| **Responsable** | [Razón Social o Nombre Comercial y CIF/NIF] |
| **Finalidad Principal** | [Finalidad principal del servicio en 1 o 2 líneas] |
| **Legitimación** | [Consentimiento / Ejecución contractual / Interés legítimo] |
| **Destinatarios** | [No se ceden salvo obligación legal / Proveedores tecnológicos bajo encargo] |
| **Transferencias** | [Indicar si existen y país, ej: "Servidores en EE.UU. bajo CCT / Adecuación"] |
| **Derechos** | [Acceder, rectificar y suprimir los datos, así como otros derechos en: privacidad@empresa.com] |
| **Información Adicional** | [Enlace directo e hipervinculado a la Política de Privacidad Completa (Capa 2)] |

### Capa 2: Información Detallada y Completa (Documento Integral)
Contiene las 16 secciones detalladas en el apartado 2.1, redactadas con desglose exhaustivo, identificación de proveedores, plazos de prescripción y tablas explicativas.

---

## 4. Matriz de Severidad de Hallazgos

| Nivel de Severidad | Criterio de Clasificación | Ejemplo Típico en Auditoría | Plazo Típico de Subsanación |
|---|---|---|---|
| **Crítica** | Omisión de requisitos estructurales obligatorios que invalidan legalmente la transparencia o exponen a sanciones directas de las autoridades. | Ausencia total de base legal, omisión de canales de derechos ARCO, falta de aprobación directiva de la política PIMS, o ausencia de aviso previo a la recolección. | Inmediato (< 5 días laborables) |
| **Mayor** | Incumplimientos que distorsionan significativamente la transparencia o generan ambigüedad grave sobre el destino o protección de los datos. | No especificar plazos de retención, omitir datos de contacto del DPO, no identificar países de transferencias internacionales, o lenguaje excesivamente ambiguo. | Corto plazo (< 15 días laborables) |
| **Menor** | Deficiencias formales o de detalle que no anulan el entendimiento fundamental de los derechos ni violan de forma directa el núcleo del control. | No indicar el carácter voluntario de datos opcionales, falta de fecha de última actualización del documento, ausencia de enlace a la web de la autoridad. | Medio plazo (< 30 días laborables) |
| **Oportunidad de Mejora** | Buenas prácticas técnicas o de diseño que optimizan la usabilidad, experiencia del usuario o comprensión sin existir infracción formal. | Incorporar iconografía estandarizada en la primera capa, mejorar el contraste tipográfico, o añadir un glosario de términos de privacidad. | Planificado en ciclo ordinario |

---

## 5. Particularidades y Variaciones Jurisdiccionales

- **RGPD (Unión Europea, Arts. 13 y 14)**:
  - Exige explicitar el interés legítimo invocado y el juicio de ponderación realizado.
  - Exige detallar la existencia de decisiones automatizadas, incluida la elaboración de perfiles, y ofrecer información significativa sobre la lógica aplicada.
  - La indicación de la autoridad de control y el derecho a reclamar es imperativa.
- **LGPD (Brasil, Art. 9)**:
  - Exige destacar de manera explícita si los datos serán objeto de tratamiento compartido y las responsabilidades recíprocas.
  - Mención formal al Encargado de Datos (*DPO / Encarregado*).
- **CCPA / CPRA (California, EE.UU.)**:
  - Exige el *Notice at Collection* previo o simultáneo.
  - Exige declarar expresamente si se "venden" (*Sell*) o "comparten" (*Share* para publicidad de comportamiento cruzado) los datos personales, y suministrar el enlace *"Do Not Sell or Share My Personal Information"*.
  - Desglose de categorías de datos sensibles (*Sensitive Personal Information*).
- **Leyes de Protección de Datos de América Latina (México, Colombia, Argentina, Chile, Perú)**:
  - Requisito de consentimiento expreso para datos sensibles, patrimoniales o financieros.
  - Explicitar si los datos se transferirán a terceros nacionales o extranjeros y recabar consentimiento específico cuando la ley no lo exceptúe.
