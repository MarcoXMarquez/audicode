# Guía Normativa de Mecanismos de Transferencia Internacional y TIA (ISO/IEC 27701:2025)

- **Documento de Referencia Técnica y Jurídica**
- **Skill Asociada**: `pii-transfer-auditor`
- **Controles Normativos**: ISO/IEC 27701:2025 Cláusula A.1.5 (A.1.5.2, A.1.5.3, A.1.5.4, A.1.5.5), Cláusula A.2.5 (A.2.5.2, A.2.5.3, A.2.5.5, A.2.5.6) y Cláusula A.3.7 (*Information transfer*).
- **Equivalencias ISO/IEC 27701:2019**: Cláusula 7.5 (7.5.1, 7.5.2, 7.5.3, 7.5.4), Cláusula 8.5 (8.5.1, 8.5.4, 8.5.5) y Cláusula 6.10.1.

---

## 1. Fundamentos y Taxonomía de las Transferencias Transfronterizas

### 1.1 Definición Operativa de Transferencia Internacional
Bajo ISO/IEC 27701:2025 (control A.1.5.2), existe una transferencia internacional o transfronteriza de datos personales cuando concurren tres elementos constitutivos:
1. **Sujeto Exportador**: Un responsable o encargado sujeto a una jurisdicción de origen transmite, hace accesible o pone a disposición datos personales.
2. **Sujeto Importador**: Una entidad jurídica diferenciada (responsable, encargado o subencargado) se encuentra ubicada físicamente o bajo la soberanía normativa de una jurisdicción distinta.
3. **Flujo de PII**: El movimiento de información incluye cualquier operación de procesamiento, alojamiento en reposo (*data at rest*), tránsito (*data in transit*) o **acceso remoto de soporte y visualización** (*data in use / remote access*).

> [!IMPORTANT]
> El acceso remoto de administradores de sistemas, ingenieros de soporte o centros de operaciones de seguridad (SOC) ubicados en terceros países constituye legal y técnicamente una **transferencia internacional completa**, aun cuando los servidores principales permanezcan físicamente en el territorio de origen.

### 1.2 Jerarquía Normativa de Mecanismos de Habilitación
Para que una transferencia sea lícita bajo el control A.1.5.2, debe sustentarse en alguno de los siguientes escalones jerárquicos:

```
[Escalón 1: Decisión de Adecuación Territorial / Sectorial]
       │  (Nivel de protección equivalente reconocido oficialmente)
       ▼
[Escalón 2: Garantías Adecuadas Contractuales o Institucionales]
       │  (Cláusulas Contractuales Tipo - SCC / Normas Corporativas Vinculantes - BCR)
       ▼
[Escalón 3: Evaluación de Impacto de la Transferencia - TIA + Medidas Suplementarias]
       │  (Análisis obligatorio post-Schrems II de leyes de vigilancia en país destino)
       ▼
[Escalón 4: Excepciones Tasadas para Situaciones Específicas / Derogaciones]
          (Solo supuestos aislados, estrictos y no recurrentes)
```

---

## 2. Catálogo Oficial de Países con Nivel Adecuado de Protección

Las decisiones de adecuación declaran que un tercer país u organización internacional ofrece un nivel de protección sustancialmente equivalente al exigido por el régimen de privacidad de origen. Cuando opera una decisión de adecuación, **no se requieren autorizaciones específicas adicionales ni garantías contractuales especiales** (salvo el cumplimiento ordinario del contrato de encargo y del deber de transparencia de A.1.5.3).

