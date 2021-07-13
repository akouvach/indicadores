delete from user_asignaciones;
delete from user_proyectos;
delete from user_clientes;
delete from user_motivos;
delete from user_usuarios;

delete from indicadoresValores;
delete from variablesValores;

delete from ponderaciones;
delete from indicadores;
delete from variables;


insert into user_usuarios (id, nombre, apellido, email) 
values 
(1, 'Matias','Salmeri','msalmeri'),
(2, 'Diego','Diego','diego'),
(3, 'Andres','Kouvach','akouvach'),
(4, 'Andres','Saenz','asaenz'),
(5, 'Rocio','rocio','rocio');

insert into user_motivos (id, descripcion)
VALUES
(1,'fin del proyecto'),
(2,'pedido de rotación'),
(3,'salida de la empresa');

insert into user_clientes (id, nombre)
values 
(1,"Cashflows"),
(2, "AT&T"),
(3, "Google");

insert into user_proyectos (id, descripcion, clienteId)
values 
(1,"payments",1),
(2,"gateway",1),
(3,"PCI",1),
(4,"CRM",2),
(5,"IA",3);

insert into user_asignaciones (empresa, du, disciplina, usuarioId, proyectoId, FechaAlta, fechaFin, motivoId)
values 
("Endava","BAD","AP",1,1,"2000-01-01","2005-01-05",1),
("Endava","BAD","AP",1,2,"2005-01-06","2010-10-30",2),
("Endava","BAD","AP",1,4,"2010-11-01",null,null),
("Endava","ROS","PDM",2,4,"2002-01-01","2003-01-31",2),
("Endava","ROS","PDM",2,2,"2003-02-01","2008-10-30",3),
("Endava","BAD","DEV",3,4,"2002-01-01","2003-01-31",2),
("Endava","BAD","DEV",3,2,"2003-02-01","2008-10-30",3),
("Endava","ROS","DEV",4,2,"2020-02-01","2020-11-30",3),
("Endava","BAD","DEV",4,4,"2020-11-30",null,null),
("Endava","ROS","PDR",5,2,"2018-02-01","2019-10-30",3),
("Endava","BAD","PDR",5,4,"2019-10-30",null,null);

/*
Select * from 
(
(
(asignaciones a inner join proyectos p on (a.proyectoId = p.id))
inner join clientes c on (p.clienteID = c.id)
)
inner join usuarios u on (u.id = a.usuarioid)
) 
left join motivos m on (a.motivoId = m.id)
*/

insert into indicadores (id,descripcion, formula, agrupadopor)
values 
(1,"Tiempo promedio en proyectos","{TiempoPromEnProy}/{TiempoPromEstables}","du,disciplina"),
(2,"Nivel de Fit en las asignaciones","{TiempoHastaPedirRotacion}*5","empresa, du, disciplina"),
(3,"Adecuación de ofertas en el mercado","{TasaDeRechazo}","disciplina,grade,ubicacion");


insert into variables (id, descripcion, formula, agrupadopor)
values 
("TiempoPromEnProy","Corresponde al tiempo promedio (en dias) de cada uno de los miembros", "Select  ua.du, ua.disciplina, avg(cast( (julianday(iif(fechaFin is null,date('now'),fechaFin)) - julianday(FechaAlta)) as Integer)) as promedioDias from user_asignaciones ua group by ua.du, ua.disciplina;","du,disciplina"),
("TiempoPromEstables","Tiempo promedio en proyectos de los miembros que están en la empresa hace mas de 5 años.","Select  ua.du, ua.disciplina,avg(cast( (julianday(iif(ua.fechaFin is null,date('now'),ua.fechaFin)) - julianday(ua.FechaAlta)) as Integer)) as promedioDias from user_asignaciones ua inner join (select aux.usuarioId from user_asignaciones aux group by usuarioId having (max(iif(aux.fechaFin is null, date('now'),aux.fechafin)) - min(aux.fechaalta)) >= 5 ) leg on (leg.usuarioId = ua.usuarioid) group by ua.du, ua.disciplina ;","du,disciplina"),
("TiempoHastaPedirRotacion","Tiempo esperado hasta pedir rotacion","select count(1) as cant from user_clientes;",""),
("TasaDeRechazo","Cantidad de ofertas rechazadas/total de ofertas realizadas","Select disciplina, Grade, ubicacion,cast(sum(iif(Extension_de_oferta<>'Aceptada',1,0)) as real) / cast (count(1) as real) as TasaRechazos from ST_New_Hires_PowerMyKPI group by disciplina, Grade,ubicacion;","disciplina, Grade,ubicacion");



