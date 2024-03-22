import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.lines import Line2D
from od_census_maps import parentesco_map, dis_map
from sector_maps import ocu_only_map, sect_map
from extended_survey import process_people_df, process_places_df, has_dis
from extended_survey import nivacad_posmap_fine

dest_map = {
    'Hogar': [
        # Hogar typos
        'hogar', 'hyogar', 'dhogar', 'hogara', 'hhogar', 'hogr', 'hoger',
        'hogar+', 'hogar.', 'gogar', 'hoagar', 'hoghar', 'hogar21',
        'hoagra', 'n/rhogar', 'el hogar', 'hogarhogar',
        'regreso a casa',

        # Actual places recovered to be home
        'monterrey', 'plan de ayala', 'luis garcia', 'segunda avenida',
        'septiembre', 'hdalgo', 'cerezo',
        'colinas de los encinos', 'lechuguilla', 'priv lerdo de tejada',
        'sta ana', 'rio cautin', 'odiseo',
        'monte rojo', 'perla', 'romero',
    ],

    'Trabajo': [
        # Trabajo typos
        'trabajo', 'trabjo', 'trabajo}', 'tabajo', 'trbajo', 'rtrabajo',
        'trebajo', 'trabsjo', '1trabajo', 'htrabajo', 'trabajo +',
        'trabajar', 'trabajo}1', 'terbajo', 'nrtrabajo', 'tarbajo',
        'al trabajo', 'de trabajo', 'empleo',

        # Work places
        'parque industrial escobedo', 'parque industrial', 'fabrica',
        'oficina', 'taller', 'taller mecanico',
        'empresa', 'visita negocio', 'molino', 'base', 'trabajo oficinas',
        'practicas', 'fabric', 'antiguo trabajo', 'otro trabajo', 'oficcina',
        'negocio', 'parque industrial finsa', 'presidencia'
    ],

    'Tienda/(Super)mercado': [
        'tienda',
        'tienda diaz', 'tienda departamental', 'tiendaa', 'detienda',
        'tienda de la esquina', 'tienda navarro', 'super tienda',
        'tienda dany', 'tienda autoservicios', 'tienda autoservicio',
        'tienda perlita', 'multitienda', 'una tienda',
        'tienda flor', 'tienda.',
        'tieda', 'tianda', 'tuenda', 'tiendita',

        'mercado', 'supermercado', 'mercado juarez', 'mercado de abastos',
        'mercado rodante',
        'super mercado', 'mercado de abasto', 'mercado estrella',

        'oxxo', 'oxoo', 'oxxo abasolo', 'oxxo piados', 'oxxo genaro',
        'tienda oxxo', 'oxxo san antonio',
        'six', 'tienda six',

        'soriana', 'rsoriana', 'sopriana',
        'soriana santa cruz', 'soriana huinala', 'soriana huinula',
        'hiper soriana', 'soriana santa rosa', 'soriana apodaca',
        'soriana tienda', 'soriana nogales', 'soriana puerta del sol',
        'soriana marne', 'soriana hiper escobedo',

        'aurrera', 'aurera', 'aurrer', 'b aurrera', 'b. aurrera', 'bodega',
        'bodega a', 'bodega au', 'bodega au.',
        'bodega aurrera',

        'super', 'siper', 'el super', 'al super', 'sumerca',

        'abarrotes', 'tienda abarrotes', 'tienda de abarrotes',
        'abarrotes mendez', 'tienda d abarrotes',
        'abarrotes juan', 'abarrotes el cabrito',

        'compras', 'comprasd', 'acompañar', 'compra', 'compraas',

        'fruteria', 'tortilleria', 'plaza', 'carniceria',
        'truteria', 'panaderia',
        'comercial', 'zapateria', 'ferreteria',

        'heb', 'heb sendero', 'heb lineal', 'heb lincon', 'heb contry',

        'walmart',

        'abarrotes clerety', 'abarrotes leo',

        'elektra', 'electra', 'centro comercial', 'plazita', 'cam',
        'plaza comercial', 'plaza sendero', 'plaza cam', 'plaza la fe',
        'plaza cendero la fe', 'inter plaza', 'plaza nte',
        'plaza patio lincon', 'plaza tegnologia', 'plaza perisur',
        'plaza garibaldi', 'plaza rosa', 'plaza fuentes',
        'la tiendita', 'mi tiendita',
        'seven', 'sevenip', 'zeven 7', '7 eleven', '7-eleven',
        'smart', 'mandado', 'pasteleria', 'dulceria', 'famsa',
        'mini super monualu', 'minisuper', 'super siete', 'super hugo',
        'super ayala', 'super mayin', 'mini super', 'super carnes',
        'merco', 'mercadia', 'mercadito', 'cto comercial', 'comercio',
        'mercdo',
        'carne', 'carniceria san juan', 'carniseria', 'carnes san juan',
        'carniceria la mayita',
        'cedis de coppel', 'coppel', 'copras',
        'sun mall public', 'sun small públic', 'sun mall', 'sun malll',
        'sun moll juarez',
        'elotes', 'fantasias miguel', 'her contry', 'surtirse', 'carhe',
        'refeaccionaria', 'autosonico',
        'paleteria michoacana', 'heladeria', 'polleria', 'modelorama',
        'mariscos dan', 'tortillas',
        'pizza litler', 'papeleria', 'refaccionaria', 'fruteria hidalgo',
        'del sol', 'parisina', 'mol', 'central abastos', 'placa sol',
        'auto zone', 'mall', 'valmar', 'palacio de hierro', 'madereria',
        'concretos escobedo', 'abastos', 'verduleria', 'tortileria',
        'agua fría', 'aurrera express', 'autoclimas santa rosa',
        'coopel juárez', 'costco', 'costco pharmacy', 'elektra cadereyta',
        'elotes anita', 'ferretería materiales san juan',
        'ferretería y materiales san juan', 'frutería', 'helados sultana',
        'mercadito domingo', 'mercado domingo', 'mercado juárez',
        'mercado oxxo', 'mercería', 'mini super ray', 'oxxo juárez',
        'oxxo pino suarez', 'oxxo progreso', 'panadería', 'papelería',
        'plaza del cercado', 'plaza e05', 'plaza esfera', 'plaza la misión',
        'plaza principal', 'plaza santiago', 'seven & leven',
        'super g ranchito', 'super gonzález', 'super ray', 'tienda de ropa',
        'tienda ranchito', 'werkstar', 'whirpool campos apodaca',
        'resuper ray', 'procelec', 'protec ge', 'pollos',
        'carnicería', 'celestica', 'cerca del suburbia', 'cherety',
        'comprar', 'el chalet comida', 'estanquillo kalin', 'femas servicios',
        'ficosa',
    ],

    'Escuela': [
        'escuela',
        'secundaria', 'kinder', 'universidad', 'prepa', 'preparatoria',
        'colegio', 'primaria', 'estudio', 'estudiar', 'estudios',
        'escula', '1escuela', 'rscuela', 'escuela}', 'Escuela', 'ecuela',
        'escuela.', 'n/rescuela',
        'facultad',
        'universidad mty', 'universidad uanl', 'universidad aunl',
        'unitec', 'univ mty',
        'colegio nacali', 'universidad autonoma',
        'guarderia', 'esc dora garza', 'escuela de electronica',
        'facultad medica',
    ],

    'Farmacia/Clínica/Hospital': [
        'hospital', 'hopital', 'doctors hospital', 'hospital clinica 6',
        'linica',
        'clinica', 'clinica 6', 'clinica 9', 'clinica 26', 'clinica 64',
        'clinica 7', 'clinica 15', 'clinica 35',
        'farmacia', 'farmacia benavides', 'farmacia guadalajara', 'farmasia',
        'farm guadalajara', 'guadalajara',
        'consulta', 'medico', 'centro medico',
        'imss', 'imss 24', 'ims', 'seguro imss', 'seguro', 'doctor',
        'centro de salud', 'cita medica',
        'dentista', 'consultorio', 'terapia', 'laboratorio', 'seguro 64',
        'similares',
        'citas', 'salud', 'rehabilitacion', 'medica', 'imms', 'cruz roja',
        'clínica 70', 'clínica san andrés', 'imss 14', 'imss 70',
        'unidad de especialidades medicas',
    ],

    'Otro hogar': [
        'visita', 'familiar', 'mama',
        'hogar hermana', 'hogar nieta', 'otro hogar', 'hogar familiar',
        'hogar de familiar',
        'visita}', 'vicita', 'vecina', 'novia', 'visita tia', 'visita hijo',
        'casa de mama', 'casa hijo', 'casa hija', 'casa de familia',
        'casa de amigo', 'casa hermana', 'casa de novia', 'casa amigo',
        'casa deb hijo', 'casa de su hijo',
        'casa familiar', 'casa fam', 'casa familia', 'casa mama',
        'casa del cuñado', 'casa cuñada',
        'casa de hermano', 'casa abuelo', 'casa de los suegros',
        'casa amiga', 'visita familiar',
        'familia', 'visita familia', 'un familiar', 'pasa por familiar',
        'familiares', 'colonia la loma', 'visita amiga',
        'casa de una amiga',
    ],

    'Recreativo': [
        'parque', 'paseo', 'restaurante', 'gym', 'cine', 'restaurant',
        'correr', 'a correr',
        'tacos pony', 'tacos', 'tacos los abuelos', 'tacos h',
        'puesto de carnitas', 'comer',
        'museo', 'recreacion', 'gimnasio', 'comida', 'ejercicio',
        'biblioteca',
        'pizzeria', 'pollo frito chiken', 'centro civico',
        'taqueria', 'parque sub', 'mariscos', 'albercas', 'club deportivo',
        'canchas', 'cabalgar', 'parque koloso', 'juego', 'spining',
        'pollo feliz', 'giomnasio', 'fonda', 'lonche', 'bar', 'bar aguaje',
        'fundidora', 'fiesta', 'pollo frito', 'caminar', 'mc donalds',
        'que pollo', 'carls junio', 'cars junir', 'parque de la huasteca',
        'cafe internet',
        'café', 'café sucursal marín', 'carnitas don chente',
        'mariscos los arenas', 'restaurante la cuchara'
    ],

    'Religioso': [
        'iglesia', 'capilla', 'iglesia ap', 'parroquia', 'templo',
    ],

    'Banco': [
        'banco', 'banco banjio', 'banco santander', 'atm', 'tramites',
        'tramite', 'cfe',
        'banorte', 'banorte universidad', 'sat', 'pago', 'pagos', 'cajero',
        'deposito', 'santander'
    ],

    'Otro': [
        'otro', 'en otro lugar',
        'estetica', 'panteon',
        'servicio', 'cita', 'dif', 'campo', 'insumos', 'parada de camion',
        'prestamo expres', 'estetica abigail', 'centro cum',
        'puesto', 'visita clientes', 'kalos', 'ayuntamiento',
        'buscar trabajo', 'smoll', 'rayos', 'contratar', 'palcio gobierno',
        'centro de monterrey', 'paraje morelos', 'estacion', 'apodaca centro',
        'sitio', 'trabajohogar', 'central camionera', 'presidnecia municipal',
        'lavanderia', 'somoil', 'purificadora', 'loteria', 'rloteria',
        'pesqueria nl', 'pesqueria', 'gasolineria', 'surtir', 'zona centro',
        'madnado', 'casa meir', 'recojer', 'ine', 'particulares',
        'gras', 'gas', 'personal', 'materno', 'entrevista',
        'centro comunitario', 'a buscar trabajo', 'convivio', 'humberto lobo',
        'vere centr', 'recoger', 'pago de servicio', 'presidencia municipal',
        'los fresnos', 'profeco', 'paseo la fe', 'ambulante', 'reunion',
        'ute', 'la normal', 'lamparas', 'rio catarina', 'centro de i',
        'comite', 'paquteria', 'telefonia', 'gas economico', 'centro mty',
        'san pedro garza garcía', 'suria', 'lugar tramite', 'apodaca',
        'destino', 'estafeta', 'capacitacion', 'cobrar', 'entrega',
        'transito', 'carrier d', 'casero', 'levanderia', 'rebeca cantu',
        'gasera', 'jardin', 'estancia', 'correos', 'vere centro', 'rosario',
        'solicitud', 'centro', 'centro monterrey', 'aldabas cavazos',
        'apec agua de riego', 'plan tierra propia',
    ]

}

