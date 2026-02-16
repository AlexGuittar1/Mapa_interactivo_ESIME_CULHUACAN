-- Crear tabla horarios
CREATE TABLE IF NOT EXISTS horarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    materia TEXT,
    grupo TEXT,
    lunes TEXT,
    martes TEXT,
    miercoles TEXT,
    jueves TEXT,
    viernes TEXT,
    profesor TEXT
);

-- Datos de la hoja: Table008 (Page 4)
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FISICA CLASICA', '1CM53', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('QUIMICA BASICA', '1CM54', '13:00 a 14:30
1103', NULL, NULL, NULL, '13:00 a 14:30
1104', 'Pablo Gopar Gloria Alejandra');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. QUIMICA BASICA', '1CM54', '10:00 a 11:30
Lab. Química', NULL, NULL, NULL, NULL, 'Pablo Gopar Gloria Alejandra');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. QUIMICA BASICA', '1CM54', '10:00 a 11:30', NULL, NULL, NULL, NULL, 'Salazar Galván Martha Elvia');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FUNDAMENTOS DE PROGRAMACION', '1CM55', NULL, '11:30 a 13:00
1208', '8:30 a 10:00
3105', NULL, NULL, 'Azorín Vega Claudia');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FUNDAMENTOS DE PROGRAMACION', '1CM55', '7:00 a 8:30
UDI 1', NULL, NULL, '10:00 a 11:30
UDI 1', NULL, 'Azorín Vega Claudia');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FUNDAMENTOS DE PROGRAMACION', '1CM55', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES I INGENIERA CIENCIA Y SOCIEDAD', '1CM56', '8:30 a 10:00
3209', '10:00 a 11:30
3201', NULL, '11:30 a 13:00
3111', NULL, 'Enriquez Arreola Sandra Luz');
-- Total de registros insertados de Table008 (Page 4): 8

-- Datos de la hoja: Table006 (Page 3)
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES I INGENIERA CIENCIA Y SOCIEDAD', '1CM36', NULL, NULL, '8:30 a 10:00
1105', '8:30 a 10:00
1108', '8:30 a 10:00
1106', '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CALCULO DIFERENCIAL E INTEGRAL', '1CM41', '10:00 a 11:30
3109', '8:30 a 10:00
3109', '8:30 a 10:00
3108', '10:00 a 11:30
3109', NULL, 'Villarreal Aguirre Jose Luis');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FUNDAMENTOS DE ALGEBRA', '1CM42', NULL, NULL, NULL, '8:30 a 10:00
1203', '8:30 a 10:00
1211', 'Ley Mandujano Jose Juan');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FISICA CLASICA', '1CM43', '8:30 a 10:00
3213', NULL, '11:30 a 13:00
3203', '13:00 a 14:30
1211', NULL, 'Cubillos Islas Irene');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FISICA CLASICA', '1CM43', NULL, '13:00 a 14:30
Lab. Física', NULL, NULL, NULL, 'Cubillos Islas Irene');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FISICA CLASICA', '1CM43', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('QUIMICA BASICA', '1CM44', NULL, '11:30 a 13:00
1211', NULL, NULL, '10:00 a 11:30
1213', 'Pablo Gopar Gloria Alejandra');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. QUIMICA BASICA', '1CM44', NULL, NULL, '13:00 a 14:30
Lab. Química', NULL, NULL, 'Pablo Gopar Gloria Alejandra');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. QUIMICA BASICA', '1CM44', NULL, NULL, '13:00 a 14:30', NULL, NULL, 'Aniceto Vargas Paula Flora');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FUNDAMENTOS DE PROGRAMACION', '1CM45', NULL, NULL, NULL, '11:30 a 13:00
1102', '11:30 a 13:00
2202', 'Salas Jimenez Veronica');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FUNDAMENTOS DE PROGRAMACION', '1CM45', '11:30 a 13:00
Lab. Computación 1', '10:00 a 11:30
UDI 6', NULL, NULL, NULL, 'Salas Jimenez Veronica');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FUNDAMENTOS DE PROGRAMACION', '1CM45', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES I INGENIERA CIENCIA Y SOCIEDAD', '1CM46', '13:00 a 14:30
1105', NULL, '10:00 a 11:30
1105', NULL, '13:00 a 14:30
1106', 'Flores Martinez Citlali');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CALCULO DIFERENCIAL E INTEGRAL', '1CM51', NULL, '8:30 a 10:00
2208', '10:00 a 11:30
2208', '8:30 a 10:00
2208', '10:00 a 11:30
2208', 'Cabrera Rivas Xochitl');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FUNDAMENTOS DE ALGEBRA', '1CM52', '11:30 a 13:00
3102', NULL, '11:30 a 13:00
3102', NULL, NULL, 'Heredia Velasco Alma Rosa');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FISICA CLASICA', '1CM53', NULL, '13:00 a 14:30
1101', NULL, '13:00 a 14:30
1101', '11:30 a 13:00
1110', 'Olivares Robles Miguel Angel');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FISICA CLASICA', '1CM53', NULL, NULL, '13:00 a 14:30
Lab. Física 1', NULL, NULL, 'Olivares Robles Miguel Angel');
-- Total de registros insertados de Table006 (Page 3): 17

-- Datos de la hoja: Table004 (Page 2)
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('QUIMICA BASICA', '1CM24', NULL, '10:00 a 11:30
1113', '10:00 a 11:30
1112', NULL, NULL, 'Rojo Hernández Maribel');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. QUIMICA BASICA', '1CM24', NULL, '13:00 a 14:30
Lab. Química', NULL, NULL, NULL, 'Rojo Hernández Maribel');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. QUIMICA BASICA', '1CM24', NULL, '13:00 a 14:30', NULL, NULL, NULL, 'Pablo Gopar Gloria Alejandra');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FUNDAMENTOS DE PROGRAMACION', '1CM25', '10:00 a 11:30
1207', NULL, NULL, NULL, '7:00 a 8:30
1214', 'Corona Ramirez Beatriz Eugenia');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FUNDAMENTOS DE PROGRAMACION', '1CM25', NULL, '11:30 a 13:00
Lab. Computación 2', NULL, '11:30 a 13:00
Lab. Computación 1', NULL, 'Corona Ramirez Beatriz Eugenia');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FUNDAMENTOS DE PROGRAMACION', '1CM25', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES I INGENIERA CIENCIA Y SOCIEDAD', '1CM26', NULL, NULL, '11:30 a 13:00
3115', '13:00 a 14:30
3104', '10:00 a 11:30
3114', 'Moreno Guzmán María Araceli');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CALCULO DIFERENCIAL E INTEGRAL', '1CM31', NULL, '7:00 a 8:30
1201', '7:00 a 8:30
1205', '11:30 a 13:00
1207', '7:00 a 8:30
1211', 'Ley Mandujano Jose Juan');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FUNDAMENTOS DE ALGEBRA', '1CM32', '8:30 a 10:00
1111', '10:00 a 11:30
1111', NULL, NULL, NULL, 'Gonzalez Lopez Santiago');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FISICA CLASICA', '1CM33', '7:00 a 8:30
1110', '8:30 a 10:00
1101', NULL, NULL, '10:00 a 11:30
1110', 'Vasco Mendez Edna Carla');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FISICA CLASICA', '1CM33', NULL, NULL, '11:30 a 13:00
Lab. Física', NULL, NULL, 'Vasco Mendez Edna Carla');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FISICA CLASICA', '1CM33', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('QUIMICA BASICA', '1CM34', '10:00 a 11:30
1102', NULL, NULL, '10:00 a 11:30
1107', NULL, 'Aniceto Vargas Paula Flora');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. QUIMICA BASICA', '1CM34', NULL, NULL, '10:00 a 11:30
Lab. Química', NULL, NULL, 'Aniceto Vargas Paula Flora');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. QUIMICA BASICA', '1CM34', NULL, NULL, '10:00 a 11:30', NULL, NULL, 'RODRIGUEZ JIMENEZ LUISA IVONE');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FUNDAMENTOS DE PROGRAMACION', '1CM35', '11:30 a 13:00
3210', NULL, NULL, NULL, '11:30 a 13:00
3204', 'Hernandez Lopez Marisol');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FUNDAMENTOS DE PROGRAMACION', '1CM35', NULL, '11:30 a 13:00
Lab. Computación 1', NULL, '7:00 a 8:30
Lab. Computación 1', NULL, 'Hernandez Lopez Marisol');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FUNDAMENTOS DE PROGRAMACION', '1CM35', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
-- Total de registros insertados de Table004 (Page 2): 18

-- Datos de la hoja: Table002 (Page 1)
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CALCULO DIFERENCIAL E INTEGRAL', '1CM11', '11:30 a 13:00
1202', '10:00 a 11:30
1202', NULL, '8:30 a 10:00
2104', '10:00 a 11:30
1202', 'Gonzalez Medina Vera');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FUNDAMENTOS DE ALGEBRA', '1CM12', NULL, '13:00 a 14:30
2208', NULL, NULL, '8:30 a 10:00
2208', 'Cabrera Rivas Xochitl');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FISICA CLASICA', '1CM13', '10:00 a 11:30
1111', '11:30 a 13:00
1111', NULL, NULL, '7:00 a 8:30
Lab. Física', 'Gonzalez Lopez Santiago');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FISICA CLASICA', '1CM13', NULL, NULL, '10:00 a 11:30
1210', NULL, NULL, 'Gonzalez Lopez Santiago');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FISICA CLASICA', '1CM13', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('QUIMICA BASICA', '1CM14', '7:00 a 8:30
1104', NULL, NULL, '7:00 a 8:30
1104', NULL, 'Aniceto Vargas Paula Flora');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. QUIMICA BASICA', '1CM14', NULL, NULL, '8:30 a 10:00
Lab. Química', NULL, NULL, 'Aniceto Vargas Paula Flora');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. QUIMICA BASICA', '1CM14', NULL, NULL, '8:30 a 10:00', NULL, NULL, 'Rojo Hernández Maribel');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FUNDAMENTOS DE PROGRAMACION', '1CM15', NULL, NULL, '7:00 a 8:30
3105', '11:30 a 13:00
2106', NULL, 'Azorín Vega Claudia');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FUNDAMENTOS DE PROGRAMACION', '1CM15', '8:30 a 10:00
Lab. Computación 2', '8:30 a 10:00
UDI 1', NULL, NULL, NULL, 'Azorín Vega Claudia');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FUNDAMENTOS DE PROGRAMACION', '1CM15', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES I INGENIERA CIENCIA Y SOCIEDAD', '1CM16', NULL, NULL, '11:30 a 13:00
1206', '10:00 a 11:30
1108', '11:30 a 13:00
1214', 'Flores Martinez Citlali');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CALCULO DIFERENCIAL E INTEGRAL', '1CM21', '8:30 a 10:00
3101', '8:30 a 10:00
3102', '8:30 a 10:00
3101', '8:30 a 10:00
3102', NULL, 'Diaz Albarran Salvador Felipe');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FUNDAMENTOS DE ALGEBRA', '1CM22', '7:00 a 8:30
1111', NULL, NULL, NULL, '8:30 a 10:00
1112', 'Gonzalez Lopez Santiago');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FISICA CLASICA', '1CM23', '11:30 a 13:00
3213', NULL, NULL, '10:00 a 11:30
1211', '11:30 a 13:00
3206', 'Cubillos Islas Irene');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FISICA CLASICA', '1CM23', NULL, NULL, '7:00 a 8:30
Lab. Física', NULL, NULL, 'Cubillos Islas Irene');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FISICA CLASICA', '1CM23', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
-- Total de registros insertados de Table002 (Page 1): 17

-- Datos de la hoja: Table008 (Page 4) (2)
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FISICA CLASICA', '1CV53', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('QUIMICA BASICA', '1CV54', NULL, NULL, NULL, '16:00 a 17:30
1205', '19:00 a 20:30
1208', 'Aquino Salinas Fernando David');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. QUIMICA BASICA', '1CV54', '16:00 a 17:30
Lab. Química', NULL, NULL, NULL, NULL, 'Aquino Salinas Fernando David');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. QUIMICA BASICA', '1CV54', '16:00 a 17:30', NULL, NULL, NULL, NULL, 'Amador Zaragoza Irma Alicia');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FUNDAMENTOS DE PROGRAMACION', '1CV55', '17:30 a 19:00
2205', NULL, NULL, NULL, '16:00 a 17:30
1202', 'Cruz Garcia Oscar');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FUNDAMENTOS DE PROGRAMACION', '1CV55', NULL, '20:30 a 22:00
Lab. Computación 1', '17:30 a 19:00
Lab. Computación 1', NULL, NULL, 'Cruz Garcia Oscar');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FUNDAMENTOS DE PROGRAMACION', '1CV55', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES I INGENIERA CIENCIA Y SOCIEDAD', '1CV56', '13:00 a 14:30
3104', NULL, '13:00 a 14:30
3104', NULL, '13:00 a 14:30
3104', 'Vigueras Bonilla Maria Juana');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FUNDAMENTOS DE ALGEBRA', '1CX12', '13:00 a 14:30
2203', NULL, '13:00 a 14:30
2203', NULL, NULL, 'Olivares Mercado Jesus');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FUNDAMENTOS DE ALGEBRA', '1CX22', NULL, NULL, '08:30 a 10:00
1204', '08:30 a 10:00
1207', NULL, 'Rodríguez Buendía Jesús');
-- Total de registros insertados de Table008 (Page 4) (2): 10

