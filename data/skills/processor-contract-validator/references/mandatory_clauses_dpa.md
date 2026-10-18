# Catálogo Exhaustivo de Cláusulas Contractuales Obligatorias en Acuerdos de Tratamiento de Datos (DPA)

- **Estándares de Referencia**: ISO/IEC 27701:2025 (Tabla A.1, Tabla A.2, Tabla A.3), ISO/IEC 27701:2019 (Cláusulas 7 y 8), RGPD (Reglamento UE 2016/679, Artículos 26, 28, 32 y 33).
- **Destinatarios**: Auditores de privacidad, oficiales de seguridad de la información (CISO), directores de privacidad (DPO) y asesores legales corporativos.

---

## 1. Introducción y Marco de Evaluación Contractual

Bajo el estándar **ISO/IEC 27701:2025**, la relación contractual entre el Responsable del Tratamiento (*PII Controller*) y el Encargado del Tratamiento (*PII Processor*) no puede sustentarse en acuerdos comerciales genéricos, cláusulas de adhesión unilaterales ni referencias ambiguas al "cumplimiento legal".

El Control **A.1.2.7** exige que el tratamiento encomendado esté formalizado mediante un acuerdo vinculante por escrito que imponga de forma obligatoria los controles de la **Tabla A.2**. Asimismo, bajo el principio de responsabilidad proactiva (*accountability*), la organización debe auditar que las cláusulas reflejen compromisos operativos verificables.

A continuación se detalla el catálogo de las 13 cláusulas obligatorias, analizando para cada una los criterios de conformidad, la redacción inaceptable habitual en proveedores de software como servicio (SaaS) o nube pública, y el modelo de cláusula conforme listo para ser adoptado en pliegos de enmienda contractual.

---

## 2. Catálogo de Cláusulas Obligatorias

### Cláusula 1: Objeto, Naturaleza, Duración y Finalidades del Tratamiento

- **Bases Normativas**:
  - ISO/IEC 27701:2025: Control A.1.2.7, Control A.2.2.3 (Guía B.2.2.3).
  - ISO/IEC 27701:2019: Cláusula 7.2.7 y 8.2.2.
  - RGPD: Artículo 28, apartado 3 (encabezado).
- **Criterio de Auditoría**: El contrato debe delimitar taxativamente el tipo de operaciones que el encargado realizará, el plazo exacto de vigencia, la naturaleza técnica del servicio, las tipologías de datos personales recopilados y las categorías de interesados o titulares.

#### Ejemplo de Cláusula Deficiente / Abusiva
> *"El Proveedor prestará servicios tecnológicos y de procesamiento de información al Cliente durante la vigencia comercial acordada. El Cliente autoriza al Proveedor a recopilar y procesar los datos que considere necesarios para la correcta ejecución del servicio y la optimización de la plataforma."*
- **Análisis de la No Conformidad**: Redacción excesivamente abierta y ambigua. No delimita las categorías de datos (PII), no enumera las tipologías de titulares afectados y permite al proveedor tratar datos con fines de "optimización de plataforma" sin instrucciones específicas del cliente.

#### Ejemplo de Cláusula Conforme (Alineada con ISO 27701:2025)
> **Cláusula 1. Alcance, Objeto y Finalidad del Tratamiento.**
> *"1.1. El presente Acuerdo de Tratamiento de Datos (DPA) regula el tratamiento de información de identificación personal (PII) encomendado por el Responsable al Encargado en el marco del Contrato Principal.  
> 1.2. **Objeto y Naturaleza**: La provisión de servicios de alojamiento y gestión de base de datos transaccional en la nube descritos en el Anexo I.  
> 1.3. **Duración**: El tratamiento se extenderá única y exclusivamente durante el término de vigencia del Contrato Principal y hasta la completa devolución o destrucción certificada de la PII.  
> 1.4. **Finalidad Exclusiva**: La PII será tratada con la única finalidad de permitir la autenticación de usuarios y el procesamiento de pagos transaccionales del Responsable.  
> 1.5. Las tipologías de PII y categorías de titulares afectados se detallan exhaustivamente en el Apéndice A de este DPA."*

---

