delete from user_asignaciones;
delete from user_proyectos;
delete from user_clientes;
delete from user_motivos;

delete from indicadoresValores;
delete from variablesValores;

delete from ponderaciones;
delete from indicadores;
delete from variables;

delete from usuarios;


insert into usuarios (id, nombre, apellido, email) 
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
("Endava","BAD","AP",1,1,"2005-01-06","2010-10-30",2),
("Endava","BAD","AP",1,1,"2010-11-01",null,null),
("Endava","BAD","PDM",1,1,"2002-01-01","2003-01-31",2),
("Endava","BAD","PDM",1,1,"2003-02-01","2008-10-30",3);

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
(1,"Tiempo promedio en proyectos","TiempoPromEnProy/TiempoPromEstables",""),
(2,"Nivel de Fit en las asignaciones","TiempoHastaPedirRotacion","empresa, du, disciplina");


insert into variables (id, descripcion, formula, agrupadopor)
values 
("TiempoPromEnProy","Corresponde al tiempo promedio de cada uno de los miembros", "Select count(1) as cant from proyectos",""),
("TiempoPromEstables","Tiempo promedio en proyectos de los miembros que están en la empresa hace mas de 5 años.","select count(1) as cant from clientes",""),
("TiempoHastaPedirRotacion","Tiempo esperado hasta pedir rotacion","select count(1) as cant from clientes","");


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
(2,"2015-01-01",50000000000,1);





            