-- Datos de la hoja: Table006 (Page 3) (2)
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES I INGENIERA CIENCIA Y SOCIEDAD', '1CV36', '16:00 a 17:30
1114', '19:00 a 20:30
1207', NULL, '16:00 a 17:30
1111', NULL, 'Santos Jacome Celsa Piedad');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CALCULO DIFERENCIAL E INTEGRAL', '1CV41', '20:30 a 22:00
1112', '20:30 a 22:00
1114', NULL, '16:00 a 17:30
1109', '14:30 a 16:00
1114', 'Lopez Gonzalez Rodolfo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FUNDAMENTOS DE ALGEBRA', '1CV42', NULL, '16:00 a 17:30
2208', '16:00 a 17:30
2208', NULL, NULL, 'Cabrera Rivas Xochitl');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FISICA CLASICA', '1CV43', '17:30 a 19:00
1212', NULL, NULL, '17:30 a 19:00
3208', '16:00 a 17:30
1215', 'Martínez López Juan Gabriel');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FISICA CLASICA', '1CV43', NULL, NULL, '19:00 a 20:30
Lab. Física', NULL, NULL, 'Martínez López Juan Gabriel');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FISICA CLASICA', '1CV43', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('QUIMICA BASICA', '1CV44', NULL, '17:30 a 19:00
1103', NULL, '14:30 a 16:00
1103', NULL, 'Amador Zaragoza Irma Alicia');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. QUIMICA BASICA', '1CV44', NULL, NULL, '20:30 a 22:00', NULL, NULL, 'Amador Zaragoza Irma Alicia');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. QUIMICA BASICA', '1CV44', NULL, NULL, '20:30 a 22:00', NULL, NULL, 'Aquino Salinas Fernando David');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FUNDAMENTOS DE PROGRAMACION', '1CV45', NULL, '19:00 a 20:30
PB05', NULL, '19:00 a 20:30
PB06', NULL, 'Gonzalez Acatitla Clarissa');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FUNDAMENTOS DE PROGRAMACION', '1CV45', '16:00 a 17:30
Lab. Computación 1', NULL, NULL, NULL, '19:00 a 20:30
Lab. Computación 1', 'Gonzalez Acatitla Clarissa');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FUNDAMENTOS DE PROGRAMACION', '1CV45', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES I INGENIERA CIENCIA Y SOCIEDAD', '1CV46', '19:00 a 20:30
1101', NULL, '17:30 a 19:00
1102', NULL, '17:30 a 19:00
1105', 'Flores Martinez Citlali');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CALCULO DIFERENCIAL E INTEGRAL', '1CV51', '19:00 a 20:30
1104', '16:00 a 17:30
1105', '19:00 a 20:30
1105', '17:30 a 19:00
1105', NULL, 'Angel Huerta Froylan');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FUNDAMENTOS DE ALGEBRA', '1CV52', '14:30 a 16:00
2103', NULL, NULL, '14:30 a 16:00
2103', NULL, 'Bañuelos Duran Amparo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FISICA CLASICA', '1CV53', NULL, '17:30 a 19:00
3206', '14:30 a 16:00
Lab. Física', '19:00 a 20:30
3208', NULL, 'Martínez López Juan Gabriel');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FISICA CLASICA', '1CV53', NULL, NULL, NULL, NULL, '14:30 a 16:00
2102', 'Martínez López Juan Gabriel');
-- Total de registros insertados de Table006 (Page 3) (2): 17

-- Datos de la hoja: Table004 (Page 2) (2)
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('QUIMICA BASICA', '1CV24', '17:30 a 19:00
1113', NULL, NULL, '17:30 a 19:00
1103', NULL, 'Rojo Hernández Maribel');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. QUIMICA BASICA', '1CV24', NULL, NULL, '16:00 a 17:30
Lab. Química', NULL, NULL, 'Rojo Hernández Maribel');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. QUIMICA BASICA', '1CV24', NULL, NULL, '16:00 a 17:30', NULL, NULL, 'Aponte Olaya Julian Hugo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FUNDAMENTOS DE PROGRAMACION', '1CV25', NULL, NULL, NULL, '16:00 a 17:30
2112', '19:00 a 20:30
2106', 'Mora Jain Jesus');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FUNDAMENTOS DE PROGRAMACION', '1CV25', '16:00 a 17:30
Lab. Computación 2', '17:30 a 19:00
Lab. Computación 1', NULL, NULL, NULL, 'Mora Jain Jesus');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FUNDAMENTOS DE PROGRAMACION', '1CV25', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES I INGENIERA CIENCIA Y SOCIEDAD', '1CV26', '19:00 a 20:30
1114', '16:00 a 17:30
1207', '17:30 a 19:00
1113', NULL, NULL, 'Santos Jacome Celsa Piedad');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CALCULO DIFERENCIAL E INTEGRAL', '1CV31', '14:30 a 16:00
1113', '14:30 a 16:00
1205', NULL, '20:30 a 22:00
1203', '14:30 a 16:00
1204', 'Morales Vergara Pedro');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FUNDAMENTOS DE ALGEBRA', '1CV32', NULL, NULL, '16:00 a 17:30
1113', NULL, '17:30 a 19:00
1214', 'Olivares Mercado Jesus');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FISICA CLASICA', '1CV33', '19:00 a 20:30
1112', NULL, '19:00 a 20:30
Lab. Física 1', '17:30 a 19:00
1109', NULL, 'Lopez Gonzalez Rodolfo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FISICA CLASICA', '1CV33', NULL, '16:00 a 17:30
1214', NULL, NULL, NULL, 'Lopez Gonzalez Rodolfo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FISICA CLASICA', '1CV33', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('QUIMICA BASICA', '1CV34', NULL, NULL, '14:30 a 16:00
1105', '14:30 a 16:00
1104', NULL, 'Pablo Gopar Gloria Alejandra');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. QUIMICA BASICA', '1CV34', NULL, NULL, NULL, '19:00 a 20:30
Lab. Química', NULL, 'Pablo Gopar Gloria Alejandra');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. QUIMICA BASICA', '1CV34', NULL, NULL, NULL, '19:00 a 20:30', NULL, 'Aquino Salinas Fernando David');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FUNDAMENTOS DE PROGRAMACION', '1CV35', NULL, '17:30 a 19:00
PB05', '17:30 a 19:00
PB06', NULL, NULL, 'Gonzalez Acatitla Clarissa');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FUNDAMENTOS DE PROGRAMACION', '1CV35', '20:30 a 22:00
Lab. Computación 1', NULL, NULL, NULL, '16:00 a 17:30
Lab. Computación 1', 'Gonzalez Acatitla Clarissa');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FUNDAMENTOS DE PROGRAMACION', '1CV35', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
-- Total de registros insertados de Table004 (Page 2) (2): 18

-- Datos de la hoja: Table002 (Page 1) (2)
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CALCULO DIFERENCIAL E INTEGRAL', '1CV11', '20:30 a 22:00
1104', '20:30 a 22:00
1105', '20:30 a 22:00
1105', '19:00 a 20:30
1105', NULL, 'Angel Huerta Froylan');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FUNDAMENTOS DE ALGEBRA', '1CV12', '19:00 a 20:30
1201', NULL, NULL, NULL, '16:00 a 17:30
1214', 'Olivares Mercado Jesus');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FISICA CLASICA', '1CV13', '16:00 a 17:30
1212', '19:00 a 20:30
Lab. Física', NULL, '16:00 a 17:30
3208', NULL, 'Martínez López Juan Gabriel');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FISICA CLASICA', '1CV13', NULL, NULL, '16:00 a 17:30
2215', NULL, NULL, 'Martínez López Juan Gabriel');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FISICA CLASICA', '1CV13', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('QUIMICA BASICA', '1CV14', NULL, NULL, '17:30 a 19:00
PB03', '17:30 a 19:00
PB03', NULL, 'Aponte Olaya Julian Hugo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. QUIMICA BASICA', '1CV14', NULL, NULL, NULL, NULL, '19:00 a 20:30
Lab. Química', 'Aponte Olaya Julian Hugo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. QUIMICA BASICA', '1CV14', NULL, NULL, NULL, NULL, '19:00 a 20:30', '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FUNDAMENTOS DE PROGRAMACION', '1CV15', NULL, '16:00 a 17:30
1209', NULL, '20:30 a 22:00
1202', NULL, 'Cruz Garcia Oscar');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FUNDAMENTOS DE PROGRAMACION', '1CV15', NULL, NULL, '19:00 a 20:30
Lab. Computación 1', NULL, '20:30 a 22:00
Lab. Computación 1', 'Cruz Garcia Oscar');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FUNDAMENTOS DE PROGRAMACION', '1CV15', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES I INGENIERA CIENCIA Y SOCIEDAD', '1CV16', '17:30 a 19:00
1114', '17:30 a 19:00
1207', NULL, NULL, '17:30 a 19:00
1115', 'Santos Jacome Celsa Piedad');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CALCULO DIFERENCIAL E INTEGRAL', '1CV21', NULL, '19:00 a 20:30
1205', '19:00 a 20:30
1202', '19:00 a 20:30
1203', '17:30 a 19:00
1204', 'Morales Vergara Pedro');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FUNDAMENTOS DE ALGEBRA', '1CV22', NULL, NULL, NULL, '14:30 a 16:00
3113', '16:00 a 17:30
3113', 'Rodriguez Gomez Juan Angel');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FISICA CLASICA', '1CV23', '14:30 a 16:00
3102', '14:30 a 16:00
Lab. Física', NULL, NULL, '14:30 a 16:00
3103', 'Cubillos Islas Irene');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FISICA CLASICA', '1CV23', NULL, NULL, '14:30 a 16:00
1106', NULL, NULL, 'Cubillos Islas Irene');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FISICA CLASICA', '1CV23', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
-- Total de registros insertados de Table002 (Page 1) (2): 17

-- Datos de la hoja: Table006 (Page 3) (5)
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LENGUAJES DE BAJO NIVEL', '3CV34', '20:30 a 22:00
2205', NULL, '17:30 a 19:00
2205', NULL, NULL, 'Valles Montanez Luis');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. LENGUAJES DE BAJO NIVEL', '3CV34', NULL, NULL, NULL, '20:30 a 22:00
UDI 9', '16:00 a 17:30
UDI 9', 'Valles Montanez Luis');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. LENGUAJES DE BAJO NIVEL', '3CV34', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ESTRUCTURA DE DATOS', '3CV35', NULL, '20:30 a 22:00
2207', '19:00 a 20:30
3105', NULL, NULL, 'De La Cruz Tellez Arturo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. ESTRUCTURA DE DATOS', '3CV35', '19:00 a 20:30
UDI 7', NULL, NULL, NULL, '19:00 a 20:30
UDI 7', 'De La Cruz Tellez Arturo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. ESTRUCTURA DE DATOS', '3CV35', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES III: DESARROLLO HUMANO', '3CV36', '17:30 a 19:00
3111', NULL, NULL, '16:00 a 17:30
3106', NULL, 'Moreno Guzmán María Araceli');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CIRCUITOS DE CA Y CD', '3CX12', '13:00 a 14:30
1110', '13:00 a 14:30
1110', '13:00 a 14:30
1110', NULL, NULL, 'Guzman Rodriguez Jose Eduardo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. CIRCUITOS DE CA Y CD', '3CX12', NULL, NULL, NULL, NULL, NULL, 'Guzman Rodriguez Jose Eduardo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. CIRCUITOS DE CA Y CD', '3CX12', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CIRCUITOS LOGICOS I', '3CX13', NULL, '13:00 a 14:30
Lab. Micros', '13:00 a 14:30
1113', '13:00 a 14:30
1113', '13:00 a 14:30
1113', 'Martinez Martinez Margarita');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. CIRCUITOS LOGICOS I', '3CX13', NULL, NULL, NULL, NULL, NULL, 'Martinez Martinez Margarita');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. CIRCUITOS LOGICOS I', '3CX13', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
-- Total de registros insertados de Table006 (Page 3) (5): 13

-- Datos de la hoja: Table004 (Page 2) (6)
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. CIRCUITOS DE CA Y CD', '3CV22', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CIRCUITOS LOGICOS I', '3CV23', '19:00 a 20:30
1113', '20:30 a 22:00
1115', '17:30 a 19:00
1112', NULL, NULL, 'Diaz Rosas Javier Fernando');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. CIRCUITOS LOGICOS I', '3CV23', NULL, NULL, NULL, '17:30 a 19:00', NULL, 'Diaz Rosas Javier Fernando');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. CIRCUITOS LOGICOS I', '3CV23', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LENGUAJES DE BAJO NIVEL', '3CV24', NULL, NULL, '19:00 a 20:30
2205', NULL, '19:00 a 20:30
2205', 'Valles Montanez Luis');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. LENGUAJES DE BAJO NIVEL', '3CV24', NULL, '17:30 a 19:00
UDI 1', NULL, NULL, '17:30 a 19:00
UDI 9', 'Valles Montanez Luis');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. LENGUAJES DE BAJO NIVEL', '3CV24', NULL, '17:30 a 19:00', NULL, NULL, '17:30 a 19:00', 'Bautista Arias Jose Luis');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ESTRUCTURA DE DATOS', '3CV25', NULL, '16:00 a 17:30
PB05', '16:00 a 17:30
PB06', NULL, NULL, 'Gonzalez Acatitla Clarissa');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. ESTRUCTURA DE DATOS', '3CV25', '17:30 a 19:00
Lab. Computación 1', NULL, NULL, '20:30 a 22:00
Lab. Computación 1', NULL, 'Gonzalez Acatitla Clarissa');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. ESTRUCTURA DE DATOS', '3CV25', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES III: DESARROLLO HUMANO', '3CV26', '20:30 a 22:00
1114', NULL, NULL, NULL, '16:00 a 17:30
1115', 'Santos Jacome Celsa Piedad');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ECUACIONES DIFERENCIALES', '3CV31', NULL, '17:30 a 19:00
1112', NULL, '17:30 a 19:00
1110', '17:30 a 19:00
1110', 'Benitez Diaz Francisco Javier');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CIRCUITOS DE CA Y CD', '3CV32', '16:00 a 17:30
3109', '16:00 a 17:30
Lab. Micros', NULL, NULL, NULL, 'Ugalde Licea Adolfo Sabino');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. CIRCUITOS DE CA Y CD', '3CV32', NULL, NULL, '16:00 a 17:30
3205', NULL, NULL, 'Ugalde Licea Adolfo Sabino');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. CIRCUITOS DE CA Y CD', '3CV32', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CIRCUITOS LOGICOS I', '3CV33', NULL, '19:00 a 20:30
1115', '20:30 a 22:00
1109', '19:00 a 20:30
1114', NULL, 'Diaz Rosas Javier Fernando');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. CIRCUITOS LOGICOS I', '3CV33', NULL, NULL, NULL, NULL, '20:30 a 22:00', 'Diaz Rosas Javier Fernando');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. CIRCUITOS LOGICOS I', '3CV33', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
-- Total de registros insertados de Table004 (Page 2) (6): 18