### Cláusula 2: Sujeción Exclusiva a Instrucciones Documentadas y Prohibición de Uso Propio

- **Bases Normativas**:
  - ISO/IEC 27701:2025: Control A.1.2.7, Control A.2.2.3.
  - ISO/IEC 27701:2019: Cláusula 8.2.2.
  - RGPD: Artículo 28, apartado 3, letra a).
- **Criterio de Auditoría**: Prohibición explícita de tratar los datos personales para finalidades distintas de las ordenadas por el responsable. Se debe verificar la ausencia de cláusulas que permitan al proveedor usar datos del cliente para investigación y desarrollo propios, enriquecimiento de perfiles, fines comerciales o entrenamiento de modelos de inteligencia artificial (IA).

#### Ejemplo de Cláusula Deficiente / Abusiva
> *"El Cliente reconoce y acepta que el Proveedor podrá recopilar, desidentificar, anonimizar y agregar los datos de uso y el contenido del Cliente para el desarrollo de nuevos productos, análisis de tendencias de mercado y entrenamiento de algoritmos y modelos de aprendizaje automático propios del Proveedor."*
- **Análisis de la No Conformidad**: Esta cláusula (muy común en contratos SaaS) viola frontalmente el control A.2.2.3. El encargado se autoatribuye la facultad de usar la PII del cliente para enriquecer sus modelos de IA o productos propios, transformándose indebidamente en responsable autónomo sin consentimiento del titular ni autorización legítima del cliente.

#### Ejemplo de Cláusula Conforme (Alineada con ISO 27701:2025)
> **Cláusula 2. Instrucciones del Responsable y Prohibición de Uso Secundario.**
> *"2.1. El Encargado tratará la PII única y exclusivamente conforme a las instrucciones documentadas y por escrito emanadas del Responsable, inclusive en lo relativo a transferencias de datos, salvo disposición imperativa del Derecho aplicable que le sea vinculante. En tal caso, el Encargado informará al Responsable antes del tratamiento, salvo que la ley lo prohíba por razones de interés público.  
> 2.2. **Prohibición Expresa de Uso Propio**: Queda terminantemente prohibido al Encargado utilizar, modificar, agregar, desidentificar o explotar la PII del Responsable, directa o indirectamente, para finalidades comerciales propias, mercadotecnia, perfilado, analítica independiente o entrenamiento de algoritmos, modelos estadísticos o sistemas de inteligencia artificial."*

---

### Cláusula 3: Deber de Confidencialidad del Personal Autorizado

- **Bases Normativas**:
  - ISO/IEC 27701:2025: Control A.1.2.7, Control A.3.10.
  - ISO/IEC 27701:2019: Cláusula 7.2.7 y Cláusula 6.12.1.2.
  - RGPD: Artículo 28, apartado 3, letra b).
- **Criterio de Auditoría**: El contrato debe obligar al encargado a garantizar que las personas autorizadas para tratar PII hayan firmado acuerdos vinculantes de confidencialidad o estén sujetas a un deber legal de secreto profesional. Debe extenderse más allá de la terminación laboral.

#### Ejemplo de Cláusula Deficiente / Abusiva
> *"Las partes mantendrán la debida reserva comercial de la información recibida según las prácticas estándar del sector."*
- **Análisis de la No Conformidad**: No vincula formalmente al personal dependiente del proveedor, confunde el secreto comercial mercantil con el deber legal de confidencialidad sobre datos personales y no contempla la vigencia indefinida del deber de secreto tras el cese laboral.

#### Ejemplo de Cláusula Conforme (Alineada con ISO 27701:2025)
> **Cláusula 3. Deber de Confidencialidad y Autorización de Personal.**
> *"3.1. El Encargado garantiza que únicamente tendrán acceso a la PII aquellos empleados, colaboradores y técnicos cuya intervención sea estrictamente indispensable para la prestación de los Servicios encomendados.  
> 3.2. El Encargado asegura que todo el personal autorizado para tratar PII ha suscrito compromisos contractuales de confidencialidad expresos y vinculantes, o se encuentra sujeto a una obligación estatutaria o profesional de secreto.  
> 3.3. Dicha obligación subsistirá con carácter indefinido, aún después de finalizada la relación laboral o contractual entre el personal y el Encargado, o tras la terminación del presente Contrato."*

