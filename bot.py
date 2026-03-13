require('dotenv').config();
const { Telegraf, Markup, session } = require('telegraf');

const BOT_TOKEN = process.env.BOT_TOKEN;
if (!BOT_TOKEN) throw new Error('❌ BOT_TOKEN no definido en .env');

const bot = new Telegraf(BOT_TOKEN);


// ============================================================
// DATOS DEL ARANCEL DEL PROFESIONAL DEL DERECHO - CAH 2017
// La Gaceta N° 34,403 del 29 de julio de 2017
// ============================================================

const ARANCEL = {
  familia: {
    emoji: '⚖️',
    nombre: 'Derecho de Familia',
    items: [
      {
        id: 'div_mutuo',
        nombre: 'Divorcio por Mutuo Consentimiento',
        articulo: 'Art. 59-a',
        tipo: 'fijo',
        monto: 15000,
        descripcion: 'Demanda de divorcio por mutuo consentimiento ante juzgado de familia.',
      },
      {
        id: 'div_contencioso',
        nombre: 'Divorcio Contencioso',
        articulo: 'Art. 60-a',
        tipo: 'fijo',
        monto: 30000,
        descripcion: 'Proceso contencioso de divorcio donde no hay acuerdo entre las partes.',
      },
      {
        id: 'convenio_regulador',
        nombre: 'Convenio Regulador en Divorcio',
        articulo: 'Art. 59-e',
        tipo: 'fijo',
        monto: 5000,
        descripcion: 'Redacción del convenio regulador en procesos de divorcio.',
      },
      {
        id: 'alimentos',
        nombre: 'Pensión Alimenticia / Demanda de Alimentos',
        articulo: 'Art. 60-d',
        tipo: 'fijo',
        monto: 30000,
        descripcion: 'Demanda de alimentos, guarda y cuidado, régimen de comunicación y prorrateo de pensión alimenticia.',
      },
      {
        id: 'guarda',
        nombre: 'Guarda y Cuidado / Régimen de Comunicación',
        articulo: 'Art. 60-d',
        tipo: 'fijo',
        monto: 30000,
        descripcion: 'Procesos de guarda y cuidado y ampliación de régimen de comunicación.',
      },
      {
        id: 'patria_potestad',
        nombre: 'Patria Potestad (pérdida/suspensión/recuperación)',
        articulo: 'Art. 60-c',
        tipo: 'fijo',
        monto: 30000,
        descripcion: 'Pérdida, suspensión, recuperación y otorgamiento de la patria potestad.',
      },
      {
        id: 'filiacion',
        nombre: 'Filiación / Reconocimiento de Paternidad',
        articulo: 'Art. 60-b',
        tipo: 'fijo',
        monto: 30000,
        descripcion: 'Procesos de paternidad, filiación y filiación post-mortem.',
      },
      {
        id: 'union_hecho',
        nombre: 'Unión de Hecho / Separación de Hecho',
        articulo: 'Art. 60-f',
        tipo: 'fijo',
        monto: 30000,
        descripcion: 'Separación de hecho, legalización y reconocimiento de unión de hecho.',
      },
      {
        id: 'adopcion_hn',
        nombre: 'Adopción (Hondureños domiciliados en HN)',
        articulo: 'Art. 68-a',
        tipo: 'fijo',
        monto: 30000,
        descripcion: 'Adopción cuando los adoptantes son hondureños con domicilio en Honduras.',
      },
      {
        id: 'adopcion_ext_residente',
        nombre: 'Adopción (Extranjeros residentes en HN)',
        articulo: 'Art. 68-b',
        tipo: 'fijo',
        monto: 50000,
        descripcion: 'Adopción cuando los adoptantes son extranjeros residentes en Honduras.',
      },
      {
        id: 'adopcion_ext_no_residente',
        nombre: 'Adopción (No residentes en Honduras)',
        articulo: 'Art. 68-c',
        tipo: 'fijo',
        monto: 60000,
        descripcion: 'Adopción cuando los adoptantes son extranjeros u hondureños no residentes en Honduras.',
      },
      {
        id: 'vd_primera',
        nombre: 'Violencia Doméstica (concluye en 1ª Audiencia)',
        articulo: 'Art. 70',
        tipo: 'fijo',
        monto: 5000,
        descripcion: 'Tramitación o defensa de violencia doméstica que concluye en la primera audiencia.',
      },
      {
        id: 'vd_sentencia',
        nombre: 'Violencia Doméstica (hasta Sentencia Definitiva)',
        articulo: 'Art. 70',
        tipo: 'fijo',
        monto: 15000,
        descripcion: 'Violencia doméstica abierta a pruebas hasta sentencia definitiva.',
      },
      {
        id: 'tutela_curatela',
        nombre: 'Tutela / Curatela / Protutor',
        articulo: 'Art. 60-c',
        tipo: 'fijo',
        monto: 30000,
        descripcion: 'Nombramiento o remoción de curatela, tutela, protutor y discernimiento de tutor testamentario.',
      },
      {
        id: 'embargo_familia',
        nombre: 'Embargo en Materia de Familia',
        articulo: 'Art. 60-e',
        tipo: 'fijo',
        monto: 10000,
        descripcion: 'Procesos de embargo, liberación de embargos y modificación de medida cautelar de embargo.',
      },
      {
        id: 'habilitacion_mutuo',
        nombre: 'Habilitación de Edad (Mutuo Consentimiento)',
        articulo: 'Art. 59-d',
        tipo: 'fijo',
        monto: 10000,
        descripcion: 'Habilitación de edad por mutuo consentimiento.',
      },
      {
        id: 'habilitacion_contenciosa',
        nombre: 'Habilitación de Edad (Contenciosa)',
        articulo: 'Art. 59-d',
        tipo: 'fijo',
        monto: 20000,
        descripcion: 'Habilitación de edad cuando la demanda se vuelve contenciosa.',
      },
      {
        id: 'apelacion_familia',
        nombre: 'Recurso de Apelación (Familia)',
        articulo: 'Art. 65-a',
        tipo: 'porcentaje_adicional',
        porcentaje: 25,
        descripcion: 'Se cobra 25% adicional de los honorarios del proceso principal de familia.',
        calculable: true,
      },
      {
        id: 'casacion_familia',
        nombre: 'Recurso de Casación (Familia)',
        articulo: 'Art. 65-b',
        tipo: 'porcentaje_adicional',
        porcentaje: 30,
        descripcion: 'Se cobra 30% adicional de los honorarios del proceso principal de familia.',
        calculable: true,
      },
      {
        id: 'revision_familia',
        nombre: 'Recurso de Revisión (Familia)',
        articulo: 'Art. 65-c',
        tipo: 'fijo',
        monto: 25000,
        descripcion: 'Honorarios por interposición del Recurso de Revisión en materia de familia.',
      },
    ],
  },

  civil: {
    emoji: '🏛️',
    nombre: 'Derecho Civil y Mercantil',
    items: [
      {
        id: 'ordinario_civil',
        nombre: 'Proceso Ordinario Civil / Mercantil',
        articulo: 'Art. 38',
        tipo: 'progresiva',
        descripcion: 'Proceso declarativo ordinario civil o mercantil. Los porcentajes se aplican de forma progresiva sobre la cuantía.',
        tarifa: [
          { hasta: 30000, pct: 30, label: 'Hasta L. 30,000' },
          { hasta: 100000, pct: 25, label: 'Exceso de L. 30,000 hasta L. 100,000' },
          { hasta: 200000, pct: 20, label: 'Exceso de L. 100,000 hasta L. 200,000' },
          { hasta: Infinity, pct: 15, label: 'Exceso de L. 200,000 en adelante' },
        ],
        calculable: true,
      },
      {
        id: 'proceso_abreviado',
        nombre: 'Proceso Declarativo Abreviado',
        articulo: 'Art. 41',
        tipo: 'pct_ordinario',
        porcentaje: 50,
        descripcion: 'Sin oposición: 50% del juicio ordinario. Con oposición: igual al juicio ordinario.',
        calculable: true,
      },
      {
        id: 'ejecucion_sentencia',
        nombre: 'Ejecución Forzosa de Sentencia',
        articulo: 'Art. 40',
        tipo: 'pct_ordinario',
        porcentaje: 50,
        descripcion: 'Sin oposición: 50% del juicio ordinario. Con oposición: igual al ordinario.',
        calculable: true,
      },
      {
        id: 'ejecucion_titulos',
        nombre: 'Ejecución de Títulos Judiciales/Extrajudiciales',
        articulo: 'Art. 42',
        tipo: 'pct_ordinario',
        porcentaje: 50,
        descripcion: 'Sin oposición: 50% del juicio ordinario. Con oposición: igual al ordinario.',
        calculable: true,
      },
      {
        id: 'cautelares',
        nombre: 'Medidas Cautelares / Embargo Precautorio',
        articulo: 'Art. 50',
        tipo: 'fijo',
        monto: 15000,
        descripcion: 'Embargos precautorios, secuestros, prohibiciones, revisiones, modificaciones y demás medidas cautelares.',
      },
      {
        id: 'sucesorio',
        nombre: 'Proceso Sucesorio / Herencia',
        articulo: 'Art. 48-a',
        tipo: 'pct_ordinario',
        porcentaje: 50,
        descripcion: 'Los honorarios en procesos sucesorios son el 50% de la tarifa del Art. 38.',
        calculable: true,
      },
      {
        id: 'conciliacion_civil',
        nombre: 'Conciliación Civil',
        articulo: 'Art. 55',
        tipo: 'conciliacion',
        porcentaje: 20,
        sinAcuerdo: 15000,
        descripcion: '20% de lo conciliado si hay acuerdo. Si no hay conciliación: L. 15,000.',
        calculable: true,
      },
      {
        id: 'diligencias_prep',
        nombre: 'Diligencias Preparatorias',
        articulo: 'Art. 51',
        tipo: 'fijo',
        monto: 15000,
        descripcion: 'Solicitudes para preparar juicios ejecutivos, ordinarios y de otro tipo, así como pruebas anticipadas.',
      },
      {
        id: 'desahucio',
        nombre: 'Proceso de Desahucio (Inquilinato)',
        articulo: 'Art. 45-b',
        tipo: 'desahucio',
        descripcion: '3 meses de renta del inmueble (mínimo L. 6,000). Si hay causal de falta de pago: 30% del valor de la mora (mínimo L. 6,000).',
        calculable: true,
      },
      {
        id: 'monitorio',
        nombre: 'Proceso Monitorio',
        articulo: 'Art. 44-2',
        tipo: 'pct_ordinario',
        porcentaje: 50,
        descripcion: '50% de lo establecido para el juicio ordinario, con o sin oposición.',
        calculable: true,
      },
      {
        id: 'apelacion_civil',
        nombre: 'Recurso de Apelación (Civil)',
        articulo: 'Art. 38 y 46-b',
        tipo: 'porcentaje_adicional',
        porcentaje: 25,
        descripcion: '25% adicional sobre los honorarios del proceso principal.',
        calculable: true,
      },
      {
        id: 'casacion_civil',
        nombre: 'Recurso de Casación (Civil)',
        articulo: 'Art. 38 y 46-c',
        tipo: 'porcentaje_adicional',
        porcentaje: 30,
        descripcion: '30% adicional sobre los honorarios del proceso principal.',
        calculable: true,
      },
    ],
  },

  penal: {
    emoji: '⚠️',
    nombre: 'Derecho Penal',
    items: [
      {
        id: 'proceso_penal',
        nombre: 'Proceso Penal Ordinario (Completo)',
        articulo: 'Art. 85',
        tipo: 'desglose',
        montoTotal: 170000,
        descripcion: 'Honorarios acumulativos desde la etapa preparatoria hasta sentencia definitiva.',
        desglose: [
          {
            etapa: 'Etapa Preparatoria',
            monto: 50000,
            sub: [
              { nombre: 'Presentación de la Denuncia', monto: 10000 },
              { nombre: 'Investigación Preliminar', monto: 10000 },
              { nombre: 'Requerimiento Fiscal', monto: 10000 },
              { nombre: 'Audiencia Inicial', monto: 20000 },
            ],
          },
          {
            etapa: 'Etapa Intermedia',
            monto: 50000,
            sub: [
              { nombre: 'Formalización de la Acusación', monto: 15000 },
              { nombre: 'Contestación de Cargos', monto: 15000 },
              { nombre: 'Auto de Apertura a Juicio', monto: 20000 },
            ],
          },
          {
            etapa: 'Debate / Juicio Oral y Público',
            monto: 70000,
            sub: [
              { nombre: 'Preparación del Debate', monto: 20000 },
              { nombre: 'Sustanciación del Juicio', monto: 20000 },
              { nombre: 'Deliberación y Sentencia', monto: 30000 },
            ],
          },
        ],
        nota: '⚠️ Se incrementa hasta 20% para casos de Crimen Organizado, Lavado de Activos, Corrupción y Extorsión.',
      },
      {
        id: 'desjudicializadoras',
        nombre: 'Medidas Desjudicializadoras',
        articulo: 'Art. 84',
        tipo: 'opciones',
        descripcion: 'Honorarios según el tipo de medida desjudicializadora aplicada.',
        opciones: [
          { nombre: 'Criterio de Oportunidad', monto: 10000 },
          { nombre: 'Conciliación Penal', monto: 10000 },
          { nombre: 'Suspensión Condicional de la Persecución', monto: 10000 },
          { nombre: 'Procedimiento Abreviado', monto: 20000 },
        ],
      },
      {
        id: 'excarcelacion',
        nombre: 'Excarcelación',
        articulo: 'Art. 83',
        tipo: 'opciones',
        descripcion: 'Honorarios cuando el profesional tramita únicamente la excarcelación.',
        opciones: [
          { nombre: 'Tramitación de Caución', monto: 10000 },
          { nombre: 'Tramitación de Conmuta', monto: 10000 },
          { nombre: 'Tramitación de Libertad Condicional', monto: 15000 },
        ],
      },
      {
        id: 'delitos_honor',
        nombre: 'Delitos contra el Honor (Querella)',
        articulo: 'Art. 82',
        tipo: 'fijo',
        monto: 20000,
        descripcion: 'Si concluye en audiencia conciliatoria: 50% (L. 10,000). Si va a juicio ordinario: aplicar Art. 85 reducido en 50%.',
      },
      {
        id: 'extradicion',
        nombre: 'Extradición',
        articulo: 'Art. 81',
        tipo: 'fijo',
        monto: 50000,
        descripcion: 'Mínimo L. 50,000 ADICIONALES a los honorarios del proceso. En ningún caso inferior al 50% de lo que correspondería por el proceso concluido.',
      },
      {
        id: 'apelacion_penal',
        nombre: 'Recurso de Apelación (Penal)',
        articulo: 'Art. 91-a',
        tipo: 'fijo',
        monto: 40000,
      },
      {
        id: 'casacion_penal',
        nombre: 'Recurso de Casación (Penal)',
        articulo: 'Art. 91-b',
        tipo: 'fijo',
        monto: 50000,
      },
      {
        id: 'revision_penal',
        nombre: 'Recurso de Revisión (Penal)',
        articulo: 'Art. 91-c',
        tipo: 'fijo',
        monto: 30000,
      },
    ],
  },

  constitucional: {
    emoji: '📜',
    nombre: 'Jurisdicción Constitucional',
    items: [
      {
        id: 'amparo_csj',
        nombre: 'Recurso de Amparo (ante Corte Suprema)',
        articulo: 'Art. 31-a',
        tipo: 'fijo',
        monto: 30000,
      },
      {
        id: 'amparo_cortes',
        nombre: 'Recurso de Amparo (ante Cortes de Apelaciones)',
        articulo: 'Art. 31-b',
        tipo: 'fijo',
        monto: 20000,
      },
      {
        id: 'amparo_juzgado',
        nombre: 'Recurso de Amparo (ante Juzgados de Letras)',
        articulo: 'Art. 31-c',
        tipo: 'fijo',
        monto: 5000,
      },
      {
        id: 'habeas_corpus',
        nombre: 'Recurso de Habeas Corpus',
        articulo: 'Art. 32',
        tipo: 'fijo',
        monto: 10000,
        descripcion: 'Redacción, presentación y sustanciación del Recurso de Habeas Corpus.',
      },
      {
        id: 'habeas_data',
        nombre: 'Recurso de Habeas Data',
        articulo: 'Art. 33',
        tipo: 'fijo',
        monto: 10000,
        descripcion: 'Redacción, presentación y sustanciación del Recurso de Habeas Data.',
      },
      {
        id: 'inconstitucionalidad',
        nombre: 'Acción de Inconstitucionalidad',
        articulo: 'Art. 30',
        tipo: 'opciones',
        descripcion: 'Redacción y sustanciación del recurso de inconstitucionalidad.',
        opciones: [
          { nombre: 'Por Acción', monto: 30000 },
          { nombre: 'Como Excepción', monto: 20000 },
          { nombre: 'Originada de Oficio', monto: 10000 },
        ],
      },
      {
        id: 'revision_constitucional',
        nombre: 'Recurso de Revisión',
        articulo: 'Art. 34',
        tipo: 'fijo',
        monto: 25000,
        descripcion: 'Redacción, presentación y sustanciación del Recurso de Revisión.',
      },
    ],
  },

  laboral: {
    emoji: '👷',
    nombre: 'Derecho Laboral',
    items: [
      {
        id: 'juicio_ordinario_lab',
        nombre: 'Juicio Ordinario Laboral (1ª Instancia)',
        articulo: 'Art. 77-b',
        tipo: 'laboral_ordinario',
        descripcion: 'L. 2,000 al presentar/contestar la demanda + 30% de lo condenado (o de lo reclamado si hay absolución). Si el empleador pierde: 20% del valor liquidado.',
        calculable: true,
      },
      {
        id: 'unica_instancia',
        nombre: 'Demanda Laboral de Única Instancia',
        articulo: 'Art. 77-a',
        tipo: 'fijo',
        monto: 5000,
        descripcion: 'Mínimo L. 5,000 si la audiencia no excede 2 horas. Si sobrepasa ese tiempo: +50% adicional por cada hora o fracción.',
      },
      {
        id: 'ejecutiva_laboral',
        nombre: 'Demanda Ejecutiva Laboral',
        articulo: 'Art. 77-b3',
        tipo: 'porcentaje',
        porcentaje: 25,
        descripcion: '25% de la cantidad ejecutada.',
        calculable: true,
      },
      {
        id: 'segunda_instancia_lab',
        nombre: 'Segunda Instancia Laboral',
        articulo: 'Art. 77-b2',
        tipo: 'laboral_segunda',
        descripcion: 'L. 2,000 fijos + 15% de la cantidad liquidada.',
        calculable: true,
      },
      {
        id: 'conciliacion_lab',
        nombre: 'Conciliación Extrajudicial Laboral',
        articulo: 'Art. 75-j',
        tipo: 'conciliacion',
        porcentaje: 20,
        sinAcuerdo: 5000,
        descripcion: '20% de lo conciliado si hay acuerdo. Si no hay conciliación: L. 5,000 + gastos.',
        calculable: true,
      },
      {
        id: 'contrato_trabajo',
        nombre: 'Elaboración de Contrato Individual de Trabajo',
        articulo: 'Art. 75-d',
        tipo: 'fijo',
        monto: 3000,
      },
      {
        id: 'reglamento_interno',
        nombre: 'Elaboración/Trámite de Reglamento Interno',
        articulo: 'Art. 75-e',
        tipo: 'fijo',
        monto: 20000,
        descripcion: 'Elaboración y trámite de Reglamento Interno de Trabajo. Más gastos de desplazamiento y viáticos.',
      },
      {
        id: 'estatuto_sindical',
        nombre: 'Estatuto Sindical y Personalidad Jurídica',
        articulo: 'Art. 75-g',
        tipo: 'fijo',
        monto: 30000,
        descripcion: 'L. 30,000 + L. 3.00 por km de distancia + 20% de gastos de depreciación del vehículo.',
      },
      {
        id: 'casacion_laboral',
        nombre: 'Recurso de Casación Laboral',
        articulo: 'Art. 77-b6',
        tipo: 'porcentaje',
        porcentaje: 10,
        descripcion: '10% sobre la cantidad condenada o reclamada.',
        calculable: true,
      },
      {
        id: 'consulta_verbal_lab',
        nombre: 'Consulta Verbal (Laboral)',
        articulo: 'Art. 75-a',
        tipo: 'fijo',
        monto: 1000,
      },
      {
        id: 'consulta_escrita_lab',
        nombre: 'Consulta Escrita (Laboral)',
        articulo: 'Art. 75-b',
        tipo: 'fijo',
        monto: 3000,
      },
    ],
  },

  administrativo: {
    emoji: '🏢',
    nombre: 'Derecho Administrativo',
    items: [
      {
        id: 'contencioso_ordinario',
        nombre: 'Proceso Contencioso-Administrativo Ordinario',
        articulo: 'Art. 58-a',
        tipo: 'progresiva',
        descripcion: 'Según el valor de lo litigado, incluyendo intereses bancarios máximos, moratorios y cantidades accesorias.',
        tarifa: [
          { hasta: 30000, pct: 30, label: 'Hasta L. 30,000' },
          { hasta: 200000, pct: 25, label: 'Exceso de L. 30,000 hasta L. 200,000' },
          { hasta: 500000, pct: 20, label: 'Exceso de L. 200,000 hasta L. 500,000' },
          { hasta: Infinity, pct: 15, label: 'Exceso de L. 500,000 en adelante' },
        ],
        calculable: true,
      },
      {
        id: 'contencioso_indeterminado',
        nombre: 'Proceso Contencioso-Adm. (Cuantía Indeterminada)',
        articulo: 'Art. 58-a',
        tipo: 'fijo',
        monto: 30000,
      },
      {
        id: 'tributario',
        nombre: 'Asuntos Tributarios o Impositivos',
        articulo: 'Art. 58-c',
        tipo: 'progresiva',
        descripcion: 'Honorarios en materia tributaria o impositiva según cuantía.',
        tarifa: [
          { hasta: 30000, pct: 25, label: 'Hasta L. 30,000' },
          { hasta: 200000, pct: 20, label: 'Exceso de L. 30,000 hasta L. 200,000' },
          { hasta: Infinity, pct: 15, label: 'Exceso de L. 200,000 en adelante' },
        ],
        calculable: true,
      },
      {
        id: 'licitacion',
        nombre: 'Preparación de una Licitación',
        articulo: 'Art. 58-d1',
        tipo: 'fijo',
        monto: 15000,
      },
      {
        id: 'concurso',
        nombre: 'Preparación de un Concurso',
        articulo: 'Art. 58-d2',
        tipo: 'fijo',
        monto: 20000,
      },
      {
        id: 'apelacion_admin',
        nombre: 'Recurso de Apelación (Contencioso-Adm.)',
        articulo: 'Art. 58-g',
        tipo: 'porcentaje_adicional',
        porcentaje: 33,
        descripcion: '33% de lo asignado a cada materia contencioso-administrativa.',
        calculable: true,
      },
    ],
  },

  general: {
    emoji: '📋',
    nombre: 'Honorarios Generales',
    items: [
      {
        id: 'consulta_verbal',
        nombre: 'Consulta Verbal (por hora)',
        articulo: 'Art. 101-a',
        tipo: 'por_hora',
        montoPorHora: 500,
        descripcion: 'Con o sin examen de documentos. Por hora o fracción de hora.',
        calculable: true,
      },
      {
        id: 'consulta_escrita',
        nombre: 'Consulta Escrita',
        articulo: 'Art. 101-b',
        tipo: 'fijo',
        monto: 5000,
        descripcion: 'Honorario convencional sobre un mínimo de L. 5,000.',
      },
      {
        id: 'contrato_privado',
        nombre: 'Redacción de Contratos Privados',
        articulo: 'Art. 108',
        tipo: 'contrato',
        descripcion: '2.5% hasta L. 25,000; 1.5% sobre el exceso. Mínimo absoluto: L. 4,000.',
        calculable: true,
      },
      {
        id: 'cobro_extrajudicial',
        nombre: 'Cobro Extrajudicial',
        articulo: 'Art. 105',
        tipo: 'porcentaje',
        porcentaje: 20,
        minimo: 3000,
        descripcion: '20% de la suma cobrada. Mínimo: L. 3,000.',
        calculable: true,
      },
      {
        id: 'honorario_hora',
        nombre: 'Honorarios por Hora',
        articulo: 'Art. 109',
        tipo: 'por_hora',
        montoPorHora: 500,
        descripcion: 'Mínimo L. 500 por hora o fracción de hora de labor profesional.',
        calculable: true,
      },
      {
        id: 'redaccion_actas',
        nombre: 'Redacción de Actas (Sociedades)',
        articulo: 'Art. 104',
        tipo: 'opciones',
        opciones: [
          { nombre: 'Con fines de lucro (por acta)', monto: 5000 },
          { nombre: 'Sin fines de lucro (por acta)', monto: 3500 },
        ],
      },
      {
        id: 'estudio_expediente',
        nombre: 'Estudio de Expedientes',
        articulo: 'Art. 103',
        tipo: 'fijo',
        monto: 2000,
        descripcion: 'En tribunales y oficinas administrativas. Mínimo L. 2,000.',
      },
      {
        id: 'comparecencia',
        nombre: 'Comparecencia a Audiencias',
        articulo: 'Art. 113',
        tipo: 'fijo',
        monto: 5000,
        descripcion: 'Audiencias de descargo, formulación de descargos y audiencias varias. L. 5,000 cada una.',
      },
      {
        id: 'cobro_judicial',
        nombre: 'Cobro Judicial (Proceso Abreviado)',
        articulo: 'Art. 8 y Art. 41',
        tipo: 'pct_ordinario',
        porcentaje: 50,
        descripcion: 'Cobro judicial de honorarios profesionales adeudados mediante proceso abreviado.',
        calculable: true,
      },
    ],
  },
};