-- Datos de la hoja: Table002 (Page 1) (6)
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ECUACIONES DIFERENCIALES', '3CV11', '17:30 a 19:00
3113', NULL, '17:30 a 19:00
3113', NULL, '17:30 a 19:00
3113', 'Rodriguez Gomez Juan Angel');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CIRCUITOS DE CA Y CD', '3CV12', '19:00 a 20:30
Lab. Micros', '19:00 a 20:30
3104', NULL, NULL, NULL, 'Ugalde Licea Adolfo Sabino');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. CIRCUITOS DE CA Y CD', '3CV12', NULL, NULL, NULL, NULL, '16:00 a 17:30
3205', 'Ugalde Licea Adolfo Sabino');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. CIRCUITOS DE CA Y CD', '3CV12', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CIRCUITOS LOGICOS I', '3CV13', '20:30 a 22:00
1113', NULL, NULL, '20:30 a 22:00
1114', '19:00 a 20:30
1113', 'Diaz Rosas Javier Fernando');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. CIRCUITOS LOGICOS I', '3CV13', NULL, NULL, '19:00 a 20:30', NULL, NULL, 'Diaz Rosas Javier Fernando');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. CIRCUITOS LOGICOS I', '3CV13', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LENGUAJES DE BAJO NIVEL', '3CV14', NULL, '16:00 a 17:30
2205', NULL, '19:00 a 20:30
2205', NULL, 'Valles Montanez Luis');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. LENGUAJES DE BAJO NIVEL', '3CV14', '16:00 a 17:30
UDI 9', NULL, '16:00 a 17:30
UDI 9', NULL, NULL, 'Valles Montanez Luis');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. LENGUAJES DE BAJO NIVEL', '3CV14', '16:00 a 17:30', NULL, '16:00 a 17:30', NULL, NULL, 'Bautista Arias Jose Luis');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ESTRUCTURA DE DATOS', '3CV15', NULL, '20:30 a 22:00
PB05', '20:30 a 22:00
PB06', NULL, NULL, 'Gonzalez Acatitla Clarissa');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. ESTRUCTURA DE DATOS', '3CV15', NULL, NULL, NULL, '16:00 a 17:30
Lab. Computación 1', '20:30 a 22:00
Lab. Computación 2', 'Gonzalez Acatitla Clarissa');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. ESTRUCTURA DE DATOS', '3CV15', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES III: DESARROLLO HUMANO', '3CV16', NULL, '17:30 a 19:00
3107', NULL, '17:30 a 19:00
3106', NULL, 'Moreno Guzmán María Araceli');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ECUACIONES DIFERENCIALES', '3CV21', '16:00 a 17:30
1108', '19:00 a 20:30
1112', NULL, '16:00 a 17:30
1110', NULL, 'Benitez Diaz Francisco Javier');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CIRCUITOS DE CA Y CD', '3CV22', NULL, NULL, '20:30 a 22:00
1108', NULL, '20:30 a 22:00
1109', 'Cabrera Tejeda Juan Jose');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. CIRCUITOS DE CA Y CD', '3CV22', NULL, NULL, NULL, '19:00 a 20:30
Lab. Micros', NULL, 'Cabrera Tejeda Juan Jose');
-- Total de registros insertados de Table002 (Page 1) (6): 17

-- Datos de la hoja: Vespertino_3_IC
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ECUACIONES DIFERENCIALES', '3CV11', '17:30 a 19:00
3113', NULL, '17:30 a 19:00
3113', NULL, '17:30 a 19:00
3113', 'Rodriguez Gomez Juan Angel');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CIRCUITOS DE CA Y CD', '3CV12', '19:00 a 20:30
Lab. Micros', '19:00 a 20:30
3104', NULL, NULL, NULL, 'Ugalde Licea Adolfo Sabino');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. CIRCUITOS DE CA Y CD', '3CV12', NULL, NULL, NULL, NULL, '16:00 a 17:30
3205', 'Ugalde Licea Adolfo Sabino');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CIRCUITOS LOGICOS I', '3CV13', '20:30 a 22:00
1113', NULL, NULL, '20:30 a 22:00
1114', '19:00 a 20:30
1113', 'Diaz Rosas Javier Fernando');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. CIRCUITOS LOGICOS I', '3CV13', NULL, NULL, '19:00 a 20:30', NULL, NULL, 'Diaz Rosas Javier Fernando');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LENGUAJES DE BAJO NIVEL', '3CV14', NULL, '16:00 a 17:30
2205', NULL, '19:00 a 20:30
2205', NULL, 'Valles Montanez Luis');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. LENGUAJES DE BAJO NIVEL', '3CV14', '16:00 a 17:30
UDI 9', NULL, '16:00 a 17:30
UDI 9', NULL, NULL, 'Valles Montanez Luis');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. LENGUAJES DE BAJO NIVEL', '3CV14', '16:00 a 17:30', NULL, '16:00 a 17:30', NULL, NULL, 'Bautista Arias Jose Luis');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ESTRUCTURA DE DATOS', '3CV15', NULL, '20:30 a 22:00
PB05', '20:30 a 22:00
PB06', NULL, NULL, 'Gonzalez Acatitla Clarissa');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. ESTRUCTURA DE DATOS', '3CV15', NULL, NULL, NULL, '16:00 a 17:30
Lab. Computación 1', '20:30 a 22:00
Lab. Computación 2', 'Gonzalez Acatitla Clarissa');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES III: DESARROLLO HUMANO', '3CV16', NULL, '17:30 a 19:00
3107', NULL, '17:30 a 19:00
3106', NULL, 'Moreno Guzmán María Araceli');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ECUACIONES DIFERENCIALES', '3CV21', '16:00 a 17:30
1108', '19:00 a 20:30
1112', NULL, '16:00 a 17:30
1110', NULL, 'Benitez Diaz Francisco Javier');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CIRCUITOS DE CA Y CD', '3CV22', NULL, NULL, '20:30 a 22:00
1108', NULL, '20:30 a 22:00
1109', 'Cabrera Tejeda Juan Jose');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. CIRCUITOS DE CA Y CD', '3CV22', NULL, NULL, NULL, '19:00 a 20:30
Lab. Micros', NULL, 'Cabrera Tejeda Juan Jose');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CIRCUITOS LOGICOS I', '3CV23', '19:00 a 20:30
1113', '20:30 a 22:00
1115', '17:30 a 19:00
1112', NULL, NULL, 'Diaz Rosas Javier Fernando');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. CIRCUITOS LOGICOS I', '3CV23', NULL, NULL, NULL, '17:30 a 19:00', NULL, 'Diaz Rosas Javier Fernando');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LENGUAJES DE BAJO NIVEL', '3CV24', NULL, NULL, '19:00 a 20:30
2205', NULL, '19:00 a 20:30
2205', 'Valles Montanez Luis');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. LENGUAJES DE BAJO NIVEL', '3CV24', NULL, '17:30 a 19:00
UDI 1', NULL, NULL, '17:30 a 19:00
UDI 9', 'Valles Montanez Luis');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. LENGUAJES DE BAJO NIVEL', '3CV24', NULL, '17:30 a 19:00', NULL, NULL, '17:30 a 19:00', 'Bautista Arias Jose Luis');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ESTRUCTURA DE DATOS', '3CV25', NULL, '16:00 a 17:30
PB05', '16:00 a 17:30
PB06', NULL, NULL, 'Gonzalez Acatitla Clarissa');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. ESTRUCTURA DE DATOS', '3CV25', '17:30 a 19:00
Lab. Computación 1', NULL, NULL, '20:30 a 22:00
Lab. Computación 1', NULL, 'Gonzalez Acatitla Clarissa');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES III: DESARROLLO HUMANO', '3CV26', '20:30 a 22:00
1114', NULL, NULL, NULL, '16:00 a 17:30
1115', 'Santos Jacome Celsa Piedad');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ECUACIONES DIFERENCIALES', '3CV31', NULL, '17:30 a 19:00
1112', NULL, '17:30 a 19:00
1110', '17:30 a 19:00
1110', 'Benitez Diaz Francisco Javier');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CIRCUITOS DE CA Y CD', '3CV32', '16:00 a 17:30
3109', '16:00 a 17:30
Lab. Micros', NULL, NULL, NULL, 'Ugalde Licea Adolfo Sabino');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. CIRCUITOS DE CA Y CD', '3CV32', NULL, NULL, '16:00 a 17:30
3205', NULL, NULL, 'Ugalde Licea Adolfo Sabino');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CIRCUITOS LOGICOS I', '3CV33', NULL, '19:00 a 20:30
1115', '20:30 a 22:00
1109', '19:00 a 20:30
1114', NULL, 'Diaz Rosas Javier Fernando');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. CIRCUITOS LOGICOS I', '3CV33', NULL, NULL, NULL, NULL, '20:30 a 22:00', 'Diaz Rosas Javier Fernando');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LENGUAJES DE BAJO NIVEL', '3CV34', '20:30 a 22:00
2205', NULL, '17:30 a 19:00
2205', NULL, NULL, 'Valles Montanez Luis');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. LENGUAJES DE BAJO NIVEL', '3CV34', NULL, NULL, NULL, '20:30 a 22:00
UDI 9', '16:00 a 17:30
UDI 9', 'Valles Montanez Luis');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ESTRUCTURA DE DATOS', '3CV35', NULL, '20:30 a 22:00
2207', '19:00 a 20:30
3105', NULL, NULL, 'De La Cruz Tellez Arturo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. ESTRUCTURA DE DATOS', '3CV35', '19:00 a 20:30
UDI 7', NULL, NULL, NULL, '19:00 a 20:30
UDI 7', 'De La Cruz Tellez Arturo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES III: DESARROLLO HUMANO', '3CV36', '17:30 a 19:00
3111', NULL, NULL, '16:00 a 17:30
3106', NULL, 'Moreno Guzmán María Araceli');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CIRCUITOS DE CA Y CD', '3CX12', '13:00 a 14:30
1110', '13:00 a 14:30
1110', '13:00 a 14:30
1110', NULL, NULL, 'Guzman Rodriguez Jose Eduardo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. CIRCUITOS DE CA Y CD', '3CX12', NULL, NULL, NULL, NULL, NULL, 'Guzman Rodriguez Jose Eduardo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CIRCUITOS LOGICOS I', '3CX13', NULL, '13:00 a 14:30
Lab. Micros', '13:00 a 14:30
1113', '13:00 a 14:30
1113', '13:00 a 14:30
1113', 'Martinez Martinez Margarita');
-- Total de registros insertados de Vespertino_3_IC: 35

