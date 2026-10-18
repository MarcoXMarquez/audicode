# Plantilla Estándar de Informe de Evaluación de Impacto en la Privacidad (PIA / EIPD)

- **Alineación Normativa**: ISO/IEC 27701:2025 (Control A.1.2.6, Cláusula 6.1.2, 8.2) e ISO/IEC 29134:2017
- **Uso**: Plantilla marco para redactar y estructurar el informe final auditable de PIA.

---

## 1. Identificación del Tratamiento y Contexto

- **Nombre del Proyecto / Sistema**: [Identificador del proyecto]
- **Unidad Organizativa / Responsable Operativo**: [Departamento / Product Owner]
- **Delegado de Protección de Datos (DPO) / Asesor de Privacidad**: [Nombre y contacto]
- **Fecha de Evaluación y Versión del Informe**: [Fecha - Versión x.y]
- **Resumen Ejecutivo**: [Breve descripción del propósito de negocio del sistema, la naturaleza de los datos tratados y la conclusión general sobre la viabilidad del tratamiento].

---

## 2. Descripción Sistemática del Tratamiento

### 2.1 Finalidades y Base Jurídica
- **Finalidades primarias y secundarias**: [Detalle explícito y legítimo de cada finalidad].
- **Base jurídica aplicable**: [Consentimiento, ejecución contractual, obligación legal, interés público o interés legítimo ponderado].

### 2.2 Inventario de Datos Personales y Colectivos Afectados
- **Categorías de Titulares (*PII Principals*)**: [Clientes, empleados, menores, usuarios web, etc.]
- **Tipología de Datos Personales**:
  * Datos identificativos básicos: [Nombres, IDs, correos, teléfonos]
  * Datos de comportamiento / telemetría: [Logs de acceso, IPs, patrones de navegación]
  * Categorías especiales / sensibles: [Datos biométricos, médicos, financieros, etc.]
- **Ciclo de Vida y Retención**: [Plazo de conservación justificado y mecanismo de purga o destrucción segura].

### 2.3 Arquitectura Técnica y Diagrama de Flujo de Datos (DFD)
- **Activos de Soporte**: [Servidores locales, contenedores cloud, bases de datos, APIs de terceros].
- **Flujos de Información**:
  1. *Entrada*: Captura de datos y canal de recolección.
  2. *Tratamiento*: Transformación, enriquecimiento, inferencia algorítmica.
  3. *Almacenamiento*: Bases de datos activas, copias de seguridad, cachés.
  4. *Salida / Destinatarios*: Terceros destinatarios, encargados del tratamiento, transferencias transfronterizas.

---

## 3. Juicio de Necesidad y Proporcionalidad

| Dimensión de Análisis | Justificación Documentada | Estado |
|---|---|:---:|
| **Idoneidad** | El tratamiento es adecuado e idóneo para alcanzar el objetivo perseguido sin incurrir en desvíos de finalidad. | Conforme / Pendiente |
| **Necesidad** | No existen medidas o tecnologías alternativas menos invasivas para lograr el mismo resultado de negocio. | Conforme / Pendiente |
| **Proporcionalidad en sentido estricto** | Los beneficios organizacionales derivados del tratamiento superan los riesgos o cargas impuestas sobre los derechos de los titulares. | Conforme / Pendiente |
| **Minimización de Datos (A.1.4.2)** | Todos los campos capturados son estrictamente indispensables para la finalidad declarada. | Conforme / Pendiente |

---

## 4. Matriz de Apreciación de Riesgos para los Derechos de los Titulares

*Conforme a Cláusula 6.1.2 de ISO/IEC 27701:2025, el riesgo debe medirse desde la perspectiva del titular.*

| ID | Escenario de Amenaza / Vulnerabilidad | Daño Potencial al Titular (*PII Principal*) | Probabilidad (1-4) | Impacto (1-4) | Riesgo Inherente | Medida Mitigadora Propuesta (Privacy by Design) | Riesgo Residual |
|---|---|---|:---:|:---:|:---:|---|:---:|
| **R01** | Acceso no autorizado o exfiltración de credenciales | Usurpación de identidad, pérdidas financieras | 3 | 4 | **Alto** | Cifrado en reposo AES-256 + MFA obligatorio | **Bajo** |
| **R02** | Sesgo algorítmico o discriminación en scoring | Exclusión indebida de contratación o créditos | 2 | 4 | **Alto** | Auditoría periódica de fairness y validación humana | **Medio** |
| **R03** | Retención indefinida de registros | Pérdida de control sobre la huella digital | 4 | 2 | **Medio** | Job automatizado de purga a los 90 días | **Bajo** |

---

## 5. Medidas de Mitigación y Asistencia de Terceros

- **Medidas Técnicas**: [Cifrado extremo a extremo, seudonimización con salteado criptográfico, segmentación de redes, logging disociado].
- **Medidas Organizativas**: [Políticas de control de acceso RBAC, acuerdos de confidencialidad NDA, capacitación a desarrolladores].
- **Asistencia del Encargado (A.2.2.2)**: [Verificación de que los proveedores involucrados han facilitado especificaciones técnicas, certificaciones SOC2/ISO 27001 y acuerdos de tratamiento DPA].

---

## 6. Consulta Previa y Gobernanza

- **Consulta a Titulares o Colectivos Afectados**: [Resumen de encuestas, paneles de usuario o representación sindical de empleados si aplica].
- **Evaluación del Riesgo Residual Global**: [Bajo / Medio / Alto].
  * *Nota*: Si el riesgo residual persiste como **Alto** y no puede ser mitigado razonablemente, es mandatoria la consulta previa ante la Autoridad de Supervisión competente.
- **Dictamen Formal del DPO**:
  * [ ] Favorable sin observaciones
  * [ ] Favorable condicionado a la implementación de mitigaciones antes de producción
  * [ ] Desfavorable (Tratamiento no viable en su diseño actual)
- **Firma y Aprobación de la Alta Dirección**: [Nombre, cargo, fecha y firma].