---

### Cláusula 4: Medidas Técnicas y Organizativas de Seguridad (Tabla A.3)

- **Bases Normativas**:
  - ISO/IEC 27701:2025: Control A.1.2.7, Control A.3.10 (articulado con Controles A.3.1 a A.3.24).
  - ISO/IEC 27701:2019: Cláusula 7.2.7 y Cláusula 6.
  - RGPD: Artículo 28, apartado 3, letra c) y Artículo 32.
- **Criterio de Auditoría**: El contrato debe referenciar explícitamente un estándar reconocido de seguridad (ISO/IEC 27001, SOC 2, Tabla A.3) y detallar medidas concretas: cifrado de datos en reposo y en tránsito, control de acceso basado en privilegios mínimos (RBAC), autenticación multifactor (MFA), gestión de vulnerabilidades y resiliencia de copias de seguridad.

#### Ejemplo de Cláusula Deficiente / Abusiva
> *"El Proveedor implementará medidas de seguridad comerciales razonables de acuerdo con su propio criterio técnico para proteger la plataforma."*
- **Análisis de la No Conformidad**: Vaga e inoperante. No especifica medidas mínimas objetivas, no compromete cifrado ni estándares internacionales y supedita la seguridad al arbitrio unilateral del proveedor.

#### Ejemplo de Cláusula Conforme (Alineada con ISO 27701:2025)
> **Cláusula 4. Medidas Técnicas y Organizativas de Seguridad.**
> *"4.1. El Encargado implementará y mantendrá en todo momento las medidas técnicas y organizativas de seguridad descritas en el Anexo de Seguridad (Anexo II), las cuales satisfacen los requisitos de la Tabla A.3 de ISO/IEC 27701:2025 y el estándar ISO/IEC 27001.  
> 4.2. Dichas salvaguardas incluirán como mínimo:  
> a) Cifrado robusto de toda la PII tanto en tránsito (TLS 1.3) como en reposo (AES-256);  
> b) Mecanismos de autenticación multifactor (MFA) obligatoria para todo acceso administrativo a los entornos de tratamiento;  
> c) Segregación lógica de datos de clientes y control de accesos basado en el principio de mínimo privilegio;  
> d) Procedimientos periódicos de gestión y remediación de vulnerabilidades y pruebas de penetración anuales;  
> e) Planes probados de continuidad del negocio y copias de seguridad inmutables frente a ransomware.  
> 4.3. El Encargado no reducirá el nivel de seguridad durante la vigencia del contrato sin el previo consentimiento por escrito del Responsable."*

---

### Cláusula 5: Régimen de Subcontratación, Autorización Previa y Derecho de Oposición

- **Bases Normativas**:
  - ISO/IEC 27701:2025: Controles A.2.5.7, A.2.5.8 y A.2.5.9 (Guías B.2.5.7 a B.2.5.9).
  - ISO/IEC 27701:2019: Cláusulas 8.5.6, 8.5.7 y 8.5.8.
  - RGPD: Artículo 28, apartados 2 y 4.
- **Criterio de Auditoría**: Toda subcontratación de PII exige autorización previa (específica o general por escrito). Si es general, el encargado debe notificar con antelación suficiente (mínimo 14 a 30 días) toda nueva incorporación o sustitución de subencargados, reconociendo el derecho formal del responsable a oponerse o resolver el contrato sin penalización. Asimismo, es obligatorio el traslado contractual íntegro de las mismas obligaciones (*flow-down* contractual) al subencargado.

#### Ejemplo de Cláusula Deficiente / Abusiva
> *"El Cliente autoriza de manera general al Proveedor a subcontratar cualquier parte de los servicios a terceros. El Proveedor mantiene una lista de afiliados y proveedores en su sitio web corporativo, la cual puede actualizar periódicamente sin previo aviso individual. El uso continuado del Servicio tras la actualización constituirá la aceptación tácita del subcontratista."*
- **Análisis de la No Conformidad**: Vulneración grave de A.2.5.7, A.2.5.8 y A.2.5.9. Elimina la notificación activa, impone aceptación tácita, no otorga plazo para ejercer oposición ni contempla la facultad de resolución contractual sin penalización económica.