-- Datos de la hoja: Matutino_3_IC
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ECUACIONES DIFERENCIALES', '3CM11', '13:00 a 14:30
1210', NULL, '7:00 a 8:30
1207', NULL, '13:00 a 14:30
1103', 'Solís Luna Nancy Brisa');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CIRCUITOS DE CA Y CD', '3CM12', '10:00 a 11:30
3107', '11:30 a 13:00
3110', NULL, NULL, NULL, 'Angoa Torres Anselmo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. CIRCUITOS DE CA Y CD', '3CM12', NULL, NULL, NULL, '7:00 a 8:30
Lab. Micros', NULL, 'Angoa Torres Anselmo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CIRCUITOS LOGICOS I', '3CM13', '8:30 a 10:00
Lab. Micros', NULL, '8:30 a 10:00
PB04', NULL, '11:30 a 13:00
PB06', 'Rodriguez Peralta Patricia');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. CIRCUITOS LOGICOS I', '3CM13', NULL, NULL, NULL, '11:30 a 13:00
PB04', NULL, 'Rodriguez Peralta Patricia');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LENGUAJES DE BAJO NIVEL', '3CM14', NULL, '10:00 a 11:30
1102', NULL, '10:00 a 11:30
1102', NULL, 'Martinez Martinez Margarita');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. LENGUAJES DE BAJO NIVEL', '3CM14', NULL, NULL, '10:00 a 11:30
Lab. Computación 1', NULL, '10:00 a 11:30
Lab. Computación 1', 'Martinez Martinez Margarita');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ESTRUCTURA DE DATOS', '3CM15', NULL, '8:30 a 10:00
1208', NULL, '8:30 a 10:00
1205', NULL, 'Azuara Perez Lorena');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. ESTRUCTURA DE DATOS', '3CM15', '7:00 a 8:30
Lab. Computación 2', NULL, '11:30 a 13:00
Lab. Computación 2', NULL, NULL, 'Azuara Perez Lorena');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES III: DESARROLLO HUMANO', '3CM16', NULL, '7:00 a 8:30
2209', NULL, NULL, '7:00 a 8:30
2209', 'Cervantes Cabello Graciela Irene');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ECUACIONES DIFERENCIALES', '3CM21', '13:00 a 14:30
1111', '13:00 a 14:30
1111', '13:00 a 14:30
1109', NULL, NULL, 'Gonzalez Lopez Santiago');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CIRCUITOS DE CA Y CD', '3CM22', '8:30 a 10:00
3107', NULL, NULL, NULL, '11:30 a 13:00
Lab. Micros', 'Angoa Torres Anselmo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. CIRCUITOS DE CA Y CD', '3CM22', NULL, NULL, NULL, '10:00 a 11:30
2215', NULL, 'Angoa Torres Anselmo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CIRCUITOS LOGICOS I', '3CM23', NULL, '11:30 a 13:00
PB02', NULL, '8:30 a 10:00
PB03', '10:00 a 11:30
PB06', 'Rodriguez Peralta Patricia');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. CIRCUITOS LOGICOS I', '3CM23', '10:00 a 11:30
Lab. Micros', NULL, NULL, NULL, NULL, 'Rodriguez Peralta Patricia');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LENGUAJES DE BAJO NIVEL', '3CM24', NULL, NULL, '11:30 a 13:00
3204', NULL, '7:00 a 8:30
1209', 'Martinez Martinez Margarita');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. LENGUAJES DE BAJO NIVEL', '3CM24', NULL, '8:30 a 10:00
Lab. Computación 1', NULL, '11:30 a 13:00
UDI 1', NULL, 'Martinez Martinez Margarita');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ESTRUCTURA DE DATOS', '3CM25', '11:30 a 13:00
1208', NULL, '10:00 a 11:30
1206', NULL, NULL, 'Azuara Perez Lorena');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. ESTRUCTURA DE DATOS', '3CM25', NULL, '10:00 a 11:30
Lab. Computación 1', NULL, '7:00 a 8:30
Lab. Computación 2', NULL, 'Azuara Perez Lorena');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES III: DESARROLLO HUMANO', '3CM26', NULL, NULL, '8:30 a 10:00
3104', NULL, '8:30 a 10:00
3104', 'Vigueras Bonilla Maria Juana');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ECUACIONES DIFERENCIALES', '3CM31', NULL, '11:30 a 13:00
1215', '7:00 a 8:30
1119', '7:00 a 8:30
1205', NULL, 'Hernandez Suarez Aldo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CIRCUITOS DE CA Y CD', '3CM32', '11:30 a 13:00
2204', NULL, NULL, NULL, '7:00 a 8:30
2206', 'Guzman Rodriguez Jose Eduardo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. CIRCUITOS DE CA Y CD', '3CM32', NULL, '10:00 a 11:30', NULL, NULL, NULL, 'Guzman Rodriguez Jose Eduardo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CIRCUITOS LOGICOS I', '3CM33', '8:30 a 10:00
3215', NULL, '8:30 a 10:00
1209', '8:30 a 10:00
Lab. Micros', NULL, 'Ramirez Hernandez Jazmin');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. CIRCUITOS LOGICOS I', '3CM33', NULL, NULL, NULL, NULL, '8:30 a 10:00
3111', 'Ramirez Hernandez Jazmin');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LENGUAJES DE BAJO NIVEL', '3CM34', NULL, NULL, '11:30 a 13:00
3212', '11:30 a 13:00
3212', NULL, 'Arcos Pichardo Alejandro');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. LENGUAJES DE BAJO NIVEL', '3CM34', '13:00 a 14:30
Lab. Computación 1', '13:00 a 14:30
Lab. Computación 1', NULL, NULL, NULL, 'Arcos Pichardo Alejandro');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ESTRUCTURA DE DATOS', '3CM35', NULL, NULL, '10:00 a 11:30
1205', NULL, '11:30 a 13:00
1211', 'Ley Mandujano Jose Juan');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. ESTRUCTURA DE DATOS', '3CM35', '10:00 a 11:30
Lab. Computación 2', NULL, NULL, '10:00 a 11:30
Lab. Computación 2', NULL, 'Ley Mandujano Jose Juan');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES III: DESARROLLO HUMANO', '3CM36', NULL, '8:30 a 10:00
1108', NULL, NULL, '10:00 a 11:30
1106', '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ECUACIONES DIFERENCIALES', '3CM41', NULL, '10:00 a 11:30
1106', NULL, '7:00 a 8:30
1103', '7:00 a 8:30
1103', 'Angel Huerta Froylan');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CIRCUITOS DE CA Y CD', '3CM42', '10:00 a 11:30
1108', NULL, '10:00 a 11:30
1109', NULL, NULL, 'Cabrera Tejeda Juan Jose');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. CIRCUITOS DE CA Y CD', '3CM42', NULL, NULL, NULL, '13:00 a 14:30
Lab. Micros', NULL, 'Cabrera Tejeda Juan Jose');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CIRCUITOS LOGICOS I', '3CM43', '11:30 a 13:00
3214', '8:30 a 10:00
1213', NULL, NULL, '10:00 a 11:30
1206', 'Ramirez Hernandez Jazmin');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. CIRCUITOS LOGICOS I', '3CM43', NULL, NULL, '11:30 a 13:00
Lab. Micros', NULL, NULL, 'Ramirez Hernandez Jazmin');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LENGUAJES DE BAJO NIVEL', '3CM44', NULL, NULL, NULL, '8:30 a 10:00
3114', NULL, 'Estrada Arriaga Carlos Alberto');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. LENGUAJES DE BAJO NIVEL', '3CM44', '13:00 a 14:30
UDI 8', '11:30 a 13:00
UDI 8', NULL, NULL, '8:30 a 10:00
UDI 8', 'Estrada Arriaga Carlos Alberto');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ESTRUCTURA DE DATOS', '3CM45', '8:30 a 10:00
1110', '7:00 a 8:30
Lab. Computación 2', NULL, NULL, NULL, 'Azuara Perez Lorena');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. ESTRUCTURA DE DATOS', '3CM45', NULL, NULL, '7:00 a 8:30
1215', '10:00 a 11:30
Lab. Computación 1', NULL, 'Azuara Perez Lorena');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES III: DESARROLLO HUMANO', '3CM46', NULL, NULL, '8:30 a 10:00
2209', NULL, '11:30 a 13:00
2209', 'Cervantes Cabello Graciela Irene');
-- Total de registros insertados de Matutino_3_IC: 40

-- Datos de la hoja: Table008 (Page 4) (4)
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ESTRUCTURA DE DATOS', '3CM45', '8:30 a 10:00
1110', '7:00 a 8:30
Lab. Computación 2', NULL, NULL, NULL, 'Azuara Perez Lorena');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. ESTRUCTURA DE DATOS', '3CM45', NULL, NULL, '7:00 a 8:30
1215', '10:00 a 11:30
Lab. Computación 1', NULL, 'Azuara Perez Lorena');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. ESTRUCTURA DE DATOS', '3CM45', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES III: DESARROLLO HUMANO', '3CM46', NULL, NULL, '8:30 a 10:00
2209', NULL, '11:30 a 13:00
2209', 'Cervantes Cabello Graciela Irene');
-- Total de registros insertados de Table008 (Page 4) (4): 4

-- Datos de la hoja: Table006 (Page 3) (4)
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LENGUAJES DE BAJO NIVEL', '3CM34', NULL, NULL, '11:30 a 13:00
3212', '11:30 a 13:00
3212', NULL, 'Arcos Pichardo Alejandro');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. LENGUAJES DE BAJO NIVEL', '3CM34', '13:00 a 14:30
Lab. Computación 1', '13:00 a 14:30
Lab. Computación 1', NULL, NULL, NULL, 'Arcos Pichardo Alejandro');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. LENGUAJES DE BAJO NIVEL', '3CM34', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ESTRUCTURA DE DATOS', '3CM35', NULL, NULL, '10:00 a 11:30
1205', NULL, '11:30 a 13:00
1211', 'Ley Mandujano Jose Juan');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. ESTRUCTURA DE DATOS', '3CM35', '10:00 a 11:30
Lab. Computación 2', NULL, NULL, '10:00 a 11:30
Lab. Computación 2', NULL, 'Ley Mandujano Jose Juan');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. ESTRUCTURA DE DATOS', '3CM35', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES III: DESARROLLO HUMANO', '3CM36', NULL, '8:30 a 10:00
1108', NULL, NULL, '10:00 a 11:30
1106', '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ECUACIONES DIFERENCIALES', '3CM41', NULL, '10:00 a 11:30
1106', NULL, '7:00 a 8:30
1103', '7:00 a 8:30
1103', 'Angel Huerta Froylan');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CIRCUITOS DE CA Y CD', '3CM42', '10:00 a 11:30
1108', NULL, '10:00 a 11:30
1109', NULL, NULL, 'Cabrera Tejeda Juan Jose');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. CIRCUITOS DE CA Y CD', '3CM42', NULL, NULL, NULL, '13:00 a 14:30
Lab. Micros', NULL, 'Cabrera Tejeda Juan Jose');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. CIRCUITOS DE CA Y CD', '3CM42', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CIRCUITOS LOGICOS I', '3CM43', '11:30 a 13:00
3214', '8:30 a 10:00
1213', NULL, NULL, '10:00 a 11:30
1206', 'Ramirez Hernandez Jazmin');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. CIRCUITOS LOGICOS I', '3CM43', NULL, NULL, '11:30 a 13:00
Lab. Micros', NULL, NULL, 'Ramirez Hernandez Jazmin');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. CIRCUITOS LOGICOS I', '3CM43', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LENGUAJES DE BAJO NIVEL', '3CM44', NULL, NULL, NULL, '8:30 a 10:00
3114', NULL, 'Estrada Arriaga Carlos Alberto');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. LENGUAJES DE BAJO NIVEL', '3CM44', '13:00 a 14:30
UDI 8', '11:30 a 13:00
UDI 8', NULL, NULL, '8:30 a 10:00
UDI 8', 'Estrada Arriaga Carlos Alberto');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. LENGUAJES DE BAJO NIVEL', '3CM44', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
-- Total de registros insertados de Table006 (Page 3) (4): 17

-- Datos de la hoja: Table004 (Page 2) (5)
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. CIRCUITOS DE CA Y CD', '3CM22', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CIRCUITOS LOGICOS I', '3CM23', NULL, '11:30 a 13:00
PB02', NULL, '8:30 a 10:00
PB03', '10:00 a 11:30
PB06', 'Rodriguez Peralta Patricia');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. CIRCUITOS LOGICOS I', '3CM23', '10:00 a 11:30
Lab. Micros', NULL, NULL, NULL, NULL, 'Rodriguez Peralta Patricia');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. CIRCUITOS LOGICOS I', '3CM23', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LENGUAJES DE BAJO NIVEL', '3CM24', NULL, NULL, '11:30 a 13:00
3204', NULL, '7:00 a 8:30
1209', 'Martinez Martinez Margarita');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. LENGUAJES DE BAJO NIVEL', '3CM24', NULL, '8:30 a 10:00
Lab. Computación 1', NULL, '11:30 a 13:00
UDI 1', NULL, 'Martinez Martinez Margarita');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. LENGUAJES DE BAJO NIVEL', '3CM24', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ESTRUCTURA DE DATOS', '3CM25', '11:30 a 13:00
1208', NULL, '10:00 a 11:30
1206', NULL, NULL, 'Azuara Perez Lorena');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. ESTRUCTURA DE DATOS', '3CM25', NULL, '10:00 a 11:30
Lab. Computación 1', NULL, '7:00 a 8:30
Lab. Computación 2', NULL, 'Azuara Perez Lorena');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. ESTRUCTURA DE DATOS', '3CM25', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES III: DESARROLLO HUMANO', '3CM26', NULL, NULL, '8:30 a 10:00
3104', NULL, '8:30 a 10:00
3104', 'Vigueras Bonilla Maria Juana');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ECUACIONES DIFERENCIALES', '3CM31', NULL, '11:30 a 13:00
1215', '7:00 a 8:30
1119', '7:00 a 8:30
1205', NULL, 'Hernandez Suarez Aldo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CIRCUITOS DE CA Y CD', '3CM32', '11:30 a 13:00
2204', NULL, NULL, NULL, '7:00 a 8:30
2206', 'Guzman Rodriguez Jose Eduardo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. CIRCUITOS DE CA Y CD', '3CM32', NULL, '10:00 a 11:30', NULL, NULL, NULL, 'Guzman Rodriguez Jose Eduardo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. CIRCUITOS DE CA Y CD', '3CM32', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CIRCUITOS LOGICOS I', '3CM33', '8:30 a 10:00
3215', NULL, '8:30 a 10:00
1209', '8:30 a 10:00
Lab. Micros', NULL, 'Ramirez Hernandez Jazmin');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. CIRCUITOS LOGICOS I', '3CM33', NULL, NULL, NULL, NULL, '8:30 a 10:00
3111', 'Ramirez Hernandez Jazmin');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. CIRCUITOS LOGICOS I', '3CM33', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
-- Total de registros insertados de Table004 (Page 2) (5): 18