insert into ponderaciones (indicadorId, fechaDesde, valorHasta, ponderacion)
values 
(1,"2000-01-01",100,5),
(1,"2000-01-01",1000,4),
(1,"2000-01-01",10000,3),
(1,"2000-01-01",1000000,2),
(1,"2000-01-01",10000000000,1),
(1,"2010-01-01",500,5),
(1,"2010-01-01",5000,4),
(1,"2010-01-01",50000,3),
(1,"2010-01-01",5000000,2),
(1,"2010-01-01",50000000000,1),
(2,"2000-01-01",100,5),
(2,"2000-01-01",1000,4),
(2,"2000-01-01",10000,3),
(2,"2000-01-01",1000000,2),
(2,"2000-01-01",10000000000,1),
(2,"2015-01-01",500,5),
(2,"2015-01-01",5000,4),
(2,"2015-01-01",50000,3),
(2,"2015-01-01",5000000,2),
(2,"2015-01-01",50000000000,1),
(3,"2015-01-01",500,5),
(3,"2015-01-01",5000,4),
(3,"2015-01-01",50000,3),
(3,"2015-01-01",5000000,2),
(3,"2015-01-01",50000000000,1);


/*
select vv.valor 
from 
(select * from variablesValores where variableId = 'TiempoPromEnProy') vv
inner join (select max(fecha) as maxFecha from variablesValores where variableId = 'TiempoPromEnProy' and fecha<'2021-07-01') ult
on (vv.fecha = ult.maxFecha)
*/

/*
Select i.* from 
(Select * from indicadoresValores where indicadorId = 1) i
inner join 
(Select max(fecha) maxFecha from indicadoresValores aux where indicadorId = 1 and fecha<'2021-07-01') m
on (i.fecha = m.maxFecha)

*/

/*
Datos de asignaciones:

Select cast( (julianday(iif(fechaFin is null,date('now'),fechaFin)) - julianday(FechaAlta)) as Integer) as antigDias, * 
from 
((user_asignaciones ua
inner join user_proyectos up
on (ua.proyectoId = up.id)
)
inner join user_clientes uc
on (uc.id = up.clienteId)
) inner join user_usuarios uu
on (uu.id = ua.usuarioId)

*/