#### Ejemplo de Cláusula Conforme (Alineada con ISO 27701:2025)
> **Cláusula 5. Subcontratación de Tratamiento (*Sub-processors*).**
> *"5.1. El Encargado no subcontratará ninguna actividad de tratamiento que involucre PII sin la autorización previa por escrito del Responsable.  
> 5.2. **Autorización General y Notificación Previa**: El Responsable autoriza de manera general el uso de los subencargados enumerados en el Anexo III. En caso de previsión de incorporar o sustituir a un subencargado, el Encargado deberá notificarlo al Responsable por escrito con una antelación mínima de treinta (30) días naturales a la fecha efectiva de intervención del tercero.  
> 5.3. **Derecho de Oposición y Resolución**: El Responsable dispondrá de un plazo de quince (15) días naturales desde la recepción del aviso para oponerse fundadamente al cambio. Si el Encargado no pudiera ofrecer una alternativa razonable sin el subencargado objetado, el Responsable tendrá derecho a resolver el presente Acuerdo y el Contrato Principal de forma inmediata y sin penalización alguna.  
> 5.4. **Traslado de Obligaciones (*Flow-Down*)**: El Encargado celebrará un contrato por escrito con cada subencargado que imponga exactamente las mismas obligaciones de protección de datos, seguridad de la Tabla A.3 y derechos de auditoría previstos en este DPA. El Encargado responderá plenamente ante el Responsable por los incumplimientos imputables a sus subencargados."*

---

### Cláusula 6: Asistencia al Responsable en el Ejercicio de Derechos de los Titulares

- **Bases Normativas**:
  - ISO/IEC 27701:2025: Control A.1.2.7, Control A.2.3.2 (Guía B.2.3.2).
  - ISO/IEC 27701:2019: Cláusula 8.3.1.
  - RGPD: Artículo 28, apartado 3, letra e).
- **Criterio de Auditoría**: El encargado debe comprometerse a asistir técnicamente al responsable mediante medidas técnicas y organizativas apropiadas para permitirle responder oportunamente a solicitudes de acceso, rectificación, supresión, limitación, portabilidad u oposición formuladas por los titulares.

#### Ejemplo de Cláusula Deficiente / Abusiva
> *"Si un titular de datos contacta directamente al Proveedor solicitando la rectificación o eliminación de sus datos, el Proveedor podrá cobrar al Cliente una tarifa horaria de soporte técnico profesional de 250 USD/hora por procesar dicha solicitud."*
- **Análisis de la No Conformidad**: Transgrede la obligación esencial de asistencia del encargado, monetiza de forma abusiva la respuesta a derechos fundamentales y no prevé el reenvío inmediato de la petición al responsable para que este tome la decisión jurídica.

#### Ejemplo de Cláusula Conforme (Alineada con ISO 27701:2025)
> **Cláusula 6. Asistencia en el Ejercicio de Derechos de los Titulares.**
> *"6.1. Teniendo en cuenta la naturaleza del tratamiento, el Encargado asistirá al Responsable, a través de medidas técnicas y organizativas apropiadas e interfaces de autogestión en la plataforma, para que este pueda cumplir con su obligación de responder a las solicitudes de los titulares de la PII (acceso, rectificación, supresión, limitación del tratamiento, portabilidad y oposición).  
> 6.2. En caso de que el Encargado reciba directamente una solicitud de un titular respecto a su PII, el Encargado no responderá directamente al interesado, salvo instrucción expresa del Responsable, y remitirá la solicitud íntegra al Responsable dentro de un plazo improrrogable de dos (2) días hábiles siguientes a su recepción."*

---

### Cláusula 7: Asistencia en Evaluaciones de Impacto (PIA) y Consultas Previas

- **Bases Normativas**:
  - ISO/IEC 27701:2025: Control A.1.2.7, Control A.2.2.2 (Guía B.2.2.2).
  - ISO/IEC 27701:2019: Cláusula 8.2.1.
  - RGPD: Artículo 28, apartado 3, letra f).