-- Datos de la hoja: Table002 (Page 1) (5)
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ECUACIONES DIFERENCIALES', '3CM11', '13:00 a 14:30
1210', NULL, '7:00 a 8:30
1207', NULL, '13:00 a 14:30
1103', 'Solís Luna Nancy Brisa');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CIRCUITOS DE CA Y CD', '3CM12', '10:00 a 11:30
3107', '11:30 a 13:00
3110', NULL, NULL, NULL, 'Angoa Torres Anselmo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. CIRCUITOS DE CA Y CD', '3CM12', NULL, NULL, NULL, '7:00 a 8:30
Lab. Micros', NULL, 'Angoa Torres Anselmo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. CIRCUITOS DE CA Y CD', '3CM12', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CIRCUITOS LOGICOS I', '3CM13', '8:30 a 10:00
Lab. Micros', NULL, '8:30 a 10:00
PB04', NULL, '11:30 a 13:00
PB06', 'Rodriguez Peralta Patricia');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. CIRCUITOS LOGICOS I', '3CM13', NULL, NULL, NULL, '11:30 a 13:00
PB04', NULL, 'Rodriguez Peralta Patricia');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. CIRCUITOS LOGICOS I', '3CM13', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LENGUAJES DE BAJO NIVEL', '3CM14', NULL, '10:00 a 11:30
1102', NULL, '10:00 a 11:30
1102', NULL, 'Martinez Martinez Margarita');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. LENGUAJES DE BAJO NIVEL', '3CM14', NULL, NULL, '10:00 a 11:30
Lab. Computación 1', NULL, '10:00 a 11:30
Lab. Computación 1', 'Martinez Martinez Margarita');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. LENGUAJES DE BAJO NIVEL', '3CM14', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ESTRUCTURA DE DATOS', '3CM15', NULL, '8:30 a 10:00
1208', NULL, '8:30 a 10:00
1205', NULL, 'Azuara Perez Lorena');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. ESTRUCTURA DE DATOS', '3CM15', '7:00 a 8:30
Lab. Computación 2', NULL, '11:30 a 13:00
Lab. Computación 2', NULL, NULL, 'Azuara Perez Lorena');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. ESTRUCTURA DE DATOS', '3CM15', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES III: DESARROLLO HUMANO', '3CM16', NULL, '7:00 a 8:30
2209', NULL, NULL, '7:00 a 8:30
2209', 'Cervantes Cabello Graciela Irene');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ECUACIONES DIFERENCIALES', '3CM21', '13:00 a 14:30
1111', '13:00 a 14:30
1111', '13:00 a 14:30
1109', NULL, NULL, 'Gonzalez Lopez Santiago');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CIRCUITOS DE CA Y CD', '3CM22', '8:30 a 10:00
3107', NULL, NULL, NULL, '11:30 a 13:00
Lab. Micros', 'Angoa Torres Anselmo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. CIRCUITOS DE CA Y CD', '3CM22', NULL, NULL, NULL, '10:00 a 11:30
2215', NULL, 'Angoa Torres Anselmo');
-- Total de registros insertados de Table002 (Page 1) (5): 17

-- Datos de la hoja: Vespertino_2_IC
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ALGEBRA LINEAL', '2CV31', NULL, '17:30 a 19:00
3203', NULL, NULL, '16:00 a 17:30
3203', 'Vargas Reyes Orlando');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CALCULO VECTORIAL', '2CV32', '19:00 a 20:30
3108', '19:00 a 20:30
3107', '20:30 a 22:00
3107', '19:00 a 20:30
3104', NULL, 'Galvan de Sampedro Roberto Pedro');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ELECTRICIDAD Y MAGNETISMO', '2CV33', '20:30 a 22:00
1212', NULL, '17:30 a 19:00
Lab. Física', NULL, '19:00 a 20:30
1215', 'Martínez López Juan Gabriel');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. ELECTRICIDAD Y MAGNETISMO', '2CV33', NULL, NULL, NULL, '20:30 a 22:00
1215', NULL, 'Martínez López Juan Gabriel');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('MATEMATICAS DISCRETAS', '2CV34', '16:00 a 17:30
3113', NULL, '19:00 a 20:30
3113', '17:30 a 19:00
3113', '20:30 a 22:00
3215', 'Rodriguez Gomez Juan Angel');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('PROGRAMACION ORIENTADA A OBJETOS', '2CV35', NULL, '20:30 a 22:00
2106', NULL, '14:30 a 16:00
2112', NULL, 'Mora Jain Jesus');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. PROGRAMACION ORIENTADA A OBJETOS', '2CV35', '17:30 a 19:00
Lab. Computación 2', NULL, NULL, NULL, '17:30 a 19:00
Lab. Computación 2', 'Mora Jain Jesus');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES II LA COMUNICACION Y LA INGENIERIA', '2CV36', NULL, '14:30 a 16:00
3102', '16:00 a 17:30
3115', NULL, NULL, 'Enriquez Arreola Sandra Luz');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ALGEBRA LINEAL', '2CV41', '20:30 a 22:00
1109', NULL, NULL, NULL, '16:00 a 17:30
1110', 'Benitez Diaz Francisco Javier');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CALCULO VECTORIAL', '2CV42', NULL, '17:30 a 19:00
1205', '17:30 a 19:00
1202', '17:30 a 19:00
1203', '19:00 a 20:30
1204', 'Morales Vergara Pedro');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ELECTRICIDAD Y MAGNETISMO', '2CV43', NULL, NULL, '16:00 a 17:30
1108', '16:00 a 17:30
1114', '17:30 a 19:00
1202', 'Cortés Pineda Patricia');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. ELECTRICIDAD Y MAGNETISMO', '2CV43', NULL, '16:00 a 17:30
Lab. Física', NULL, NULL, NULL, 'Cortés Pineda Patricia');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('MATEMATICAS DISCRETAS', '2CV44', '19:00 a 20:30
3208', '19:00 a 20:30
3208', '19:00 a 20:30
3208', '19:00 a 20:30
3209', NULL, 'Arcos Pichardo Alejandro');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('PROGRAMACION ORIENTADA A OBJETOS', '2CV45', '17:30 a 19:00
2207', NULL, NULL, '20:30 a 22:00
2207', NULL, 'De La Cruz Tellez Arturo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. PROGRAMACION ORIENTADA A OBJETOS', '2CV45', NULL, NULL, '20:30 a 22:00
Lab. Computación 1', NULL, '20:30 a 22:00', 'De La Cruz Tellez Arturo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES II LA COMUNICACION Y LA INGENIERIA', '2CV46', '16:00 a 17:30
3214', '20:30 a 22:00
3110', NULL, NULL, NULL, 'Enriquez Arreola Sandra Luz');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('PROGRAMACION ORIENTADA A OBJETOS', '2CX15', '13:00 a 14:30
Lab. Computación 2', '13:00 a 14:30
1104', '13:00 a 14:30
1104', '13:00 a 14:30
Lab. Computación 1', NULL, 'Azuara Perez Lorena');
-- Total de registros insertados de Vespertino_2_IC: 17

-- Datos de la hoja: Table004 (Page 2) (4)
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. PROGRAMACION ORIENTADA A OBJETOS', '2CV45', NULL, NULL, '20:30 a 22:00
Lab. Computación 1', NULL, '20:30 a 22:00', 'De La Cruz Tellez Arturo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. PROGRAMACION ORIENTADA A OBJETOS', '2CV45', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES II LA COMUNICACION Y LA INGENIERIA', '2CV46', '16:00 a 17:30
3214', '20:30 a 22:00
3110', NULL, NULL, NULL, 'Enriquez Arreola Sandra Luz');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('PROGRAMACION ORIENTADA A OBJETOS', '2CX15', '13:00 a 14:30
Lab. Computación 2', '13:00 a 14:30
1104', '13:00 a 14:30
1104', '13:00 a 14:30
Lab. Computación 1', NULL, 'Azuara Perez Lorena');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. PROGRAMACION ORIENTADA A OBJETOS', '2CX15', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. PROGRAMACION ORIENTADA A OBJETOS', '2CX15', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
-- Total de registros insertados de Table004 (Page 2) (4): 6

