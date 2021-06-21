from sqlite3.dbapi2 import Error
import db
from datetime import datetime
import varios


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

def calcularIndicador(indicador,formula,agruparpor):
    try:
        myDict = {}

        #obtengo la lista de variables que participan de la
        #formula de un indicador para después, ir a buscar
        #sus valores.
        vars = varios.getVariableList(formula)
        
        if(agruparpor==""):
            #si no se agrupa, el valor de la variable
            #debería traer un solo valor

            #recorro la lista y busco los valores
            for v in vars: 
                #busco el valor y devuelvo la primer fila y columna 
                myDict[v]= db.getValorIndicador(v)[0][0]
        
            # con el conjunto de valores recuperados
            # proceso la formula y almaceno su valor
            for v in myDict:
                formula = formula.replace("{" + v + "}",str(myDict[v]))
            rdoIndicador = eval(formula)
            rdoPonderado = db.getPonderacionIndicador(indicador,datetime.today(),rdoIndicador)[0][0]
            db.indicadoresValoresInsert(indicador,"",datetime.today(), rdoPonderado,0)

        else:
            #corresponde a un indicador que debería tener
            #asociadas variables también agrupadas.
            for v in vars:  
                print("------analizando variable: ",v,"-------------")
                #voy a buscar todos los valores para cada 
                # variable del presente indicador que 
                # se supone estar agrupado
                
                rdo = db.getValorIndicador(v)
                for fila in rdo:
                    # fila[0] se supone que tiene el grupo
                    # y fila[1] el valor para la presente variable 
                    myDict[v+fila[0]]=fila[1]

            # ya está el diccionario actualizado
            # voy a buscar el total de grupos para los cuales
            # calcular el valor del indicador
            # en caso de no existir dicho grupo se reemplazará
            # con 1            

            grupos = db.getGruposIndicador(indicador)
            for g in grupos:
                formuAux=formula
                for v in vars:
                    auxGrupo = v+g[0]
                    if(auxGrupo not in myDict):
                        #lo agrego al diccionario con valor 1
                        myDict[auxGrupo] = 1
                    formuAux = formuAux.replace("{" + v + "}",str(myDict[auxGrupo]))
                #para cada grupo calculo la fórmula
                rdoIndicador = eval(formuAux)
                rdoPonderado = db.getPonderacionIndicador(indicador,datetime.today(),rdoIndicador)[0][0]
                db.indicadoresValoresInsert(indicador,g[0],datetime.today(), rdoPonderado,0)


    except Exception as error:
        print("Error en el calculo de indicador..",error)

def calcularIndicadores():
    try:
        print("------Calculando indicadores ----------------")
        records = db.getIndicadores()
        print("Total rows are:  ", len(records))
    
        for row in records:
            print("Id: ", row[0])
            print("descripcion: ", row[1])
            print("formula: ", row[2])
            print("agruparpor: ", row[3])
            # para cada indicador debo obtener el valor de cada variable
            # y reemplazarlo por su valor para finalmente evaluar toda la expresión
            indicador = row[0]
            formula = row[2]
            agruparpor = row[3]

            calcularIndicador(indicador,formula,agruparpor)

        print("----------Terminó de calcular indicadores ---------------")

    except:
        print("Error calculating variables", )

#db.crearYcargarDb()
calcularVariables()
calcularIndicadores()


#db.dbEjecutar("select count(1) as cant from variables;")