motivos_map = {
    'Visita Enfermo': [
        'visitar amiga enferma', 'visita a un enfermo', 'visito a un enfermo',
        'cuida a su familia enferma', 'visitar a un familiar enfermo',
        'visitar un enfermo',
        'visitar familiar enfermo', 'cuidar a familiar enfermo',
        'cuidar a familiar enferma',
        'visita padre internado', 'visita hospital',
        'visitar a un familiar ven el hospital',
        'visitar familiar clínica 6', 'cuida a su papá en el hospital'
    ],

    'Visita': [
        'visita', 'visita a su papa', 'visitar familiares',
        'visitar a familiares', 'visita a un familiar',
        'visitar a un familiar', 'visita a familia', 'visitas',
        'visitar una hija', 'visita familiar', 'visita a familiar',
        'visitar una hermana', 'visitar una amiga', 'fui de visita',
        'visita a su hija', 'visitar a sus papas', 'visitar a sus hijos',
        'visitar a su mamá', 'visita esposo', 'visitar asu hija',
        'visitar asu hermana', 'visitar asu mamá', 'visitar asu abuelita',
        'visitar abuelita', 'visitar a su novia',
        'visitar casa de su mama', 'de visita',
        'va de visita a casa de la novia', 'visitar a su hija',
        'visita familiares', 'visitar a su hermana', 'visita a esposo',
        'visita a hijo',
        'visita hijot', 'visita hija', 'visita novia', 'visitar familiar',
        'visitar un familiar', 'visita a hija', 'visitar  a familiar',
        'visita abuela', 'visitar amiga', 'visita familia',
        'visita familiar esperar a que baje el tráfico para regresar a casa',
        'visita a familiares', 'visita amigio', 'visita amiga',
        'visita familiare', 'visita amigos', 'visitar a la mamá',
        'visitar a la abuela', 'visitar a la hermana', 'visitar personas',
        'visita a una amistad', 'visitar',
        'visitar a una heemana', 'visita a una amiga', 'visitar a su mama',
        'visitar a una amiga', 'visitar a sus padres', 'visitar a la prima',
        'visitar a su hijo y se queda el fin de semana con el',
        'visitar al abuela', 'visita al abuela',
        'visita acon una amiga', 'visita al abueka', 'visita a la abuela',
        'visita al familiar', 'visitar a la familia',
        'visita a su hijo', 'visitar a hijo', 'visitar un amigo',
        'visitar amigo',
        'visitar a su padre', 'visita a su mama', 'visita de familiar',
        'visito a su hijo', 'visitó a un familiar', 'visito a familia',
        'visito a un familiar', 'visitó otra casa', 'visitó a sus familiares',
        'vista', 'vicitar a familiar',
        'vicita', 'vicitar familia', 'familiar', 'casa familiar',
        'vicita familiar', 'vicitar',
        'ir a la casa de la hermana', 'casa de abuela', 'a casa de la abuela',
        'se fue a casa de su abuela', 'casa de su hija',
        'casa de su mama',  'casa de sus hermanas',
        'se fue a quedar con otro hijo',
        'vicitar a familia', 'vicitar personas',
        'vicitar a un paciente familiar', 'vicitar paciente conocido',
        'vicitar a personas',
        'vicita a sus nietos', 'vista a amigo', 'familia', 'vita a personas',
        'vivito a familiar', 'viasita', 'otro hogar',
        'ver a su mama', 'vivitar a su mama', 'vista familiar',
    ],

    'Panteón': [
        'visitar un familiar al panteón', 'visitar el panteón', 'panteon',
        'panteón', 'visitar panteon', 'visita al pantalón',
        'visita a panteón', 'visita a panteon'
    ],

    'Veterinario': [
        'llevar a su perro al veterinario',
        'llevando al perro a la veterinaria',
        'ir por el perro a la veterinaria',
        'visita veterinario', 'llevo al perro con el veterinario'
    ],

    'Religión': [
        'iglesia', 'ir a junta ala iglesia', 'ir a iglesia', 'reunión iglesia',
        'reunión de la iglesia', 'visita a la iglesia',
        'iglesia a dar gracias por cirugía', 'asistir a iglesia',
        'ir a la iglesia', 'junta iglesia',
        'fue a misa', 'misa de 7', 'misa', 'a misa', 'ir a misa',
        'fue a misa de las 5',
        'religión', 'religion', 'culto religioso', 'servicio religioso',
        'religioso', 'evento religioso',
        'actividad religiosa', 'acto religioso', 'pláticas religiosas',
        'predicar', 'orar', 'culto', 'rezo',
        'fue a una casa de oracion', 'rezor', 'escuchar la palabra de dios',
        'ayuda al sacerdote', 'rosario',
        'dirigir un rosario de la parroquia', 'estudio de biblia',
        'clases de biblia', 'oracion',
    ],

    'Pagos/Tramite/Banco/Cajero': [
        'pagos', 'pagos de venta de productos',
        'pago de servicio  y aclaracion',
        'hacer pagos', 'pago', 'pago de servicio',
        'pago de recibo de cfe', 'pago de servicios', 'pago de recibo',
        'pago telefono', 'pagos servicios', 'pagos otro',
        'pago de servicio de agua', 'pago de tel', 'un pago',
        'pagos de recibos',
        'pagos de recibo', 'hacer unos pagos',
        'banco pagos', 'pago recibos', 'pago de recibos', 'realizar  pagos',
        'checar pago de pensión', 'pagos servició',
        'pago servicios',
        'revisar si se bonifica el dinero que pago del recibo de telmex',
        'hacer pago de recibos',
        'dejar pago al banco', 'a hacer pagos', 'hacer un pago',
        'tramites', 'tramite', 'tramite personal', 'tramite de ine',
        'tramites dejar papeles', 'tramite legal', 'tramites banco',
        'pagó de pensión', 'pagar funeral', 'pagar servicio', 'pagar la luz',
        'pagar facturas', 'pagó recibos',
        'pagar servicios funerarios', 'pagar cable',
        'pagar el recibo del agua',
        'checar recibo de agua',
        'cajero', 'retirar dinero cajero automático', 'cajero de banco',
        'cobrar cajero', 'visita a cajero',
        'trámite', 'banco', 'trámites', 'banamex', 'retiro de efectivo',
        'papeleo', 'trámite personal',
        'ine', 'cuestiones bancarias', 'movimientos bancarios', 'movimientos',
        'treamites', 'movimiento bancario',
        'arreglar pensión', 'trámite bancario', 'retiro bancario',
        'cobrar banco', 'al banco', 'depositar en banco',
        'al banco a retirar el dinero',
        'retirar dinero del banco', 'trámite credencial de elector',
        'trámite en sucursal', 'trámites credencial de elector',
        'trámite de credencial elector', 'trámites de papelería de sat',
        'trámites ine', 'trámite de la credencial del ine',
        'darle continuidad a un trámite', 'trámite de licencia',
        'trámites de papelería', 'sacar efectivo', 'transferencia',
        'deposito', 'recibir envío de dinero', 'firmar papelería',
        'dejar incapacidades', 'arregar papeleria',
        'recojer apoyo', 'tamites', 'arreglar pasaporte mexicana',
        'retiro de dinero', 'firmar papeleria',
        'cobro de nómina', 'firmar papeleria cobrar pension', 'iva a la afore',
        'firma de divorcio', 'denuncia', 'cobrar(abonos)', 'trmites',
        'cobrar pensión', 'cobrar finiquito', 'por incapacidad',
        'va por la ife', 'sacar ife', 'aclaración de recibo de agua',
        'liquidacion', 'cobro de pencion', 'dejar abono',
        'hacer un cobro', 'sacar dinero', 'depositar dinero',
        'asuntos de papeleria', 'retirar dinero', 'pagoi'
    ],

    'Diligencias': [
        'dejar productos de su trabajo', 'llevar almuerzo a los hijos',
        'recoger despensa', 'dejar unas recetas de su esposo',
        'recoger medicamento', 'llevar lonche', 'dejar lonche', 'dejar lonch',
        'llevar almuerzo a sus hijos',
        'recoger papeleria',
        'llevar lonche escuela', 'dejar lonche a su hija',
        'llevar lonche a su hija', 'dejar lonche a nieto',
        'llevar lonche a la escuela',
        'llevo lonche a los niños', 'dejar lonch a hijo',
        'dejar lonch a hijo a la esc', 'llevo lonche', 'fue a dejar lonche',
        'lonche al esposo', 'dejar lonche escuela', 'llevar lonche a su hijo',
        'llevar lonche a su nieto', 'llevar lonch a la escuela',
        'recoger medicamento de su hijo', 'recoger medicamento de hijo',
        'llevar el lunch a su hija', 'llevar lunch a su hija',
        'por medicamento para su esposo', 'recoger medicamento para su esposo',
        'recoger medicamento de mamá',
        'recojer medicamento para su esposa',
        'recoger medicamentos para su esposa', 'hacer diligencias',
        'llevar almuerzo a su nieta', 'recoger ropa',
        'cobrar y dejar productos',
        'cobrar (abonos)', 'trasladar cosas',
        'recoger botes', 'llevó comida a su esposo', 'diligencia',
        'llevar almuerzo al niño', 'llevar alimentos', 'llevar loche',
        'revisar el recibe de telmex en oficinas', 'impresiones',
        'recoger auto',
        'arreglar asuntos', 'llevar ropa a su esposo',
        'recojer despensa', 'ir a dejar comida', 'taller checar su moto',
        'llevar la camioneta al taller mecánico', 'mecánico',
        'servicio mecánico', 'taller mecánico', 'llevar almuerzo',
        'dejar almuerzo',
        'préstamo', 'surtir mercancia', 'recoger camioneta con mecánico',
        'inscripción escuela', 'entrega de documentos', 'recoger mercancia',
        'cobrar y dejar productos que vende', 'recoger vehiculo',
        'recoger algo', 'surtir mercancías', 'dejar vehiculo',
        'entregar incapacidades', 'entrega', 'cobrar su renta',
        'recoger vehículo de mantenimiento', 'recoger apoyo de gobierno',
        'mantenimiento de vehiculo', 'compostura de su auto',
        'checar su auto en el taller mecánico', 'reparación de su auto',
        'mecanica',
    ],

    'Recreación': [
        'ejercicios', 'ejercicio', 'correr hacer ejercicio',
        'ejercicio caminar',
        'ejercicio gym', 'hacer ejercicio',
        'paseo caminata ejercicio', 'ejercicio correr', 'a ser ejercicio',
        'salio a jugar', 'salió a correr',
        'paseo', 'de paseo', 'caminar', 'gym', 'gimnasio', 'entrenar',
        'entrenamiento', 'comida con sus hijos',
        'entretenimiento', 'spa', 'biblioteca', 'caminata',
        'caminar por la colonia', 'caminar en el parque', 'salir a caminar',
        'caminata al parque', 'a caminar',
        'salió a caminar con su hija', 'salio', 'salir', 'divercion',
        'realizar deporte', 'tomar cafe con sus amigos',
        'platicar con los compañeros jubilados', 'ir a cenar', 'camibar',
        'jugar con sus amigos futbol', 'gim',
        'acondicionamiento físico', 'diversión', 'otro museo',
        'convivir con amigas', 'fiesta', 'asistir a juego fútbol',
        'gimnacio', 'juego de lotería', 'deportes', 'desfile', 'convivio',
        'pasear perro', 'esparcimiento',
    ],

    'Compras': [
        'fue al oxxo', 'compras medicamento', 'comprar tacos', 'compras',
        'pagos y  compras',
        'recorrer varios negocios de ventas en peny riel', 'oxxo', 'mandado',
        'salio al oxxo',
        'tienda', 'a la tienda', 'fue a la tienda', 'abarrotes', 'plaza',
        'por papelería',
    ],

    'Comer': [
        'comer', 'a comer con su esposo a su negocio', 'ir a comer',
        'comer a casa', 'a comer con su esposo', 'salió a comer',
        'viaje 2 se dirijio a comer a su vivienda',
        'regresa a trabajar tomo su tiempo para comer', 'a comer',
        'fue a comer',
        'salio a comer', 'regreso de comer', 'comer con su hermana',
        'salir a comer', 'salida a comer',
        'ir a dejar de comer a su esposo', 'regreso a comer', 'para comer',
        'fue a comer a casa', 'a comer a casa',
        'ir a comer a casa', 'comer en casa', 'fue a comer a su casa',
        'fueron a comer', 'comer negocios', 'comida',
        'lonche', 'desayuno', 'cena', 'hora de comida', 'lunch', 'lunche',
        'almuerzo', 'almorsar',
    ],

    'Otro': [
        'dejar decomer', 'llevo a sus vacas a comer pasto', 'personal',
        'asuntos personales', 'xx', 'xxx', 'asunto personal',
        'buscar trabajo', 'entrevista de trabajo', 'buscar empleo',
        'no dio dato', 'cruza de caballos', 'no quizo especificar',
        'funeral', 'velorio', 'entrevista', 'asunto familiar', 'cobrar',
        'junta escolar', 'descanso', 'reunion', 'estancia',
        'reunión', 'reunión para oración', 'reunión de cumpleaños',
        'reunión amigas', 'reunion de amigos en la plaza a jugar domino',
        'belleza', 'corte de pelo', 'entrevista trabajo',
        'entrevista de  trabajo', 'entrevista de trabajó',
        'entrevista de empleo',
        'revisar otra casa que tienen', 'solicitud de trabajo',
        'surtir material de trabajo', 'ver un clien te trabaja por su cuenta',
        'trabajo de uber', 'buscando trabajo', 'buscar trabjo',
        'checar un trabajo', 'busca trabajo', 'pasos',

        'no hay regreso habitante sale 23:30 y '
        'trasladarse a dejar camión urbano a taller de la '
        'ruta correspondiente se desocupa 1:40 am',

        'sale a predicar la biblia', 'se sentía mal de salud', 'cita',
        'capacitacion', 'cita de divorcio',

        'servicio funeral', 'platica', 'platica', 'problemas',
        'junta en la escuela', 'clases de tejido', 'junta sindical',
        'servicio de tintorería', 'translafarse a negoció de tacos a cosmoy',
        'viaje 2 regresa a cada al siguiente día', 'venta de productos',
        'hacer limpieza de terreno', 'vender y entregar borregos',
        'torre administrativa', 'regresa al siguiente día',
        'paquteria', 'aaunto familiar', 'compromiso personal',
        'motivos personales', 'lavar un carro', 'dif',

        'entregó un pedido de comida', 'entregar pedido de comida',
        'información de la presidencia', 'recolección pet',
        'ciber', 'ir parada de camion', 'parada camion',
        'que le compren el plástico', 'lavar', 'evento',
        'paquetria', 'junta de padres', 'hacer tarea en equipo',
        'limpieza de terreno', 'bailoterapia',
        'esperar transporte de personal',
        'cortarse el pelo', 'platicar', 'cargar gas', 'ensayo matachin',
        'anda buscando lugar en el kinder para su niño', 'ensayo',
        'junta en primaria', 'organizar boda', 'aprendizaje manual',
        'buscar leña', 'vigilancia', 'hechar gas', 'fue a la ciberia',
        'preguntar por la ayuda a las personas de la 3era edad',
        'platicas de estudios', 'fue de paso.', 'barber',
        'junta padres de familia', 'no quiso dar información',
        'investigacion para tarea', 'hacer tarea', 'no quiso decir',
        'cortar pelo', 'motivo personal', 'cortarce el pelo',
        'buscando empleo', 'escuchar informe de gobierno',
        'cortar cabello', 'coordinación', 'aclaraciones', 'particular',
        'estetica', 'apoyo al comedor',
        'tomar la ruta de camión que lo lleva a la prepa',
        'ver a amigo', 'recolecta de material fierro y plástico',
        'vender alimentos', 'da clases de inglés a domicilio',
        'apoyo', 'junta de sindicato', 'venta', 'no dijo', 'xxxx',
        'junta de pensionados', 'recolección de cartón y plástico',
        'recolección de plástico y carton', 'mantenimiento',
        'espiritual', 'sacar la basura', 'cabalgata', 'transporte escolar',
        'solicito empleo', 'busco empleo', 'material de cosméticos',
        'llega así auto. (conductor)', 'vende artículos para el hogares',
        'por seguridad no lo dirá', 'alimentar animales',
        'corte de cabello', 'grabación', 'recolectar de plástico',
        'platicas de parkinson', 'información', 'entrea de pedido',
        'informacion', 'junta de escuela de su nieto', 'ayuda de gobierno',
        'empeñar', 'centro', 'cuestiones personales', 'limpieza',
        'Otro',
    ],

    'Trabajo': [
        'ayuda en taller de costura', 'junta', 'regreso a la oficina',
        'regreso al trabajo', 'servicio', 'servicio social',
        'ventas', 'hacer servicio social', 'trabajo de un dìa',
        'regreso a trabajar', 'trabajo social', 'trabajo eventual',
        'dejar papelería para trabajar',
        'ayudar a su mamà en trabajo mercado sobre ruedas',
        'trabajo voluntario',
        'trabajo',
        'trabajar vendedor ambulante', 'practicas-facultad de medicina',
        'practica', 'practicas profesionales',
        'práctica profesional en hospital', 'práctica profesional',
        'prácticas profesionales', 'prácticas',
        'prácticas del estudio las hace en una empresa', 'servició social',
        'vende en mercado', 'venta en mercado sobré ruedas',
        'ayudar a su padres en el puesto', 'apoyar a hermano negocio',
        'venta en el mercado',
        'checar cuentas en negocio', 'dar clases', 'vender', 'venta en mercado',
        'vender su comida',
        'limpieza de vivienda', 'su hermana lo empleo para vender tacos',
        'regreso de comida', 'paquetero en tienda aurrera',
        'vender en el mercado',
    ],

    'Cuidar personas': [
        'al cuidado de vecina por consulta de su madre',
        'cuidar casa de su hijo', 'cuidar un familiar',
        'cuidar a su mama', 'cuidar persona',
        'cuidar a su madre durante la noche', 'a cuidar a su mama',
        'cuidar sobrinos', 'cuidar señora', 'cuidar nietos', 'cuidar asu mama',
        'cuidar a su esposa',
        'cuidado', 'cuidar a su abuelita'
    ],

    'Salud': [
        'consulta', 'terapia', 'sald', 'consulta medica', 'cita medica',
        'consulta médica', 'salud', 'rehabilitación',
        'terapias', 'rehabilitacion', 'le aplican insulina', 'consultá médica',
        'consultá', 'apoyo psicológico'
    ],

    'Hogar': [
        'comida en casa', 'hora de comida a casa',
        'regreso de traer a sus hijos', 'hogar',
    ],

    'acompañar / recoger': [
        'ir por el nieto a casa de su hijo',
        'ir por la mamá para llevarla a casa de ella',
        'llevar a su mamá a su casa',
        'dejar a su hijo en la escuela', 'dejar hijos escuela',
        'recoger hijos', 'recoger a hija', 'llevar a sus hijas a la escuela',
        'fue a dejar a su hija a la escuela', 'fue a buscar a su hija',
        'fue a dejar asu hijo a la escuela',
        'fue a recoger a su hijo', 'fue a dejar asu hijo ala escuela',
        'fue a buscar a su hijo', 'fue a dejar asu hija ala escuela',
        'regreso por su hija a la escuela',
        'fue a dejar a su hijo a la escuela',
        'traslado a su hija a terapias',
        'llevar almuerzo a su hijo', 'dejar a sus hijas a la escuela',
        'dejar a su hijo en el trabajo',
        'lllevo a sus hijos a la esc.', 'llevarr a su hijo a la sec.',
        'llevar a sus hijos a la esc.',
        'dejar a hija con abuelos', 'llevar a su hijo a guarderia',
        'escuela de hija', 'trabajo de mamá',
        'acompaña habitante 2', 'ir  por niño',
        'pasar por la hermana para ir soriana vallesoleado',
        'a dejar a su bebe encargada',
        'ir por su bebe', 'llevo a su niño al kinder', 'llevar niño al doctor',
        'llevar niño al dr.',
        'recoger', 'recoger a su niña', 'recoger a su niña de guardería',
        'recoger niños cioegio',
        'llevar por pension a su papá', 'lleva papa a la carretera',
    ],

    'Taxi/Uber': [
        'taxista', 'llevo pasaje a la clínica', 'es conductor de uber',
        'dejar pasaje', 'llevo a pasaje', 'dejo pasajero',
        'dejo a un pasaje',
    ],

    'Estudio': ['estudio', 'accesorias de materias', ],

}