| País / Territorio | Ámbito de Cobertura de la Adecuación | Limitaciones / Condiciones de Validez |
|---|---|---|
| **Andorra** | Pleno (Sector público y privado). | Marco legal integral homologado. |
| **Argentina** | Pleno (Ley 25.326 y disposiciones de la AAIP). | Tratamiento general de datos. |
| **Canadá** | **Parcial / Comercial**: Entidades cubiertas por PIPEDA (*Personal Information Protection and Electronic Documents Act*). | No cubre organismos del sector público ni relaciones laborales provinciales no reguladas por leyes federales. |
| **Islas Feroe** | Pleno. | Territorio dependiente con legislación armonizada. |
| **Guernesey** | Pleno (Bailiwick of Guernsey). | Legislación de protección de datos de las Islas del Canal. |
| **Isla de Man** | Pleno. | Ordenanzas locales homologadas. |
| **Israel** | **Parcial**: Datos tratados en bases automatizadas conforme a la Ley de Privacidad 5741-1981. | Excluye transferencias manuales no automatizadas. |
| **Japón** | **Comercial**: Datos transferidos a operadores de información empresarial (*APPI*). | Excluye sector público, organizaciones sin fines de lucro y exige reglas suplementarias de transferencias ulteriores (*onward transfers*). |
| **Jersey** | Pleno (Bailiwick of Jersey). | Legislación integral homologada. |
| **Nueva Zelanda** | Pleno (*Privacy Act 2020*). | Sistema de principios de privacidad homologado. |
| **República de Corea** | Pleno (*Personal Information Protection Act* - PIPA). | Cubre sector público y privado con salvaguardas reforzadas para transferencias ulteriores. |
| **Suiza** | Pleno (Nueva Ley Federal de Protección de Datos - nLPD). | Reconocimiento mutuo integral. |
| **Reino Unido** | Pleno (UK GDPR y *Data Protection Act 2018*). | Sujeto a cláusula de extinción (*sunset clause*) y monitoreo continuo por divergencias normativas. |
| **Estados Unidos (EU-US DPF)** | **Condicionado y Restringido**: Exclusivamente entidades comerciales estadounidenses certificadas activas en el *Data Privacy Framework* (DPF). | **NO es una adecuación territorial general**. Si el proveedor estadounidense NO figura en la lista pública activa del DPF (verificada ante el Departamento de Comercio), la transferencia requiere SCC y TIA obligatoria. |
| **Uruguay** | Pleno (Ley 18.331 de Protección de Datos Personales). | Marco normativo integral homologado. |

---

## 3. Cláusulas Contractuales Tipo (Standard Contractual Clauses - SCC)

Cuando el país de destino no cuenta con decisión de adecuación, el instrumento predominante son las **Cláusulas Contractuales Tipo**. En el contexto internacional de ISO/IEC 27701, se toma como referencia de mejores prácticas la Decisión de Ejecución (UE) 2021/914 de la Comisión Europea.

### 3.1 Estructura Modular de las SCC
El auditor debe verificar que el contrato implemente el **módulo correspondiente al rol exacto de las partes**:

1. **Módulo 1: Responsable a Responsable (Controller-to-Controller / C2C)**:
   - Cesión de datos entre dos organizaciones independientes que determinan fines y medios.
   - Exige compromisos directos de transparencia, atención de derechos del interesado y limitación de finalidades por el importador.
2. **Módulo 2: Responsable a Encargado (Controller-to-Processor / C2P)**:
   - Supuesto estándar de contratación de proveedores de nube o servicios tecnológicos foráneos.
   - El importador procesa PII únicamente siguiendo las instrucciones documentadas del exportador.
3. **Módulo 3: Encargado a Subencargado (Processor-to-Processor / P2P)**:
   - Utilizado cuando un encargado contrata a un subcontratista o centro de datos fuera del territorio de origen en nombre del responsable.
   - Exige que el encargado cuente con autorización previa (específica o general) del responsable final.
4. **Módulo 4: Encargado a Responsable (Processor-to-Controller / P2C)**:
   - Casos donde un encargado procesa datos por encargo de un cliente establecido en un tercer país y le devuelve o remite los resultados.

### 3.2 Anexos Técnicos y Obligatorios de las SCC
Unas SCC sin anexos completados de forma circunstanciada carecen de validez probatoria. El auditor debe exigir la acreditación de:
- **Anexo I.A (Identificación de las Partes)**: Nombres, domicilios, personas de contacto, funciones y autoridades de supervisión competentes.
- **Anexo I.B (Descripción de la Transferencia)**:
  * Categorías de titulares de datos afectados (ej. empleados, clientes, prospectos).
  * Categorías de PII transferidas (describir si hay categorías especiales o datos biométricos).
  * Frecuencia de la transferencia (continua, en tiempo real, periódica, puntual).
  * Naturaleza y finalidad del tratamiento.
  * Periodo de conservación previsto.
