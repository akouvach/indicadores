from sqlite3.dbapi2 import Error
import db
from datetime import date
from datetime import datetime


def calcularVariables():
    try:
        print("Calculando variables....")
        records = db.getVariables()
        print("Total rows are:  ", len(records))
        #print("Printing each row", records[0])
        for row in records:
            print("\nId: ", row[0])
            print("descripcion: ", row[1])
            print("formula: ", row[2])
            stmt = row[2]
            rdo = db.dbEjecutar(stmt)
            print("resultados:", rdo)
            print("agruparpor: ", row[3])
            miFecha = datetime.today()
            if row[3]=="":
                #no tiene agrupamiento, se espera una sola fila y columna
                db.variablesValoresInsert(row[0],miFecha, "", rdo[0][0], 0)
            else:
                #hay que recorrer los resultados e insertar una fila por cada grupo
                for fila in rdo:
                    cols = len(fila)
                    valor = fila[cols-1]
                    grupo=';'.join(map(str, fila[:cols-1]))
                    db.variablesValoresInsert(row[0],miFecha,grupo,valor, 0)
                    print("Fila:",fila)

        print("Fin calculo de variables....")

    except :
        print("Error calculating variables")

def calcularIndicadores():
    try:
        print("--------------------------------------------")
        print("------Calculando indicadores ----------------")
        print("--------------------------------------------")
        records = db.getIndicadores()
        print("Total rows are:  ", len(records))
        operators = set('+-*/()')
        op_out = []    #This holds the operators that are found in the string (left to right)
        num_out = []   #this holds the non-operators that are found in the string (left to right)
        buff = []            
        variable = ""
        acumulando=False

        for row in records:
            print("Id: ", row[0])
            print("descripcion: ", row[1])
            print("formula: ", row[2])
            print("agruparpor: ", row[3])
            # para cada indicador debo obtener el valor de cada variable
            # y reemplazarlo por su valor para finalmente evaluar toda la expresión
            indicador = row[0]
            formula = row[2]
            variable = ""
            acumulando=False
            myDict = {}

            for c in formula:  #examine 1 character at a time
                #print(c)
                if c=="}":
                    #termino de acumular para detectar una variable
                    print("variable detectada:", variable)
                    myDict[variable]= db.getValorIndicador(variable)
                    
                    variable=""
                    acumulando=False
                
                if acumulando:
                    variable += c
                
                if c=="{":
                    #empieza una nueva variable
                    variable=""
                    acumulando=True
                
            print("final:", myDict)
            for v in myDict:
                #print(v, myDict[v])
                formula = formula.replace("{" + v + "}",str(myDict[v]))
            print ("formula final:", formula)
            rdoIndicador = eval(formula)
            print("indicador:",rdoIndicador)
            db.indicadoresValoresInsert(indicador,datetime.today(), rdoIndicador,0)

            #agrego el valor a los indicadores

                
        print("----------Terminó de calcular indicadores ---------------")


    except:
        print("Error calculating variables", )


#db.crearYcargarDb()
calcularVariables()
#calcularIndicadores()


#db.dbEjecutar("select count(1) as cant from variables;")

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