def load_od(od_path):

    drop_cols = [
        'H-P', 'ID-HOGAR',
        # 'NunHabitante', 'Num_Viaje',
        #' NumVisita', 'TipoEnc', 'RealizoEnc',
        'Encuestador', 'Supervisor',
        # 'RefDom', 'Cod_EdoDomicilio',
        'Obs_ENCUESTA', 'Obs_Encuestador',
        'TodosEstan',

        # Derived, no longer used
        'genero', 'estudios', 'disc', 'tiempo_s', 'tiempo_m', 'tiempo_h',

        # Empty cols,
        'Discapacidad_O', 'ViajeAyer',  'Tiempo',
        'motivos',

        # Empty legs
        'M7_Transp', 'M7_TpoTranspordo', 'M7_TipoTransp', 'M7_Transp_O',
        'M7Tpo_Caminata', 'M7N_Ruta', 'M7_HHTpoParada', 'M7_MMTpoParada',
        'M7_HHTpoAbordo', 'M7_HHTpoAbordo_O', 'M7_MMTpoAbordo', 'M7_Pago',
        'M8_Transp', 'M8_TpoTranspordo', 'M8_TipoTransp', 'M8_Transp_O',
        'M8Tpo_Caminata', 'M8N_Ruta', 'M8_HHTpoParada', 'M8_MMTpoParada',
        'M8_HHTpoAbordo', 'M8_HHTpoAbordo_O', 'M8_MMTpoAbordo', 'M8_Pago',

        # Address columns
        # 'ColDom', 'CalleDom', 'NExtDom', 'NIntDom', 'CPDom',
        # 'Latitud', 'Longitud',

        # Adressess
        # 'RefOri', 'CalleOri', 'Esquina_Ori', 'Cruce_Ori', 'OtroEstadoOri',
        # 'OtroEstadoOri_O', 'CodOri',  'Cod_MunOri', 'Cod_EdoOri',
        # 'Cod_MunDest', 'ColDest', 'RefDest', 'CalleDest', 'Esquina_Dest',
        # 'Cruce_Dest', 'OtroEstadoDest', 'OtroEstadoDest_O',
        # 'CodDest', 'Cod_EdoDest', 'Cod_IDEdoDest', 'Cod_IDMunDest',
        # 'Cod_IDLocDest', 'Cod_LocDest', 'Cod_IDColDest',
        # 'Cod_ColDest', 'Cod_IDRefDest', 'Cod_RefDest',
        # 'Tiempo Tot de Viaje',
        # 'ColOri'
    ]

    rename_map = {
        'Cod_MunDomicilio': 'MUN', 'FE': 'FACTOR', 'Punto_zona': 'TAZ'
    }

    od = (
        pd.read_csv(od_path, low_memory=False)
        #.drop(columns=drop_cols)
        .rename(columns=rename_map)
    )

    # Fix some houshold typos and drop duplicated trips
    od['H-P-V'] = od['H-P-V'].replace(
        [
            '2418-+707/2-0', '403-623/1-2', '26861-6/4-0', '20474-12/1-1',
            '1012-777/1-2', '1012-777/1-4', '1012-777/1-6', '1012-777/1-3',
            '1012-777/1-5',
            '55424-20/2-2', '55424-20/2-3', '55424-20/2-4',
            '59822-3/1-1', '59822-3/2-1', '40401-2/1-1',
            '180-122/5-1', '180-122/5-2',
            '51598-6/2-2',
            '5933-310A/4-1', '5933-310A/4-2',
            '40311-10/0-0'
        ],
        [
            '2418-707/2-0', '403-626/1-2', '26861-6/1-0', '20474-12/1-0',
            'Drop', 'Drop', 'Drop', '1012-777/1-2',
            '1012-777/1-3',
            'Drop', '55424-20/2-2', 'Drop',
            '59822-3/1-0', '59822-3/2-0', '40401-2/1-4',
            'Drop', 'Drop',
            '51598-6/1-2',
            'Drop', 'Drop',
            '40311-10/3-0'
        ]
    )
    od = od[od['H-P-V'] != 'Drop']

    od[['HOGAR', 'HABITANTE', 'VIAJE']] = (
        od['H-P-V'].str.extract(
            "(?P<HOGAR>.+)\/(?P<HABITANTE>\d{1,2})-(?P<VIAJE>\d{1,2})$"
        )
    )
    od['HOGAR'] = od.HOGAR.str.strip().str.upper()
    od['HABITANTE'] = od['HABITANTE'].astype(int)
    od['VIAJE'] = od['VIAJE'].astype(int)

    # There is one 0 labeled inhabitant, remove
    # od = od.query('HABITANTE > 0')

    # od = od.drop(columns='H-P-V')
    # od['HOGAR'] = od.HOGAR.astype('category').cat.codes + 1
    od = od.set_index(['HOGAR', 'HABITANTE', 'VIAJE']).sort_index()

    # Drop duplicates
    od = od.drop(index=[
        ('11081-A-18', 3, 1),
        ('22894-12', 1, 5),
        ('23474-32', 2, 3),
        ('30325-6', 1, 3), ('30325-6', 1, 4),
        ('40534-14', 3, 3),
        ('47729-10', 2, 5), ('47729-10', 3, 3), ('47729-10', 5, 3),
        ('53623-2', 1, 3), ('53623-2', 3, 3),
        ('55424-20', 3, 3), ('55424-20', 3, 4)
    ])

    # Cleanup columns
    od['LineaTelef'] = od.LineaTelef.str.strip().replace('NO', 'No').fillna('No')
    od['Internet'] = od.Internet.str.strip().replace('NO', 'No').fillna('No')
    od['Género'] = od.Género.str.strip().replace(
        ['hombre', 'HOMBRE', 'mujer', 'MUJER'],
        ['Hombre', 'Hombre', 'Mujer', 'Mujer']
    )
    od['RelaciónHogar'] = od.RelaciónHogar.str.strip().replace(
        ['Jefe (a) de Familia', 'otro', 'Madre/esposa', 'Padre/esposo'],
        ['Jefe(a) de familia', 'Otro', 'Madre/Esposa', 'Padre/Esposo']
    )
    od['RelaciónHogar'] = od.RelaciónHogar.mask(
        od.RelaciónHogar == 'Otro',
        od.RelaciónHogar_O.str.strip()
    ).fillna('Otro')
    od = od.drop(columns='RelaciónHogar_O')
    od['RelaciónHogar'] = od.RelaciónHogar.replace(
        ['AMIGO (A)', 'N/P', 'Novia Unión Libre', 'Suegro(a)', 'pareja',
         'HERMANO (A)', 'NIETO (A)', ],
        ['Amigo (a)', 'Otro', 'Novia', 'Suegro (a)', 'Pareja',
         'Hermano (a)', 'Nieto (a)']
    )
    od['Discapacidad'] = od.Discapacidad.str.strip().replace(
        ['No aplica', 'Del oído', 'Inmovilidad de alguna parte'],
        ['Ninguna', 'Del Oído', 'Inmovilidad en alguna parte del cuerpo']
    )
    od['Estudios'] = od.Estudios.str.strip().replace(
        ['Primaria o secundaria', 'Sin Instrucción'],
        ['Primaria o Secundaria', 'Sin instrucción']
    )

    if 'motivo_original' in od.columns:
        od['Motivo'] = od.motivo_original.str.lower()
        od = od.drop(columns='motivo_original')
    else:
        od['Motivo'] = od.Motivo.str.lower()

    od['Motivo'] = od.Motivo.replace(
         'acompañar/ recoger', 'acompañar / recoger'
     )

    # Fix different survey dates for the same household
    # this causes trips that begin end at different dates
    # and degative stay durations
    od['FechaHoraEnc'] = od.groupby(['HOGAR']).FechaHoraEnc.transform('first')

    od['Hora Inicio V'] = pd.to_timedelta(
        od['Hora Inicio V'].apply(fix_time)
    )
    od['Hora Término Viaje'] = pd.to_timedelta(
        od['Hora Término Viaje'].apply(fix_time)
    )
    od['Tiempo Tot de Viaje'] = pd.to_timedelta(
        od['Tiempo Tot de Viaje'].apply(fix_time)
    )
    # Only 3 mismatches in the new OD,
    # for them to match
    od['Hora Término Viaje'] = od['Hora Inicio V'] + od['Tiempo Tot de Viaje']

    od['duracion'] = (
        od['Hora Término Viaje']
        - od['Hora Inicio V']
    )

    od['FechaHoraEnc'] = pd.to_datetime(od.FechaHoraEnc.apply(fix_date))
    od['fecha_inicio'] = (
        od['FechaHoraEnc']
        + od['Hora Inicio V']
    )
    od['fecha_termino'] = od['fecha_inicio'] + od['duracion']

    # od = od.drop(
    #         columns=['Hora Término Viaje', 'Hora Inicio V', 'FechaHoraEnc']
    # )

    # Fix wrong captured taz
    od.loc['2179-11', 'TAZ'] = 416
    od.loc['2180-S/N', 'TAZ'] = 416
    od.loc['2195-927', 'TAZ'] = 404
    od.loc['2457-231', 'TAZ'] = 573
    od.loc['2601-121', 'TAZ'] = 564
    od.loc['4029-137', 'TAZ'] = 978

    od['Lugar_Or'] = od.Lugar_Or.str.normalize('NFKD').str.lower().str.strip()
    od['LugarDest'] = od.LugarDest.str.normalize('NFKD').str.lower().str.strip()

    viv_cols = [
        'MUN', 'TAZ',
        'LineaTelef', 'Internet',
        'VHAuto', 'VHMoto', 'VHPickup', 'VHCamion', 'VHBici', 'VHPatineta',
        'VHPatines', 'VHScooter', 'VHOtro',
        'CHBaños', 'CHDormitorios',
        'Hab14masTrabajo', 'HabitantesTotal', 'HbitantesMayor6',
        'HbitantesMenor5',
    ]
    od[viv_cols] = od[viv_cols].fillna(0)

    # Replace wrong classes in origin, destination, purpose
    # Reduce number classes

    od['Origen'] = (
        od.Lugar_Or
        .replace(dest_map['Hogar'], 'Hogar')
        .replace(dest_map['Trabajo'], 'Lugar de Trabajo')
        .replace(dest_map['Tienda/(Super)mercado'], 'Tienda/(Super)mercado')
        .replace(dest_map['Escuela'], 'Escuela')
        .replace(
            dest_map['Farmacia/Clínica/Hospital'], 'Farmacia/Clínica/Hospital')
        .replace(dest_map['Otro hogar'], 'Otro hogar')
        .replace(dest_map['Recreativo'], 'Recreativo')
        .replace(dest_map['Religioso'], 'Otro')
        .replace(dest_map['Banco'], 'Otro')
        .replace(dest_map['Otro'], 'Otro')
    )

    od['Destino'] = (
        od.LugarDest
        .replace(dest_map['Hogar'], 'Hogar')
        .replace(dest_map['Trabajo'], 'Lugar de Trabajo')
        .replace(dest_map['Tienda/(Super)mercado'], 'Tienda/(Super)mercado')
        .replace(dest_map['Escuela'], 'Escuela')
        .replace(
            dest_map['Farmacia/Clínica/Hospital'], 'Farmacia/Clínica/Hospital')
        .replace(dest_map['Otro hogar'], 'Otro hogar')
        .replace(dest_map['Recreativo'], 'Recreativo')
        .replace(dest_map['Religioso'], 'Otro')
        .replace(dest_map['Banco'], 'Otro')
        .replace(dest_map['Otro'], 'Otro')
    )

    od['motivos'] = (
        od.Motivo_O.dropna().str.lower().str.strip()
        .replace(motivos_map['Visita Enfermo'], 'otro')
        .replace(motivos_map['Visita'], 'otro')
        .replace(motivos_map['Panteón'], 'otro')
        .replace(motivos_map['Veterinario'], 'otro')
        .replace(motivos_map['Religión'], 'otro')
        .replace(
            motivos_map['Pagos/Tramite/Banco/Cajero'],
            'Otro'
        )
        .replace(motivos_map['Recreación'], 'recreación')
        .replace(motivos_map['Compras'], 'compras')
        .replace(motivos_map['Comer'], 'otro')
        .replace(motivos_map['Otro'], 'otro')
        .replace(motivos_map['Diligencias'], 'otro')
        .replace(motivos_map['Trabajo'], 'trabajo')
        .replace(motivos_map['Cuidar personas'], 'otro')
        .replace(motivos_map['Salud'], 'salud')
        .replace(motivos_map['Hogar'], 'regreso a casa')
        .replace(motivos_map['acompañar / recoger'], 'acompañar / recoger')
        .replace(motivos_map['Taxi/Uber'], 'otro')
        .replace(motivos_map['Estudio'], 'estudios')
    )

    od.loc[
        od.Motivo == 'otro', 'Motivo'
    ] = od.loc[od.Motivo == 'otro', 'motivos']

    od['HabitantesObs'] = (
        od.reset_index()
        .groupby('HOGAR')
        .HABITANTE.transform('nunique').values
        )

    # purp of the origin for the first trip must be either
    # Home, Work, School or Other, adjust
    od.loc[(slice(None), slice(None), 1), 'Origen'] = (
        od.loc[(slice(None), slice(None), 1)]
        .pipe(
            lambda df: df.where(df.Origen.isin(['Hogar', 'Otro']), 'Hogar')
        ).Origen
    )

    return od


def fix_time(s):
    if isinstance(s, float) and np.isnan(s):
        return s

    sl = len(s)
    if sl == 5:
        return s + ':00'
    elif sl == 8:
        return s
    elif sl == 19:
        return s[-8:] + pd.to_timedelta('1 day')
    elif sl == 20:
        # This is low, but kept for backwards compatibility
        # with old versions of the survey
        return pd.to_datetime(s)
    else:
        print(sl)
        raise NotImplementedError


def fix_date(s):
    if '/' in s:
        d, m, y = s.split('/')
        return f'{y}-{m}-{d} 00:00:00'
    else:
        return s


def plot_trips(h, df):
    df = df.loc[h].reset_index()
    motivos_map = {
        'acompañar / recoger': 0,
        'compras': 1,
        'estudios': 2,
        'otro': 5,
        'recreación': 4,
        'regreso a casa': 3,
        'salud': 6,
        'trabajo': 7
    }

    cmap = mpl.colormaps['tab10']

    custom_lines = [
        Line2D([0], [0], color=cmap(v), lw=4)
        for v in motivos_map.values()
    ]

    max_hab = df.HABITANTE.max()

    plt.figure(figsize=(14, max_hab/2))

    for fecha in df.fecha_inicio.unique():
        plt.axvline(fecha, color='grey', ls='--', lw=1)
    for fecha in df.fecha_termino.unique():
        plt.axvline(fecha, color='grey', ls='--', lw=1)
    plt.hlines(
        df.HABITANTE,
        df.fecha_inicio,
        df.fecha_termino,
        lw=20, colors=cmap(df.Motivo.map(motivos_map))
    )
    plt.xticks(rotation=0)
    df_h = df.groupby('HABITANTE').first().reset_index()
    plt.yticks(
        df_h.HABITANTE,
        [
            f'{r.Género[0]}{r.Edad} {r.Ocupacion}, '
            f'{r.RelaciónHogar} ({r.HABITANTE})'
            for i, r in df_h.iterrows()
        ]
    )
    plt.ylim(0, df.HABITANTE.max() + 1)
    plt.legend(custom_lines, motivos_map.keys(), bbox_to_anchor=(1.01, 1))


def insert_trip(df, hogar, habitante, trip_num,
                motivo, modo, fecha_inicio, fecha_termino):
    """ Inserts a trip between existing trips.
    Automatically sets Origin Destination from prev and next trip.
    Must provide fecha inicio and termino, motivo y modo.
    """
    df = df.copy()

    df_hab = df.loc[(hogar, habitante)]

    # Find current trip number.
    new_trip = df.loc[(hogar, habitante, trip_num)].copy()
    new_trip.loc[['Lugar_Or', 'LugarDest']] = np.nan
    new_trip.loc[['ZonaOri']] = df_hab.loc[trip_num-1, 'ZonaDest']
    new_trip.loc[['ZonaDest']] = df_hab.loc[trip_num, 'ZonaOri']
    new_trip.loc[['Origen']] = df_hab.loc[trip_num-1, 'Destino']
    new_trip.loc[['Destino']] = df_hab.loc[trip_num, 'Origen']
    new_trip.loc[
        ['Motivo', 'Modo Agrupado', 'fecha_inicio', 'fecha_termino']
    ] = [motivo, modo, fecha_inicio, fecha_termino]
    new_trip.loc['duracion'] = new_trip.fecha_termino - new_trip.fecha_inicio

    # Renumber viajes
    df = df.reset_index()
    cond = (
        (df.HOGAR == hogar)
        & (df.HABITANTE == habitante)
        & (df.VIAJE >= trip_num)
    )
    df.loc[cond, 'VIAJE'] = df.loc[cond, 'VIAJE'] + 1
    df = df.set_index(['HOGAR', 'HABITANTE', 'VIAJE'])

    df.loc[(hogar, habitante, trip_num)] = new_trip

    return df.sort_index()


