--TO-DO 20210714: 
en la dbo.vw_INDICADORESVALORES
group01_name group01_value, group02_name group02_value  ...


select top 10 *, (select s from dbo.SplitString(grupo,';') where ItemIndex = 0)
from dbo.indicadoresValores

select * from dbo.vw_INDICADORESVALORES
select * from dbo.vw_INDICADORES 
