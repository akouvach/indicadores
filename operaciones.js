/*
Aquí se encuentran un conjunto de funciones que operan con un conjunto
de parámetros.  Son internas y no se conectan directamente con la base de datos
*/

function ejecutar_op(parametros){

    console.log("ejecutar_op", parametros.parametros[0].rdo);
    let params = parametros.parametros[0].rdo;
    console.log("parametros:", params)
    let stmt = parametros.funcion + "(params)";
    let rdo = eval(stmt);
    return rdo;
}

function promedio(parametros){
    console.log("fn promedio - parametros", parametros);
    let prom=parametros.reduce((acum, value)=>acum+value,0.0)/parametros.length;
    console.log("valor:",prom);
    return prom;
}