# Matriz y Catálogo de Umbrales de Activación de PIA (ISO/IEC 27701:2025)

- **Control Normativo Principal**: Control A.1.2.6 (Guía B.1.2.6) - *Privacy impact assessment*
- **Requisitos del SGIP**: Cláusula 6.1.2 (Apreciación del riesgo) y Cláusula 8.2 (Operación del riesgo)
- **Estándar Metodológico de Referencia**: ISO/IEC 29134:2017 e ISO/IEC 27557:2022
- **Propósito**: Catálogo formal de criterios objetivos para el tamizaje previo (*threshold screening*) que determina si un tratamiento de datos personales requiere obligatoriamente una Evaluación de Impacto en la Privacidad (PIA / EIPD).

---

## 1. Criterios de Activación de Alto Riesgo

La siguiente tabla compendia los 10 factores de riesgo tipificados por la normativa internacional (ISO/IEC 27701, directrices WP248/EDPB y legislación comparada).

| # | Criterio de Riesgo | Descripción Operativa y Ejemplos | Activación Autónoma | Ponderación |
|---|---|---|:---:|:---:|
| **C1** | **Evaluación sistemática o exhaustiva / Perfilado** | Creación de perfiles (*profiling*), puntuación de crédito (*credit scoring*), evaluación continua de desempeño laboral con herramientas analíticas, segmentación predictiva del comportamiento o personalidad. | **SÍ** (si tiene efectos jurídicos) | 20 pts |
| **C2** | **Toma de decisiones automatizadas con efectos jurídicos o significativos** | Decisiones algorítmicas tomadas sin intervención humana significativa que producen efectos jurídicos sobre la persona o la afectan de modo similar (denegación de crédito, filtrado automático de CVs para contratación, fijación personalizada de primas de seguro). | **SÍ** | 20 pts |
| **C3** | **Tratamiento a gran escala de datos sensibles / categorías especiales** | Datos de salud física o mental, historias clínicas, datos genéticos, datos biométricos orientados a la identificación unívoca, origen étnico o racial, opiniones políticas, convicciones religiosas o filosóficas, afiliación sindical, antecedentes penales o infracciones. | **SÍ** (a gran escala) | 20 pts |
| **C4** | **Observación, monitoreo o vigilancia sistemática a gran escala** | Monitoreo sistemático de espacios de acceso público (CCTV inteligente), telemetría continua de vehículos o dispositivos personales, geolocalización en tiempo real, rastreo continuo de navegación web y huella digital (*device fingerprinting*). | **SÍ** (en espacios públicos) | 20 pts |
| **C5** | **Datos de titulares vulnerables o en relación de asimetría** | Tratamiento de datos de menores de edad, personas con discapacidad, adultos mayores en situación de dependencia, pacientes hospitalizados, o empleados sujetos a monitoreo continuo en el entorno laboral donde no hay libertad plena de consentimiento. | NO (requiere 2º criterio) | 15 pts |
| **C6** | **Uso de tecnologías emergentes, invasivas o Inteligencia Artificial** | Despliegue de IA generativa conectada a PII, modelos LLM con datos de clientes, reconocimiento facial en tiempo real, visión artificial para análisis de emociones, interfaces cerebro-computador o dispositivos IoT masivos en el hogar. | NO (requiere 2º criterio) | 15 pts |
| **C7** | **Cruce, correlación o combinación de conjuntos de datos (*Data Matching*)** | Cruce de dos o más bases de datos generadas con finalidades distintas, o integración de datos obtenidos de fuentes públicas o brokers de datos con bases de clientes internas, superando las expectativas razonables del titular. | NO (requiere 2º criterio) | 10 pts |
| **C8** | **Exclusión o impedimento del ejercicio de un derecho o servicio básico** | Tratamientos que condicionan o impiden el acceso de un titular a un servicio esencial (bancario, sanitario, telecomunicaciones, educación) o el ejercicio de un derecho fundamental. | **SÍ** | 15 pts |
| **C9** | **Tratamiento masivo o a gran escala (*Large Scale*)** | Tratamientos que involucran a un volumen masivo de titulares (ej. > 10,000 usuarios activos), cobertura geográfica multi-país, o retención masiva de metadatos de comunicaciones. | NO (requiere 2º criterio) | 10 pts |
| **C10**| **Transferencias internacionales a países sin decisión de adecuación** | Flujos transfronterizos recurrentes de PII hacia jurisdicciones con leyes de vigilancia estatal intrusiva o sin garantías de protección efectiva homologables a estándares internacionales. | NO (requiere 2º criterio) | 10 pts |

