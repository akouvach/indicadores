import db

db.getVariables()


""" function cargarVariables(){
    //esta función va a calcular los valores y los cargará en
    //el objeto valores
    definiciones.variables.forEach(myVar => {
        //Intento procesar cada una de las variables
        console.log("------------------------------------------------------------------------");
        console.log(myVar.formula);
        parsearFormulas(myVar.formula); // le agrega los resultados intermedio
        let rdo = calcularRdo(myVar.formula); // calcula el resultado final de la variable
        myVar.rdo = rdo;
        console.log(rdo);
        agregarResultado(myVar); // registrar lo resultados del cálculo        
    });

}

function agregarResultado(variables){
    if(!valores.variables){
        valores.variables=[];
    }
    //valores.variables=variables;
    let aux={};
    aux.variable = variables.var;
    aux.rdo = variables.rdo;
    aux.fecha = formatoFecha(new Date(),"dd/mm/yyyy");
    

    valores.variables.push(aux);
    console.log(valores);
}

function hayOperaciones(valores){
    // me fijo si hay operaciones en el conjunto de valores.
    let existe=false;
    valores.forEach(v=>{
        if(typeof(v.operacion) == "string" && v.operacion[2]=="_"){
            //es una función propia. Hay que seguir calclando cosas
            existe = true;
        }
    });
    return existe;
    
}

function parsearFormulas(formula){
    console.log("analizando:",formula);

    if(formula.valores && hayOperaciones(formula.valores)){
        //debo seguir analizando para intentar completar los resultados
        console.log("valores",formula.valores);
        formula.valores.forEach(f=>{
            parsearFormulas(f);
        });  
    } 

    //ya no hay nada, actualizo el resultado parcial
    console.log("----------debería calcular algo--------");
    console.log("formula", formula);
    let rdo = ejecutar(formula);
    formula.rdo=rdo;
}

function calcularRdo(formula){
    console.log("formula:",formula);
    return formula.rdo;
}

function ejecutar(formula){
    let prefijo = formula.operacion.slice(0,3);
    let stmt = {};
    console.log("prefijo:",prefijo);
    switch(prefijo){
        case "op_":
            stmt.funcion = formula.operacion.slice(3);
            stmt.parametros = formula.valores;
            console.log("voy a ejecutar:", stmt);
            return ejecutar_op(stmt);
            break;
        case "ta_":
            stmt.funcion = formula.operacion.slice(3);
            stmt.parametros = formula.valores;
            console.log("voy a ejecutar:", stmt);
            return ejecutar_ta(stmt);
            break;
        case "co_":
            console.log("constante:", formula.valores[0]);
            return formula.valores[0];
            break;
        default:
            console.error("no se encontró el prefijo");
            return -1;
    }

}


function formatoFecha(fecha, formato) {
    const map = {
        dd: fecha.getDate(),
        mm: fecha.getMonth() + 1,
        yy: fecha.getFullYear().toString().slice(-2),
        yyyy: fecha.getFullYear()
    }

    return formato.replace(/dd|mm|yy|yyy/gi, matched => map[matched])
} """