- **Anexo II (Medidas Técnicas y Organizativas - TOMs)**:
  * Medidas de cifrado en reposo y en tránsito (algoritmos, longitud de claves).
  * Medidas de control de acceso lógico y físico.
  * Protección contra ataques de denegación de servicio e integridad de red.
  * Certificaciones formales del importador (ISO/IEC 27001, ISO/IEC 27701, SOC 2 Tipo II).
- **Anexo III (Lista de Subencargados Autorizados)**:
  * Obligatorio para Módulos 2 y 3. Identifica razón social, ubicación física de servidores y función concreta.

### 3.3 Cláusulas Específicas sobre Acceso de Gobiernos Extranjeros
Bajo la Cláusula 14 y 15 de las SCC modernas (y controles A.2.5.5 y A.2.5.6 de ISO 27701:2025):
- El importador debe comprometerse a **notificar con prontitud al exportador** si recibe una orden legalmente vinculante de una autoridad policial, militar o judicial solicitando la revelación de PII.
- Si la ley extranjera prohíbe notificar al exportador, el importador debe emplear sus mejores esfuerzos para obtener una exención de confidencialidad y publicar anualmente estadísticas agregadas de solicitudes recibidas.
- El importador debe **revisar la legalidad de la solicitud** y oponerse judicialmente si detecta motivos razonables para considerar que la orden excede las competencias de la autoridad requirente.

---

## 4. Normas Corporativas Vinculantes (Binding Corporate Rules - BCR)

Las BCR constituyen el mecanismo preferente para grupos multinacionales o conglomerados empresariales con operaciones en múltiples jurisdicciones.

### 4.1 Tipología y Características
- **BCR para Responsables (BCR-C)**: Regulan las transferencias internas entre filiales y la matriz cuando actúan como responsables del tratamiento.
- **BCR para Encargados (BCR-P)**: Aplican a proveedores corporativos que prestan servicios de procesamiento de datos a clientes externos y subcontratan internamente con filiales globales.

### 4.2 Requisitos Mandatorios para su Validez en Auditoría
1. **Vinculatoriedad Jurídica Exigible**: Deben ser legalmente vinculantes tanto para los miembros del grupo como frente a los titulares de datos personales (cláusulas de tercero beneficiario).
2. **Homologación Previa**: Deben contar con la resolución formal de aprobación emitida por la Autoridad de Protección de Datos líder (*Lead Supervisory Authority*).
3. **Mecanismo de Auditoría y Verificación**: El grupo debe mantener un programa regular de auditorías independientes de privacidad con informe remitido a la alta dirección y a las autoridades.
4. **Responsabilidad Solidaria**: La entidad de cabecera o matriz establecida en la jurisdicción de origen debe aceptar la responsabilidad y la carga de la prueba por cualquier infracción cometida por una filial extranjera.

---

## 5. Excepciones Tasadas para Situaciones Específicas (Derogaciones)

El control A.1.5.2 reconoce supuestos tasados donde, en defecto de decisión de adecuación y de garantías contractuales (SCC/BCR), es admisible transferir PII:

1. **Consentimiento Explícito e Informado**:
   - El titular debe haber sido advertido específicamente de los riesgos particulares que la transferencia entraña debido a la ausencia de decisión de adecuación y de salvaguardas adecuadas.
2. **Ejecución o Formalización de un Contrato**:
   - Cuando la transferencia sea estrictamente necesaria para la ejecución de un contrato entre el titular y el responsable (ej. reserva de hotel internacional a petición del cliente).
3. **Interés Público Importante**:
   - Supuestos formalmente tasados por la ley aplicable (ej. intercambio de datos entre autoridades fiscales o sanitarias en pandemias).
4. **Reclamaciones Judiciales**:
   - Necesidad imperiosa para la formulación, ejercicio o defensa de reclamaciones judiciales o arbitrales.

