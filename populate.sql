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

            