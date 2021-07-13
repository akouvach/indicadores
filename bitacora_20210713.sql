--TO-DO:
--DIEGO:
--view x indicador para llegar --> a esta vista

--nueva tabla (corregir data)
select * from indicadoresValores_pivot where indicadorId = 1 order by fecha desc limit 2 --ok! 2021-07-04 18:35:07.457021

--ultima fecha de la nueva tabla (funciona sin convert)
select max(fecha) from indicadoresValores_pivot where indicadorId = 1

--ejemplo create view
create view saraza as
select * from indicadoresValores_pivot

--ejemplos convert a datetime y timestamp (gracias Andres!)
select datetime(fecha), strftime(fecha) from saraza 