- **Criterio de Auditoría**: El encargado debe proporcionar al responsable la información técnica, arquitectónica y de flujos de datos necesaria para la elaboración de Evaluaciones de Impacto en la Privacidad (PIA / EIPD según ISO/IEC 29134 o RGPD Art. 35) y asistir en eventuales consultas ante autoridades de control.

#### Ejemplo de Cláusula Deficiente / Abusiva
> *"El Cliente es el único responsable legal y técnico de realizar cualquier evaluación de impacto que considere necesaria. El Proveedor no asume ninguna obligación de responder cuestionarios ni proporcionar documentación interna de seguridad o diagramas de arquitectura."*
- **Análisis de la No Conformidad**: Incumplimiento explícito del control A.2.2.2 y del RGPD Art. 28.3.f. La negativa a suministrar información técnica impide al responsable valorar objetivamente los riesgos para los derechos de los titulares.

#### Ejemplo de Cláusula Conforme (Alineada con ISO 27701:2025)
> **Cláusula 7. Asistencia en Evaluaciones de Impacto en la Privacidad (PIA).**
> *"7.1. El Encargado prestará asistencia razonable y oportuna al Responsable facilitando toda la información técnica, arquitectónica, diagramas de flujo de datos y documentación de seguridad que le sea requerida para la elaboración y actualización de Evaluaciones de Impacto en la Privacidad (PIA / EIPD) vinculadas a los Servicios.  
> 7.2. Asimismo, el Encargado colaborará activamente con el Responsable en las consultas previas que este deba evacuar ante la autoridad de control de protección de datos competente."*

---

### Cláusula 8: Notificación Inmediata de Brechas de Seguridad sobre PII

- **Bases Normativas**:
  - ISO/IEC 27701:2025: Control A.1.2.7, Guía B.2.2.2, Guía B.3.12 (párrafo Encargados).
  - ISO/IEC 27701:2019: Cláusula 7.2.7 y Cláusula 8.2.1.
  - RGPD: Artículo 28, apartado 3, letra f) y Artículo 33, apartado 2.
- **Criterio de Auditoría**: Obligación de notificar al responsable cualquier violación de seguridad de datos confirmada o sospechada de inmediato. El plazo contractual no debe superar las 24 a 48 horas tras tener conocimiento de los hechos, debiendo acompañar una descripción del incidente, volumen de registros, medidas de contención adoptadas y punto de contacto.

#### Ejemplo de Cláusula Deficiente / Abusiva
> *"El Proveedor notificará al Cliente sobre violaciones de seguridad confirmadas que afecten a su cuenta en un plazo de tiempo comercialmente razonable, a entera discreción del Proveedor, una vez que haya concluido de forma definitiva su investigación forense interna."*
- **Análisis de la No Conformidad**: Muy peligrosa y no conforme. La expresión "tiempo comercialmente razonable" y condicionar el aviso a la conclusión de la investigación interna retrasa la notificación más allá de las 72 horas legales del RGPD, exponiendo al responsable a sanciones gravísimas por reporte extemporáneo.

#### Ejemplo de Cláusula Conforme (Alineada con ISO 27701:2025)
> **Cláusula 8. Notificación y Gestión de Brechas de Seguridad de PII.**
> *"8.1. El Encargado notificará por escrito al Responsable cualquier brecha de seguridad que afecte o pueda haber afectado a la PII tratada bajo este Acuerdo de manera inmediata y, en todo caso, dentro de las veinticuatro (24) horas siguientes a tener conocimiento o sospecha fundada del incidente.  
> 8.2. **Contenido Mínimo de la Notificación**:  
> a) Descripción de la naturaleza del incidente, categorías de PII y número aproximado de titulares afectados;  
> b) Identificación y datos de contacto del Oficial de Protección de Datos (DPO) o del coordinador de seguridad del Encargado;  
> c) Consecuencias probables o riesgos estimados derivados de la brecha;  
> d) Medidas técnicas y de contención inmediatas ya implementadas o previstas para mitigar el impacto.  
> 8.3. El Encargado asistirá al Responsable en la documentación y notificación a las autoridades reguladoras y a los titulares afectados, absteniéndose de emitir declaraciones públicas sobre el incidente que mencionen al Responsable sin su autorización previa."*