---

## 2. Reglas de Decisión del Umbral de PIA

### 2.1 Regla General de Combinación (Regla de los 2 Criterios)
- **PIA OBLIGATORIA**: Cuando el tratamiento cumple **dos (2) o más criterios** de la lista (o un puntaje de riesgo $\ge 30$ puntos).
- **PIA RECOMENDADA**: Cuando el tratamiento cumple **un (1) criterio** de riesgo no calificado como autónomo (o un puntaje de riesgo entre $15$ y $29$ puntos).
- **PIA NO REQUERIDA**: Cuando el tratamiento no activa ningún criterio de riesgo (puntaje $< 15$ puntos). Se debe documentar la ficha de tamizaje inicial (*screening record*) como evidencia auditable para ISO/IEC 27701 (Cláusula 8.2).

### 2.2 Regla de Activación Autónoma Inmediata (Un Solo Criterio Suficiente)
La PIA es **ESTRICTAMENTE OBLIGATORIA**, independientemente de otros factores, si se presenta cualquiera de los siguientes supuestos:
1. **Decisiones automatizadas o perfilado** que produzcan efectos jurídicos directos sobre el titular (Criterio C2).
2. **Tratamiento a gran escala de datos biométricos** para identificación o datos de salud (Criterio C3).
3. **Vigilancia o monitoreo sistemático a gran escala** de zonas de acceso público (Criterio C4).
4. **Exclusión algorítmica** de acceso a servicios públicos, financieros o esenciales (Criterio C8).

---

## 3. Guía de Evaluación por Tipología de Tratamiento

### 3.1 Proyectos de Inteligencia Artificial (IA / Machine Learning)
- **Factores Clave a Evaluar**:
  * ¿El modelo se entrena con datos personales reales extraídos de la web o de bases de clientes?
  * ¿Existe riesgo de alucinación o memorización de PII en los pesos del modelo?
  * ¿Las predicciones del modelo clasifican a personas con fines laborales, disciplinarios o crediticios?
- **Dictamen Típico**: OBLIGATORIA (combinación frecuente de C1, C2 y C6).

### 3.2 Sistemas Biométricos (Control de Acceso / Fichaje)
- **Factores Clave a Evaluar**:
  * ¿Se almacenan plantillas biométricas (*biometric templates*) reversibles o hashes no protegidos?
  * ¿El almacenamiento es local en el dispositivo del titular (*on-card*) o centralizado en un servidor corporativo?
  * ¿Existe alternativa no biométrica voluntaria para el titular?
- **Dictamen Típico**: OBLIGATORIA si el almacenamiento es centralizado o aplica a empleados en masa (C3 + C5).

### 3.3 Migraciones Cloud Masivas y Arquitecturas Multi-Región
- **Factores Clave a Evaluar**:
  * ¿Los datos se transfieren a nubes con soporte en países terceros (EE.UU., India)?
  * ¿El proveedor de nube ofrece cifrado con claves gestionadas por el cliente (*BYOK*)?
  * ¿El contrato incluye cláusula de asistencia en PIA (A.2.2.2)?
- **Dictamen Típico**: RECOMENDADA a OBLIGATORIA si incluye datos sensibles o flujos transfronterizos complejos (C9 + C10).

---

## 4. Registro Auditable del Tamizaje (*Threshold Screening Record*)

Todo tamizaje de PIA debe documentar formalmente en el SGIP:
1. **Fecha de evaluación y versión del proyecto**.
2. **Responsable del proyecto y evaluador técnico de privacidad**.
3. **Criterios analizados** (C1 al C10) con justificación objetiva de presencia/ausencia.
4. **Puntaje total y dictamen resultante** (Obligatoria / Recomendada / No Requerida).
5. **Visto Bueno del Delegado de Protección de Datos (DPO)** o responsable de privacidad.
6. **Revisión periódica**: Reevaluar el tamizaje si el alcance o la arquitectura del sistema cambian sustancialmente (Cláusula 8.2).