// ============================================================
// ÍNDICE DE BÚSQUEDA POR PALABRAS CLAVE
// ============================================================

const BUSQUEDA_INDEX = [
  // FAMILIA
  { palabras: ['alimentos', 'pension', 'alimenticia', 'manutención', 'cuota alimentaria', 'pensión alimenticia', 'demanda alimentos'], cat: 'familia', id: 'alimentos' },
  { palabras: ['divorcio mutuo', 'divorcio consentimiento', 'divorcio voluntario', 'separacion mutua'], cat: 'familia', id: 'div_mutuo' },
  { palabras: ['divorcio contencioso', 'divorcio litigioso', 'divorcio demanda', 'divorcio forzoso'], cat: 'familia', id: 'div_contencioso' },
  { palabras: ['divorcio'], cat: 'familia', id: 'div_mutuo' },
  { palabras: ['guarda', 'custodia', 'visitas', 'régimen comunicación', 'comunicación hijos'], cat: 'familia', id: 'guarda' },
  { palabras: ['patria potestad', 'suspensión patria potestad', 'pérdida patria potestad'], cat: 'familia', id: 'patria_potestad' },
  { palabras: ['filiacion', 'paternidad', 'reconocimiento paternidad', 'reconocimiento forzoso'], cat: 'familia', id: 'filiacion' },
  { palabras: ['union hecho', 'unión libre', 'convivencia', 'separacion hecho'], cat: 'familia', id: 'union_hecho' },
  { palabras: ['adopcion', 'adoptar', 'adopción'], cat: 'familia', id: 'adopcion_hn' },
  { palabras: ['violencia doméstica', 'violencia intrafamiliar', 'maltrato', 'violencia familiar'], cat: 'familia', id: 'vd_primera' },
  { palabras: ['tutela', 'curatela', 'protutor'], cat: 'familia', id: 'tutela_curatela' },
  // CIVIL
  { palabras: ['proceso ordinario', 'juicio ordinario', 'demanda civil', 'demanda ordinaria', 'civil ordinario'], cat: 'civil', id: 'ordinario_civil' },
  { palabras: ['conciliación', 'conciliacion', 'mediación', 'arreglo extrajudicial'], cat: 'civil', id: 'conciliacion_civil' },
  { palabras: ['embargo', 'precautorio', 'medida cautelar', 'secuestro judicial'], cat: 'civil', id: 'cautelares' },
  { palabras: ['desahucio', 'inquilinato', 'arrendamiento', 'alquiler', 'desalojo inquilino'], cat: 'civil', id: 'desahucio' },
  { palabras: ['sucesion', 'herencia', 'testamento', 'intestado', 'sucesorio'], cat: 'civil', id: 'sucesorio' },
  { palabras: ['monitorio', 'proceso monitorio'], cat: 'civil', id: 'monitorio' },
  { palabras: ['ejecución sentencia', 'ejecutar sentencia', 'cobrar sentencia'], cat: 'civil', id: 'ejecucion_sentencia' },
  // PENAL
  { palabras: ['proceso penal', 'defensa penal', 'delito', 'acusado', 'imputado', 'penal'], cat: 'penal', id: 'proceso_penal' },
  { palabras: ['excarcelacion', 'excarcelación', 'libertad', 'caución', 'conmuta', 'libertad condicional'], cat: 'penal', id: 'excarcelacion' },
  { palabras: ['extradicion', 'extradición'], cat: 'penal', id: 'extradicion' },
  { palabras: ['criterio oportunidad', 'procedimiento abreviado', 'suspensión condicional'], cat: 'penal', id: 'desjudicializadoras' },
  // CONSTITUCIONAL
  { palabras: ['amparo', 'recurso amparo', 'violación derechos'], cat: 'constitucional', id: 'amparo_csj' },
  { palabras: ['habeas corpus', 'detención ilegal', 'libertad detenido'], cat: 'constitucional', id: 'habeas_corpus' },
  { palabras: ['habeas data', 'datos personales', 'rectificación datos'], cat: 'constitucional', id: 'habeas_data' },
  { palabras: ['inconstitucionalidad', 'recurso inconstitucionalidad'], cat: 'constitucional', id: 'inconstitucionalidad' },
  // LABORAL
  { palabras: ['laboral', 'trabajo', 'despido', 'prestaciones', 'indemnización', 'empleado', 'trabajador'], cat: 'laboral', id: 'juicio_ordinario_lab' },
  { palabras: ['contrato trabajo', 'contrato laboral', 'contrato empleado'], cat: 'laboral', id: 'contrato_trabajo' },
  { palabras: ['conciliación laboral', 'arreglo laboral'], cat: 'laboral', id: 'conciliacion_lab' },
  { palabras: ['reglamento interno', 'reglamento trabajo'], cat: 'laboral', id: 'reglamento_interno' },
  { palabras: ['sindicato', 'estatuto sindical', 'personalidad juridica sindical'], cat: 'laboral', id: 'estatuto_sindical' },
  // ADMINISTRATIVO
  { palabras: ['tributario', 'impuestos', 'fiscal', 'impugnación tributaria', 'ajuste fiscal'], cat: 'administrativo', id: 'tributario' },
  { palabras: ['licitación', 'licitacion', 'concurso público'], cat: 'administrativo', id: 'licitacion' },
  { palabras: ['contencioso administrativo', 'contencioso-administrativo'], cat: 'administrativo', id: 'contencioso_ordinario' },
  // GENERAL
  { palabras: ['consulta', 'consultoria', 'asesoría', 'opinion legal', 'consulta verbal'], cat: 'general', id: 'consulta_verbal' },
  { palabras: ['contrato privado', 'redactar contrato', 'elaborar contrato', 'contrato'], cat: 'general', id: 'contrato_privado' },
  { palabras: ['cobro extrajudicial', 'recuperar deuda', 'cobrar deuda'], cat: 'general', id: 'cobro_extrajudicial' },
  { palabras: ['honorario hora', 'por hora', 'tarifa hora'], cat: 'general', id: 'honorario_hora' },
  { palabras: ['audiencia', 'descargo', 'comparecencia'], cat: 'general', id: 'comparecencia' },
];