---

### Cláusula 9: Destino Final de la PII al Término del Servicio (Devolución o Destrucción Segura)

- **Bases Normativas**:
  - ISO/IEC 27701:2025: Control A.1.2.7, Control A.2.4.3 (Guía B.2.4.3).
  - ISO/IEC 27701:2019: Cláusula 7.2.7 y Cláusula 8.4.3.
  - RGPD: Artículo 28, apartado 3, letra g).
- **Criterio de Auditoría**: A la extinción de los servicios, el encargado debe devolver íntegramente la PII o destruirla de forma segura y certificada (conforme a estándares tipo NIST SP 800-88 o DIN 66399) a elección del responsable, suprimiendo copias existentes salvo que una ley imperativa exija su conservación bloqueada.

#### Ejemplo de Cláusula Deficiente / Abusiva
> *"A la rescisión del servicio, el Proveedor conservará una copia de respaldo de los datos del Cliente durante un período indefinido en sus sistemas de archivo a efectos de respaldo técnico corporativo."*
- **Análisis de la No Conformidad**: Violación del principio de limitación del plazo de conservación y del control A.2.4.3. No permite al cliente optar por la devolución, no aporta certificado de borrado y retiene PII indefinidamente.

#### Ejemplo de Cláusula Conforme (Alineada con ISO 27701:2025)
> **Cláusula 9. Destino Final de la PII a la Terminación.**
> *"9.1. A la terminación de la prestación de los Servicios, el Encargado deberá, a elección expresa del Responsable:  
> a) Devolver íntegramente al Responsable toda la PII tratada, junto con todas las copias existentes, en un formato estructurado, comúnmente utilizado y legible (JSON / CSV estándar); o bien  
> b) Destruir de manera definitiva, irreversible y segura toda la PII alojada en sus servidores, sistemas, soportes magnéticos y copias de seguridad.  
> 9.2. El Encargado emitirá y entregará al Responsable un Certificado de Destrucción Segura en un plazo no superior a treinta (30) días naturales desde la finalización del servicio, acreditando la sanitización conforme a normas reconocidas (ej. NIST SP 800-88 R1).  
> 9.3. Únicamente se retendrán datos en la medida en que una norma legal imperativa exija su conservación, en cuyo caso la PII permanecerá debidamente bloqueada e inaccesible para cualquier finalidad distinta a la atención de responsabilidades legales."*

---

### Cláusula 10: Derecho de Auditoría, Inspección y Demostración de Cumplimiento

- **Bases Normativas**:
  - ISO/IEC 27701:2025: Control A.1.2.7, Control A.2.2.6 (Guía B.2.2.6).
  - ISO/IEC 27701:2019: Cláusula 7.2.7 y Cláusula 8.2.5.
  - RGPD: Artículo 28, apartado 3, letra h).
- **Criterio de Auditoría**: El contrato debe otorgar al responsable el derecho irrestricto de auditar, inspeccionar y verificar las instalaciones, sistemas y procesos del encargado, directamente o mediante un auditor externo acreditado. El encargado debe poner a disposición del cliente toda la información probatoria necesaria para demostrar el cumplimiento.

#### Ejemplo de Cláusula Deficiente / Abusiva
> *"Debido a la confidencialidad de la arquitectura multi-inquilino (*multi-tenant*), no se autorizan bajo ninguna circunstancia auditorías in situ ni inspecciones técnicas presenciales por parte del Cliente. Como prueba única de cumplimiento, el Proveedor pondrá a disposición un resumen ejecutivo de su certificación anual previo pago de una tarifa de gestión de 5.000 USD."*
- **Análisis de la No Conformidad**: Cláusula abusiva típica de proveedores multinacionales. Suprime de facto el derecho legal de auditoría, impone barreras económicas desproporcionadas y despoja al responsable de sus facultades de verificación inspectora.