def fix_od_chains(trips):
    trips.loc[
        ('1020-26', 2, 2),
        ['ZonaOri', 'ZonaDest', 'Origen', 'Destino']
    ] = [431.0, 431.0, 'Otro', 'Hogar']

    trips.loc[
        ('134-2-009-34', 1, 2),
        ['ZonaOri', 'ZonaDest', 'Origen', 'Destino']
    ] = [620, 620, 'Otro', 'Otro']

    trips.loc[
        ('1342012-26', 2, 3), ['ZonaOri', 'ZonaDest', 'Origen', 'Destino']
    ] = [617, 206, 'Hogar', 'Otro']
    trips.loc[
        ('1342012-26', 2, 6), ['ZonaOri', 'ZonaDest', 'Origen', 'Destino']
    ] = [206, 203, 'Otro', 'Otro']

    trips.loc[
        ('1342012-8', 2, 2), ['ZonaOri', 'ZonaDest', 'Origen', 'Destino']
    ] = [206, 214, 'Otro', 'Otro']

    trips.loc[
        ('14493-6', 1, 1), ['ZonaOri', 'ZonaDest', 'Origen', 'Destino']
    ] = [404, 634, 'Hogar', 'Otro']
    trips.loc[
        ('14493-6', 1, 2), ['ZonaOri', 'ZonaDest', 'Origen', 'Destino']
    ] = [634, 404, 'Otro', 'Hogar']

    trips.loc[
        ('14525-10', 1, 1), ['ZonaOri', 'ZonaDest', 'Origen', 'Destino']
    ] = [406, 81, 'Hogar', 'Otro']
    trips.loc[
        ('14525-10', 1, 2), ['ZonaOri', 'ZonaDest', 'Origen', 'Destino']
    ] = [81, 406, 'Otro', 'Hogar']

    trips.loc[
        ('16167-20', 1, 1), ['ZonaOri', 'ZonaDest', 'Origen', 'Destino']
    ] = [421, 241, 'Hogar', 'Otro']
    trips.loc[
        ('16167-20', 1, 2), ['ZonaOri', 'ZonaDest', 'Origen', 'Destino']
    ] = [241, 421, 'Otro', 'Hogar']

    trips.loc[
        ('17841-14', 2, 4),
        ['ZonaOri', 'ZonaDest', 'Origen', 'Destino', 'Motivo']
    ] = [426, 426, 'Otro', 'Hogar', 'regreso a casa']

    trips.loc[
        ('17863-12', 1, 1), ['ZonaOri', 'ZonaDest', 'Origen', 'Destino']
    ] = [429, 372, 'Hogar', 'Otro']
    trips.loc[
        ('17863-12', 1, 2), ['ZonaOri', 'ZonaDest', 'Origen', 'Destino']
    ] = [372, 429, 'Otro', 'Hogar']

    trips.loc[
        ('17889-16', 3, 1), ['ZonaOri', 'ZonaDest', 'Origen', 'Destino']
    ] = [428, 4, 'Hogar', 'Otro']
    trips.loc[
        ('17889-16', 3, 2), ['ZonaOri', 'ZonaDest', 'Origen', 'Destino']
    ] = [4, 428, 'Otro', 'Hogar']

    trips.loc[
        ('17927-12', 1, 1), ['ZonaOri', 'ZonaDest', 'Origen', 'Destino']
    ] = [428, 238, 'Hogar', 'Otro']
    trips.loc[
        ('17927-12', 1, 2), ['ZonaOri', 'ZonaDest', 'Origen', 'Destino']
    ] = [238, 238, 'Otro', 'Hogar']

    trips.loc[('181-118', 5, 2), ['Origen']] = ['Escuela']

    trips.loc[
        ('18322-20', 3, 1), ['ZonaOri', 'ZonaDest', 'Origen', 'Destino']
    ] = [335, 221, 'Hogar', 'Otro']
    trips.loc[
        ('18322-20', 3, 2), ['ZonaOri', 'ZonaDest', 'Origen', 'Destino']
    ] = [221, 335, 'Otro', 'Hogar']

    trips.loc[('19880-8', 3, 4), ['fecha_inicio', 'fecha_termino']] = [
        pd.to_datetime('2019-09-18 17:40:00'),  # +00:00'),
        pd.to_datetime('2019-09-18 17:50:00')  # +00:00')
    ]

    # WARNING: This changes trip id here, but not in the tiplegs table.
    # FIXME TODO
    # trips = insert_trip(
    #             trips, '19880-8', 2, 4, 'regreso a casa', 'caminando',
    #             pd.to_datetime('2019-09-18 17:40:00+00:00'),
    #             pd.to_datetime('2019-09-18 17:50:00+00:00'),
    #            )

    # trips.loc[
    #     ('25161A-4', 1, 2), ['fecha_inicio', 'fecha_termino']
    # ] = trips.loc[
    #     ('25161A-4', 1, 2), ['fecha_inicio', 'fecha_termino']
    # ] + pd.to_timedelta('4 days')
    # trips.loc[
    #     ('25161A-4', 4, 2), ['fecha_inicio', 'fecha_termino']
    # ] = trips.loc[
    #     ('25161A-4', 4, 2), ['fecha_inicio', 'fecha_termino']
    # ] + pd.to_timedelta('4 days')

    trips.loc[
        ('25161A-4', 3, 2),
        ['ZonaOri', 'ZonaDest', 'Origen', 'Destino', 'Motivo']
    ] = [282, 282, 'Otro', 'Hogar', 'regreso a casa']
    trips.loc[
        ('28755-4', 4, 1), ['ZonaOri', 'ZonaDest', 'Origen', 'Destino']
    ] = [68, 204, 'Hogar', 'Otro']
    trips.loc[
        ('28755-4', 4, 2), ['ZonaOri', 'ZonaDest', 'Origen', 'Destino']
    ] = [204, 68, 'Otro', 'Hogar']

    trips.loc[
        ('34518-6', 2, 2), ['ZonaOri', 'ZonaDest', 'Origen', 'Destino']
    ] = [2, 5, 'Otro', 'Hogar']

    trips.loc['353-201', ['ZonaOri', 'ZonaDest']] = trips.loc[
        '353-201', ['ZonaOri', 'ZonaDest']
    ].replace(620, 621).values
    trips.loc[
        ('353-201', 4, 2), ['ZonaOri', 'ZonaDest', 'Origen', 'Destino']
    ] = [1, 621, 'Tienda/(Super)mercado', 'Hogar']

    trips.loc[
        ('35709-6', 2, 1), ['ZonaOri', 'ZonaDest', 'Origen', 'Destino']
    ] = [239, 221, 'Hogar', 'Otro']
    trips.loc[
        ('35709-6', 2, 2), ['ZonaOri', 'ZonaDest', 'Origen', 'Destino']
    ] = [221, 239, 'Otro', 'Hogar']

    trips.loc[
        ('42188-18', 2, 1), ['ZonaOri', 'ZonaDest', 'Origen', 'Destino']
    ] = [237, 221, 'Hogar', 'Otro']
    trips.loc[
        ('42188-18', 2, 2), ['ZonaOri', 'ZonaDest', 'Origen', 'Destino']
    ] = [221, 237, 'Otro', 'Hogar']

    trips.loc[
        ('42192-16', 3, 1), ['ZonaOri', 'ZonaDest', 'Origen', 'Destino']
    ] = [239, 754, 'Hogar', 'Otro']
    trips.loc[
        ('42192-16', 3, 2), ['ZonaOri', 'ZonaDest', 'Origen', 'Destino']
    ] = [754, 239, 'Otro', 'Hogar']

    trips.loc[
        ('42192-22', 1, 1), ['ZonaOri', 'ZonaDest', 'Origen', 'Destino']
    ] = [239, 706, 'Hogar', 'Otro']
    trips.loc[
        ('42192-22', 1, 2), ['ZonaOri', 'ZonaDest', 'Origen', 'Destino']
    ] = [706, 239, 'Otro', 'Hogar']

    trips.loc[
        ('42211-34', 3, 1), ['ZonaOri', 'ZonaDest', 'Origen', 'Destino']
    ] = [239, 706, 'Hogar', 'Otro']
    trips.loc[
        ('42211-34', 3, 2), ['ZonaOri', 'ZonaDest', 'Origen', 'Destino']
    ] = [706, 239, 'Otro', 'Hogar']

    trips.loc[
        ('45501-6', 2, 1), ['ZonaOri', 'ZonaDest', 'Origen', 'Destino']
    ] = [770, 606, 'Hogar', 'Otro']
    trips.loc[
        ('45501-6', 2, 2), ['ZonaOri', 'ZonaDest', 'Origen', 'Destino']
    ] = [606, 770, 'Otro', 'Hogar']

    trips.loc[
        ('58995-4', 4, 1), ['ZonaOri', 'ZonaDest', 'Origen', 'Destino']
    ] = [446, 715, 'Hogar', 'Otro']
    trips.loc[
        ('58995-4', 4, 2), ['ZonaOri', 'ZonaDest', 'Origen', 'Destino']
    ] = [715, 446, 'Otro', 'Hogar']

    trips.loc['6043-403', ['ZonaOri', 'ZonaDest']] = trips.loc[
        '6043-403', ['ZonaOri', 'ZonaDest']
    ].replace(107, 108).values
    trips.loc[('6043-403', 1, 2), 'Origen'] = 'Recreativo'
    trips.loc[('6043-403', 2, 2), 'Origen'] = 'Recreativo'

    trips.loc[
        ('9681-5', 2, 3), ['ZonaOri', 'ZonaDest', 'Origen', 'Destino']
    ] = [207, 87, 'Otro', 'Otro']


def check_od_chains(trips):
    # Check in prev destination is current origin
    # current orgin starts at trips > 2
    idxs = pd.IndexSlice
    cur_idx = trips.loc[idxs[:, :, 2:]].index
    prev_idx = pd.MultiIndex.from_arrays([
        cur_idx.get_level_values(0),
        cur_idx.get_level_values(1),
        cur_idx.get_level_values(2) - 1
    ])

    no_chain = (
        trips.loc[cur_idx].Origen != trips.loc[prev_idx].Destino.values
    ).pipe(lambda s: s[s].index.droplevel(2).unique())

    return no_chain


def check_overlap(df):
    idxs = pd.IndexSlice
    # Index for current trips (trip number > 2)
    cur_idx = df.loc[idxs[:, :, 2:]].index
    # index for previous trips
    prev_idx = pd.MultiIndex.from_arrays(
        [
            cur_idx.get_level_values(0),
            cur_idx.get_level_values(1),
            cur_idx.get_level_values(2) - 1
        ]
    )

    overlaps = (
        df.loc[cur_idx].fecha_inicio.values
        < df.loc[prev_idx].fecha_termino.values
    )

    return cur_idx[overlaps]#.droplevel(2).unique()


def get_purpose_tmat(trips, ignore=None):
    if ignore is not None:
        trips = trips.drop(index=ignore)
    trips = trips.copy()

    idxs = pd.IndexSlice
    cur_idx = trips.loc[idxs[:, :, 2:]].index
    prev_idx = pd.MultiIndex.from_arrays([
        cur_idx.get_level_values(0),
        cur_idx.get_level_values(1),
        cur_idx.get_level_values(2) - 1
    ])

    return pd.crosstab(
        trips.loc[prev_idx].Motivo.values,
        trips.loc[cur_idx].Motivo.values
    )


def index_next_trip(idx):
    nidx = pd.MultiIndex.from_arrays([
        idx.get_level_values(0),
        idx.get_level_values(1),
        idx.get_level_values(2) + 1
    ])

    return nidx


def index_prev_trip(idx):
    nidx = pd.MultiIndex.from_arrays([
        idx.get_level_values(0),
        idx.get_level_values(1),
        idx.get_level_values(2) - 1
    ])

    return nidx


def fix_home_loc(trips, hogar, habitante):

    idxs = pd.IndexSlice
    taz = trips.loc[(hogar, habitante, 1)].TAZ

    # Find wrong home from first trip
    if trips.loc[(hogar, habitante, 1), 'Origen'] == 'Hogar':
        wrong_taz = trips.loc[(hogar, habitante, 1), 'ZonaOri']
    elif trips.loc[(hogar, habitante, 1), 'Destino'] == 'Hogar':
        wrong_taz = trips.loc[(hogar, habitante, 1), 'ZonaDest']
    else:
        assert False, (hogar, habitante)

    # Replace all instances with true TAZ
    # WARNING. This assumes all zones with wrong taz are actually taz
    # This may not be true, and trips amons tazs may indeed ocurr.
    trips.loc[
        (hogar, habitante), ['ZonaOri', 'ZonaDest']
    ] = trips.loc[
        (hogar, habitante), ['ZonaOri', 'ZonaDest']
    ].replace(wrong_taz, taz).values

    # Replace Origen Destino home with true TAZ
    idx = trips.loc[(hogar, habitante)].query("Origen == 'Hogar'").index
    trips.loc[idxs[hogar, habitante, idx], 'ZonaOri'] = taz
    idx = trips.loc[(hogar, habitante)].query("Destino == 'Hogar'").index
    trips.loc[idxs[hogar, habitante, idx], 'ZonaDest'] = taz

    # Fix chains by backprogating next trip Origin to previous trip Destination
    # only if destination is not home, if home then propagate forward.
    # Iterating over all trips of the inhabitant
    # These are typically wrong by duplicating origen destino in the row
    # If this is the case, we keep the home as the true value and change the
    # other
    last_trip = trips.loc[(hogar, habitante, 1)]['last']
    # p_zorigen = trips.loc[(hogar, habitante, 1)].ZonaOri
    p_zdestino = trips.loc[(hogar, habitante, 1)].ZonaDest
    # p_origen = trips.loc[(hogar, habitante, 1)].Origen
    p_destino = trips.loc[(hogar, habitante, 1)].Destino
    for i in range(2, last_trip + 1):
        zorigen = trips.loc[(hogar, habitante, i)].ZonaOri
        # zdestino = trips.loc[(hogar, habitante, i)].ZonaDest
        origen = trips.loc[(hogar, habitante, i)].Origen
        # destino = trips.loc[(hogar, habitante, i)].Destino
        if zorigen != p_zdestino:
            # There is a chain problem
            # Is either home?
            assert origen != 'Hogar'
            assert p_destino != 'Hogar'

            # Is one is TAZ an the other is different from TAZ
            # keep the different one
            if zorigen != taz:
                z = zorigen
            elif p_zdestino != taz:
                z = p_zdestino
            else:
                assert False, "Not implemented."
            # Make the change
            trips.loc[(hogar, habitante, i-1), 'ZonaDest'] = z
            trips.loc[(hogar, habitante, i), 'ZonaOri'] = z

        # Update vars
        # p_zorigen = trips.loc[(hogar, habitante, i)].ZonaOri
        p_zdestino = trips.loc[(hogar, habitante, i)].ZonaDest
        # p_origen = trips.loc[(hogar, habitante, i)].Origen
        p_destino = trips.loc[(hogar, habitante, i)].Destino