> [!CAUTION]
> **REGLA DE NO-USO ESTRUCTURAL**: Las excepciones tienen carácter restrictivo. Está terminantemente prohibido utilizar el consentimiento o la necesidad contractual como base legal para transferencias masivas, continuas, recurrentes o estructurales de infraestructura (ej. contratar un ERP o CRM SaaS foráneo amparado en el consentimiento de los empleados o clientes).

---

## 6. Metodología de Evaluación de Impacto de la Transferencia (TIA - Transfer Impact Assessment)

Tras la sentencia *Schrems II* del Tribunal de Justicia de la Unión Europea y la consolidación de los controles A.1.5.2 y A.1.5.3 de ISO/IEC 27701:2025, suscribir formalmente unas SCC **ya no es suficiente por sí mismo**. La organización exportadora debe evaluar si la legislación y la práctica administrativa del país de destino impiden al importador cumplir de facto las obligaciones contractuales.

### 6.1 Flujo Metodológico en 6 Pasos para Auditar una TIA

```
[Paso 1: Mapeo del Flujo y Sensibilidad]
       │  (Volumen, categorías especiales, tránsito de paquetes IP)
       ▼
[Paso 2: Análisis del Marco Jurídico del País Receptor]
       │  (FISA 702, EO 14086, Cloud Act, China PIPL/DSL, India DPDP)
       ▼
[Paso 3: Evaluación de la Práctica de Acceso Gubernamental]
       │  (Probabilidad de requerimientos según el sector económico)
       ▼
[Paso 4: Determinación de Medidas Suplementarias]
       │  (Técnicas, Contractuales, Organizativas)
       ▼
[Paso 5: Dictamen de Viabilidad y Nivel de Riesgo Residual]
       │  (Alto, Medio, Bajo -> Aprobación o Suspensión de la Transferencia)
       ▼
[Paso 6: Monitorización Continua y Reevaluación Periódica]
          (Mínimo cada 12 meses o ante reformas legales en destino)
```

### 6.2 Análisis de Legislaciones de Vigilancia de Mayor Impacto
El auditor debe verificar si la TIA evalúa explícitamente el régimen legal de las siguientes jurisdicciones frecuentes:

- **Estados Unidos**:
  * *FISA Section 702* (*Foreign Intelligence Surveillance Act*): Permite al gobierno interceptar comunicaciones de no ciudadanos estadounidenses a través de proveedores de servicios de comunicaciones electrónicas (*Electronic Communication Service Providers*).
  * *Executive Order 14086*: Establece salvaguardas reforzadas para las actividades de inteligencia de señales de EE.UU. y el Tribunal de Revisión de Protección de Datos (*Data Protection Review Court* - DPRC).
  * *CLOUD Act*: Faculta a los tribunales de EE.UU. a ordenar a proveedores sujetos a su jurisdicción la entrega de datos, sin importar en qué país estén almacenados físicamente los servidores.
- **China**:
  * *Personal Information Protection Law* (PIPL) y *Data Security Law* (DSL): Imponen controles estrictos de seguridad de datos, evaluación obligatoria por el CAC (*Cyberspace Administration of China*) y acceso irrestricto de agencias estatales a redes bajo causales de seguridad nacional.
- **India**:
  * *Digital Personal Data Protection Act* (DPDPA 2023) y directivas CERT-In: Exigen registro y conservación de logs por 5 años y cooperación ante requerimientos de seguridad pública.

### 6.3 Catálogo de Medidas Suplementarias Admisibles

#### A. Medidas Técnicas (Eficacia Primaria)
1. **Cifrado de Extremo a Extremo en Reposo y en Tránsito**:
   - Algoritmos robustos de cifrado simétrico (AES-256) y asimétrico (RSA 4096 / ECC).
   - **Custodia Exclusiva de Claves**: Las claves de descifrado deben generarse, conservarse y administrarse exclusivamente por el exportador o un tercero custodio radicado en una jurisdicción con nivel adecuado. Si el importador en el tercer país tiene acceso a las claves en texto claro, la medida técnica pierde toda validez frente a leyes de vigilancia.