-- Datos de la hoja: Table002 (Page 1) (4)
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ALGEBRA LINEAL', '2CV31', NULL, '17:30 a 19:00
3203', NULL, NULL, '16:00 a 17:30
3203', 'Vargas Reyes Orlando');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CALCULO VECTORIAL', '2CV32', '19:00 a 20:30
3108', '19:00 a 20:30
3107', '20:30 a 22:00
3107', '19:00 a 20:30
3104', NULL, 'Galvan de Sampedro Roberto Pedro');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ELECTRICIDAD Y MAGNETISMO', '2CV33', '20:30 a 22:00
1212', NULL, '17:30 a 19:00
Lab. Física', NULL, '19:00 a 20:30
1215', 'Martínez López Juan Gabriel');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. ELECTRICIDAD Y MAGNETISMO', '2CV33', NULL, NULL, NULL, '20:30 a 22:00
1215', NULL, 'Martínez López Juan Gabriel');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. ELECTRICIDAD Y MAGNETISMO', '2CV33', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('MATEMATICAS DISCRETAS', '2CV34', '16:00 a 17:30
3113', NULL, '19:00 a 20:30
3113', '17:30 a 19:00
3113', '20:30 a 22:00
3215', 'Rodriguez Gomez Juan Angel');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('PROGRAMACION ORIENTADA A OBJETOS', '2CV35', NULL, '20:30 a 22:00
2106', NULL, '14:30 a 16:00
2112', NULL, 'Mora Jain Jesus');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. PROGRAMACION ORIENTADA A OBJETOS', '2CV35', '17:30 a 19:00
Lab. Computación 2', NULL, NULL, NULL, '17:30 a 19:00
Lab. Computación 2', 'Mora Jain Jesus');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. PROGRAMACION ORIENTADA A OBJETOS', '2CV35', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES II LA COMUNICACION Y LA INGENIERIA', '2CV36', NULL, '14:30 a 16:00
3102', '16:00 a 17:30
3115', NULL, NULL, 'Enriquez Arreola Sandra Luz');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ALGEBRA LINEAL', '2CV41', '20:30 a 22:00
1109', NULL, NULL, NULL, '16:00 a 17:30
1110', 'Benitez Diaz Francisco Javier');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CALCULO VECTORIAL', '2CV42', NULL, '17:30 a 19:00
1205', '17:30 a 19:00
1202', '17:30 a 19:00
1203', '19:00 a 20:30
1204', 'Morales Vergara Pedro');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ELECTRICIDAD Y MAGNETISMO', '2CV43', NULL, NULL, '16:00 a 17:30
1108', '16:00 a 17:30
1114', '17:30 a 19:00
1202', 'Cortés Pineda Patricia');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. ELECTRICIDAD Y MAGNETISMO', '2CV43', NULL, '16:00 a 17:30
Lab. Física', NULL, NULL, NULL, 'Cortés Pineda Patricia');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. ELECTRICIDAD Y MAGNETISMO', '2CV43', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('MATEMATICAS DISCRETAS', '2CV44', '19:00 a 20:30
3208', '19:00 a 20:30
3208', '19:00 a 20:30
3208', '19:00 a 20:30
3209', NULL, 'Arcos Pichardo Alejandro');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('PROGRAMACION ORIENTADA A OBJETOS', '2CV45', '17:30 a 19:00
2207', NULL, NULL, '20:30 a 22:00
2207', NULL, 'De La Cruz Tellez Arturo');
-- Total de registros insertados de Table002 (Page 1) (4): 17

-- Datos de la hoja: Matutino_2_IC
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ALGEBRA LINEAL', '2CM11', '11:30 a 13:00
1107', NULL, '11:30 a 13:00
1110', NULL, NULL, 'Carvajal Quiroz Eliel');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CALCULO VECTORIAL', '2CM12', '13:00 a 14:30
1202', '11:30 a 13:00
1202', NULL, '10:00 a 11:30
2104', '11:30 a 13:00
1202', 'Gonzalez Medina Vera');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ELECTRICIDAD Y MAGNETISMO', '2CM13', '10:00 a 11:30
1110', NULL, '8:30 a 10:00
1109', NULL, '8:30 a 10:00
1110', 'Vasco Mendez Edna Carla');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. ELECTRICIDAD Y MAGNETISMO', '2CM13', NULL, '10:00 a 11:30
Lab. Física', NULL, NULL, NULL, 'Vasco Mendez Edna Carla');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('MATEMATICAS DISCRETAS', '2CM14', NULL, '13:00 a 14:30
PB02', '13:00 a 14:30
PB02', '13:00 a 14:30
PB02', '13:00 a 14:30
PB02', 'Valverde Jiménez Jessica');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('PROGRAMACION ORIENTADA A OBJETOS', '2CM15', NULL, NULL, '10:00 a 11:30
1201', '8:30 a 10:00
1204', NULL, 'Corona Ramirez Beatriz Eugenia');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. PROGRAMACION ORIENTADA A OBJETOS', '2CM15', '8:30 a 10:00
Lab. Computación 1', '8:30 a 10:00
Lab. Computación 2', NULL, NULL, NULL, 'Corona Ramirez Beatriz Eugenia');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES II LA COMUNICACION Y LA INGENIERIA', '2CM16', NULL, NULL, NULL, '11:30 a 13:00
1108', '10:00 a 11:30
1108', 'Ramírez Negrete María de Lourdes');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ALGEBRA LINEAL', '2CM21', '7:00 a 8:30
3112', NULL, NULL, '10:00 a 11:30
3113', NULL, 'Perez Torres Carlos');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CALCULO VECTORIAL', '2CM22', NULL, '7:00 a 8:30
2208', '7:00 a 8:30
2208', '7:00 a 8:30
2208', '7:00 a 8:30
2208', 'Cabrera Rivas Xochitl');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ELECTRICIDAD Y MAGNETISMO', '2CM23', '10:00 a 11:30
3213', NULL, NULL, '8:30 a 10:00
1211', '10:00 a 11:30
3206', 'Cubillos Islas Irene');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. ELECTRICIDAD Y MAGNETISMO', '2CM23', NULL, NULL, '8:30 a 10:00
Lab. Física', NULL, NULL, 'Cubillos Islas Irene');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('MATEMATICAS DISCRETAS', '2CM24', '8:30 a 10:00
3114', '8:30 a 10:00
3113', '10:00 a 11:30
3114', '11:30 a 13:00
3113', NULL, 'Rodriguez Gomez Juan Angel');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('PROGRAMACION ORIENTADA A OBJETOS', '2CM25', '11:30 a 13:00
1207', NULL, NULL, NULL, '8:30 a 10:00
1214', 'Corona Ramirez Beatriz Eugenia');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. PROGRAMACION ORIENTADA A OBJETOS', '2CM25', NULL, '10:00 a 11:30
Lab. Computación 2', '11:30 a 13:00
Lab. Computación 1', NULL, NULL, 'Corona Ramirez Beatriz Eugenia');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES II LA COMUNICACION Y LA INGENIERIA', '2CM26', NULL, '11:30 a 13:00
3208', NULL, NULL, '11:30 a 13:00
3114', 'Moreno Guzmán María Araceli');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ALGEBRA LINEAL', '2CM31', NULL, NULL, '11:30 a 13:00
2208', '13:00 a 14:30
2208', NULL, 'Cabrera Rivas Xochitl');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CALCULO VECTORIAL', '2CM32', '8:30 a 10:00
1210', '11:30 a 13:00
1113', '8:30 a 10:00
1205', '7:00 a 8:30
1203', NULL, 'Ley Mandujano Jose Juan');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ELECTRICIDAD Y MAGNETISMO', '2CM33', NULL, '8:30 a 10:00
1212', NULL, '11:30 a 13:00
1211', '8:30 a 10:00
3206', 'Cubillos Islas Irene');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. ELECTRICIDAD Y MAGNETISMO', '2CM33', NULL, NULL, '10:00 a 11:30
Lab. Física', NULL, NULL, 'Cubillos Islas Irene');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('MATEMATICAS DISCRETAS', '2CM34', NULL, '13:00 a 14:30
3203', '13:00 a 14:30
3101', '10:00 a 11:30
3110', '13:00 a 14:30
3108', 'Rodríguez Acosta Adolfo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('PROGRAMACION ORIENTADA A OBJETOS', '2CM35', '10:00 a 11:30
3105', '10:00 a 11:30
3204', NULL, NULL, NULL, 'Flores Ascencio Sabas');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. PROGRAMACION ORIENTADA A OBJETOS', '2CM35', '11:30 a 13:00
Lab. Computación 2', NULL, NULL, NULL, '11:30 a 13:00
Lab. Computación 1', 'Flores Ascencio Sabas');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES II LA COMUNICACION Y LA INGENIERIA', '2CM36', NULL, NULL, NULL, '8:30 a 10:00
2209', '10:00 a 11:30
2209', 'Cervantes Cabello Graciela Irene');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ALGEBRA LINEAL', '2CM41', '11:30 a 13:00
1111', NULL, '11:30 a 13:00
1109', NULL, NULL, 'Gonzalez Lopez Santiago');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CALCULO VECTORIAL', '2CM42', '13:00 a 14:30
3102', '13:00 a 14:30
3101', NULL, '11:30 a 13:00
3105', '11:30 a 13:00
3102', 'Heredia Velasco Alma Rosa');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ELECTRICIDAD Y MAGNETISMO', '2CM43', NULL, NULL, '13:00 a 14:30
Lab. Física', '13:00 a 14:30
1115', '13:00 a 14:30
1101', 'Cortés Pineda Patricia');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. ELECTRICIDAD Y MAGNETISMO', '2CM43', '8:30 a 10:00
3115', NULL, NULL, NULL, NULL, 'Cortés Pineda Patricia');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('MATEMATICAS DISCRETAS', '2CM44', NULL, '11:30 a 13:00
3203', '10:00 a 11:30
3106', '8:30 a 10:00
3110', '10:00 a 11:30
3108', 'Rodríguez Acosta Adolfo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('PROGRAMACION ORIENTADA A OBJETOS', '2CM45', NULL, '8:30 a 10:00
UDI 9', NULL, NULL, '8:30 a 10:00
1213', 'Valdés Galicia Claudio Augusto');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. PROGRAMACION ORIENTADA A OBJETOS', '2CM45', NULL, NULL, '8:30 a 10:00
Lab. Computación 1', '14:30 a 16:00
1105', NULL, 'Valdés Galicia Claudio Augusto');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES II LA COMUNICACION Y LA INGENIERIA', '2CM46', '10:00 a 11:30
1105', '10:00 a 11:30
1108', NULL, NULL, NULL, 'Flores Martinez Citlali');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ALGEBRA LINEAL', '2CV11', NULL, '16:00 a 17:30
1206', NULL, NULL, '16:00 a 17:30
2201', 'Márquez Rubio Juan Francisco');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CALCULO VECTORIAL', '2CV12', '16:00 a 17:30
1104', '19:00 a 20:30
1105', '16:00 a 17:30
1105', '16:00 a 17:30
1105', NULL, 'Angel Huerta Froylan');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ELECTRICIDAD Y MAGNETISMO', '2CV13', '17:30 a 19:00
1112', NULL, NULL, '20:30 a 22:00
1108', '17:30 a 19:00
1114', 'Lopez Gonzalez Rodolfo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. ELECTRICIDAD Y MAGNETISMO', '2CV13', NULL, NULL, '17:30 a 19:00
Lab. Física 1', NULL, NULL, 'Lopez Gonzalez Rodolfo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('MATEMATICAS DISCRETAS', '2CV14', '20:30 a 22:00
2213', '20:30 a 22:00
2213', '20:30 a 22:00
2213', NULL, '20:30 a 22:00
2213', 'Muñoz Guerrero Mario Antonio');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('PROGRAMACION ORIENTADA A OBJETOS', '2CV15', NULL, '17:30 a 19:00
1209', NULL, '17:30 a 19:00
1113', NULL, 'Cruz Garcia Oscar');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. PROGRAMACION ORIENTADA A OBJETOS', '2CV15', '19:00 a 20:30
Lab. Computación 2', NULL, NULL, NULL, '19:00 a 20:30
Lab. Computación 2', 'Cruz Garcia Oscar');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. PROGRAMACION ORIENTADA A OBJETOS', '2CV15', '19:00 a 20:30', NULL, NULL, NULL, '19:00 a 20:30', 'Resendiz Colin Pilar');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES II LA COMUNICACION Y LA INGENIERIA', '2CV16', NULL, NULL, '19:00 a 20:30
1102', '19:00 a 20:30
1106', NULL, 'Flores Martinez Citlali');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ALGEBRA LINEAL', '2CV21', NULL, NULL, NULL, '19:00 a 20:30
1110', '19:00 a 20:30
1110', 'Benitez Diaz Francisco Javier');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CALCULO VECTORIAL', '2CV22', '17:30 a 19:00
1104', '17:30 a 19:00
1105', '17:30 a 19:00
1105', '20:30 a 22:00
1105', NULL, 'Angel Huerta Froylan');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ELECTRICIDAD Y MAGNETISMO', '2CV23', '16:00 a 17:30
1112', '19:00 a 20:30
1114', NULL, NULL, '16:00 a 17:30
1114', 'Lopez Gonzalez Rodolfo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. ELECTRICIDAD Y MAGNETISMO', '2CV23', NULL, NULL, '16:00 a 17:30
Lab. Física', NULL, NULL, 'Lopez Gonzalez Rodolfo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('MATEMATICAS DISCRETAS', '2CV24', '14:30 a 16:00
1115', '16:00 a 17:30
1112', NULL, '16:00 a 17:30
1201', '14:30 a 16:00
1205', 'Rodríguez Buendía Jesús');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('PROGRAMACION ORIENTADA A OBJETOS', '2CV25', NULL, NULL, '19:00 a 20:30
PB06', '17:30 a 19:00
PB06', NULL, 'Gonzalez Acatitla Clarissa');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. PROGRAMACION ORIENTADA A OBJETOS', '2CV25', '19:00 a 20:30
Lab. Computación 1', NULL, NULL, NULL, '17:30 a 19:00
Lab. Computación 1', 'Gonzalez Acatitla Clarissa');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES II LA COMUNICACION Y LA INGENIERIA', '2CV26', NULL, '20:30 a 22:00
1207', '20:30 a 22:00
1110', NULL, NULL, 'Santos Jacome Celsa Piedad');
-- Total de registros insertados de Matutino_2_IC: 49

-- Datos de la hoja: Table008 (Page 4) (3)
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ELECTRICIDAD Y MAGNETISMO', '2CV23', '16:00 a 17:30
1112', '19:00 a 20:30
1114', NULL, NULL, '16:00 a 17:30
1114', 'Lopez Gonzalez Rodolfo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. ELECTRICIDAD Y MAGNETISMO', '2CV23', NULL, NULL, '16:00 a 17:30
Lab. Física', NULL, NULL, 'Lopez Gonzalez Rodolfo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. ELECTRICIDAD Y MAGNETISMO', '2CV23', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('MATEMATICAS DISCRETAS', '2CV24', '14:30 a 16:00
1115', '16:00 a 17:30
1112', NULL, '16:00 a 17:30
1201', '14:30 a 16:00
1205', 'Rodríguez Buendía Jesús');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('PROGRAMACION ORIENTADA A OBJETOS', '2CV25', NULL, NULL, '19:00 a 20:30
PB06', '17:30 a 19:00
PB06', NULL, 'Gonzalez Acatitla Clarissa');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. PROGRAMACION ORIENTADA A OBJETOS', '2CV25', '19:00 a 20:30
Lab. Computación 1', NULL, NULL, NULL, '17:30 a 19:00
Lab. Computación 1', 'Gonzalez Acatitla Clarissa');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. PROGRAMACION ORIENTADA A OBJETOS', '2CV25', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES II LA COMUNICACION Y LA INGENIERIA', '2CV26', NULL, '20:30 a 22:00
1207', '20:30 a 22:00
1110', NULL, NULL, 'Santos Jacome Celsa Piedad');
-- Total de registros insertados de Table008 (Page 4) (3): 8

-- Datos de la hoja: Table006 (Page 3) (3)
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('MATEMATICAS DISCRETAS', '2CM44', NULL, '11:30 a 13:00
3203', '10:00 a 11:30
3106', '8:30 a 10:00
3110', '10:00 a 11:30
3108', 'Rodríguez Acosta Adolfo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('PROGRAMACION ORIENTADA A OBJETOS', '2CM45', NULL, '8:30 a 10:00
UDI 9', NULL, NULL, '8:30 a 10:00
1213', 'Valdés Galicia Claudio Augusto');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. PROGRAMACION ORIENTADA A OBJETOS', '2CM45', NULL, NULL, '8:30 a 10:00
Lab. Computación 1', '14:30 a 16:00
1105', NULL, 'Valdés Galicia Claudio Augusto');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. PROGRAMACION ORIENTADA A OBJETOS', '2CM45', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES II LA COMUNICACION Y LA INGENIERIA', '2CM46', '10:00 a 11:30
1105', '10:00 a 11:30
1108', NULL, NULL, NULL, 'Flores Martinez Citlali');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ALGEBRA LINEAL', '2CV11', NULL, '16:00 a 17:30
1206', NULL, NULL, '16:00 a 17:30
2201', 'Márquez Rubio Juan Francisco');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CALCULO VECTORIAL', '2CV12', '16:00 a 17:30
1104', '19:00 a 20:30
1105', '16:00 a 17:30
1105', '16:00 a 17:30
1105', NULL, 'Angel Huerta Froylan');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ELECTRICIDAD Y MAGNETISMO', '2CV13', '17:30 a 19:00
1112', NULL, NULL, '20:30 a 22:00
1108', '17:30 a 19:00
1114', 'Lopez Gonzalez Rodolfo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. ELECTRICIDAD Y MAGNETISMO', '2CV13', NULL, NULL, '17:30 a 19:00
Lab. Física 1', NULL, NULL, 'Lopez Gonzalez Rodolfo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. ELECTRICIDAD Y MAGNETISMO', '2CV13', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('MATEMATICAS DISCRETAS', '2CV14', '20:30 a 22:00
2213', '20:30 a 22:00
2213', '20:30 a 22:00
2213', NULL, '20:30 a 22:00
2213', 'Muñoz Guerrero Mario Antonio');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('PROGRAMACION ORIENTADA A OBJETOS', '2CV15', NULL, '17:30 a 19:00
1209', NULL, '17:30 a 19:00
1113', NULL, 'Cruz Garcia Oscar');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. PROGRAMACION ORIENTADA A OBJETOS', '2CV15', '19:00 a 20:30
Lab. Computación 2', NULL, NULL, NULL, '19:00 a 20:30
Lab. Computación 2', 'Cruz Garcia Oscar');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. PROGRAMACION ORIENTADA A OBJETOS', '2CV15', '19:00 a 20:30', NULL, NULL, NULL, '19:00 a 20:30', 'Resendiz Colin Pilar');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES II LA COMUNICACION Y LA INGENIERIA', '2CV16', NULL, NULL, '19:00 a 20:30
1102', '19:00 a 20:30
1106', NULL, 'Flores Martinez Citlali');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ALGEBRA LINEAL', '2CV21', NULL, NULL, NULL, '19:00 a 20:30
1110', '19:00 a 20:30
1110', 'Benitez Diaz Francisco Javier');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CALCULO VECTORIAL', '2CV22', '17:30 a 19:00
1104', '17:30 a 19:00
1105', '17:30 a 19:00
1105', '20:30 a 22:00
1105', NULL, 'Angel Huerta Froylan');
-- Total de registros insertados de Table006 (Page 3) (3): 17

-- Datos de la hoja: Table004 (Page 2) (3)
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. PROGRAMACION ORIENTADA A OBJETOS', '2CM25', NULL, '10:00 a 11:30
Lab. Computación 2', '11:30 a 13:00
Lab. Computación 1', NULL, NULL, 'Corona Ramirez Beatriz Eugenia');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. PROGRAMACION ORIENTADA A OBJETOS', '2CM25', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES II LA COMUNICACION Y LA INGENIERIA', '2CM26', NULL, '11:30 a 13:00
3208', NULL, NULL, '11:30 a 13:00
3114', 'Moreno Guzmán María Araceli');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ALGEBRA LINEAL', '2CM31', NULL, NULL, '11:30 a 13:00
2208', '13:00 a 14:30
2208', NULL, 'Cabrera Rivas Xochitl');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CALCULO VECTORIAL', '2CM32', '8:30 a 10:00
1210', '11:30 a 13:00
1113', '8:30 a 10:00
1205', '7:00 a 8:30
1203', NULL, 'Ley Mandujano Jose Juan');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ELECTRICIDAD Y MAGNETISMO', '2CM33', NULL, '8:30 a 10:00
1212', NULL, '11:30 a 13:00
1211', '8:30 a 10:00
3206', 'Cubillos Islas Irene');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. ELECTRICIDAD Y MAGNETISMO', '2CM33', NULL, NULL, '10:00 a 11:30
Lab. Física', NULL, NULL, 'Cubillos Islas Irene');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. ELECTRICIDAD Y MAGNETISMO', '2CM33', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('MATEMATICAS DISCRETAS', '2CM34', NULL, '13:00 a 14:30
3203', '13:00 a 14:30
3101', '10:00 a 11:30
3110', '13:00 a 14:30
3108', 'Rodríguez Acosta Adolfo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('PROGRAMACION ORIENTADA A OBJETOS', '2CM35', '10:00 a 11:30
3105', '10:00 a 11:30
3204', NULL, NULL, NULL, 'Flores Ascencio Sabas');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. PROGRAMACION ORIENTADA A OBJETOS', '2CM35', '11:30 a 13:00
Lab. Computación 2', NULL, NULL, NULL, '11:30 a 13:00
Lab. Computación 1', 'Flores Ascencio Sabas');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. PROGRAMACION ORIENTADA A OBJETOS', '2CM35', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES II LA COMUNICACION Y LA INGENIERIA', '2CM36', NULL, NULL, NULL, '8:30 a 10:00
2209', '10:00 a 11:30
2209', 'Cervantes Cabello Graciela Irene');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ALGEBRA LINEAL', '2CM41', '11:30 a 13:00
1111', NULL, '11:30 a 13:00
1109', NULL, NULL, 'Gonzalez Lopez Santiago');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CALCULO VECTORIAL', '2CM42', '13:00 a 14:30
3102', '13:00 a 14:30
3101', NULL, '11:30 a 13:00
3105', '11:30 a 13:00
3102', 'Heredia Velasco Alma Rosa');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ELECTRICIDAD Y MAGNETISMO', '2CM43', NULL, NULL, '13:00 a 14:30
Lab. Física', '13:00 a 14:30
1115', '13:00 a 14:30
1101', 'Cortés Pineda Patricia');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. ELECTRICIDAD Y MAGNETISMO', '2CM43', '8:30 a 10:00
3115', NULL, NULL, NULL, NULL, 'Cortés Pineda Patricia');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. ELECTRICIDAD Y MAGNETISMO', '2CM43', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
-- Total de registros insertados de Table004 (Page 2) (3): 18

-- Datos de la hoja: Table002 (Page 1) (3)
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ALGEBRA LINEAL', '2CM11', '11:30 a 13:00
1107', NULL, '11:30 a 13:00
1110', NULL, NULL, 'Carvajal Quiroz Eliel');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CALCULO VECTORIAL', '2CM12', '13:00 a 14:30
1202', '11:30 a 13:00
1202', NULL, '10:00 a 11:30
2104', '11:30 a 13:00
1202', 'Gonzalez Medina Vera');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ELECTRICIDAD Y MAGNETISMO', '2CM13', '10:00 a 11:30
1110', NULL, '8:30 a 10:00
1109', NULL, '8:30 a 10:00
1110', 'Vasco Mendez Edna Carla');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. ELECTRICIDAD Y MAGNETISMO', '2CM13', NULL, '10:00 a 11:30
Lab. Física', NULL, NULL, NULL, 'Vasco Mendez Edna Carla');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. ELECTRICIDAD Y MAGNETISMO', '2CM13', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('MATEMATICAS DISCRETAS', '2CM14', NULL, '13:00 a 14:30
PB02', '13:00 a 14:30
PB02', '13:00 a 14:30
PB02', '13:00 a 14:30
PB02', 'Valverde Jiménez Jessica');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('PROGRAMACION ORIENTADA A OBJETOS', '2CM15', NULL, NULL, '10:00 a 11:30
1201', '8:30 a 10:00
1204', NULL, 'Corona Ramirez Beatriz Eugenia');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. PROGRAMACION ORIENTADA A OBJETOS', '2CM15', '8:30 a 10:00
Lab. Computación 1', '8:30 a 10:00
Lab. Computación 2', NULL, NULL, NULL, 'Corona Ramirez Beatriz Eugenia');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. PROGRAMACION ORIENTADA A OBJETOS', '2CM15', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES II LA COMUNICACION Y LA INGENIERIA', '2CM16', NULL, NULL, NULL, '11:30 a 13:00
1108', '10:00 a 11:30
1108', 'Ramírez Negrete María de Lourdes');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ALGEBRA LINEAL', '2CM21', '7:00 a 8:30
3112', NULL, NULL, '10:00 a 11:30
3113', NULL, 'Perez Torres Carlos');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CALCULO VECTORIAL', '2CM22', NULL, '7:00 a 8:30
2208', '7:00 a 8:30
2208', '7:00 a 8:30
2208', '7:00 a 8:30
2208', 'Cabrera Rivas Xochitl');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('ELECTRICIDAD Y MAGNETISMO', '2CM23', '10:00 a 11:30
3213', NULL, NULL, '8:30 a 10:00
1211', '10:00 a 11:30
3206', 'Cubillos Islas Irene');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. ELECTRICIDAD Y MAGNETISMO', '2CM23', NULL, NULL, '8:30 a 10:00
Lab. Física', NULL, NULL, 'Cubillos Islas Irene');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. ELECTRICIDAD Y MAGNETISMO', '2CM23', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('MATEMATICAS DISCRETAS', '2CM24', '8:30 a 10:00
3114', '8:30 a 10:00
3113', '10:00 a 11:30
3114', '11:30 a 13:00
3113', NULL, 'Rodriguez Gomez Juan Angel');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('PROGRAMACION ORIENTADA A OBJETOS', '2CM25', '11:30 a 13:00
1207', NULL, NULL, NULL, '8:30 a 10:00
1214', 'Corona Ramirez Beatriz Eugenia');
-- Total de registros insertados de Table002 (Page 1) (3): 17

-- Datos de la hoja: Vespertino_1_IC
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CALCULO DIFERENCIAL E INTEGRAL', '1CV11', '20:30 a 22:00
1104', '20:30 a 22:00
1105', '20:30 a 22:00
1105', '19:00 a 20:30
1105', NULL, 'Angel Huerta Froylan');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FUNDAMENTOS DE ALGEBRA', '1CV12', '19:00 a 20:30
1201', NULL, NULL, NULL, '16:00 a 17:30
1214', 'Olivares Mercado Jesus');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FISICA CLASICA', '1CV13', '16:00 a 17:30
1212', '19:00 a 20:30
Lab. Física', NULL, '16:00 a 17:30
3208', NULL, 'Martínez López Juan Gabriel');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FISICA CLASICA', '1CV13', NULL, NULL, '16:00 a 17:30
2215', NULL, NULL, 'Martínez López Juan Gabriel');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('QUIMICA BASICA', '1CV14', NULL, NULL, '17:30 a 19:00
PB03', '17:30 a 19:00
PB03', NULL, 'Aponte Olaya Julian Hugo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. QUIMICA BASICA', '1CV14', NULL, NULL, NULL, NULL, '19:00 a 20:30
Lab. Química', 'Aponte Olaya Julian Hugo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. QUIMICA BASICA', '1CV14', NULL, NULL, NULL, NULL, '19:00 a 20:30', '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FUNDAMENTOS DE PROGRAMACION', '1CV15', NULL, '16:00 a 17:30
1209', NULL, '20:30 a 22:00
1202', NULL, 'Cruz Garcia Oscar');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FUNDAMENTOS DE PROGRAMACION', '1CV15', NULL, NULL, '19:00 a 20:30
Lab. Computación 1', NULL, '20:30 a 22:00
Lab. Computación 1', 'Cruz Garcia Oscar');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES I INGENIERA CIENCIA Y SOCIEDAD', '1CV16', '17:30 a 19:00
1114', '17:30 a 19:00
1207', NULL, NULL, '17:30 a 19:00
1115', 'Santos Jacome Celsa Piedad');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CALCULO DIFERENCIAL E INTEGRAL', '1CV21', NULL, '19:00 a 20:30
1205', '19:00 a 20:30
1202', '19:00 a 20:30
1203', '17:30 a 19:00
1204', 'Morales Vergara Pedro');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FUNDAMENTOS DE ALGEBRA', '1CV22', NULL, NULL, NULL, '14:30 a 16:00
3113', '16:00 a 17:30
3113', 'Rodriguez Gomez Juan Angel');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FISICA CLASICA', '1CV23', '14:30 a 16:00
3102', '14:30 a 16:00
Lab. Física', NULL, NULL, '14:30 a 16:00
3103', 'Cubillos Islas Irene');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FISICA CLASICA', '1CV23', NULL, NULL, '14:30 a 16:00
1106', NULL, NULL, 'Cubillos Islas Irene');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('QUIMICA BASICA', '1CV24', '17:30 a 19:00
1113', NULL, NULL, '17:30 a 19:00
1103', NULL, 'Rojo Hernández Maribel');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. QUIMICA BASICA', '1CV24', NULL, NULL, '16:00 a 17:30
Lab. Química', NULL, NULL, 'Rojo Hernández Maribel');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. QUIMICA BASICA', '1CV24', NULL, NULL, '16:00 a 17:30', NULL, NULL, 'Aponte Olaya Julian Hugo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FUNDAMENTOS DE PROGRAMACION', '1CV25', NULL, NULL, NULL, '16:00 a 17:30
2112', '19:00 a 20:30
2106', 'Mora Jain Jesus');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FUNDAMENTOS DE PROGRAMACION', '1CV25', '16:00 a 17:30
Lab. Computación 2', '17:30 a 19:00
Lab. Computación 1', NULL, NULL, NULL, 'Mora Jain Jesus');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES I INGENIERA CIENCIA Y SOCIEDAD', '1CV26', '19:00 a 20:30
1114', '16:00 a 17:30
1207', '17:30 a 19:00
1113', NULL, NULL, 'Santos Jacome Celsa Piedad');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CALCULO DIFERENCIAL E INTEGRAL', '1CV31', '14:30 a 16:00
1113', '14:30 a 16:00
1205', NULL, '20:30 a 22:00
1203', '14:30 a 16:00
1204', 'Morales Vergara Pedro');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FUNDAMENTOS DE ALGEBRA', '1CV32', NULL, NULL, '16:00 a 17:30
1113', NULL, '17:30 a 19:00
1214', 'Olivares Mercado Jesus');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FISICA CLASICA', '1CV33', '19:00 a 20:30
1112', NULL, '19:00 a 20:30
Lab. Física 1', '17:30 a 19:00
1109', NULL, 'Lopez Gonzalez Rodolfo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FISICA CLASICA', '1CV33', NULL, '16:00 a 17:30
1214', NULL, NULL, NULL, 'Lopez Gonzalez Rodolfo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('QUIMICA BASICA', '1CV34', NULL, NULL, '14:30 a 16:00
1105', '14:30 a 16:00
1104', NULL, 'Pablo Gopar Gloria Alejandra');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. QUIMICA BASICA', '1CV34', NULL, NULL, NULL, '19:00 a 20:30
Lab. Química', NULL, 'Pablo Gopar Gloria Alejandra');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. QUIMICA BASICA', '1CV34', NULL, NULL, NULL, '19:00 a 20:30', NULL, 'Aquino Salinas Fernando David');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FUNDAMENTOS DE PROGRAMACION', '1CV35', NULL, '17:30 a 19:00
PB05', '17:30 a 19:00
PB06', NULL, NULL, 'Gonzalez Acatitla Clarissa');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FUNDAMENTOS DE PROGRAMACION', '1CV35', '20:30 a 22:00
Lab. Computación 1', NULL, NULL, NULL, '16:00 a 17:30
Lab. Computación 1', 'Gonzalez Acatitla Clarissa');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES I INGENIERA CIENCIA Y SOCIEDAD', '1CV36', '16:00 a 17:30
1114', '19:00 a 20:30
1207', NULL, '16:00 a 17:30
1111', NULL, 'Santos Jacome Celsa Piedad');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CALCULO DIFERENCIAL E INTEGRAL', '1CV41', '20:30 a 22:00
1112', '20:30 a 22:00
1114', NULL, '16:00 a 17:30
1109', '14:30 a 16:00
1114', 'Lopez Gonzalez Rodolfo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FUNDAMENTOS DE ALGEBRA', '1CV42', NULL, '16:00 a 17:30
2208', '16:00 a 17:30
2208', NULL, NULL, 'Cabrera Rivas Xochitl');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FISICA CLASICA', '1CV43', '17:30 a 19:00
1212', NULL, NULL, '17:30 a 19:00
3208', '16:00 a 17:30
1215', 'Martínez López Juan Gabriel');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FISICA CLASICA', '1CV43', NULL, NULL, '19:00 a 20:30
Lab. Física', NULL, NULL, 'Martínez López Juan Gabriel');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('QUIMICA BASICA', '1CV44', NULL, '17:30 a 19:00
1103', NULL, '14:30 a 16:00
1103', NULL, 'Amador Zaragoza Irma Alicia');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. QUIMICA BASICA', '1CV44', NULL, NULL, '20:30 a 22:00', NULL, NULL, 'Amador Zaragoza Irma Alicia');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. QUIMICA BASICA', '1CV44', NULL, NULL, '20:30 a 22:00', NULL, NULL, 'Aquino Salinas Fernando David');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FUNDAMENTOS DE PROGRAMACION', '1CV45', NULL, '19:00 a 20:30
PB05', NULL, '19:00 a 20:30
PB06', NULL, 'Gonzalez Acatitla Clarissa');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FUNDAMENTOS DE PROGRAMACION', '1CV45', '16:00 a 17:30
Lab. Computación 1', NULL, NULL, NULL, '19:00 a 20:30
Lab. Computación 1', 'Gonzalez Acatitla Clarissa');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES I INGENIERA CIENCIA Y SOCIEDAD', '1CV46', '19:00 a 20:30
1101', NULL, '17:30 a 19:00
1102', NULL, '17:30 a 19:00
1105', 'Flores Martinez Citlali');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CALCULO DIFERENCIAL E INTEGRAL', '1CV51', '19:00 a 20:30
1104', '16:00 a 17:30
1105', '19:00 a 20:30
1105', '17:30 a 19:00
1105', NULL, 'Angel Huerta Froylan');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FUNDAMENTOS DE ALGEBRA', '1CV52', '14:30 a 16:00
2103', NULL, NULL, '14:30 a 16:00
2103', NULL, 'Bañuelos Duran Amparo');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FISICA CLASICA', '1CV53', NULL, '17:30 a 19:00
3206', '14:30 a 16:00
Lab. Física', '19:00 a 20:30
3208', NULL, 'Martínez López Juan Gabriel');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FISICA CLASICA', '1CV53', NULL, NULL, NULL, NULL, '14:30 a 16:00
2102', 'Martínez López Juan Gabriel');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('QUIMICA BASICA', '1CV54', NULL, NULL, NULL, '16:00 a 17:30
1205', '19:00 a 20:30
1208', 'Aquino Salinas Fernando David');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. QUIMICA BASICA', '1CV54', '16:00 a 17:30
Lab. Química', NULL, NULL, NULL, NULL, 'Aquino Salinas Fernando David');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. QUIMICA BASICA', '1CV54', '16:00 a 17:30', NULL, NULL, NULL, NULL, 'Amador Zaragoza Irma Alicia');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FUNDAMENTOS DE PROGRAMACION', '1CV55', '17:30 a 19:00
2205', NULL, NULL, NULL, '16:00 a 17:30
1202', 'Cruz Garcia Oscar');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FUNDAMENTOS DE PROGRAMACION', '1CV55', NULL, '20:30 a 22:00
Lab. Computación 1', '17:30 a 19:00
Lab. Computación 1', NULL, NULL, 'Cruz Garcia Oscar');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES I INGENIERA CIENCIA Y SOCIEDAD', '1CV56', '13:00 a 14:30
3104', NULL, '13:00 a 14:30
3104', NULL, '13:00 a 14:30
3104', 'Vigueras Bonilla Maria Juana');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FUNDAMENTOS DE ALGEBRA', '1CX12', '13:00 a 14:30
2203', NULL, '13:00 a 14:30
2203', NULL, NULL, 'Olivares Mercado Jesus');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FUNDAMENTOS DE ALGEBRA', '1CX22', NULL, NULL, '08:30 a 10:00
1204', '08:30 a 10:00
1207', NULL, 'Rodríguez Buendía Jesús');
-- Total de registros insertados de Vespertino_1_IC: 52

-- Datos de la hoja: Matutino_1_IC
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CALCULO DIFERENCIAL E INTEGRAL', '1CM11', '11:30 a 13:00
1202', '10:00 a 11:30
1202', NULL, '8:30 a 10:00
2104', '10:00 a 11:30
1202', 'Gonzalez Medina Vera');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FUNDAMENTOS DE ALGEBRA', '1CM12', NULL, '13:00 a 14:30
2208', NULL, NULL, '8:30 a 10:00
2208', 'Cabrera Rivas Xochitl');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FISICA CLASICA', '1CM13', '10:00 a 11:30
1111', '11:30 a 13:00
1111', NULL, NULL, '7:00 a 8:30
Lab. Física', 'Gonzalez Lopez Santiago');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FISICA CLASICA', '1CM13', NULL, NULL, '10:00 a 11:30
1210', NULL, NULL, 'Gonzalez Lopez Santiago');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FISICA CLASICA', '1CM13', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('QUIMICA BASICA', '1CM14', '7:00 a 8:30
1104', NULL, NULL, '7:00 a 8:30
1104', NULL, 'Aniceto Vargas Paula Flora');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. QUIMICA BASICA', '1CM14', NULL, NULL, '8:30 a 10:00
Lab. Química', NULL, NULL, 'Aniceto Vargas Paula Flora');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. QUIMICA BASICA', '1CM14', NULL, NULL, '8:30 a 10:00', NULL, NULL, 'Rojo Hernández Maribel');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FUNDAMENTOS DE PROGRAMACION', '1CM15', NULL, NULL, '7:00 a 8:30
3105', '11:30 a 13:00
2106', NULL, 'Azorín Vega Claudia');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FUNDAMENTOS DE PROGRAMACION', '1CM15', '8:30 a 10:00
Lab. Computación 2', '8:30 a 10:00
UDI 1', NULL, NULL, NULL, 'Azorín Vega Claudia');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FUNDAMENTOS DE PROGRAMACION', '1CM15', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES I INGENIERA CIENCIA Y SOCIEDAD', '1CM16', NULL, NULL, '11:30 a 13:00
1206', '10:00 a 11:30
1108', '11:30 a 13:00
1214', 'Flores Martinez Citlali');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CALCULO DIFERENCIAL E INTEGRAL', '1CM21', '8:30 a 10:00
3101', '8:30 a 10:00
3102', '8:30 a 10:00
3101', '8:30 a 10:00
3102', NULL, 'Diaz Albarran Salvador Felipe');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FUNDAMENTOS DE ALGEBRA', '1CM22', '7:00 a 8:30
1111', NULL, NULL, NULL, '8:30 a 10:00
1112', 'Gonzalez Lopez Santiago');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FISICA CLASICA', '1CM23', '11:30 a 13:00
3213', NULL, NULL, '10:00 a 11:30
1211', '11:30 a 13:00
3206', 'Cubillos Islas Irene');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FISICA CLASICA', '1CM23', NULL, NULL, '7:00 a 8:30
Lab. Física', NULL, NULL, 'Cubillos Islas Irene');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FISICA CLASICA', '1CM23', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('QUIMICA BASICA', '1CM24', NULL, '10:00 a 11:30
1113', '10:00 a 11:30
1112', NULL, NULL, 'Rojo Hernández Maribel');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. QUIMICA BASICA', '1CM24', NULL, '13:00 a 14:30
Lab. Química', NULL, NULL, NULL, 'Rojo Hernández Maribel');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. QUIMICA BASICA', '1CM24', NULL, '13:00 a 14:30', NULL, NULL, NULL, 'Pablo Gopar Gloria Alejandra');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FUNDAMENTOS DE PROGRAMACION', '1CM25', '10:00 a 11:30
1207', NULL, NULL, NULL, '7:00 a 8:30
1214', 'Corona Ramirez Beatriz Eugenia');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FUNDAMENTOS DE PROGRAMACION', '1CM25', NULL, '11:30 a 13:00
Lab. Computación 2', NULL, '11:30 a 13:00
Lab. Computación 1', NULL, 'Corona Ramirez Beatriz Eugenia');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FUNDAMENTOS DE PROGRAMACION', '1CM25', NULL, NULL, NULL, NULL, NULL, '-- Sin Asignar --');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES I INGENIERA CIENCIA Y SOCIEDAD', '1CM26', NULL, NULL, '11:30 a 13:00
3115', '13:00 a 14:30
3104', '10:00 a 11:30
3114', 'Moreno Guzmán María Araceli');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CALCULO DIFERENCIAL E INTEGRAL', '1CM31', NULL, '7:00 a 8:30
1201', '7:00 a 8:30
1205', '11:30 a 13:00
1207', '7:00 a 8:30
1211', 'Ley Mandujano Jose Juan');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FUNDAMENTOS DE ALGEBRA', '1CM32', '8:30 a 10:00
1111', '10:00 a 11:30
1111', NULL, NULL, NULL, 'Gonzalez Lopez Santiago');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FISICA CLASICA', '1CM33', '7:00 a 8:30
1110', '8:30 a 10:00
1101', NULL, NULL, '10:00 a 11:30
1110', 'Vasco Mendez Edna Carla');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FISICA CLASICA', '1CM33', NULL, NULL, '11:30 a 13:00
Lab. Física', NULL, NULL, 'Vasco Mendez Edna Carla');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('QUIMICA BASICA', '1CM34', '10:00 a 11:30
1102', NULL, NULL, '10:00 a 11:30
1107', NULL, 'Aniceto Vargas Paula Flora');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. QUIMICA BASICA', '1CM34', NULL, NULL, '10:00 a 11:30
Lab. Química', NULL, NULL, 'Aniceto Vargas Paula Flora');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. QUIMICA BASICA', '1CM34', NULL, NULL, '10:00 a 11:30', NULL, NULL, 'RODRIGUEZ JIMENEZ LUISA IVONE');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FUNDAMENTOS DE PROGRAMACION', '1CM35', '11:30 a 13:00
3210', NULL, NULL, NULL, '11:30 a 13:00
3204', 'Hernandez Lopez Marisol');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FUNDAMENTOS DE PROGRAMACION', '1CM35', NULL, '11:30 a 13:00
Lab. Computación 1', NULL, '7:00 a 8:30
Lab. Computación 1', NULL, 'Hernandez Lopez Marisol');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CALCULO DIFERENCIAL E INTEGRAL', '1CM41', '10:00 a 11:30
3109', '8:30 a 10:00
3109', '8:30 a 10:00
3108', '10:00 a 11:30
3109', NULL, 'Villarreal Aguirre Jose Luis');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FUNDAMENTOS DE ALGEBRA', '1CM42', NULL, NULL, NULL, '8:30 a 10:00
1203', '8:30 a 10:00
1211', 'Ley Mandujano Jose Juan');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FISICA CLASICA', '1CM43', '8:30 a 10:00
3213', NULL, '11:30 a 13:00
3203', '13:00 a 14:30
1211', NULL, 'Cubillos Islas Irene');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FISICA CLASICA', '1CM43', NULL, '13:00 a 14:30
Lab. Física', NULL, NULL, NULL, 'Cubillos Islas Irene');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('QUIMICA BASICA', '1CM44', NULL, '11:30 a 13:00
1211', NULL, NULL, '10:00 a 11:30
1213', 'Pablo Gopar Gloria Alejandra');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. QUIMICA BASICA', '1CM44', NULL, NULL, '13:00 a 14:30
Lab. Química', NULL, NULL, 'Pablo Gopar Gloria Alejandra');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. QUIMICA BASICA', '1CM44', NULL, NULL, '13:00 a 14:30', NULL, NULL, 'Aniceto Vargas Paula Flora');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FUNDAMENTOS DE PROGRAMACION', '1CM45', NULL, NULL, NULL, '11:30 a 13:00
1102', '11:30 a 13:00
2202', 'Salas Jimenez Veronica');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FUNDAMENTOS DE PROGRAMACION', '1CM45', '11:30 a 13:00
Lab. Computación 1', '10:00 a 11:30
UDI 6', NULL, NULL, NULL, 'Salas Jimenez Veronica');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES I INGENIERA CIENCIA Y SOCIEDAD', '1CM46', '13:00 a 14:30
1105', NULL, '10:00 a 11:30
1105', NULL, '13:00 a 14:30
1106', 'Flores Martinez Citlali');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('CALCULO DIFERENCIAL E INTEGRAL', '1CM51', NULL, '8:30 a 10:00
2208', '10:00 a 11:30
2208', '8:30 a 10:00
2208', '10:00 a 11:30
2208', 'Cabrera Rivas Xochitl');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FUNDAMENTOS DE ALGEBRA', '1CM52', '11:30 a 13:00
3102', NULL, '11:30 a 13:00
3102', NULL, NULL, 'Heredia Velasco Alma Rosa');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FISICA CLASICA', '1CM53', NULL, '13:00 a 14:30
1101', NULL, '13:00 a 14:30
1101', '11:30 a 13:00
1110', 'Olivares Robles Miguel Angel');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FISICA CLASICA', '1CM53', NULL, NULL, '13:00 a 14:30
Lab. Física 1', NULL, NULL, 'Olivares Robles Miguel Angel');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('QUIMICA BASICA', '1CM54', '13:00 a 14:30
1103', NULL, NULL, NULL, '13:00 a 14:30
1104', 'Pablo Gopar Gloria Alejandra');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. QUIMICA BASICA', '1CM54', '10:00 a 11:30
Lab. Química', NULL, NULL, NULL, NULL, 'Pablo Gopar Gloria Alejandra');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. QUIMICA BASICA', '1CM54', '10:00 a 11:30', NULL, NULL, NULL, NULL, 'Salazar Galván Martha Elvia');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('FUNDAMENTOS DE PROGRAMACION', '1CM55', NULL, '11:30 a 13:00
1208', '8:30 a 10:00
3105', NULL, NULL, 'Azorín Vega Claudia');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('LAB. FUNDAMENTOS DE PROGRAMACION', '1CM55', '7:00 a 8:30
UDI 1', NULL, NULL, '10:00 a 11:30
UDI 1', NULL, 'Azorín Vega Claudia');
INSERT INTO horarios (materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor) VALUES ('HUMANIDADES I INGENIERA CIENCIA Y SOCIEDAD', '1CM56', '8:30 a 10:00
3209', '10:00 a 11:30
3201', NULL, '11:30 a 13:00
3111', NULL, 'Enriquez Arreola Sandra Luz');
-- Total de registros insertados de Matutino_1_IC: 53