def build_trips(od_df):
    # Get trip table
    trip_cols = [
        'TAZ',
        # 'HabitantesTotal',
        # 'Edad', 'Género', 'RelaciónHogar', 'Estudios',
        'Ocupacion',  # 'Ocupacion_O', 'SectorEconom', 'SectorEconom_O',
        'Lugar_Or', 'LugarDest',
        # 'Macrozona Origen', 'Macrozona Destino',
        'ZonaOri', 'ZonaDest',
        'Origen', 'Destino',
        'Motivo',
        # 'Motivo_O', 'motivos',
        'Modo Agrupado',
        'fecha_inicio', 'fecha_termino', 'duracion',
        # 'Tiempo Tot de Viaje', # same as duracion, verified
        # 'TipoEstacionamiento', 'TpoBusqueda', 'TpoEstacionadoHH',
        # 'TpoEstacionadoMM', 'CostoEstacionamiento',
        'FACTOR'
    ]

    # Legs columns
    m1_cols = [
        'M1_Transp',                     'M1_TipoTransp', 'M1_Transp_O',
        'M1Tpo_Caminata', 'M1N_Ruta', 'M1_HHTpoParada', 'M1_MMTpoParada',
        'M1_HHTpoAbordo', 'M1_HHTpoAbordo_O', 'M1_MMTpoAbordo', 'M1_Pago'
    ]
    m2_cols = [
        'M2_Transp', 'M2_TpoTranspordo', 'M2_TipoTransp', 'M2_Transp_O',
        'M2Tpo_Caminata', 'M2N_Ruta', 'M2_HHTpoParada', 'M2_MMTpoParada',
        'M2_HHTpoAbordo', 'M2_HHTpoAbordo_O', 'M2_MMTpoAbordo', 'M2_Pago'
    ]
    m3_cols = [
        'M3_Transp', 'M3_TpoTranspordo', 'M3_TipoTransp', 'M3_Transp_O',
        'M3Tpo_Caminata', 'M3N_Ruta', 'M3_HHTpoParada', 'M3_MMTpoParada',
        'M3_HHTpoAbordo', 'M3_HHTpoAbordo_O', 'M3_MMTpoAbordo', 'M3_Pago'
    ]
    m4_cols = [
        'M4_Transp', 'M4_TpoTranspordo', 'M4_TipoTransp', 'M4_Transp_O',
        'M4Tpo_Caminata', 'M4N_Ruta', 'M4_HHTpoParada', 'M4_MMTpoParada',
        'M4_HHTpoAbordo', 'M4_HHTpoAbordo_O', 'M4_MMTpoAbordo', 'M4_Pago'
    ]
    m5_cols = [
        'M5_Transp', 'M5_TpoTranspordo', 'M5_TipoTransp', 'M5_Transp_O',
        'M5Tpo_Caminata', 'M5N_Ruta', 'M5_HHTpoParada', 'M5_MMTpoParada',
        'M5_HHTpoAbordo', 'M5_HHTpoAbordo_O', 'M5_MMTpoAbordo', 'M5_Pago'
    ]
    m6_cols = [
        'M6_Transp', 'M6_TpoTranspordo', 'M6_TipoTransp', 'M6_Transp_O',
        'M6Tpo_Caminata', 'M6N_Ruta', 'M6_HHTpoParada', 'M6_MMTpoParada',
        'M6_HHTpoAbordo', 'M6_HHTpoAbordo_O', 'M6_MMTpoAbordo', 'M6_Pago'
    ]

    m_cols = m1_cols + m2_cols + m3_cols + m4_cols + m5_cols + m6_cols

    trips = od_df[trip_cols + m_cols].drop(0, level='VIAJE')
    # Save old index
    old_trip_idx = trips.reset_index(level='VIAJE').VIAJE

    trips = od_df[trip_cols + m_cols].drop(0, level='VIAJE').pipe(
        lambda df: (
            df.droplevel('VIAJE')
            .set_index(
                (
                    df.groupby(['HOGAR', 'HABITANTE']).cumcount() + 1
                ).rename('VIAJE'),
                append=True
            )
        )
    )

    legs_wide = trips[m_cols].copy()
    trips = trips.drop(columns=m_cols).copy()

    # First trips that do not begin home have unknown origin.
    # Checked by hand, all assignments make sense
    trips.loc[(slice(None), slice(None), 1), 'Origen'] = (
        trips.loc[(slice(None), slice(None), 1)]
        .pipe(
            lambda df: df.where(df.Origen.isin(['Hogar']), 'Otro')
        ).Origen
    )

    # Change destino del viaje anterior por actual valor
    # This enables chain checks and fixes
    old_idx = trips.loc[
        trips.Origen == 'el destino de viaje inmediato anterior'
    ].index
    new_idx = pd.MultiIndex.from_arrays(
        [
            old_idx.get_level_values(0),
            old_idx.get_level_values(1),
            old_idx.get_level_values(2) - 1
        ]
    )
    trips.loc[old_idx, 'Origen'] = trips.loc[new_idx, 'Destino'].values

    # Fix Nans, mostly by hand
    trips.loc[
        [('22899-4', 2, 2), ('36217-2', 1, 2)],
        'Destino'
    ] = 'Hogar'
    trips.loc[
        ('4819-703', 3, 1),
        ['Destino', 'Motivo']
    ] = ['Tienda/(Super)mercado', 'compras']
    trips.loc[
        ('4819-703', 3, 2),
        'Destino'
    ] = 'Hogar'
    trips.loc[
        (trips.Motivo.isna()) & (trips.Destino == 'Otro'),
        'Motivo'
    ] = 'otro'
    trips.loc[
        (trips.Motivo.isna()) & (trips.Destino == 'Lugar de Trabajo'),
        'Motivo'
    ] = 'trabajo'
    trips.loc[
        (trips.Motivo.isna()) & (trips.Destino == 'Tienda/(Super)mercado'),
        'Motivo'
    ] = 'compras'

    # Fix chains in Origen Destino
    # Also mostly by hand
    fix_od_chains(trips)
    # It is not posible to fix all
    # Some inhabitants are missing trips
    missing_trips = check_od_chains(trips)

    # Now that first trip origin is correct, and
    # trips are chained. We look at forbbiden transitions
    # in origin->destination and in trip purpose.

    # Trips from Home to Home
    home_to_home = trips.query("Destino == 'Hogar' & Origen == 'Hogar'")
    assert len(
        [i for i in home_to_home.index.droplevel(2) if i in missing_trips]
    ) == 0

    # If motivo == trabajo, change destino -> Lugar de Trabajo
    # and origin of next trip to lugar de trabajo
    home_to_home_tr = home_to_home.query("Motivo == 'trabajo'")
    trips.loc[home_to_home_tr.index, 'Destino'] = 'Lugar de Trabajo'
    trips.loc[
        index_next_trip(home_to_home_tr.index),
        'Origen'
    ] = 'Lugar de Trabajo'

    home_to_home = trips.query("Destino == 'Hogar' & Origen == 'Hogar'")
    assert np.all(check_od_chains(trips) == missing_trips)

    # For motivo acompañar / recoger, by hand fix
    trips.loc[
        ('42779-12', 2, slice(9, 10)),
        ['ZonaOri', 'ZonaDest', 'Origen', 'Destino']
    ] = [
        [231, 232, 'Hogar', 'Otro'],
        [232, 231, 'Otro', 'Hogar']
    ]
    home_to_home = trips.query("Destino == 'Hogar' & Origen == 'Hogar'")
    assert np.all(check_od_chains(trips) == missing_trips)

    # Other home-home trips seem to be walks or car short trips
    # that may be fine
    # Or dates seem weird, leave as is, but keep track of them
    home_to_home = trips.query("Destino == 'Hogar' & Origen == 'Hogar'")

    # Last trip number
    trips['last'] = trips.reset_index().groupby(
        ['HOGAR', 'HABITANTE']
    ).VIAJE.transform('max').values

    # Trips going home with a purpose not return to home
    to_home_other_purpose = trips.query(
        "Destino == 'Hogar' & Motivo != 'regreso a casa'"
    )

    # Trusting the chain of Origen Destino, we change purpose.
    # Most cases asre last trip anyway.
    # A few of them are not to Home TAZ, but home taz seems wrong,
    # need to check this further down
    # For now, change all
    (
        to_home_other_purpose.TAZ != to_home_other_purpose.ZonaDest
    ).pipe(lambda s: s[s].index)

    trips.loc[to_home_other_purpose.index, 'Motivo'] = 'regreso a casa'

    assert np.all(check_od_chains(trips) == missing_trips)

    # Trips with purpose return to home not going home
    to_home_not_home = trips.query(
        "Destino != 'Hogar' & Motivo == 'regreso a casa'"
    )

    # None of these is last trip
    # We can try to impute purpose based on destination
    # Destination Otro or Otro hogar, impute otro
    trips.loc[
        to_home_not_home.query(
            "Destino == 'Otro' | Destino == 'Otro hogar'"
        ).index,
        'Motivo'
    ] = 'otro'
    to_home_not_home = trips.query(
        "Destino != 'Hogar' & Motivo == 'regreso a casa'"
    )

    # People going to hospitals, checked manually
    trips.loc[
        to_home_not_home.query(
            "Destino == 'Farmacia/Clínica/Hospital'"
        ).index,
        'Motivo'
    ] = 'salud'
    to_home_not_home = trips.query(
        "Destino != 'Hogar' & Motivo == 'regreso a casa'"
    )

    # Students got to school to study, housewifes acompany
    trips.loc[
        to_home_not_home.query(
            "Destino == 'Escuela' & Ocupacion == 'Estudiante'"
        ).index,
        'Motivo'
    ] = 'estudios'
    trips.loc[
        to_home_not_home.query(
            "Destino == 'Escuela' & Ocupacion == 'Ama de casa'"
        ).index,
        'Motivo'
    ] = 'acompañar / recoger'
    trips.loc[
        to_home_not_home.query(
            "Destino == 'Escuela' & Ocupacion == 'Otro'"
        ).index,
        'Motivo'
    ] = 'otro'
    to_home_not_home = trips.query(
        "Destino != 'Hogar' & Motivo == 'regreso a casa'"
    )

    # Destino lugar de trabajo is work trip as per LugarDest
    trips.loc[
        to_home_not_home.query(
            "Destino == 'Lugar de Trabajo'"
        ).index,
        'Motivo'
    ] = 'trabajo'
    to_home_not_home = trips.query(
        "Destino != 'Hogar' & Motivo == 'regreso a casa'"
    )

    # Destino tienda is shopping trip as per LugarDest
    trips.loc[
        to_home_not_home.query(
            "Destino == 'Tienda/(Super)mercado'"
        ).index,
        'Motivo'
    ] = 'compras'
    to_home_not_home = trips.query(
        "Destino != 'Hogar' & Motivo == 'regreso a casa'"
    )

    # TODO. The following are a little more complicated
    # A trip to school that's not to study can be valid if
    # 1. Adult goes to work
    # 2. An adult acompanies a kid
    # 3. Adult goes to other such as a parent meeting.
    trips.query(
        "Destino == 'Escuela' "
        "& Motivo != 'estudios' "
        "& Motivo != 'acompañar / recoger'"
    ).Motivo.value_counts()

    # TODO Study trips that do not go to a School alse warrant investigation
    trips.query(
        "Destino != 'Escuela' & Motivo == 'estudios'"
    ).Destino.value_counts()

    # TODO Health trips not to a hospital or other
    trips.query("Motivo == 'salud'").Destino.value_counts()

    # Now we look at conflicting purpose chains
    # Lets get the pupose transition matrix, ignoring people with missing trips
    get_purpose_tmat(trips, ignore=missing_trips)
    # The regreso a hogar chained trips are the Hogar->Hogar trips,
    # which can happen OK

    # TODO How many small kids move alone?
    # Is there an adult that travels to the same location at the same time?
    # If so, should we assume Motivo == 'acompañar'?

    # Look at conflicting home locations, there seems to be some typos
    # Lat lon coordinates usually point at TAZ
    # Should we trust TAZ and change ZonaOri and ZonaDest for Home?
    trips.query(
        "(Destino == 'Hogar' & TAZ != ZonaDest) "
        "| (Origen == 'Hogar' & TAZ != ZonaOri)"
    ).shape

    habs = trips.groupby(['HOGAR', 'HABITANTE']).first().copy()

    habs['hogares'] = (
        trips.query("Destino == 'Hogar'")
        .groupby(['HOGAR', 'HABITANTE'])
        .ZonaDest.unique()
        .reindex(habs.index)
        .apply(
            lambda l: l.tolist() if isinstance(l, np.ndarray) else []
        )
        + trips.query("Origen == 'Hogar'")
        .groupby(['HOGAR', 'HABITANTE'])
        .ZonaOri.unique()
        .reindex(habs.index)
        .apply(
            lambda l: l.tolist() if isinstance(l, np.ndarray) else []
        )
    ).apply(np.unique)

    habs['n_hogares'] = habs.hogares.apply(len)

    habs['TAZ_in_hogares'] = [d in l for d, l in zip(habs.TAZ, habs.hogares)]

    habs.query('n_hogares > 1').shape
    habs.query('not TAZ_in_hogares').shape
    habs.query('n_hogares > 1 & not TAZ_in_hogares').shape
    habs_problems = habs.query('n_hogares > 1 | not TAZ_in_hogares').copy()
    assert len(
        [
            i for i in habs_problems.index.get_level_values(0)
            if i in missing_trips
        ]
    ) == 0

    for hogar, habitante in habs_problems.index:
        fix_home_loc(trips, hogar, habitante)

    trips['Modo Agrupado'] = trips['Modo Agrupado'].str.strip().str.lower()

    trips.loc[
        (trips.Motivo == 'estudios')
        & (trips['Modo Agrupado'] == 'modos combinados sin tpub'),
        'Modo Agrupado'] = [
        'transporte escolar',
        'transporte escolar',
        'uber, cabify , didi o similar',
        'transporte escolar',
        'transporte escolar',
        'transporte escolar',
        'transporte escolar',
        'tpub',
        'tpub',
        'tpub'
    ]

    trips_next_idx = trips.index.intersection(index_next_trip(trips.index))
    trips_prev_idx = index_prev_trip(trips_next_idx)
    trips['stay_duration_h'] = (
        trips.loc[trips_next_idx].fecha_inicio.values
        - trips.loc[trips_prev_idx].fecha_termino
    ).dt.total_seconds()/3600

    trips = trips.drop(columns='Ocupacion')

    return trips, legs_wide


def build_legs(legs_wide):

    m1_cols = [
        'M1_Transp',                     'M1_TipoTransp', 'M1_Transp_O',
        'M1Tpo_Caminata', 'M1N_Ruta', 'M1_HHTpoParada', 'M1_MMTpoParada',
        'M1_HHTpoAbordo', 'M1_HHTpoAbordo_O', 'M1_MMTpoAbordo', 'M1_Pago'
    ]
    m2_cols = [
        'M2_Transp', 'M2_TpoTranspordo', 'M2_TipoTransp', 'M2_Transp_O',
        'M2Tpo_Caminata', 'M2N_Ruta', 'M2_HHTpoParada', 'M2_MMTpoParada',
        'M2_HHTpoAbordo', 'M2_HHTpoAbordo_O', 'M2_MMTpoAbordo', 'M2_Pago'
    ]
    m3_cols = [
        'M3_Transp', 'M3_TpoTranspordo', 'M3_TipoTransp', 'M3_Transp_O',
        'M3Tpo_Caminata', 'M3N_Ruta', 'M3_HHTpoParada', 'M3_MMTpoParada',
        'M3_HHTpoAbordo', 'M3_HHTpoAbordo_O', 'M3_MMTpoAbordo', 'M3_Pago'
    ]
    m4_cols = [
        'M4_Transp', 'M4_TpoTranspordo', 'M4_TipoTransp', 'M4_Transp_O',
        'M4Tpo_Caminata', 'M4N_Ruta', 'M4_HHTpoParada', 'M4_MMTpoParada',
        'M4_HHTpoAbordo', 'M4_HHTpoAbordo_O', 'M4_MMTpoAbordo', 'M4_Pago'
    ]
    m5_cols = [
        'M5_Transp', 'M5_TpoTranspordo', 'M5_TipoTransp', 'M5_Transp_O',
        'M5Tpo_Caminata', 'M5N_Ruta', 'M5_HHTpoParada', 'M5_MMTpoParada',
        'M5_HHTpoAbordo', 'M5_HHTpoAbordo_O', 'M5_MMTpoAbordo', 'M5_Pago'
    ]
    m6_cols = [
        'M6_Transp', 'M6_TpoTranspordo', 'M6_TipoTransp', 'M6_Transp_O',
        'M6Tpo_Caminata', 'M6N_Ruta', 'M6_HHTpoParada', 'M6_MMTpoParada',
        'M6_HHTpoAbordo', 'M6_HHTpoAbordo_O', 'M6_MMTpoAbordo', 'M6_Pago'
    ]

    legs1 = legs_wide[m1_cols].rename(
        columns=lambda c: c.replace('M1', '').strip('_')
    )
    legs2 = legs_wide[m2_cols].rename(
        columns=lambda c: c.replace('M2', '').strip('_')
    )
    legs3 = legs_wide[m3_cols].rename(
        columns=lambda c: c.replace('M3', '').strip('_')
    )
    legs4 = legs_wide[m4_cols].rename(
        columns=lambda c: c.replace('M4', '').strip('_')
    )
    legs5 = legs_wide[m5_cols].rename(
        columns=lambda c: c.replace('M5', '').strip('_')
    )
    legs6 = legs_wide[m6_cols].rename(
        columns=lambda c: c.replace('M6', '').strip('_')
    )

    nan_vals = [
        0, False, '0',
        'no utilizó otro modo de transporte',
        'no utilizó otro modo de transporte',
        'no utilizo otro medio de transporte',
        'no utilizó otro medio de transporte',
    ]
    for legs in [legs1, legs2, legs3, legs4, legs5, legs6]:
        legs.loc[:, 'TipoTransp'] = (
            legs.loc[:, 'TipoTransp']
            .str.strip()
            .str.lower()
            .str.normalize('NFKD')
            .replace(nan_vals, np.nan)
            .replace('transporte público', 'público')
            .replace('vehículo particular', 'particular')
            .replace('a pie (caminando)', 'caminó')
            .replace('transpote por aplicación', 'transporte por aplicación')
        )

        legs.loc[:, 'Transp'] = (
            legs.loc[:, 'Transp']
            .str.strip()
            .str.lower()
            .str.normalize('NFKD')
            .replace(nan_vals, np.nan)
            .replace('autobús  suburbano', 'autobús suburbano')
            .replace(
                'uber, cabify , didi o similar',
                'uber, cabify, didi, o similar'
            )
        )
        legs['TpoAbordo'] = (
            legs[['HHTpoAbordo', 'HHTpoAbordo_O']].max(axis=1)*60
            + legs.MMTpoAbordo
        )
        legs['TpoParada'] = legs.HHTpoParada*60 + legs.MMTpoParada
        legs.drop(
            columns=[
                'HHTpoAbordo', 'HHTpoAbordo_O', 'MMTpoAbordo',
                'HHTpoParada', 'MMTpoParada'
            ],
            inplace=True
        )

    legs6 = legs6.dropna(subset='Transp')
    legs5 = legs5.dropna(subset='Transp')
    legs4 = legs4.dropna(subset='Transp')
    # Legs 4 have mislabeled walking legs
    legs4.loc[
        (legs4.Transp == 'a pie (caminando)')
        & legs4.TipoTransp.isna(),
        'TipoTransp'
    ] = 'caminó'
    # Legs 3 has a mislabled leg
    legs3.loc[
        legs3.Transp.notnull()
        & legs3.TipoTransp.isna(),
        'TipoTransp'
    ] = 'caminó'
    legs3 = legs3.dropna(subset='Transp')
    legs2 = legs2.dropna(subset='Transp')
    legs2.loc[('59928-4', 2, 2), 'TipoTransp'] = 'otro modo'
    legs2 = legs2.dropna(subset='TipoTransp')
    legs2 = legs2.drop(index=('35090-30', 2, 2))

    # For Legs1, many legs seem
    # to mix walk first leg to
    # another mode, reported in TipoTransp
    cond = (
        (legs1.Transp == 'a pie (caminando)')
        & (legs1.TipoTransp == 'otro modo')
        & (legs1.TpoAbordo == 0)
    )
    legs1.loc[cond, 'TipoTransp'] = 'caminó'

    cond = (
        (legs1.Transp == 'a pie (caminando)')
        & (legs1.TipoTransp == 'otro modo')
        & (legs1.TpoAbordo > 0)
    )
    legs1.loc[cond, 'Transp'] = 'otro'

    # return legs1, legs2, legs3, legs4, legs5, legs6

    # nnans = legs6.replace(nan_cols, np.nan).T.isna().sum()
    # legs6 = legs6[(nnans < 12)].copy()
    # return legs6

    # nnans = legs5.replace(nan_cols, np.nan).T.isna().sum()
    # legs5 = legs5[(nnans < 11)].copy()

    # nnans = legs4.replace(nan_cols, np.nan).T.isna().sum()
    # legs4 = legs4[(nnans < 12)].copy()

    # nnans = legs3.replace(nan_cols, np.nan).T.isna().sum()
    # legs3 = legs3[(nnans < 11)].copy()

    # legs2 = legs2.query(
    #     "Transp != 'No utilizó otro medio de transporte'"
    # ).copy()

    legs1 = legs1.assign(TRAMO=1).set_index('TRAMO', append=True)
    legs2 = legs2.assign(TRAMO=2).set_index('TRAMO', append=True)
    legs3 = legs3.assign(TRAMO=3).set_index('TRAMO', append=True)
    legs4 = legs4.assign(TRAMO=4).set_index('TRAMO', append=True)
    legs5 = legs5.assign(TRAMO=5).set_index('TRAMO', append=True)
    legs6 = legs6.assign(TRAMO=6).set_index('TRAMO', append=True)

    legs = pd.concat(
        [legs2, legs3, legs4, legs5, legs6, legs1],
        axis=0
    ).sort_index()

    legs['Transp'] = legs.Transp.str.strip().replace(
        [
            'taxi', 'Caminó', 'Autobús foráneo', 'Automóvil (Pasajero)',
            'Automóvil (conductor)', 'Metro Enlace',
            'Automóvil\xa0(Conductor)', 'Automóvil\xa0(pasajero)',
            'Motocicleta (conductor)', 'Uber, Cabify, Didi, o similar',
            'Autobús  Suburbano', 'Transporte de personal',
        ],
        [
            'Taxi', 'A pie (caminando)', 'Autobús Foráneo',
            'Automóvil (pasajero)', 'Automóvil (Conductor)', 'Metro enlace',
            'Automóvil (Conductor)', 'Automóvil (pasajero)',
            'Motocicleta (Conductor)', 'Uber, Cabify , Didi o similar',
            'Autobús Suburbano', 'Transporte de Personal'
        ]
    ).replace(
        [
            'A pie (caminando)', 'Uber, Cabify , Didi o similar',
            'Automóvil (Conductor)', 'Automóvil (pasajero)',
            'Autobús Suburbano', 'Camión Urbano', 'Ecovía', 'Metrobús',
            'Metrorrey', 'Microbús', 'Transmetro',
            'Transporte Público', 'Metro enlace',
            'Motocicleta (Conductor)', 'Motocicleta (pasajero)', 'Bicicleta',
            'Autobús Foráneo', 'Otro'
        ],
        [
            'caminando', 'app', 'auto', 'auto',
            'TPUB', 'TPUB', 'TPUB', 'TPUB', 'TPUB', 'TPUB', 'TPUB',
            'TPUB', 'TPUB',
            'moto', 'moto', 'bici',
            'otro', 'otro'
        ]
    )

    return legs