2. **Seudonimización Estricta Previa a la Transferencia**:
   - Los datos personales son disociados de forma que el importador no pueda reidentificar al titular sin información adicional almacenada de forma separada y segura en el país de origen.

#### B. Medidas Contractuales (Eficacia Complementaria)
- Obligación del importador de agotar todos los recursos procesales disponibles para impugnar requerimientos desproporcionados.
- Deber de notificación al exportador y al DPO con carácter inmediato ante cualquier requerimiento policial o de inteligencia.
- Cláusula de indemnización directa por daños derivados del acceso gubernamental no autorizado.

#### C. Medidas Organizativas (Gobernanza)
- Procedimiento interno formal para el escalamiento inmediato de solicitudes judiciales foráneas (*Law Enforcement Response Policy*).
- Auditorías anuales de transparencia con publicación del número y tipología de órdenes recibidas.
- Segregación estricta de accesos físicos y lógicos en los centros de datos receptores.

---

## 7. Libro de Registro de Transferencias y Notificación de Encargados (A.1.5.4, A.1.5.5, A.2.5.2)

### 7.1 Campos Mínimos del Registro Formal de Transferencias (A.1.5.4)
Para cumplir con el deber de trazabilidad y permitir la atención de derechos de los titulares (propagación de rectificaciones o supresiones bajo A.1.3.8), el registro debe contener:

| Campo | Descripción Requerida |
|---|---|
| `transfer_id` | Identificador único alfanumérico del flujo de transferencia. |
| `timestamp` / `frequency` | Fecha de ejecución o periodicidad (ej. continua en tiempo real, lote diario). |
| `origin_country` | País y territorio de procedencia de los datos. |
| `destination_country` | País territorial y región cloud receptora (sin ambigüedades). |
| `recipient_name` | Razón social formal de la entidad receptora. |
| `recipient_role` | Rol del receptor: Responsable Independiente, Corresponsable, Encargado, Subencargado. |
| `data_categories` | Tipología pormenorizada de datos personales involucrados. |
| `transfer_mechanism` | Base legal formal (Adecuación, SCC Módulo X, BCR, Derogación Art. 49). |
| `tia_reference` | Código o enlace al expediente de Evaluación de Impacto de Transferencia vigente. |
| `safeguards_summary` | Resumen de medidas técnicas (cifrado en tránsito, repositorio de claves). |
| `review_date` | Fecha de la última auditoría o revisión programada del flujo. |

### 7.2 Libro de Registro de Divulgaciones Legales a Autoridades (A.1.5.5)
Toda revelación o entrega de PII efectuada ante requerimientos judiciales o policiales foráneos debe documentarse en un expediente inmutable que contenga:
1. Fecha y hora de recepción del requerimiento.
2. Identificación formal de la autoridad solicitante (tribunal, agencia fiscal, policía).
3. Fundamento legal esgrimido y copia del mandamiento judicial vinculante.
4. Tipo y volumen de PII divulgada.
5. Dictamen jurídico interno que avaló la vinculatoriedad y proporcionalidad de la orden.
6. Acreditación de notificación remitida al cliente (para encargados bajo A.2.5.5) o justificación legal formal de la prohibición de notificación.

### 7.3 Obligaciones Específicas de los Encargados (A.2.5.2, A.2.5.5, A.2.5.6)
Cuando la organización auditada actúe en calidad de encargado del tratamiento:
- **A.2.5.2 (Notificación de cambios geográficos)**: Debe notificar al responsable con **antelación formal mínima de 30 días** antes de habilitar una nueva región de procesamiento o trasladar servidores a un nuevo país, permitiendo al responsable evaluar el impacto y ejercer su derecho de veto contractual.
- **A.2.5.5 (Notificación de requerimientos de revelación)**: Debe alertar al responsable inmediatamente ante cualquier solicitud gubernamental de entrega de datos, coordinando la estrategia de respuesta.
- **A.2.5.6 (Rechazo de solicitudes no vinculantes)**: Debe denegar formalmente cualquier solicitud de autoridades que no cuente con mandato judicial plenamente vinculante o que infrinja tratados internacionales de asistencia judicial mutua (MLAT).