insert into "indicadoresValores_pivot" (indicadorId, grupo, Fecha, valor, esSimulacion, du, disciplina, empresa, grade, ubicacion, grupo06, grupo07, grupo08, grupo09, grupo10)
	select '1','BAD;AP','2021-06-20 06:59:55.844868','5','0', 	'BAD', 'AP', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','BAD;DEV','2021-06-20 06:59:55.853958','5','0', 	'BAD', 'DEV', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','BAD;PDR','2021-06-20 06:59:55.888545','4','0', 	'BAD', 'PDR', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','DEV;AP','2021-06-20 06:59:55.909914','5','0', 	'DEV', 'AP', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','ROS;DEV','2021-06-20 06:59:55.929535','5','0', 	'ROS', 'DEV', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','ROS;PDM','2021-06-20 06:59:55.951228','5','0', 	'ROS', 'PDM', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','ROS;PDR','2021-06-20 06:59:55.972929','4','0', 	'ROS', 'PDR', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '2','1;BAD;DEV','2021-06-20 06:59:56.016187','5','0','BAD', 'DEV', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','BAD;AP','2021-06-20 07:04:49.546338','5','0', 	'BAD', 'AP', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','BAD;DEV','2021-06-20 07:04:49.566480','5','0', 	'BAD', 'DEV', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','BAD;PDR','2021-06-20 07:04:49.585432','4','0', 	'BAD', 'PDR', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','DEV;AP','2021-06-20 07:04:49.630143','5','0', 	'DEV', 'AP', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','ROS;DEV','2021-06-20 07:04:49.666705','5','0', 	'ROS', 'DEV', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','ROS;PDM','2021-06-20 07:04:49.696879','5','0', 	'ROS', 'PDM', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','ROS;PDR','2021-06-20 07:04:49.718237','4','0', 	'ROS', 'PDR', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '2','1;BAD;DEV','2021-06-20 07:04:49.782634','5','0','BAD', 'DEV', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','BAD;AP','2021-06-20 11:54:40.244360','5','0', 	'BAD', 'AP', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','BAD;DEV','2021-06-20 11:54:40.254367','5','0', 	'BAD', 'DEV', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','BAD;PDR','2021-06-20 11:54:40.260393','4','0', 	'BAD', 'PDR', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','DEV;AP','2021-06-20 11:54:40.268363','5','0', 	'DEV', 'AP', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','ROS;DEV','2021-06-20 11:54:40.275382','5','0', 	'ROS', 'DEV', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','ROS;PDM','2021-06-20 11:54:40.281360','5','0', 	'ROS', 'PDM', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','ROS;PDR','2021-06-20 11:54:40.288362','4','0', 	'ROS', 'PDR', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '2','1;BAD;DEV','2021-06-20 11:54:40.308385','5','0','BAD', 'DEV', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','BAD;AP','2021-06-21 07:16:29.430087','5','0', 	'BAD', 'AP', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','BAD;DEV','2021-06-21 07:16:29.430087','5','0', 	'BAD', 'DEV', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','BAD;PDR','2021-06-21 07:16:29.445707','4','0', 	'BAD', 'PDR', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','DEV;AP','2021-06-21 07:16:29.445707','5','0', 	'DEV', 'AP', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','ROS;DEV','2021-06-21 07:16:29.461778','5','0', 	'ROS', 'DEV', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','ROS;PDM','2021-06-21 07:16:29.468777','5','0', 	'ROS', 'PDM', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','ROS;PDR','2021-06-21 07:16:29.474777','4','0', 	'ROS', 'PDR', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '2','1;BAD;DEV','2021-06-21 07:16:29.480970','5','0','BAD', 'DEV', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','BAD;AP','2021-06-21 07:18:32.394689','5','0', 	'BAD', 'AP', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','BAD;DEV','2021-06-21 07:18:32.400693','5','0', 	'BAD', 'DEV', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','BAD;PDR','2021-06-21 07:18:32.405690','4','0', 	'BAD', 'PDR', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','DEV;AP','2021-06-21 07:18:32.409690','5','0', 	'DEV', 'AP', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','ROS;DEV','2021-06-21 07:18:32.414106','5','0', 	'ROS', 'DEV', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','ROS;PDM','2021-06-21 07:18:32.414106','5','0', 	'ROS', 'PDM', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','ROS;PDR','2021-06-21 07:18:32.414106','4','0', 	'ROS', 'PDR', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '2','1;ROS;DEV','2021-06-21 07:18:32.437104','5','0','ROS', 'DEV', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','BAD;AP','2021-06-21 07:18:51.256682','5','0', 	'BAD', 'AP', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','BAD;DEV','2021-06-21 07:18:51.272310','5','0', 	'BAD', 'DEV', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','BAD;PDR','2021-06-21 07:18:51.272310','4','0', 	'BAD', 'PDR', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','DEV;AP','2021-06-21 07:18:51.288097','5','0', 	'DEV', 'AP', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','ROS;DEV','2021-06-21 07:18:51.293105','5','0', 	'ROS', 'DEV', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','ROS;PDM','2021-06-21 07:18:51.299098','5','0', 	'ROS', 'PDM', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','ROS;PDR','2021-06-21 07:18:51.305100','4','0', 	'ROS', 'PDR', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '2','1;ROS;DEV','2021-06-21 07:18:51.313167','5','0','ROS', 'DEV', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','BAD;AP','2021-06-21 07:30:22.987806','5','0', 	'BAD', 'AP', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','BAD;DEV','2021-06-21 07:30:22.987806','5','0', 	'BAD', 'DEV', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','BAD;PDR','2021-06-21 07:30:22.987806','4','0', 	'BAD', 'PDR', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','DEV;AP','2021-06-21 07:30:22.987806','5','0', 	'DEV', 'AP', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','ROS;DEV','2021-06-21 07:30:23.003430','5','0', 	'ROS', 'DEV', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','ROS;PDM','2021-06-21 07:30:23.003430','5','0', 	'ROS', 'PDM', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','ROS;PDR','2021-06-21 07:30:23.003430','4','0', 	'ROS', 'PDR', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '2','1;ROS;DEV','2021-06-21 07:30:23.032710','5','0','ROS', 'DEV', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','BAD;AP','2021-07-04 18:32:37.519717','5','0', 	'BAD', 'AP', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','BAD;DEV','2021-07-04 18:32:37.543530','5','0', 	'BAD', 'DEV', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','BAD;PDR','2021-07-04 18:32:37.577412','4','0', 	'BAD', 'PDR', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','DEV;AP','2021-07-04 18:32:37.599091','5','0', 	'DEV', 'AP', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','ROS;DEV','2021-07-04 18:32:37.625966','5','0', 	'ROS', 'DEV', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','ROS;PDM','2021-07-04 18:32:37.651994','5','0', 	'ROS', 'PDM', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','ROS;PDR','2021-07-04 18:32:37.682428','4','0', 	'ROS', 'PDR', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '2','1;ROS;DEV','2021-07-04 18:32:37.721224','5','0','ROS', 'DEV', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','DEV;AP','2021-07-04 18:32:43.312399','5','0', 	'DEV', 'AP', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','ROS;DEV','2021-07-04 18:32:43.325235','5','0', 	'ROS', 'DEV', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','ROS;PDM','2021-07-04 18:32:43.353994','5','0', 	'ROS', 'PDM', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','ROS;PDR','2021-07-04 18:32:43.373221','4','0', 	'ROS', 'PDR', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','BAD;AP','2021-07-04 18:32:43.387778','5','0', 	'BAD', 'AP', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','BAD;DEV','2021-07-04 18:32:43.408313','5','0', 	'BAD', 'DEV', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '2','1;ROS;DEV','2021-07-04 18:32:43.443225','5','0','ROS', 'DEV', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '3','1;EN;AMBA','2021-07-04 18:32:43.485284','5','0', 	NULL, 1, NULL, 'EN', 'AMBA', NULL, NULL, NULL, NULL, NULL union 
	select '3','1;EN;Cordoba','2021-07-04 18:32:43.507816','5','0', NULL, 1, NULL, 'EN', 'Cordoba', NULL, NULL, NULL, NULL, NULL union 
	select '3','1;EN;Otros','2021-07-04 18:32:43.523015','5','0', 	NULL, 1, NULL, 'EN', 'Otros', NULL, NULL, NULL, NULL, NULL union 
	select '3','1;SE;AMBA','2021-07-04 18:32:43.538242','5','0', 	NULL, 1, NULL, 'SE', 'AMBA', NULL, NULL, NULL, NULL, NULL union 
	select '3','1;ST;AMBA','2021-07-04 18:32:43.552408','5','0', 	NULL, 1, NULL, 'ST', 'AMBA', NULL, NULL, NULL, NULL, NULL union 
	select '3','1;ST;Cordoba','2021-07-04 18:32:43.565052','5','0', NULL, 1, NULL, 'ST', 'Cordoba', NULL, NULL, NULL, NULL, NULL union 
	select '3','1;ST;Otros','2021-07-04 18:32:43.574277','5','0', 	NULL, 1, NULL, 'ST', 'Otros', NULL, NULL, NULL, NULL, NULL union 
	select '3','1;TL;AMBA','2021-07-04 18:32:43.589050','5','0', 	NULL, 1, NULL, 'TL', 'AMBA', NULL, NULL, NULL, NULL, NULL union 
	select '3','1;TL;Cordoba','2021-07-04 18:32:43.599459','5','0', NULL, 1, NULL, 'TL', 'Cordoba', NULL, NULL, NULL, NULL, NULL union 
	select '3','1;TL;Otros','2021-07-04 18:32:43.609181','5','0', 	NULL, 1, NULL, 'TL', 'Otros', NULL, NULL, NULL, NULL, NULL union 
	select '3','2;CL;AMBA','2021-07-04 18:32:43.627069','5','0', 	NULL, 2, NULL, 'CL', 'AMBA', NULL, NULL, NULL, NULL, NULL union 
	select '3','2;CL;Cordoba','2021-07-04 18:32:43.639827','5','0', NULL, 2, NULL, 'CL', 'Cordoba', NULL, NULL, NULL, NULL, NULL union 
	select '3','2;EN;AMBA','2021-07-04 18:32:43.652360','5','0', 	NULL, 2, NULL, 'EN', 'AMBA', NULL, NULL, NULL, NULL, NULL union 
	select '3','2;JT;AMBA','2021-07-04 18:32:43.664066','5','0', 	NULL, 2, NULL, 'JT', 'AMBA', NULL, NULL, NULL, NULL, NULL union 
	select '3','2;SE;Cordoba','2021-07-04 18:32:43.674769','5','0', NULL, 2, NULL, 'SE', 'Cordoba', NULL, NULL, NULL, NULL, NULL union 
	select '3','3;CL;AMBA','2021-07-04 18:32:43.686354','5','0', 	NULL, 3, NULL, 'CL', 'AMBA', NULL, NULL, NULL, NULL, NULL union 
	select '3','3;EN;AMBA','2021-07-04 18:32:43.698224','5','0', 	NULL, 3, NULL, 'EN', 'AMBA', NULL, NULL, NULL, NULL, NULL union 
	select '3','3;ST;AMBA','2021-07-04 18:32:43.709298','5','0', 	NULL, 3, NULL, 'ST', 'AMBA', NULL, NULL, NULL, NULL, NULL union 
	select '3','4;CL;AMBA','2021-07-04 18:32:43.722368','5','0', 	NULL, 4, NULL, 'CL', 'AMBA', NULL, NULL, NULL, NULL, NULL union 
	select '3','4;EN;AMBA','2021-07-04 18:32:43.733963','5','0', 	NULL, 4, NULL, 'EN', 'AMBA', NULL, NULL, NULL, NULL, NULL union 
	select '3','4;EN;Cordoba','2021-07-04 18:32:43.740974','5','0', NULL, 4, NULL, 'EN', 'Cordoba', NULL, NULL, NULL, NULL, NULL union 
	select '3','4;ST;Cordoba','2021-07-04 18:32:43.756387','5','0', NULL, 4, NULL, 'ST', 'Cordoba', NULL, NULL, NULL, NULL, NULL union 
	select '3','4;ST;Otros','2021-07-04 18:32:43.763540','5','0', 	NULL, 4, NULL, 'ST', 'Otros', NULL, NULL, NULL, NULL, NULL union 
	select '3','4;TL;AMBA','2021-07-04 18:32:43.778689','5','0', 	NULL, 4, NULL, 'TL', 'AMBA', NULL, NULL, NULL, NULL, NULL union 
	select '1','BAD;AP','2021-07-04 18:35:07.310038','5','0', 		'BAD', 'AP', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','BAD;DEV','2021-07-04 18:35:07.332286','5','0', 		'BAD', 'DEV', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','BAD;PDR','2021-07-04 18:35:07.364628','4','0', 		'BAD', 'PDR', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','DEV;AP','2021-07-04 18:35:07.387645','5','0', 		'DEV', 'AP', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','ROS;DEV','2021-07-04 18:35:07.411101','5','0', 		'ROS', 'DEV', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','ROS;PDM','2021-07-04 18:35:07.435816','5','0', 		'ROS', 'PDM', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '1','ROS;PDR','2021-07-04 18:35:07.457021','4','0', 		'ROS', 'PDR', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 
	select '2','1;BAD;DEV','2021-07-04 18:35:07.501371','5','0', 	'BAD', 'DEV', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL union 	
	select '3','1;EN;AMBA','2021-07-04 18:35:07.543962','5','0', 	NULL, 1, NULL, 'EN', 'AMBA', NULL, NULL, NULL, NULL, NULL union 
	select '3','1;EN;Cordoba','2021-07-04 18:35:07.576034','5','0', NULL, 1, NULL, 'EN', 'Cordoba', NULL, NULL, NULL, NULL, NULL union 
	select '3','1;EN;Otros','2021-07-04 18:35:07.608480','5','0', 	NULL, 1, NULL, 'EN', 'Otros', NULL, NULL, NULL, NULL, NULL union 
	select '3','1;SE;AMBA','2021-07-04 18:35:07.635777','5','0', 	NULL, 1, NULL, 'SE', 'AMBA', NULL, NULL, NULL, NULL, NULL union 
	select '3','1;ST;AMBA','2021-07-04 18:35:07.658984','5','0', 	NULL, 1, NULL, 'ST', 'AMBA', NULL, NULL, NULL, NULL, NULL union 
	select '3','1;ST;Cordoba','2021-07-04 18:35:07.688352','5','0', NULL, 1, NULL, 'ST', 'Cordoba', NULL, NULL, NULL, NULL, NULL union 
	select '3','1;ST;Otros','2021-07-04 18:35:07.718465','5','0', 	NULL, 1, NULL, 'ST', 'Otros', NULL, NULL, NULL, NULL, NULL union 
	select '3','1;TL;AMBA','2021-07-04 18:35:07.749121','5','0', 	NULL, 1, NULL, 'TL', 'AMBA', NULL, NULL, NULL, NULL, NULL union 
	select '3','1;TL;Cordoba','2021-07-04 18:35:07.777313','5','0', NULL, 1, NULL, 'TL', 'Cordoba', NULL, NULL, NULL, NULL, NULL union 
	select '3','1;TL;Otros','2021-07-04 18:35:07.789009','5','0', 	NULL, 1, NULL, 'TL', 'Otros', NULL, NULL, NULL, NULL, NULL union 
	select '3','2;CL;AMBA','2021-07-04 18:35:07.825956','5','0', 	NULL, 2, NULL, 'CL', 'AMBA', NULL, NULL, NULL, NULL, NULL union 
	select '3','2;CL;Cordoba','2021-07-04 18:35:07.859535','5','0', NULL, 2, NULL, 'CL', 'Cordoba', NULL, NULL, NULL, NULL, NULL union 
	select '3','2;EN;AMBA','2021-07-04 18:35:07.885507','5','0', 	NULL, 2, NULL, 'EN', 'AMBA', NULL, NULL, NULL, NULL, NULL union 
	select '3','2;JT;AMBA','2021-07-04 18:35:07.900651','5','0', 	NULL, 2, NULL, 'JT', 'AMBA', NULL, NULL, NULL, NULL, NULL union 
	select '3','2;SE;Cordoba','2021-07-04 18:35:07.928210','5','0', NULL, 2, NULL, 'SE', 'Cordoba', NULL, NULL, NULL, NULL, NULL union 
	select '3','3;CL;AMBA','2021-07-04 18:35:07.959976','5','0', 	NULL, 3, NULL, 'CL', 'AMBA', NULL, NULL, NULL, NULL, NULL union 
	select '3','3;EN;AMBA','2021-07-04 18:35:07.984140','5','0', 	NULL, 3, NULL, 'EN', 'AMBA', NULL, NULL, NULL, NULL, NULL union 
	select '3','3;ST;AMBA','2021-07-04 18:35:08.002561','5','0', 	NULL, 3, NULL, 'ST', 'AMBA', NULL, NULL, NULL, NULL, NULL union 
	select '3','4;CL;AMBA','2021-07-04 18:35:08.011530','5','0', 	NULL, 4, NULL, 'CL', 'AMBA', NULL, NULL, NULL, NULL, NULL union 
	select '3','4;EN;AMBA','2021-07-04 18:35:08.046232','5','0', 	NULL, 4, NULL, 'EN', 'AMBA', NULL, NULL, NULL, NULL, NULL union 
	select '3','4;EN;Cordoba','2021-07-04 18:35:08.069646','5','0', NULL, 4, NULL, 'EN', 'Cordoba', NULL, NULL, NULL, NULL, NULL union 
	select '3','4;ST;Cordoba','2021-07-04 18:35:08.098463','5','0', NULL, 4, NULL, 'ST', 'Cordoba', NULL, NULL, NULL, NULL, NULL union 
	select '3','4;ST;Otros','2021-07-04 18:35:08.124983','5','0', 	NULL, 4, NULL, 'ST', 'Otros', NULL, NULL, NULL, NULL, NULL union 
	select '3','4;TL;AMBA','2021-07-04 18:35:08.154170','5','0', 	NULL, 4, NULL, 'TL', 'AMBA', NULL, NULL, NULL, NULL, NULL