def get_educ_asi(r):
    educ = r.EDUC
    edad = r.Edad
    if r.ASISTEN == 0:
        return 'Blanco por pase'
    if educ == 'Sin Educación':
        return 'Básica'
    elif educ == 'Básica':
        if edad <= 14:
            return 'Básica'
        else:
            return 'MediaSup'
    elif educ == 'MediaSup':
        if edad < 18:
            return 'MediaSup'
        else:
            return 'Superior'
    elif educ == 'Superior':
        return 'Superior'
    else:
        raise NotImplementedError


def build_people_table(od_df, trips):
    people_cols = [
        'MUN', 'TAZ', 'Género', 'Edad', 'RelaciónHogar', 'Discapacidad',
        'Estudios', 'Estudios_O', 'Ocupacion', 'Ocupacion_O',
        'SectorEconom', 'SectorEconom_O',
        # 'FACTOR',
    ]

    # Agregate the people table, trust first variables
    people = od_df[people_cols].groupby(['HOGAR', 'HABITANTE']).first().copy()
    people['Ocupacion'] = people.Ocupacion.str.strip().str.lower()

    # Auxiliary dataframe to find conflicting people values
    conf_people = (
        od_df
        .reset_index(level=2)[people_cols]
        .groupby(['HOGAR', 'HABITANTE'])
        .nunique()
    )

    # Género -> SEXO
    people['SEXO'] = people.Género.map({'Mujer': 'F', 'Hombre': 'M'})
    people = people.drop(columns='Género')

    # Edad -> EDAD
    people['EDAD'] = pd.cut(
        people.Edad,
        (0, 3, 5, 6, 8, 12, 15, 18, 25, 50, 60, 65, 131),
        right=False,
        labels=[
            '0-2', '3-4', '5', '6-7', '8-11', '12-14', '15-17', '18-24',
            '25-49', '50-59', '60-64', '65-130'
        ]
    )

    # RelacionHogar -> PARENTESCO
    # This variable is not required by the model,
    # but matches CENSUS, used for imputation

    # Fix duplicated and missing Jefe de Familia in RELACION HOGAR
    is_head_idx = od_df.reset_index(level=2).loc[
        (conf_people > 1).T.sum() > 0,
        people_cols
    ].query('RelaciónHogar == "Jefe(a) de familia"').index
    people.loc[is_head_idx, 'RelaciónHogar'] = 'Jefe(a) de familia'

    # Find vive solo, if first inhabitante change to jefe,
    # else change to Sin parentesco
    people.loc[
        (
            (people.RelaciónHogar == 'Vive solo(a) / Independiente')
            & (people.index.get_level_values(1) == 1)
        ),
        'RelaciónHogar'
    ] = 'Jefe(a) de familia'

    people.loc[
        (
            (people.RelaciónHogar == 'Vive solo(a) / Independiente')
            & (people.index.get_level_values(1) > 1)
        ),
        'RelaciónHogar'
    ] = 'Otro'

    # Remap
    for k, v in parentesco_map.items():
        people['RelaciónHogar'] = people.RelaciónHogar.replace(v, k)
    people['PARENTESCO'] = people.RelaciónHogar.replace(
        'No especificado', np.nan
    )
    people = people.drop(columns='RelaciónHogar')

    # Note, Jefe can be missing in OD, since households are not complete.
    # Found 4 missing jefes
    # Just one Jefe is recovered

    # Discapacidad -> DIS
    people['DIS'] = people.Discapacidad.map(dis_map)
    people = people.drop(columns='Discapacidad')

    # Estudios -> EDUC
    people.loc[
        people.Estudios == 'Otro',
        'Estudios'
    ] = people.loc[people.Estudios == 'Otro', 'Estudios_O']
    people['EDUC'] = (
        people.Estudios
        .replace(
            ['Sin instrucción', 'Preescolar', 'Sin Educación'],
            'Sin Educación'
        )
        .replace('Primaria o Secundaria', 'Básica')
        .replace(
            ['Carrera técnica o preparatoria', 'Preparatoria Trunca'],
            'MediaSup'
        )
        .replace(
            [
                'Licenciatura', 'Postgrado',
                'Carrera de Química Trunca', '4 Semestres facultad'
            ],
            'Superior'
        )
        .replace(['Educación Especial', 'Esc especial'], 'Sin Educación')
        .replace(['No dio información', 'N/P', None], np.nan)
    )
    people['EDUC2'] = (
        people.Estudios
        .replace(
            ['Sin instrucción', 'Preescolar', 'Sin Educación'],
            'Sin Educación'
        )
        .replace('Primaria o Secundaria', 'Básica')
        .replace(
            ['Carrera técnica o preparatoria', 'Preparatoria Trunca'],
            'MediaSup'
        )
        .replace(
            [
                'Licenciatura',
                'Carrera de Química Trunca', '4 Semestres facultad'
            ],
            'Licenciatura'
        )
        .replace(['Educación Especial', 'Esc especial'], 'Sin Educación')
        .replace(['No dio información', 'N/P', None], np.nan)
    )

    # ASISTEN
    # People who have student as ocupation or that realize a study trip
    people['ASISTEN'] = 0
    idx_study_trips = (
        trips.query("Motivo == 'estudios'")
        .index.droplevel(2).unique()
    )
    people.loc[idx_study_trips, 'ASISTEN'] = 1
    people.loc[people.Ocupacion == 'estudiante', 'ASISTEN'] = 1
    # NOTE: There are still several inconsistencies
    # regarding trips start and end times and stay duration.
    # This make identifying part time students hard.
    # We can try to using stay_duration_h but this information
    # is not in the census.
    # As an alternative we can look at the ocupations status.
    # Workers that study can be classified into part time students depending
    # on the working hours.
    # Need to look at the distribution of those varibales in census.

    # TAZ_ASI
    # TAZ where they attend school
    # 15 inhabitants have two different destination zones for study trip.
    # Choose first arbitrarly
    idx_study_trips = trips.query("Motivo == 'estudios'").index
    taz_asi = (
        trips.loc[idx_study_trips, 'ZonaDest']
        .groupby(['HOGAR', 'HABITANTE']).first()
    )
    people['TAZ_ASI'] = 'Blanco por pase'
    people.loc[people.ASISTEN == 1, 'TAZ_ASI'] = np.nan
    people.loc[taz_asi.index, 'TAZ_ASI'] = taz_asi

    # EDUC_ASI
    # EDUC reports maximum completed education level.
    # Current atending level must be estimated.
    people['EDUC_ASI'] = 'Blanco por pase'
    people['EDUC_ASI'] = people.apply(get_educ_asi, axis=1)

    # TIE_TRASLADO_ESCU
    people['TIE_TRASLADO_ESCU'] = 'Blanco por pase'
    people.loc[people.ASISTEN == 1, 'TIE_TRASLADO_ESCU'] = np.nan
    idx_study_trips = trips.query("Motivo == 'estudios'").index
    duracion_cat = pd.cut(
        (
            (trips.loc[idx_study_trips, 'duracion'].dt.total_seconds()/60)
            .groupby(['HOGAR', 'HABITANTE']).max()
        ),
        [-1, 15, 30, 60, 120, 1e6],
        labels=[
            'Hasta 15 minutos', '16 a 30 minutos', '31 minutos a 1 hora',
            'Más de 1 hora y hasta 2 horas', 'Más de 2 horas'
        ],
        right=True,
    )
    people.loc[duracion_cat.index, 'TIE_TRASLADO_ESCU'] = duracion_cat

    people = people.drop(columns=['Estudios', 'Estudios_O'])

    # MED_TRASLADO_ESC TODO
    # This columns is realy not usefull.
    # We should keep all the used modes as in the census
    # First need to finish preprocessing the legs table.
    med_traslado_esc = (
        trips.query("Motivo == 'estudios'")['Modo Agrupado']
        .replace(
            ['automóvil (pasajero)', 'automóvil (conductor)'],
            'Automóvil o camioneta'
        )
        .replace('bicicleta', 'Bicicleta')
        .replace('a pie (caminando)', 'Caminando')
        .replace('motocicleta', 'Motocicleta o motoneta')
        .replace('uber, cabify , didi o similar', 'Taxi (App Internet)')
        .replace('taxi', 'Taxi (sitio, calle, otro)')
        .replace('transporte escolar', 'Transporte escolar')
        .replace(['tpub', 'modos combinados con tpub'], 'TPUB')
        .replace(['otro', 'transporte de personal'], 'Otro')
    )

    people['SectorEconom'] = (
        people.SectorEconom
        .str.lower().str.strip()
        .replace('servicio', 'servicios')
        .replace('transporte y comunicación', 'transporte y comunicaciones')
    )
    people['SectorEconom_O'] = (
        people.SectorEconom_O
        .str.lower().str.strip()
    )
    people['Ocupacion_O'] = (
        people.Ocupacion_O
        .str.lower().str.strip()
    )
    people['Ocupacion'] = (
        people.Ocupacion
        .str.lower().str.strip()
        .replace('sin instrucción', 'sin empleo')
        .replace(
            'profesionista independiente',
            'trabajador(a) por cuenta propia'
        )
    )

    people.loc[
        (
            (people.Ocupacion == 'ama de casa')
            & (people.SectorEconom == 'otro')
        ),
        'SectorEconom_O'
    ] = None
    people.loc[people.Ocupacion_O == 'no aplica', 'Ocupacion_O'] = None

    people.loc[
        (people.Ocupacion != 'otro') & people.Ocupacion_O.notnull(),
        ['Ocupacion', 'Ocupacion_O', 'SectorEconom', 'SectorEconom_O']] = [
        ['empleado (a)', None, 'servicios', None],
        ['jubilado', None, 'otro', None],
        ['empleado (a)', None, 'servicios', None],
        ['profesionista empleado', None, 'servicios', None]
    ]

    people.loc[
        (
            (people.SectorEconom != 'otro')
            & people.SectorEconom_O.notnull()
        ),
        'SectorEconom_O'
    ] = None

    people.loc[
        (
            (people.Ocupacion_O == 'empleado (a)')
        ),
        ['Ocupacion', 'Ocupacion_O']
    ] = ['empleado (a)', None]

    people.loc[
        people.Ocupacion_O.astype(str).str.contains('taxi'),
        ['Ocupacion', 'Ocupacion_O', 'SectorEconom', 'SectorEconom_O']
    ] = [
        'trabajador(a) por cuenta propia', None,
        'transporte y comunicaciones', None
    ]

    people.loc[
        people.Ocupacion_O.astype(str).str.contains('uber'),
        ['Ocupacion', 'Ocupacion_O', 'SectorEconom', 'SectorEconom_O']
    ] = [
        'trabajador(a) por cuenta propia', None,
        'transporte y comunicaciones', None
    ]

    people.loc[
        (
            (people.Ocupacion == 'otro')
            & (people.SectorEconom == 'transporte y comunicaciones')
        ),
        ['Ocupacion', 'Ocupacion_O', 'SectorEconom', 'SectorEconom_O']
    ] = ['empleado (a)', None, 'transporte y comunicaciones', None]

    people.loc[
        people.Ocupacion_O.isin(['campesino', 'ejidatario']),
        ['Ocupacion', 'Ocupacion_O', 'SectorEconom', 'SectorEconom_O']
    ] = [
        'trabajador(a) por cuenta propia',
        None, 'agricultura y ganadería', None
    ]

    people.loc[
        (
            (people.Ocupacion == 'otro')
            & (people.SectorEconom == 'gobierno')
        ),
        ['Ocupacion', 'Ocupacion_O', 'SectorEconom', 'SectorEconom_O']
    ] = ['empleado (a)', None, 'gobierno', None]

    people.loc[
        people.Ocupacion_O == 'negocio propio',
        ['Ocupacion', 'Ocupacion_O']
    ] = ['patrón(a) o empleador(a)', None]

    people.loc[
        (people.Ocupacion == 'patrón(a) o empleador(a)')
        & (people.SectorEconom == 'otro'),
        ['SectorEconom', 'SectorEconom_O']
    ] = [None, None]

    people.loc[
        (people.Ocupacion_O == 'contratista')
        & (people.SectorEconom == 'otro'),
        ['Ocupacion', 'Ocupacion_O', 'SectorEconom', 'SectorEconom_O']
    ] = ['patrón(a) o empleador(a)', None, 'construcción', None]

    people.loc[
        (people.Ocupacion_O == 'contratista'),
        ['Ocupacion', 'Ocupacion_O']
    ] = ['patrón(a) o empleador(a)', None]

    people.loc[
        (
            (people.Ocupacion == 'otro')
            & (people.SectorEconom == 'construcción')
        ),
        ['Ocupacion', 'Ocupacion_O', 'SectorEconom', 'SectorEconom_O']
    ] = ['empleada(o) u obrera(o)', None, 'construcción', None]

    people.loc[
        people.Ocupacion_O.isin(
            [
                'vendedor ambulante', 'por su cuenta', 'puesto',
                'trabaja por su cuenta',
                'empleado independiente', 'jefe propio',
                'trabajador independiente', 'oficio propio',
                'por cuenta propia',
            ]
        ),
        ['Ocupacion', 'Ocupacion_O']
    ] = ['trabajador(a) por cuenta propia', None]

    people.loc[
        (
            people.Ocupacion_O.isin(
                [
                    'estilista', 'estetica', 'negocio propio estética',
                    'trabaja independiente en casa estética'
                ]
            )
        ),
        ['Ocupacion', 'Ocupacion_O', 'SectorEconom', 'SectorEconom_O']
    ] = ['trabajador(a) por cuenta propia', None, 'servicios', None]

    people.loc[
        people.Ocupacion_O.isin(
            ['mesero (a)', 'cocinero', 'chef', 'mecanico']
        ),
        ['Ocupacion', 'Ocupacion_O', 'SectorEconom', 'SectorEconom_O']
    ] = ['empleada(o) u obrera(o)', None, 'servicios', None]

    people.loc[
        people.Ocupacion_O.isin(['tablajero', 'carpintero', 'construcción']),
        ['Ocupacion', 'Ocupacion_O', 'SectorEconom', 'SectorEconom_O']
    ] = ['empleada(o) u obrera(o)', None, 'construcción', None]

    people.loc[
        (
            (people.Ocupacion == 'otro')
            & (people.SectorEconom == 'comercio')
        ),
        ['Ocupacion', 'Ocupacion_O', 'SectorEconom', 'SectorEconom_O']
    ] = ['empleada(o) u obrera(o)', None, 'comercio', None]

    people.loc[
        people.Ocupacion_O.isin(['panadero']),
        ['Ocupacion', 'Ocupacion_O', 'SectorEconom', 'SectorEconom_O']
    ] = ['empleada(o) u obrera(o)', None, 'comercio', None]

    people.loc[
        (
            (people.Ocupacion == 'otro')
            & (people.SectorEconom == 'industria manufacturera')
        ),
        ['Ocupacion', 'Ocupacion_O', 'SectorEconom', 'SectorEconom_O']
    ] = ['empleada(o) u obrera(o)', None, 'industria manufacturera', None]

    people.loc[
        people.Ocupacion_O.isin(
            [
                'albañil', 'soldador', 'electricista', 'eléctrico',
                'pintor', 'herrero',
                'reparador de canceles', 'pulidor de.pisos', 'plomero',
                'instalador de fibra',
            ]
        ),
        ['Ocupacion', 'Ocupacion_O', 'SectorEconom', 'SectorEconom_O']
    ] = ['empleada(o) u obrera(o)', None, 'construcción', None]

    people.loc[
        people.Ocupacion_O.astype(str).str.contains('empres'),
        ['Ocupacion', 'Ocupacion_O']
    ] = ['patrón(a) o empleador(a)', None]

    people.loc[
        people.Ocupacion_O.isin(
            [
                'operador de ruta urbana', 'transportista-fletes', 'trailero',
                'chofer', 'paquetera', 'paqueter smart',
                'chofer de camión urbano', 'chofer de transporte de personal',
                'chofer de tráiler', 'transportista',
                'operador de transporte de autobus', 'operador', 'operadora',
                'operador 5 ruedas', 'transporte escolar',
                'operador de transporte escolar',
                'chofer de transporte de personal',
            ]
        ),
        ['Ocupacion', 'Ocupacion_O', 'SectorEconom', 'SectorEconom_O']
    ] = ['empleada(o) u obrera(o)', None, 'transporte y comunicaciones', None]

    people.loc[
        people.Ocupacion_O.isin(
            [
                'trabaja en su propio transporte', 'chofer de aplicación',
                'chofer de didi'
            ]
        ),
        ['Ocupacion', 'Ocupacion_O', 'SectorEconom', 'SectorEconom_O']
    ] = [
        'trabajador(a) por cuenta propia', None,
        'transporte y comunicaciones', None
    ]

    people.loc[
        people.Ocupacion_O.isin(
            [
                'fabrica de baños', 'mantenimiento fabrica'
            ]
        ),
        ['Ocupacion', 'Ocupacion_O', 'SectorEconom', 'SectorEconom_O']
    ] = ['empleada(o) u obrera(o)', None, 'industria manufacturera', None]

    people.loc[
        people.Ocupacion_O.isin(
            [
                'panaderia', 'carnicero', 'empacador', 'almacenista',
                'jefe de almacen', 'cargador', 'paqueteria sorian'
            ]
        ),
        ['Ocupacion', 'Ocupacion_O', 'SectorEconom', 'SectorEconom_O']
    ] = ['empleada(o) u obrera(o)', None, 'comercio', None]

    people.loc[
        people.Ocupacion_O.isin(
            [
                'publico', 'servidor publico'
            ]
        ),
        ['Ocupacion', 'Ocupacion_O', 'SectorEconom', 'SectorEconom_O']
    ] = ['empleada(o) u obrera(o)', None, 'gobierno', None]

    people.loc[
        (
            (people.Ocupacion == 'otro')
            & (people.SectorEconom == 'servicios')
        ),
        ['Ocupacion', 'Ocupacion_O', 'SectorEconom', 'SectorEconom_O']
    ] = ['empleada(o) u obrera(o)', None, 'servicios', None]

    people.loc[
        people.Ocupacion_O.isin(
            [
                'jornalero'
            ]
        ),
        ['Ocupacion', 'Ocupacion_O']
    ] = ['jornalera(o) o peón(a)', None]

    people['Ocupacion_O'] = (
        people['Ocupacion_O']
        .replace(['n/p', 'n/g', 'n/r'], None)
    )
    people['SectorEconom_O'] = (
        people['SectorEconom_O']
        .replace(['n/p', 'n/g', 'n/r', 'ninguno'], None)
    )

    people.loc[
        (
            (people.SectorEconom == 'otro')
            & (people.Ocupacion == 'comerciante')
            & (people.SectorEconom_O.isna())
        ),
        'SectorEconom',
    ] = 'comercio'

    people.loc[
        people.Ocupacion_O == 'pensionado',
        ['Ocupacion', 'Ocupacion_O']
    ] = ['Es pensionada(o) o jubilada(o)', None]

    people.loc[
        people.Ocupacion_O == 'mecánico',
        ['Ocupacion', 'Ocupacion_O', 'SectorEconom', 'SectorEconom_O']
    ] = ['empleada(o) u obrera(o)', None, 'servicios', None]

    people.loc[
        people.Ocupacion_O == 'pensionado (a)',
        ['Ocupacion', 'Ocupacion_O', 'SectorEconom', 'SectorEconom_O']
    ] = ['Es pensionada(o) o jubilada(o)', None, 'otro', None]

    people.loc[
        people.Ocupacion_O.isin(
            [
                'maestro', 'maestra', 'profesora', 'profesor', 'educación',
                'maestra particular', 'asistente educativo', 'educadora'
            ]
        ),
        ['Ocupacion', 'Ocupacion_O', 'SectorEconom', 'SectorEconom_O']
    ] = ['empleada(o) u obrera(o)', None, 'servicios', None]

    people.loc[
        people.Ocupacion_O.isin(
            [
                'trilero', 'operador de tráiler',
                'operador de autobús', 'operador de camión'
            ]
        ),
        ['Ocupacion', 'Ocupacion_O', 'SectorEconom', 'SectorEconom_O']
    ] = ['empleada(o) u obrera(o)', None, 'transporte y comunicaciones', None]

    people.loc[
        people.Ocupacion_O.isin(
            [
                'empleada doméstica', 'trabajo domestico',
                'limpieza en casas', 'trabajadora doméstica',
                'empleada domestica'
            ]
        ),
        ['Ocupacion', 'Ocupacion_O', 'SectorEconom', 'SectorEconom_O']
    ] = ['empleada(o) u obrera(o)', None, 'servicios', None]

    people.loc[
        people.SectorEconom_O.isin(
            ['ayudante general']
        ),
        'SectorEconom_O'
    ] = None

    people.loc[
        people.Ocupacion_O.isin(
            ['ayudante general']
        ),
        ['Ocupacion', 'Ocupacion_O']
    ] = ['empleada(o) u obrera(o)', None]

    people.loc[
        people.SectorEconom_O.isin(
            ['pensionado']
        ),
        ['Ocupacion', 'Ocupacion_O', 'SectorEconom', 'SectorEconom_O']
    ] = ['jubilado', None, 'otro', None]

    people.loc[
        people.SectorEconom_O.isin(
            [
                'pemex', 'refineria', 'refinería de pemex',
                'compañía dentro de pemex',
                'refinería pemex', 'compañías interior de refinería',
                'guardia refineria'
            ]
        ),
        ['Ocupacion_O', 'SectorEconom', 'SectorEconom_O']
    ] = [None, 'industria manufacturera', None]

    people.loc[
        (
            (people.Ocupacion_O == 'no estudia ni trabaja')
        ),
        ['Ocupacion', 'Ocupacion_O', 'SectorEconom', 'SectorEconom_O']
    ] = ['sin empleo', None, 'otro', None]

    people.loc[
        (
            (people.Ocupacion_O == 'no estudia')
        ),
        ['Ocupacion', 'Ocupacion_O', 'SectorEconom', 'SectorEconom_O']
    ] = ['sin empleo', None, 'otro', None]

    people.loc[
        people.Ocupacion_O.isin(
            ['guardia', 'guardia de seguridad', 'vigilante']
        ),
        ['Ocupacion', 'Ocupacion_O', 'SectorEconom', 'SectorEconom_O']
    ] = ['empleada(o) u obrera(o)', None, 'servicios', None]

    people.loc[
        (
            (people.Ocupacion_O == 'independiente')
        ),
        ['Ocupacion', 'Ocupacion_O', 'SectorEconom', 'SectorEconom_O']
    ] = ['trabajador(a) por cuenta propia', None, 'otro', None]

    people.loc[
        (
            (people.Ocupacion_O == 'jardinero')
        ),
        ['Ocupacion', 'Ocupacion_O', 'SectorEconom', 'SectorEconom_O']
    ] = ['trabajador(a) por cuenta propia', None, 'servicios', None]

    people.loc[
        (
            (people.SectorEconom_O == 'salud')
        ),
        ['SectorEconom', 'SectorEconom_O']
    ] = ['servicios', None]

    people.loc[
        (
            (people.SectorEconom_O == 'fabrica')
        ),
        ['SectorEconom', 'SectorEconom_O']
    ] = ['industria manufacturera', None]

    people.loc[
        (
            (people.SectorEconom_O == 'industria alimenticia')
        ),
        ['SectorEconom', 'SectorEconom_O']
    ] = ['industria manufacturera', None]

    people.loc[
        (
            (people.SectorEconom_O.isin(['educación', 'educacion']))
        ),
        ['SectorEconom', 'SectorEconom_O']
    ] = ['servicios', None]

    people.loc[
        people.Ocupacion_O.isin(
            ['policía municipal']
        ),
        ['Ocupacion', 'Ocupacion_O', 'SectorEconom', 'SectorEconom_O']
    ] = ['empleada(o) u obrera(o)', None, 'gobierno', None]

    people.loc[
        people.SectorEconom_O.isin(
            ['recolector de metal']
        ),
        ['Ocupacion', 'Ocupacion_O', 'SectorEconom', 'SectorEconom_O']
    ] = ['empleada(o) u obrera(o)', None, 'comercio', None]

    people.loc[
        people.SectorEconom_O.isin(
            ['albañil']
        ),
        ['SectorEconom', 'SectorEconom_O']
    ] = ['construcción', None]

    people.loc[
        people.SectorEconom_O.isin(
            ['hacen chocolates']
        ),
        ['SectorEconom', 'SectorEconom_O']
    ] = ['industria manufacturera', None]

    people.loc[
        people.SectorEconom_O.isin(
            ['privado']
        ),
        'SectorEconom_O'
    ] = None

    people.loc[people.Ocupacion_O.isin(
        [
            "estudiante universitario", "estudia y trabaja",
            "trabaja y estudia", "estudiante y trabaja"
        ]
    ), 'ASISTEN'] = 1

    for r, o_list in ocu_only_map.items():
        for ocu in o_list:
            people.loc[
                (
                    (people.Ocupacion == 'otro')
                    & (people.SectorEconom_O.isna())
                    & (people.SectorEconom == 'otro')
                    & (people.Ocupacion_O == ocu)
                ),
                ['Ocupacion', 'Ocupacion_O', 'SectorEconom', 'SectorEconom_O']
            ] = r

    people.loc[
        (
            (people.Ocupacion_O.notnull())
        ),
        ['Ocupacion', 'Ocupacion_O', 'SectorEconom', 'SectorEconom_O']
    ] = [
            ['empleado (a)', None, 'servicios', None],
            ['empleado (a)', None, 'servicios', None],
            ['empleado (a)', None, 'servicios', None],
            ['empleado (a)', None, 'servicios', None],
            ['empleado (a)', None, 'servicios', None],
            ['otro', None, 'otro', None],
            ['empleado (a)', None, 'comercio', None],
            ['empleado (a)', None, 'servicios', None],
            ['empleado (a)', None, 'servicios', None],
            ['empleado (a)', None, 'servicios', None],
            ['empleado (a)', None, 'industria manufacturera', None],
            ['empleado (a)', None, 'comercio', None],
            ['empleado (a)', None, 'servicios', None],
            ['empleado (a)', None, 'servicios', None],
            ['empleado (a)', None, 'comercio', None],
            ['empleado (a)', None, 'comercio', None],
            ['empleado (a)', None, 'servicios', None],
            ['empleado (a)', None, 'servicios', None],
            ['empleado (a)', None, 'industria manufacturera', None],
            ['empleado (a)', None, 'comercio', None],
            ['empleado (a)', None, 'servicios', None],
            ['empleado (a)', None, 'servicios', None],
            ['empleado (a)', None, 'servicios', None],
    ]

    for secto, sect in sect_map.items():
        people.loc[
            (
                (people.SectorEconom_O == secto)
            ),
            ['SectorEconom', 'SectorEconom_O']
        ] = [sect, None]

    people.loc[
        (
            people.SectorEconom_O.notnull()
            & (people.Ocupacion == 'comerciante')
        ),
        ['Ocupacion', 'SectorEconom', 'SectorEconom_O']
    ] = ['trabajador(a) por cuenta propia', 'comercio', None]

    people.loc[
        (
            people.SectorEconom_O.notnull()
        ),
        ['Ocupacion', 'SectorEconom', 'SectorEconom_O']
    ] = [
        ['trabajador(a) por cuenta propia', 'comercio', None],
        ['trabajador(a) por cuenta propia', 'construcción', None],
        ['trabajador(a) por cuenta propia', 'otro', None],
        ['trabajador(a) por cuenta propia', 'otro', None],
        ['trabajador(a) por cuenta propia', 'otro', None],
        ['trabajador(a) por cuenta propia', 'servicios', None],
        ['trabajador(a) por cuenta propia', 'servicios', None],
        ['trabajador(a) por cuenta propia', 'otro', None],
        ['trabajador(a) por cuenta propia', 'transporte y comunicaciones', None],
        ['trabajador(a) por cuenta propia', 'otro', None],
        ['trabajador(a) por cuenta propia', 'otro', None],
        ['trabajador(a) por cuenta propia', 'otro', None],
        ['trabajador(a) por cuenta propia', 'otro', None],
        ['trabajador(a) por cuenta propia', 'otro', None],
        ['trabajador(a) por cuenta propia', 'comercio', None],
        ['trabajador(a) por cuenta propia', 'comercio', None],
        ['trabajador(a) por cuenta propia', 'construcción', None],
        ['trabajador(a) por cuenta propia', 'comercio', None],
        ['trabajador(a) por cuenta propia', 'servicios', None],
        ['trabajador(a) por cuenta propia', 'comercio', None],
        ['trabajador(a) por cuenta propia', 'construcción', None],
        ['trabajador(a) por cuenta propia', 'otro', None],
    ]

    people = people.drop(columns=['Ocupacion_O', 'SectorEconom_O'])

    people['Ocupacion'] = (
        people.Ocupacion
        .replace([
            'empleado (a)', 'obrero(a)', 'profesionista empleado',
            'oficinista'
        ], 'empleada(o) u obrera(o)')
        .replace('jubilado', 'Es pensionada(o) o jubilada(o)')
        .replace('jornalera(o) o peón(a)', 'empleada(o) u obrera(o)')
        .replace('ama de casa', 'Se dedica a los quehaceres del hogar')
        .replace('sin empleo', 'No trabaja')
        .replace('comerciante', 'trabajador(a) por cuenta propia')
    )
    people['SITTRA'] = people.Ocupacion.copy()
    people['CONACT'] = people.Ocupacion.copy()
    people = people.drop(columns='Ocupacion')

    people['SITTRA'] = (
        people.SITTRA
        .replace('Se dedica a los quehaceres del hogar', 'Blanco por pase')
        .replace('Es pensionada(o) o jubilada(o)', 'Blanco por pase')
        .replace('estudiante', 'Blanco por pase')
        .replace('No trabaja', 'Blanco por pase')
        .replace('otro', None)
    )

    people['CONACT'] = (
        people.CONACT
        .replace('empleada(o) u obrera(o)', 'Trabajó')
        .replace('otro', 'Trabajó')
        .replace('estudiante', 'No trabaja')
        .replace('trabajador(a) por cuenta propia', 'Trabajó')
        .replace('patrón(a) o empleador(a)', 'Trabajó')
    )

    people.loc[
        (
            people.CONACT != 'Trabajó'
        ),
        'SectorEconom'
    ] = 'Blanco por pase'

    people = people.rename(columns={'SectorEconom': 'ACTIVIDADES_C'})

    # TAZ_TRAB
    # Choose first arbitrarly
    idx_work_trips = trips.query("Motivo == 'trabajo'").index
    taz_trab = (
        trips.loc[idx_work_trips, 'ZonaDest']
        .groupby(['HOGAR', 'HABITANTE']).first()
    )
    people['TAZ_TRAB'] = 'Blanco por pase'
    people.loc[people.CONACT == 'Trabajó', 'TAZ_TRAB'] = np.nan
    people.loc[taz_trab.index, 'TAZ_TRAB'] = taz_asi

    # TIE_TRASLADO_TRAB
    people['TIE_TRASLADO_TRAB'] = 'Blanco por pase'
    people.loc[people.CONACT == 'Trabajó', 'TIE_TRASLADO_TRAB'] = np.nan
    idx_work_trips = trips.query("Motivo == 'trabajo'").index
    duracion_cat = pd.cut(
        (
            trips.loc[idx_work_trips, 'duracion'].dt.total_seconds()/60
        ).groupby(['HOGAR', 'HABITANTE']).max(),
        [-1, 15, 30, 60, 120, 1e6],
        labels=[
            'Hasta 15 minutos', '16 a 30 minutos', '31 minutos a 1 hora',
            'Más de 1 hora y hasta 2 horas', 'Más de 2 horas'
        ],
        right=True,
    )
    people.loc[duracion_cat.index, 'TIE_TRASLADO_TRAB'] = duracion_cat

    # Drop 4 households without family head
    # people = people.drop(['22899-4', '25131-4', '3275-118', '59886-12'])

    people['ASISTEN'] = people.ASISTEN.replace(
        [0.0, 1.0], ['No', 'Sí']
    )

    return people