#### Ejemplo de Cláusula Conforme (Alineada con ISO 27701:2025)
> **Cláusula 10. Auditorías, Inspecciones y Demostración de Cumplimiento.**
> *"10.1. El Encargado pondrá a disposición del Responsable, a requerimiento de este, toda la información y evidencias documentales necesarias para demostrar el estricto cumplimiento de las obligaciones estipuladas en este DPA y en la norma ISO/IEC 27701:2025.  
> 10.2. El Encargado permitirá y facilitará la realización de auditorías e inspecciones periódicas llevadas a cabo por el Responsable o por un auditor independiente debidamente cualificado y designado por este.  
> 10.3. Las auditorías se coordinarán con un preaviso razonable de al menos diez (10) días hábiles y se desarrollarán durante el horario laboral ordinario, velando por evitar disrupciones operativas y salvaguardar la confidencialidad de otros clientes.  
> 10.4. El Encargado facilitará informes actualizados de auditoría externa independiente (ej. informes SOC 2 Tipo II, certificados ISO/IEC 27001 e ISO/IEC 27701 en vigor) que cubran los centros de datos y sistemas involucrados en el tratamiento."*

---

### Cláusula 11: Deber de Advertencia Inmediata ante Instrucciones Infractoras

- **Bases Normativas**:
  - ISO/IEC 27701:2025: Control A.2.2.5 (Guía B.2.2.5).
  - ISO/IEC 27701:2019: Cláusula 8.2.4.
  - RGPD: Artículo 28, apartado 3, párrafo final.
- **Criterio de Auditoría**: Obligación del encargado de alertar de forma documentada al responsable si, a su juicio razonable, una directriz o instrucción operativa recibida transgrede la normativa de protección de datos aplicable.

#### Ejemplo de Cláusula Deficiente / Abusiva
> *Cláusula omitida en el contrato o estipulación donde el proveedor declina toda responsabilidad por instrucciones recibidas sin obligación de emitir advertencias.*
- **Análisis de la No Conformidad**: Omisión del control A.2.2.5. El encargado no puede actuar como mero ejecutor ciego si detecta una ilegalidad manifiesta en las directrices del cliente.

#### Ejemplo de Cláusula Conforme (Alineada con ISO 27701:2025)
> **Cláusula 11. Deber de Alerta ante Instrucciones Infractoras.**
> *"El Encargado informará inmediatamente por escrito al Responsable si, según su evaluación técnica o jurídica informada, una instrucción de tratamiento impartida por el Responsable infringe la norma ISO/IEC 27701:2025, el RGPD o cualquier otra legislación aplicable en materia de privacidad y protección de datos personales."*

---

### Cláusula 12: Registro de Actividades de Tratamiento del Encargado (ROPA)

- **Bases Normativas**:
  - ISO/IEC 27701:2025: Control A.2.2.7 (Guía B.2.2.7).
  - ISO/IEC 27701:2019: Cláusula 8.2.6.
  - RGPD: Artículo 30, apartado 2.
- **Criterio de Auditoría**: Compromiso del encargado de mantener actualizado un registro de actividades de tratamiento realizadas por cuenta del cliente con los campos obligatorios normativos.

#### Ejemplo de Cláusula Conforme (Alineada con ISO 27701:2025)
> **Cláusula 12. Registro de Actividades de Tratamiento.**
> *"El Encargado mantendrá un registro formal, seguro y actualizado de todas las categorías de actividades de tratamiento efectuadas por cuenta del Responsable, conteniendo los datos de contacto de las partes y de sus DPOs, las categorías de tratamientos realizados, transferencias internacionales si existieran y una descripción general de las medidas técnicas y organizativas de seguridad implementadas según la Tabla A.3."*

---

### Cláusula 13: Régimen Específico para Acuerdos de Corresponsabilidad (*Joint PII Controllers*)

- **Bases Normativas**:
  - ISO/IEC 27701:2025: Control A.1.2.8 (Guía B.1.2.8).
  - ISO/IEC 27701:2019: Cláusula 7.2.8.
  - RGPD: Artículo 26.