// ============================================================
// FUNCIONES DE CÁLCULO
// ============================================================

function fL(n) {
  return `L. ${n.toLocaleString('es-HN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

function calcProgresiva(monto, tarifa) {
  let total = 0, anterior = 0;
  const desglose = [];
  for (const t of tarifa) {
    if (monto <= anterior) break;
    const tope = t.hasta === Infinity ? monto : Math.min(monto, t.hasta);
    const base = tope - anterior;
    const hon = base * (t.pct / 100);
    desglose.push({ label: t.label, base, pct: t.pct, hon });
    total += hon;
    anterior = t.hasta === Infinity ? monto : t.hasta;
    if (monto <= t.hasta) break;
  }
  return { total, desglose };
}

function calcContrato(monto) {
  let total = 0;
  const desglose = [];
  if (monto <= 25000) {
    total = monto * 0.025;
    desglose.push({ label: 'Hasta L. 25,000 al 2.5%', hon: total });
  } else {
    const p1 = 25000 * 0.025;
    const p2 = (monto - 25000) * 0.015;
    total = p1 + p2;
    desglose.push({ label: 'Hasta L. 25,000 al 2.5%', hon: p1 });
    desglose.push({ label: `Exceso de L. 25,000 al 1.5%`, hon: p2 });
  }
  if (total < 4000) { total = 4000; desglose.push({ label: '⚠️ Aplicado mínimo de L. 4,000', hon: 4000 }); }
  return { total, desglose };
}

// ============================================================
// HELPERS DE MENSAJES
// ============================================================

function getItem(cat, id) {
  return ARANCEL[cat]?.items.find(i => i.id === id) || null;
}

function buildItemMsg(cat, item) {
  const catObj = ARANCEL[cat];
  let msg = `${catObj.emoji} *${catObj.nombre}*\n`;
  msg += `━━━━━━━━━━━━━━━━━━━━━━\n`;
  msg += `📌 *${item.nombre}*\n`;
  msg += `🔖 _${item.articulo}_\n\n`;
  if (item.descripcion) msg += `📝 ${item.descripcion}\n\n`;

  switch (item.tipo) {
    case 'fijo':
      msg += `💰 *Honorario Mínimo:*\n➡️ *${fL(item.monto)}*\n`;
      break;
    case 'desglose':
      msg += `💰 *Total Mínimo:* *${fL(item.montoTotal)}*\n\n📊 *Desglose Acumulativo:*\n`;
      for (const e of item.desglose) {
        msg += `\n🔹 *${e.etapa}:* ${fL(e.monto)}\n`;
        for (const s of e.sub) msg += `  • ${s.nombre}: ${fL(s.monto)}\n`;
      }
      if (item.nota) msg += `\n${item.nota}\n`;
      break;
    case 'opciones':
      msg += `💰 *Honorarios según tipo:*\n\n`;
      for (const o of item.opciones) msg += `• ${o.nombre}: *${fL(o.monto)}*\n`;
      break;
    case 'progresiva':
      msg += `📊 *Tarifa Progresiva:*\n\n`;
      for (const t of item.tarifa) {
        const ultimoExceso = item.tarifa.indexOf(t) > 0 ? item.tarifa[item.tarifa.indexOf(t) - 1].hasta : 0;
        msg += `• ${t.label}: *${t.pct}%*\n`;
      }
      msg += `\n💡 _Se aplica cada porcentaje solo sobre el tramo correspondiente_\n`;
      break;
    case 'pct_ordinario':
      msg += `💰 *${item.porcentaje}% del Juicio Ordinario (Art. 38)*\n`;
      msg += `\n_Usa la calculadora para obtener el monto exacto_\n`;
      break;
    case 'porcentaje':
      msg += `💰 *${item.porcentaje}%* del monto\n`;
      if (item.minimo) msg += `📍 Mínimo: *${fL(item.minimo)}*\n`;
      break;
    case 'porcentaje_adicional':
      msg += `💰 *${item.porcentaje}% adicional* sobre los honorarios del proceso principal\n`;
      break;
    case 'conciliacion':
      msg += `💰 *Si hay acuerdo:* ${item.porcentaje}% de lo conciliado\n`;
      msg += `💰 *Sin acuerdo:* ${fL(item.sinAcuerdo)}\n`;
      break;
    case 'por_hora':
      msg += `💰 *${fL(item.montoPorHora)} por hora o fracción*\n`;
      break;
    case 'contrato':
      msg += `📊 *Tarifa Contratos Privados:*\n`;
      msg += `• Hasta L. 25,000: *2.5%*\n`;
      msg += `• Exceso de L. 25,000: *1.5%*\n`;
      msg += `• Mínimo absoluto: *L. 4,000*\n`;
      break;
    case 'laboral_ordinario':
      msg += `💰 *Honorarios:*\n`;
      msg += `• L. 2,000 al presentar/contestar demanda\n`;
      msg += `• + 30% de lo condenado (o de lo reclamado si hay absolución)\n`;
      msg += `• _Si el patrono pierde: 20% del valor liquidado_\n`;
      break;
    case 'laboral_segunda':
      msg += `💰 *Honorarios:*\n`;
      msg += `• L. 2,000 fijos\n`;
      msg += `• + 15% de la cantidad liquidada\n`;
      break;
    case 'desahucio':
      msg += `💰 *Honorarios:*\n`;
      msg += `• *3 meses de renta* del inmueble\n`;
      msg += `• Mínimo absoluto: *L. 6,000*\n`;
      msg += `\nSi hay *causal de falta de pago:*\n`;
      msg += `• *30% del valor de la mora*\n`;
      msg += `• Mínimo: *L. 6,000*\n`;
      break;
  }

  msg += `\n\n📌 _Valores sujetos a incremento automático del 10% cada 10 años (Art. 131)._`;
  return msg;
}

// ============================================================
// CONFIGURACIÓN DEL BOT
// ============================================================

bot.use(session());
bot.use((ctx, next) => {
  if (!ctx.session) ctx.session = {};
  return next();
});

// ============================================================
// TECLADOS
// ============================================================

function teclado_principal() {
  return Markup.inlineKeyboard([
    [Markup.button.callback('⚖️  Derecho de Familia', 'cat:familia')],
    [Markup.button.callback('🏛️  Civil y Mercantil', 'cat:civil')],
    [Markup.button.callback('⚠️  Derecho Penal', 'cat:penal')],
    [Markup.button.callback('📜  Constitucional', 'cat:constitucional')],
    [Markup.button.callback('👷  Derecho Laboral', 'cat:laboral')],
    [Markup.button.callback('🏢  Derecho Administrativo', 'cat:administrativo')],
    [Markup.button.callback('📋  Honorarios Generales', 'cat:general')],
    [
      Markup.button.callback('🔢 Calculadora', 'calculadora'),
      Markup.button.callback('📥 Descargar PDF', 'pdf'),
    ],
  ]);
}

function teclado_cat(catKey) {
  const cat = ARANCEL[catKey];
  const botones = cat.items.map(item => [Markup.button.callback(`${item.nombre}`, `item:${catKey}:${item.id}`)]);
  botones.push([Markup.button.callback('🏠 Menú Principal', 'inicio')]);
  return Markup.inlineKeyboard(botones);
}

function teclado_item(catKey, itemId) {
  const item = getItem(catKey, itemId);
  const botones = [];
  if (item && item.calculable) {
    botones.push([Markup.button.callback('🔢 Calcular Honorarios', `calc:${catKey}:${itemId}`)]);
  }
  botones.push([Markup.button.callback(`↩️ Volver a ${ARANCEL[catKey].emoji} ${ARANCEL[catKey].nombre}`, `cat:${catKey}`)]);
  botones.push([Markup.button.callback('🏠 Menú Principal', 'inicio')]);
  return Markup.inlineKeyboard(botones);
}

function teclado_calculadora() {
  return Markup.inlineKeyboard([
    [Markup.button.callback('🏛️ Civil Ordinario (Art. 38)', 'calc:civil:ordinario_civil')],
    [Markup.button.callback('🏢 Contencioso-Administrativo', 'calc:administrativo:contencioso_ordinario')],
    [Markup.button.callback('💼 Tributario / Fiscal', 'calc:administrativo:tributario')],
    [Markup.button.callback('📄 Contrato Privado (Art. 108)', 'calc:general:contrato_privado')],
    [Markup.button.callback('🤝 Conciliación Civil', 'calc:civil:conciliacion_civil')],
    [Markup.button.callback('⚖️ Proceso Sucesorio', 'calc:civil:sucesorio')],
    [Markup.button.callback('👷 Laboral Ordinario', 'calc:laboral:juicio_ordinario_lab')],
    [Markup.button.callback('👷 Laboral 2ª Instancia', 'calc:laboral:segunda_instancia_lab')],
    [Markup.button.callback('🏠 Desahucio / Inquilinato', 'calc:civil:desahucio')],
    [Markup.button.callback('💸 Cobro Extrajudicial', 'calc:general:cobro_extrajudicial')],
    [Markup.button.callback('⏱️ Honorarios por Hora', 'calc:general:honorario_hora')],
    [Markup.button.callback('➕ % Adicional (Apelación/Casación)', 'calc:extra:pct')],
    [Markup.button.callback('🏠 Menú Principal', 'inicio')],
  ]);
}

// ============================================================
// COMANDOS
// ============================================================

const BIENVENIDA = `👨‍⚖️ *ARANCEL DEL PROFESIONAL DEL DERECHO*
🇭🇳 *Colegio de Abogados de Honduras — CAH*

━━━━━━━━━━━━━━━━━━━━━━
Consulta los *honorarios mínimos* establecidos en el Arancel aprobado el 30 de abril de 2017 y publicado en *La Gaceta N° 34,403* del 29 de julio de 2017.

📋 *¿Qué puedo hacer?*
• Consultar honorarios por materia
• Calcular honorarios con tablas progresivas
• Buscar trámites por palabra clave
• Descargar el Arancel vigente en PDF

💡 *Tip:* Escribe directamente lo que buscas. Ej: _"alimentos"_, _"divorcio"_, _"amparo"_, _"desahucio"_

👇 *Selecciona una categoría:*

━━━━━━━━━━━━━━━━━━━━━━
💡 _Idea y desarrollo: *Abg. Brayan Fernando Padilla Rodríguez*_`;

bot.start(ctx => ctx.reply(BIENVENIDA, { parse_mode: 'Markdown', ...teclado_principal() }));
bot.help(ctx =>
  ctx.reply(
    `📖 *Comandos disponibles:*\n\n` +
    `/start — Menú principal\n` +
    `/buscar [término] — Buscar un trámite\n` +
    `/calcular — Abrir calculadora\n` +
    `/pdf — Descargar Arancel vigente\n` +
    `/menu — Volver al menú\n\n` +
    `💡 *Ejemplos de búsqueda:*\n` +
    `\`/buscar alimentos\`\n\`/buscar divorcio\`\n\`/buscar amparo\`\n\`/buscar desahucio\`\n\`/buscar laboral\``,
    { parse_mode: 'Markdown' }
  )
);
bot.command('menu', ctx => ctx.reply('👇 *Menú Principal:*', { parse_mode: 'Markdown', ...teclado_principal() }));
bot.command('calcular', ctx => ctx.reply('🔢 *Calculadora de Honorarios*\n\nSelecciona el tipo de cálculo:', { parse_mode: 'Markdown', ...teclado_calculadora() }));
bot.command('pdf', ctx => enviarPDF(ctx));
bot.command('buscar', ctx => {
  const q = ctx.message.text.replace('/buscar', '').trim();
  if (!q) return ctx.reply('🔍 Escribe qué buscas. Ej: `/buscar alimentos`', { parse_mode: 'Markdown' });
  return buscar(ctx, q);
});