def build_household_table(od_df, people):
    viv_cols = [
        'MUN', 'TAZ',
        'LineaTelef', 'Internet',
        'VHAuto', 'VHMoto', 'VHPickup', 'VHCamion',
        'VHBici', 'VHPatineta', 'VHPatines', 'VHScooter', 'VHOtro',
        'CHBaños', 'CHDormitorios',
        'Hab14masTrabajo', 'HabitantesTotal',
        'HbitantesMayor6', 'HbitantesMenor5', 'HabitantesObs', 'NSE',
        'NIntDom'
    ]

    viv_df = od_df[viv_cols].groupby('HOGAR').first()

    viv_df['NumberOfVehicles'] = (
        viv_df.VHAuto + viv_df.VHPickup + viv_df.VHMoto
    )

    # Auxiliary columns to fix household counts
    viv_df['HabitantesObs'] = people.groupby(['HOGAR']).size()
    viv_df['Hab14masTrabajoObs'] = (
        people.query("Edad >= 14 & CONACT == 'Trabajó'")
        .groupby(['HOGAR']).size()
    )
    viv_df['Hab14masTrabajoObs'] = viv_df['Hab14masTrabajoObs'].fillna(0.0)
    viv_df['Hab14masNTrabajoObs'] = (
        people.query("Edad >= 14 & CONACT != 'Trabajó'")
        .groupby(['HOGAR']).size()
    )
    viv_df['Hab14masNTrabajoObs'] = viv_df['Hab14masNTrabajoObs'].fillna(0.0)

    # Fix counts
    viv_df_2 = viv_df.copy()

    viv_df_2['Hab14masTrabajo'] = viv_df_2.Hab14masTrabajo.mask(
        viv_df.Hab14masTrabajo < viv_df.Hab14masTrabajoObs,
        viv_df.Hab14masTrabajoObs
    )

    viv_df_2['HbitantesMayor6'] = viv_df_2.HbitantesMayor6.mask(
        viv_df_2.HabitantesObs > viv_df_2.HbitantesMayor6,
        viv_df_2.HabitantesObs
    )

    viv_df_2['HabitantesTotal'] = (
        viv_df_2.HbitantesMenor5 + viv_df_2.HbitantesMayor6
    )

    viv_df_2['Hab14masTrabajoSup'] = (
        viv_df_2.HbitantesMayor6 - viv_df_2.Hab14masNTrabajoObs
    )
    viv_df_2['Hab14masTrabajo'] = viv_df_2.Hab14masTrabajo.mask(
        viv_df_2.Hab14masTrabajo > viv_df_2.Hab14masTrabajoSup,
        viv_df_2.Hab14masTrabajoSup
    )

    perc_adj = (
        (viv_df_2.drop(columns='Hab14masTrabajoSup') != viv_df).sum(axis=1) > 0
    ).sum()/len(viv_df)*100
    print(f"{perc_adj}% of households have been ajusted.")

    perc_incom = (
        viv_df_2.HabitantesObs != viv_df_2.HbitantesMayor6
    ).sum()/len(viv_df)*100
    print(
        f"{perc_incom} of households are missing members "
        "above 6 years of age."
    )

    viv_df = viv_df_2.drop(
        columns=['Hab14masTrabajoSup', 'Hab14masNTrabajoObs']
    )

    viv_df = viv_df.rename(
        columns={'LineaTelef': 'TELEFONO', 'Internet': 'INTERNET'}
    )
    viv_df['AUTOPROP'] = (
        (viv_df.VHAuto + viv_df.VHPickup)
        .astype(bool)
        .map({True: 'Sí', False: 'No'})
    )
    viv_df['MOTOCICLETA'] = (
        viv_df.VHMoto.astype(bool)
        .map({True: 'Sí', False: 'No'})
    )
    viv_df['BICICLETA'] = (
        viv_df.VHBici.astype(bool).map({True: 'Sí', False: 'No'})
    )
    viv_df['NUMPERS'] = viv_df.HabitantesTotal.astype(int)
    viv_df['CUADORM'] = viv_df.CHDormitorios.astype(int)

    # Augment columns
    aug_cols = ['EDUC', 'EDAD', 'ACTIVIDADES_C', 'ASISTEN', 'CONACT', 'SITTRA']
    viv_df[aug_cols] = (
        people.query("PARENTESCO == 'Jefa(e)'")[aug_cols]
        .droplevel(1).reindex(viv_df.index)
    )

    viv_df = viv_df.replace('Si', 'Sí')

    # Drop the 4 households withou family head
    # viv_df = viv_df.drop(['22899-4', '25131-4', '3275-118', '59886-12'])

    viv_df = viv_df.fillna(value=np.nan)

    # Dwelling type will be infered from dwellings with
    # inner adress number.
    # Just two classes
    viv_df['CLAVIVP'] = (
        viv_df.NIntDom
        .str.strip().str.lower()
        .replace(['0', 's/n', '', 's7n', 'n/p', 'n/r', 'nt'], None)
        .notnull()
        .map({True: 'ConNumInt', False: 'SinNumInt'})
    )
    viv_df = viv_df.drop(columns='NIntDom')

    return viv_df


