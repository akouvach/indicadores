Select disciplina, Grade, ubicacion,cast(sum(iif(Extension_de_oferta<>'Aceptada',1,0)) as real) / cast (count(1) as real) as TasaRechazos from ST_New_Hires_PowerMyKPI group by  disciplina, Grade,ubicacion