// ============================================================
// BÚSQUEDA
// ============================================================

async function buscar(ctx, texto) {
  const q = texto.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  const encontrados = [];

  for (const entry of BUSQUEDA_INDEX) {
    for (const p of entry.palabras) {
      const pNorm = p.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
      if (pNorm.includes(q) || q.includes(pNorm.split(' ')[0])) {
        if (!encontrados.find(e => e.id === entry.id && e.cat === entry.cat)) {
          encontrados.push(entry);
        }
        break;
      }
    }
  }

  // Búsqueda en nombres directamente
  for (const [catKey, cat] of Object.entries(ARANCEL)) {
    for (const item of cat.items) {
      const nombre = item.nombre.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
      const desc = (item.descripcion || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
      if ((nombre.includes(q) || desc.includes(q)) && !encontrados.find(e => e.id === item.id && e.cat === catKey)) {
        encontrados.push({ cat: catKey, id: item.id, palabras: [] });
      }
    }
  }

  if (!encontrados.length) {
    return ctx.reply(
      `🔍 No encontré resultados para *"${texto}"*\n\n💡 Intenta con:\n• alimentos, divorcio, guarda\n• amparo, habeas corpus, penal\n• laboral, desahucio, contrato\n• tributario, licitación`,
      { parse_mode: 'Markdown', ...teclado_principal() }
    );
  }

  if (encontrados.length === 1) {
    return mostrarItem(ctx, encontrados[0].cat, encontrados[0].id);
  }

  const botones = encontrados.slice(0, 9).map(e => {
    const item = getItem(e.cat, e.id);
    if (!item) return null;
    return [Markup.button.callback(`${ARANCEL[e.cat].emoji} ${item.nombre}`, `item:${e.cat}:${e.id}`)];
  }).filter(Boolean);
  botones.push([Markup.button.callback('🏠 Menú Principal', 'inicio')]);

  const reply = ctx.callbackQuery ? ctx.editMessageText.bind(ctx) : ctx.reply.bind(ctx);
  await reply(`🔍 Resultados para *"${texto}"* (${encontrados.length} encontrados):\n\nSelecciona el trámite:`, {
    parse_mode: 'Markdown',
    ...Markup.inlineKeyboard(botones),
  }).catch(() => ctx.reply(`🔍 Resultados para *"${texto}"*:`, { parse_mode: 'Markdown', ...Markup.inlineKeyboard(botones) }));
}

// ============================================================
// MOSTRAR CATEGORÍA / ÍTEM
// ============================================================

async function mostrarCat(ctx, catKey) {
  const cat = ARANCEL[catKey];
  const msg = `${cat.emoji} *${cat.nombre}*\n\n📋 Selecciona el trámite o proceso:`;
  const edit = ctx.editMessageText?.bind(ctx);
  if (edit) {
    await edit(msg, { parse_mode: 'Markdown', ...teclado_cat(catKey) }).catch(() =>
      ctx.reply(msg, { parse_mode: 'Markdown', ...teclado_cat(catKey) })
    );
  } else {
    await ctx.reply(msg, { parse_mode: 'Markdown', ...teclado_cat(catKey) });
  }
}

async function mostrarItem(ctx, catKey, itemId) {
  const item = getItem(catKey, itemId);
  if (!item) return;
  const msg = buildItemMsg(catKey, item);
  const edit = ctx.editMessageText?.bind(ctx);
  if (edit) {
    await edit(msg, { parse_mode: 'Markdown', ...teclado_item(catKey, itemId) }).catch(() =>
      ctx.reply(msg, { parse_mode: 'Markdown', ...teclado_item(catKey, itemId) })
    );
  } else {
    await ctx.reply(msg, { parse_mode: 'Markdown', ...teclado_item(catKey, itemId) });
  }
}

// ============================================================
// PDF
// ============================================================

const PDF_PATH = require('path').join(__dirname, 'ARANCEL-DEL-PROFESIONAL-DEL-DERECHO.pdf');

async function enviarPDF(ctx) {
  const aviso = await ctx.reply(`⏳ _Enviando el PDF del Arancel..._`, { parse_mode: 'Markdown' });

  try {
    await ctx.replyWithDocument(
      { source: PDF_PATH, filename: 'Arancel-del-Profesional-del-Derecho-CAH-2017.pdf' },
      {
        caption:
          `📄 *Arancel del Profesional del Derecho*\n` +
          `🇭🇳 Colegio de Abogados de Honduras — CAH\n\n` +
          `🗓 _Aprobado: 30 de abril de 2017_\n` +
          `📰 _La Gaceta N° 34,403 — 29 de julio de 2017_\n\n` +
          `💡 _Idea y desarrollo: Abg. Brayan Fernando Padilla Rodríguez_`,
        parse_mode: 'Markdown',
        ...Markup.inlineKeyboard([
          [Markup.button.callback('🏠 Menú Principal', 'inicio')],
        ]),
      }
    );
    await ctx.telegram.deleteMessage(ctx.chat.id, aviso.message_id).catch(() => {});
  } catch (err) {
    console.error('[PDF] Error enviando documento:', err.message);
    await ctx.telegram.deleteMessage(ctx.chat.id, aviso.message_id).catch(() => {});
    await ctx.reply(
      `⚠️ _No se pudo enviar el PDF en este momento._\n\n` +
      `📌 _Contacta al Abg. Brayan Fernando Padilla Rodríguez para obtenerlo._`,
      {
        parse_mode: 'Markdown',
        ...Markup.inlineKeyboard([
          [Markup.button.url('🌐 Sitio Oficial CAH', 'https://www.cah.hn')],
          [Markup.button.callback('🏠 Menú Principal', 'inicio')],
        ]),
      }
    );
  }
}

// ============================================================
// CALCULADORA — LÓGICA
// ============================================================

async function iniciarCalculo(ctx, catKey, itemId) {
  const item = getItem(catKey, itemId);
  ctx.session.calculando = { catKey, itemId };

  let pregunta = '';
  if (itemId === 'honorario_hora' || itemId === 'consulta_verbal') {
    pregunta = `⏱️ *Calculadora: ${item?.nombre || 'Por Hora'}*\n\nIngresa el *número de horas* trabajadas:\n\nEjemplo: \`3\` o \`1.5\``;
    ctx.session.calculando.tipo = 'horas';
  } else if (itemId === 'desahucio') {
    pregunta = `🏠 *Calculadora: Desahucio*\n\nIngresa el *valor mensual de la renta* en Lempiras:\n\nEjemplo: \`6500\``;
    ctx.session.calculando.tipo = 'desahucio';
  } else if (catKey === 'extra' && itemId === 'pct') {
    pregunta = `➕ *Calculadora: Porcentaje Adicional*\n\nIngresa el *monto de los honorarios principales* (del proceso base) en Lempiras:\n\nLuego te pediré el porcentaje (25% apelación o 30% casación).\n\nEjemplo: \`45000\``;
    ctx.session.calculando.tipo = 'pct_extra_base';
  } else {
    pregunta = `🔢 *Calculadora: ${item?.nombre || 'Honorarios'}*\n\nIngresa el *monto o cuantía* en Lempiras:\n\n_Sin puntos ni comas, solo números_\nEjemplo: \`150000\``;
    ctx.session.calculando.tipo = 'monto';
  }

  await ctx.reply(pregunta, { parse_mode: 'Markdown' });
}

async function procesarCalculo(ctx, valor) {
  const { catKey, itemId, tipo } = ctx.session.calculando;
  const item = getItem(catKey, itemId);
  ctx.session.calculando = null;

  let msg = `🔢 *Resultado del Cálculo*\n━━━━━━━━━━━━━━━━━━━━━━\n`;

  if (tipo === 'horas') {
    const total = Math.max(valor * 500, 500);
    msg += `⏱️ Horas: *${valor}*\n`;
    msg += `• L. 500 × ${valor} = *${fL(total)}*\n`;
    msg += `\n💰 *TOTAL: ${fL(total)}*\n`;

  } else if (tipo === 'desahucio') {
    const normal = Math.max(valor * 3, 6000);
    const mora = Math.max(valor * 0.30, 6000);
    msg += `🏠 Renta mensual: *${fL(valor)}*\n\n`;
    msg += `📊 *Caso Normal (3 meses de renta):*\n`;
    msg += `• 3 × ${fL(valor)} = ${fL(valor * 3)}\n`;
    msg += `• ✅ Aplicado mínimo: *${fL(normal)}*\n\n`;
    msg += `📊 *Con causal de falta de pago (30% mora):*\n`;
    msg += `• 30% de la mora acumulada (ingresa el valor total de la mora para cálculo exacto)\n`;
    msg += `• Mínimo: *L. 6,000*\n`;

  } else if (tipo === 'pct_extra_base') {
    ctx.session.calculando = { catKey, itemId, tipo: 'pct_extra_pct', base: valor };
    return ctx.reply(
      `➕ Base ingresada: *${fL(valor)}*\n\nAhora ingresa el *porcentaje adicional*:\n• \`25\` para Recurso de Apelación\n• \`30\` para Recurso de Casación\n• \`33\` para Apelación Contencioso-Adm.`,
      { parse_mode: 'Markdown' }
    );

  } else if (tipo === 'pct_extra_pct') {
    const base = ctx.session.calculando?.base || valor;
    ctx.session.calculando = null;
    const adicional = base * (valor / 100);
    const total = base + adicional;
    msg += `📊 Honorarios base: *${fL(base)}*\n`;
    msg += `• + ${valor}% = *${fL(adicional)}*\n`;
    msg += `\n━━━━━━━━━━━━━━━━━━━━━━\n`;
    msg += `💰 *TOTAL CON RECURSO: ${fL(total)}*\n`;

  } else if (item?.tipo === 'progresiva') {
    const { total, desglose } = calcProgresiva(valor, item.tarifa);
    msg += `💵 Cuantía: *${fL(valor)}*\n\n📊 *Desglose Progresivo:*\n`;
    for (const d of desglose) {
      msg += `\n• *${d.pct}%* sobre ${fL(d.base)}\n`;
      msg += `  = *${fL(d.hon)}*\n`;
    }
    msg += `\n━━━━━━━━━━━━━━━━━━━━━━\n`;
    msg += `💰 *HONORARIO MÍNIMO: ${fL(total)}*\n\n`;
    msg += `📌 *Recursos adicionales:*\n`;
    msg += `• + Apelación (25%): *${fL(total * 0.25)}* → Total: *${fL(total * 1.25)}*\n`;
    msg += `• + Casación (30%): *${fL(total * 0.30)}* → Total: *${fL(total * 1.30)}*\n`;

  } else if (item?.tipo === 'pct_ordinario') {
    const { total } = calcProgresiva(valor, ARANCEL.civil.items.find(i => i.id === 'ordinario_civil').tarifa);
    const honorario = total * (item.porcentaje / 100);
    msg += `💵 Cuantía: *${fL(valor)}*\n\n`;
    msg += `📊 Juicio Ordinario base: *${fL(total)}*\n`;
    msg += `• × ${item.porcentaje}% = *${fL(honorario)}*\n`;
    msg += `\n💰 *HONORARIO MÍNIMO: ${fL(honorario)}*\n`;

  } else if (item?.tipo === 'contrato') {
    const { total, desglose } = calcContrato(valor);
    msg += `💵 Valor del contrato: *${fL(valor)}*\n\n📊 *Desglose:*\n`;
    for (const d of desglose) msg += `• ${d.label}: *${fL(d.hon)}*\n`;
    msg += `\n💰 *HONORARIO MÍNIMO: ${fL(total)}*\n`;

  } else if (item?.tipo === 'conciliacion') {
    const conAcuerdo = Math.max(valor * (item.porcentaje / 100), 0);
    msg += `💵 Monto conciliado: *${fL(valor)}*\n\n`;
    msg += `✅ *Si hay acuerdo (${item.porcentaje}%):*\n`;
    msg += `• ${fL(valor)} × ${item.porcentaje}% = *${fL(conAcuerdo)}*\n\n`;
    msg += `❌ *Si NO hay acuerdo:* *${fL(item.sinAcuerdo)}*\n`;
    msg += `\n💰 *CON ACUERDO: ${fL(conAcuerdo)}*\n`;
    msg += `💰 *SIN ACUERDO: ${fL(item.sinAcuerdo)}*\n`;

  } else if (item?.tipo === 'laboral_ordinario') {
    const base = 2000;
    const pct = valor * 0.30;
    const patrono = valor * 0.20;
    msg += `💵 Monto condenado/reclamado: *${fL(valor)}*\n\n`;
    msg += `📊 *Si representa al trabajador:*\n`;
    msg += `• Presentación/Contestación: *${fL(base)}*\n`;
    msg += `• 30% de ${fL(valor)}: *${fL(pct)}*\n`;
    msg += `• ─────────────────────\n`;
    msg += `• *TOTAL: ${fL(base + pct)}*\n\n`;
    msg += `📊 *Si representa al patrono (que pierde):*\n`;
    msg += `• 20% de ${fL(valor)}: *${fL(patrono)}*\n`;

  } else if (item?.tipo === 'laboral_segunda') {
    const base = 2000;
    const pct = valor * 0.15;
    msg += `💵 Monto liquidado: *${fL(valor)}*\n\n`;
    msg += `• Fijo: *${fL(base)}*\n`;
    msg += `• 15% de ${fL(valor)}: *${fL(pct)}*\n`;
    msg += `\n💰 *TOTAL: ${fL(base + pct)}*\n`;

  } else if (item?.tipo === 'porcentaje') {
    const honorario = Math.max(valor * (item.porcentaje / 100), item.minimo || 0);
    msg += `💵 Monto: *${fL(valor)}*\n`;
    msg += `• ${item.porcentaje}% = *${fL(valor * item.porcentaje / 100)}*\n`;
    if (item.minimo && honorario === item.minimo) msg += `• ⚠️ Se aplica mínimo: *${fL(item.minimo)}*\n`;
    msg += `\n💰 *HONORARIO: ${fL(honorario)}*\n`;

  } else if (item?.tipo === 'porcentaje_adicional') {
    const adicional = valor * (item.porcentaje / 100);
    msg += `💵 Honorarios base: *${fL(valor)}*\n`;
    msg += `• + ${item.porcentaje}% = *${fL(adicional)}*\n`;
    msg += `\n💰 *TOTAL CON RECURSO: ${fL(valor + adicional)}*\n`;
  } else {
    msg += `💵 Monto: *${fL(valor)}*\n\nNo se encontró una fórmula específica para este ítem.\n`;
  }

  msg += `\n\n⚠️ _Honorarios mínimos según Arancel del CAH (La Gaceta N° 34,403, 2017)_`;

  await ctx.reply(msg, {
    parse_mode: 'Markdown',
    ...Markup.inlineKeyboard([
      [Markup.button.callback('🔄 Calcular Otro Monto', `calc:${catKey}:${itemId}`)],
      [Markup.button.callback('🔢 Calculadora General', 'calculadora')],
      [Markup.button.callback('🏠 Menú Principal', 'inicio')],
    ]),
  });
}

// ============================================================
// TEXTO LIBRE
// ============================================================

bot.on('text', async ctx => {
  const texto = ctx.message.text.trim();

  // Si está en proceso de cálculo
  if (ctx.session.calculando) {
    const tipo = ctx.session.calculando.tipo;

    // Manejo especial para porcentaje en cálculo adicional
    if (tipo === 'pct_extra_pct') {
      const pct = parseFloat(texto.replace(/[^0-9.]/g, ''));
      if (isNaN(pct) || pct <= 0 || pct > 100) {
        return ctx.reply('❌ Porcentaje inválido. Ingresa solo el número, ej: `25` o `30`', { parse_mode: 'Markdown' });
      }
      return procesarCalculo(ctx, pct);
    }

    // Monto numérico
    const val = parseFloat(texto.replace(/[^0-9.]/g, ''));
    if (isNaN(val) || val <= 0) {
      return ctx.reply('❌ Ingresa un número válido. Ejemplo: `150000`\n\nO escribe /menu para cancelar.', { parse_mode: 'Markdown' });
    }
    return procesarCalculo(ctx, val);
  }

  // Búsqueda directa
  if (texto.startsWith('/')) return;
  if (texto.length >= 3) await buscar(ctx, texto);
});

// ============================================================
// CALLBACKS
// ============================================================

bot.action('inicio', ctx => {
  ctx.answerCbQuery();
  return ctx.editMessageText(BIENVENIDA, { parse_mode: 'Markdown', ...teclado_principal() })
    .catch(() => ctx.reply(BIENVENIDA, { parse_mode: 'Markdown', ...teclado_principal() }));
});

bot.action('calculadora', ctx => {
  ctx.answerCbQuery();
  const msg = '🔢 *Calculadora de Honorarios*\n\nSelecciona el tipo de proceso o trámite para calcular:';
  return ctx.editMessageText(msg, { parse_mode: 'Markdown', ...teclado_calculadora() })
    .catch(() => ctx.reply(msg, { parse_mode: 'Markdown', ...teclado_calculadora() }));
});

bot.action('pdf', ctx => {
  ctx.answerCbQuery();
  return enviarPDF(ctx);
});

bot.action(/^cat:(.+)$/, ctx => {
  ctx.answerCbQuery();
  return mostrarCat(ctx, ctx.match[1]);
});

bot.action(/^item:(.+):(.+)$/, ctx => {
  ctx.answerCbQuery();
  return mostrarItem(ctx, ctx.match[1], ctx.match[2]);
});

bot.action(/^calc:(.+):(.+)$/, ctx => {
  ctx.answerCbQuery();
  return iniciarCalculo(ctx, ctx.match[1], ctx.match[2]);
});

// ============================================================
// ERRORES
// ============================================================

bot.catch((err, ctx) => {
  console.error(`[ERROR] ${ctx.updateType}:`, err.message);
  ctx.reply('❌ Ocurrió un error inesperado. Escribe /menu para volver al inicio.').catch(() => {});
});

// ============================================================
// INICIO DEL BOT
// ============================================================

const PORT = process.env.PORT || 3000;
const WEBHOOK_URL = process.env.WEBHOOK_URL;

// Siempre levantar servidor Express para satisfacer health checks (Koyeb/Render)
const express = require('express');
const app = express();
app.use(express.json());
app.get('/', (_, res) => res.send('✅ Arancel CAH Bot activo — Abg. Brayan Fernando Padilla Rodríguez'));
app.listen(PORT, () => console.log(`🚀 Servidor HTTP en puerto ${PORT}`));

if (process.env.NODE_ENV === 'production' && WEBHOOK_URL) {
  // Modo Webhook
  app.use(bot.webhookCallback(`/webhook/${BOT_TOKEN}`));
  bot.telegram.setWebhook(`${WEBHOOK_URL}/webhook/${BOT_TOKEN}`)
    .then(() => console.log(`✅ Webhook configurado: ${WEBHOOK_URL}`));
} else {
  // Modo Polling — para Koyeb Free / desarrollo local
  bot.launch({ dropPendingUpdates: true })
    .then(() => console.log('🤖 Bot iniciado en modo Polling'))
    .catch(err => console.error('❌ Error iniciando bot:', err));
}

process.once('SIGINT', () => bot.stop('SIGINT'));
process.once('SIGTERM', () => bot.stop('SIGTERM'));