def personas_as_od(personas_path):
    personas = process_people_df(personas_path)
    personas = personas.set_index(['ID_VIV', 'NUMPER']).sort_index()

    # Drop columns not in OD
    # No way to use them for imputation
    # We are interested in CLAVIP
    personas = personas.drop(
        columns=[
            'IDENT_MADRE', 'IDENT_PADRE', 'ENT_PAIS_NAC', 'NACIONALIDAD',
            'SERSALUD', 'AFRODES', 'REGIS_NAC',
            'DHSERSAL1', 'DHSERSAL2', 'RELIGION',
            'HLENGUA', 'HESPANOL', 'ELENGUA', 'PERTE_INDIGENA',
            'ENT_PAIS_ASI', 'NOMCAR_C',
            'ALFABET', 'ENT_PAIS_RES_5A', 'MUN_RES_5A', 'IDENT_PAREJA',
            'AGUINALDO', 'VACACIONES', 'SERVICIO_MEDICO', 'UTILIDADES',
            'INCAP_SUELDO', 'SAR_AFORE', 'CREDITO_VIVIENDA', 'ENT_PAIS_TRAB',
            'ID_PERSONA', 'INGTRMEN', 'SITUA_CONYUGAL', 'OCUPACION_C'
        ]
    )

    # Recategorize some PARENTESCOS to the OD equivalent
    personas['PARENTESCO'] = personas.PARENTESCO.astype('O')
    personas.loc[
        personas.PARENTESCO.isin(
            ['Esposa(o)', 'Madre o padre']
        )
        & (personas.SEXO == 'F'),
        'PARENTESCO'
    ] = 'Madre/Esposa'
    personas.loc[
        personas.PARENTESCO.isin(
            ['Esposa(o)', 'Madre o padre']
        )
        & (personas.SEXO == 'M'),
        'PARENTESCO'
    ] = 'Padre/Esposo'

    # Keep only global DIS column
    personas = personas.drop(
        columns=[
            'DIS_VER', 'DIS_OIR', 'DIS_CAMINAR', 'DIS_RECORDAR',
            'DIS_BANARSE', 'DIS_HABLAR', 'DIS_MENTAL'
        ]
    )
    # Recode it to yes, no, unknown to enable comparison with OD
    personas['DIS'] = personas.DIS.apply(has_dis)

    # Create a EDUC columns from nivacad and escolari.
    # This is different from the synthetic pop one
    # It is less aggregated, since the transit sim requires
    # more edeucation classes than the ones constrained in the census
    personas['EDUC'] = (
            personas.NIVACAD.astype(str)
            + '_'
            + personas.ESCOLARI.astype(str)
        ).replace(
            {
                'nan_nan': np.nan,
                'Blanco por pase_Blanco por pase':
                'Blanco por pase'
            }
        ).map(nivacad_posmap_fine)
    personas = personas.drop(columns=['NIVACAD', 'ESCOLARI'])

    # MED_TRASLADO_ESC and MED_TRASLADO_TRAB
    # We should keep this columns and add them to OD from legs table.
    # tpub_cols = [
    #     'MED_TRASLADO_ESC_Camión, autobús, combi, colectivo',
    #     'MED_TRASLADO_ESC_Metro, tren ligero, tren suburbano',
    #     'MED_TRASLADO_ESC_Metrobús (autobús en carril confinado)',
    # ]
    # personas['MED_TRASLADO_ESC_TPUB'] = (
    #     (personas[tpub_cols].astype(int).sum(axis=1).astype(bool).astype(int)
    #     )
    # personas = personas.drop(columns=tpub_cols)
    # personas['MED_TRASLADO_ESC'] = personas.apply(get_modo_agr, axis=1)
    # Drop for now
    personas = personas.drop(
        columns=[c for c in personas.columns if c.startswith('MED_TRASLADO_')]
    )

    # SITTRA
    # agregate into OD categories
    personas['SITTRA'] = (
        personas.SITTRA
        .replace('jornalera(o) o peón(a)', 'empleada(o) u obrera(o)')
        .replace('ayudante con pago', 'empleada(o) u obrera(o)')
        .replace('trabajador(a) sin pago', 'empleada(o) u obrera(o)')
    )

    # CONACT
    # agregate into OD cats
    personas['CONACT'] = (
        personas.CONACT
        .replace('Es estudiante', 'No trabaja')
        .replace('Buscó trabajo', 'No trabaja')
        .replace(
            'Se dedica a los quehaceres del hogar / se rescata que trabaja',
            'Trabajó'
        )
        .replace(
            'Está incapacitado permanentemente para trabajar',
            'No trabaja'
        )
        .replace('Tenía trabajo pero no trabajó', 'Trabajó')
        .replace('Declara estudiante / se rescata que trabaja', 'Trabajó')
        .replace(
            'Declara otra situación de actividad / se rescata que trabaja',
            'Trabajó'
        )
        .replace(
            'Declara jubilado o pensionado / se rescata que trabaja',
            'Trabajó'
        )
        .replace(
            'Declara que busca trabajo /  se rescata que trabaja',
            'Trabajó'
        )
        .replace(
            'No se tiene información / se rescata que trabaja',
            'Trabajó'
        )
        .replace(
            'Declara que tiene limitaciónes / se rescata que trabaja',
            'Trabajó'
        )
        .replace('Blanco por pase', 'No trabaja')
    )

    # ACTIVIDADES_C
    act_map = {
        'Construcción': 'construcción',
        'Transportes, correos y almacenamiento': 'transporte y comunicaciones',
        'Comercio al por mayor': 'comercio',
        'Comercio al por menor': 'comercio',
        'Servicios de alojamiento temporal y de preparación de alimentos y bebidas': 'servicios',
        'Servicios de apoyo a los negocios y manejo de residuos, y servicios de remediación': 'servicios',
        'Industrias manufactureras': 'industria manufacturera',
        'Actividades legislativas, gubernamentales, de impartición de justicia y de organismos internacionales y extraterritoriales': 'gobierno',
        'Otros servicios excepto actividades gubernamentales': 'servicios',
        'Servicios profesionales, científicos y técnicos': 'servicios',
        'Servicios educativos': 'servicios',
        'Generación, transmisión, distribución y comercialización de energía eléctrica, suministro de agua y de gas natural por ductos al consumidor final': 'otro',
        'Información en medios masivos': 'otro',
        'Servicios inmobiliarios y de alquiler de bienes muebles e intangibles': 'servicios',
        'Servicios de salud y de asistencia social': 'servicios',
        'Servicios financieros y de seguros': 'servicios',
        'Minería': 'minería',
        'Agricultura, cría y explotación de animales, aprovechamiento forestal, pesca y caza': 'agricultura y ganadería',
        'Servicios de esparcimiento, culturales y deportivos, y otros servicios recreativos': 'servicios',
        'Corporativos': 'servicios'}

    for k, v in act_map.items():
        personas['ACTIVIDADES_C'] = personas.ACTIVIDADES_C.replace(k, v)

    # personas['EDAD'] = pd.cut(
    #     personas.EDAD,
    #     (0, 3, 5, 6, 8, 12, 15, 18, 25, 50, 60, 65, 131),
    #     right=False,
    #     labels=[
    #         '0-2', '3-4', '5', '6-7', '8-11', '12-14', '15-17', '18-24',
    #         '25-49', '50-59', '60-64', '65-130'
    #     ]
    # )

    return personas


def viviendas_as_od(viviendas_path, personas, viv_df):
    viviendas = process_places_df(viviendas_path)
    viviendas = viviendas.set_index('ID_VIV').sort_index()

    # This columns are nor shared by the OD, nor can be recovered.
    drop_viv_cols = [
        'PAREDES', 'TECHOS', 'PISOS', 'COCINA',
        'TOTCUART', 'LUG_COC', 'COMBUSTIBLE',
        'ESTUFA', 'ELECTRICIDAD', 'FOCOS', 'FOCOS_AHORRA',
        'AGUA_ENTUBADA', 'ABA_AGUA_ENTU', 'ABA_AGUA_NO_ENTU',
        'TINACO', 'CISTERNA', 'BOMBA_AGUA', 'REGADERA',
        'BOILER', 'CALENTADOR_SOLAR', 'AIRE_ACON', 'PANEL_SOLAR',
        'SERSAN', 'CONAGUA', 'USOEXC', 'DRENAJE',
        'SEPARACION1', 'SEPARACION2', 'SEPARACION3', 'SEPARACION4',
        'DESTINO_BAS', 'REFRIGERADOR', 'LAVADORA', 'HORNO',
        'RADIO', 'TELEVISOR', 'COMPUTADORA',
        'CELULAR', 'SERV_TV_PAGA', 'SERV_PEL_PAGA',
        'CON_VJUEGOS', 'TENENCIA', 'ESCRITURAS', 'FORMA_ADQUI',
        'FINANCIAMIENTO1', 'FINANCIAMIENTO2', 'FINANCIAMIENTO3',
        'DEUDA', 'MCONMIG', 'MNUMPERS', 'INGR_PEROTROPAIS',
        'INGR_PERDENTPAIS', 'INGR_AYUGOB', 'INGR_JUBPEN',
        'ALIMENTACION', 'ALIM_ADL1', 'ALIM_ADL2',
        'ING_ALIM_ADL1', 'ING_ALIM_ADL2', 'ING_ALIM_ADL3',
        'INGTRHOG'
    ]
    viviendas = viviendas.drop(columns=drop_viv_cols)

    share_cols = [
        'MUN', 'TELEFONO', 'INTERNET', 'AUTOPROP', 'MOTOCICLETA',
        'BICICLETA', 'NUMPERS', 'CUADORM'
    ]
    aug_cols = ['EDUC', 'EDAD', 'ACTIVIDADES_C', 'ASISTEN', 'CONACT', 'SITTRA']

    viviendas_common = viviendas[share_cols + ['CLAVIVP']].copy()
    viviendas_common['Hab14masTrabajo'] = (
        personas.query("EDAD >= 14 & CONACT == 'Trabajó'")
        .groupby('ID_VIV').size()
        .reindex(viviendas.index).fillna(0)
        .astype(int)
    )
    viviendas_common[aug_cols] = (
        personas.query("PARENTESCO == 'Jefa(e)'")[aug_cols]
        .droplevel(1).reindex(viviendas.index)
    )
    viviendas_common = viviendas_common.query(
        "MUN.isin(@viv_df.MUN.unique())"
    ).copy()

    viviendas_common['EDAD'] = pd.cut(
        viviendas_common.EDAD,
        (0, 3, 5, 6, 8, 12, 15, 18, 25, 50, 60, 65, 131),
        right=False,
        labels=[
            '0-2', '3-4', '5', '6-7', '8-11', '12-14', '15-17', '18-24',
            '25-49', '50-59', '60-64', '65-130'
        ]
    )

    return viviendas_common