- **Criterio de Auditoría**: En esquemas donde dos o más organizaciones determinan conjuntamente las finalidades y medios del tratamiento, el contrato debe:
  1. Delimitar con precisión las funciones y responsabilidades de cada corresponsable.
  2. Asignar la responsabilidad de entrega del aviso de privacidad y atención de derechos ARCO.
  3. Designar un **Punto de Contacto Único** accesible para los titulares de datos.
  4. Establecer el protocolo coordinado de notificación de brechas a las autoridades.
  5. Poner a disposición de los titulares los aspectos esenciales del acuerdo.

#### Ejemplo de Cláusula Conforme para Acuerdos de Corresponsabilidad (A.1.2.8)
> **Cláusula Especial. Gobernanza de Corresponsabilidad en el Tratamiento.**
> *"1. Las Partes acuerdan que operan como Corresponsables del Tratamiento (*Joint PII Controllers*) respecto a los datos recopilados conjuntamente a través de la plataforma colaborativa.  
> 2. **Reparto de Obligaciones**: La Parte A será responsable de proveer la información a los titulares y recabar el consentimiento en el portal de registro. La Parte B será responsable de implementar las medidas técnicas de cifrado de la base de datos común según el Control A.3.10.  
> 3. **Punto de Contacto Único**: Se designa expresamente a la Parte A como Punto de Contacto Único ante los titulares para la atención de solicitudes de ejercicio de derechos ARCO/DSAR a través del correo `dpo-conjunto@ejemplo.com`. Lo anterior sin perjuicio del derecho del titular a dirigirse indistintamente a cualquiera de las partes.  
> 4. **Gestión de Brechas**: Ante cualquier brecha de seguridad que afecte a la base común, la parte que la detecte lo comunicará a la otra en un plazo máximo de doce (12) horas. La Parte A liderará la notificación formal a la Autoridad de Control en el plazo improrrogable de 72 horas."*

---

## 3. Matriz de Ponderación y Lista de Verificación Rápida para el Auditor

| Nº | Cláusula Auditada | Control ISO 27701:2025 | Impacto de Ausencia | ¿Admite Exclusión en SoA? |
|---|---|---|---|---|
| 1 | Objeto, duración y categorías de PII | A.1.2.7 / A.2.2.3 | Crítico (Contrato inválido) | No (Indisponible) |
| 2 | Instrucciones documentadas / No uso propio | A.2.2.3 | Crítico (Uso ilícito de PII) | No (Indisponible) |
| 3 | Deber de confidencialidad del personal | A.1.2.7 / A.3.10 | Crítico (Fuga de datos) | No (Indisponible) |
| 4 | Medidas de seguridad técnicas (Tabla A.3) | A.1.2.7 / A.3.10 | Crítico (Vulnerabilidad técnica) | Requiere justificación técnica |
| 5 | Subcontratación y derecho de oposición | A.2.5.7, A.2.5.8, A.2.5.9 | Mayor (Pérdida de control de cadena) | No (Indisponible) |
| 6 | Asistencia en derechos de titulares (DSAR) | A.1.2.7 / A.2.3.2 | Mayor (Sanción por desatención) | No (Indisponible) |
| 7 | Asistencia en evaluaciones de impacto (PIA) | A.1.2.7 / A.2.2.2 | Menor / Mayor (Imposibilidad de PIA) | Si el servicio no amerita PIA |
| 8 | Notificación inmediata de brechas (<48h) | A.1.2.7 / B.2.2.2 / B.3.12 | Crítico (Sanción de autoridad) | No (Indisponible) |
| 9 | Destino final: devolución o destrucción segura | A.1.2.7 / A.2.4.3 | Mayor (Retención no autorizada) | No (Indisponible) |
| 10 | Derecho de auditoría e inspección técnica | A.1.2.7 / A.2.2.6 | Crítico (Incapacidad de auditar) | No (Indisponible) |
| 11 | Alerta de instrucciones ilegales | A.2.2.5 | Menor (Riesgo de co-responsabilidad) | No (Indisponible) |
| 12 | Registro de actividades (ROPA encargado) | A.2.2.7 | Menor (Gobernanza interna) | Conforme a excepciones legales |
| 13 | Punto de contacto único (Corresponsables) | A.1.2.8 | Mayor (Infracción de transparencia) | Solo aplica a corresponsabilidad |
