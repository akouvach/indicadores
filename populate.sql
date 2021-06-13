delete from asignaciones;
delete from proyectos;
delete from clientes;
delete from usuarios;
delete from motivos;

insert into usuarios (id, nombre, apellido, email) 
values 
(1, 'Matias','Salmeri','msalmeri'),
(2, 'Diego','Diego','diego'),
(3, 'Andres','Kouvach','akouvach'),
(4, 'Andres','Saenz','asaenz'),
(5, 'Rocio','rocio','rocio');

insert into motivos (id, descripcion)
VALUES
(1,'fin del proyecto'),
(2,'pedido de rotación'),
(3,'salida de la empresa');

insert into clientes (id, nombre)
values 
(1,"Cashflows"),
(2, "AT&T"),
(3, "Google");

insert into proyectos (id, descripcion, clienteId)
values 
(1,"payments",1),
(2,"gateway",1),
(3,"PCI",1),
(4,"CRM",2),
(5,"IA",3);

insert into asignaciones (empresa, du, disciplina, usuarioId, proyectoId, FechaAlta, fechaFin, motivoId)
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


