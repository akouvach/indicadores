/*
Aquí se encuentran las funciones que se conectarán a los diferentes origenes
de datos.
La funcion de ejecutar debería ser la misma pero , dependiendo de la base 
de datos, tendrá una forma de implementarse diferente.
*/

let fuente = "json";

function ejecutar_ta(parametros){
    
    switch(fuente){
        case "json":
            return ejecutarJson(parametros);
            break;
        case "sql":
            return ejecutarSql();
            break;
        default:
            console.log("implementación no encontrada");
            return [];
    }

}


function ejecutarJson(parametros){
    console.log(`fn: ${parametros.funcion} - ${parametros.parametros[0]}`);
    let params = parametros.parametros[0];
    let stmt = parametros.funcion + "(params)";
    let rdo = eval(stmt);
    return rdo;
}

function asignaciones(parametros){
    console.log("Asignaciones parametros",parametros);

    let tempFiltro = bd_asignaciones.filter(item=>{
        //console.log("analizando item:", item);
        let incluir=true;
        parametros.filtros.forEach(f=>{
            stmt=f;
            stmt = stmt.replace(")",",item)")
            let rdo=eval(stmt);
            //console.log("ejecutando:",stmt, rdo);
            if(incluir && !rdo){
                //cambio el valor de incluir para no incluir
                incluir = false;
            }
        });
        return incluir;
    });
    console.log("filtrados",tempFiltro);
    
    //Sobre estos registros filtrados voy a aplicarle el agrupamiento
    let tempGroup = [];

    tempFiltro.forEach((item)=>{
        let encontrado = false;
        let aux = tempGroup.filter
        if(tempGroup.filter())
    });
    
    
    let rdoFinal = [];

    tempGroup.forEach(item=>{
        // voy a reemplazar los prefijos de r_ con el item que corresponde
        let aux = parametros.mostrar;
        aux = aux.replace("r_","item.");
        let valor = eval(aux);
        //console.log(aux,valor)
        rdoFinal.push(valor);
    });

    console.log(rdoFinal);
    return rdoFinal;

}

function b_null(campo, registro){
    //console.log(`b_null: comparando ${registro[campo]}, ${campo}`,registro);
    if(registro[campo]==null || registro[campo]==undefined){
        return true;
    }
    return false;
}

function b_hoy(){
    return new Date();
}

function b_fechaDiff(desde,hasta){
    //calcula la diferencia entre fechas en días
    //console.log("calculando diferencia entre fechas:", desde, hasta)
    let dif = hasta - desde;
    return parseInt(dif/1000/60/60/24); //devuelvo milisegundos a días.
} 

function b_date(valor){
    return new Date(valor);
}
function prueba(){
    let p= b_fechaDiff(new Date("2020-01-01"), new Date())
    console.log(p)
}