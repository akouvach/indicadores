from datetime import date, datetime, timedelta
import random

from Solver.varios import getVariableList
import Solver.db as db


def calcularVariables(miFecha = datetime.today()):
    try:
        records = db.getVariablesData()
        for row in records:
            variableId = row[0]
            variableDescripcion = row[1]
            formula = row[2]
            agrupadopor = row[3]
            print("\nId:{} desc: {} formula: {} agrup:{} "
            .format(variableId, variableDescripcion,formula,agrupadopor))
            
            stmt = formula
            rdo = db.dbEjecutar(stmt)
            
            # //elimino el registro por si existía
            db.deleteVariablesValoresData(variableId,miFecha, "")
            if agrupadopor=="":
                #no tiene agrupamiento, se espera una sola fila y columna
                db.insertVariablesValoresData(variableId,miFecha, "", rdo[0][0], 0)
            else:
                #hay que recorrer los resultados e insertar una fila por cada grupo
                for fila in rdo:
                    cols = len(fila)
                    valor = fila[cols-1]
                    grupo=';'.join(map(str, fila[:cols-1]))
                    db.insertVariablesValoresData(row[0],miFecha,grupo,valor, 0)

        print("Fin calculo de variables....")

    except Exception as error:
        print("Error calculating variables", error)

def calcularIndicador(indicador,formula,agruparpor, miFecha, aleatorio=0):
    try:
        # en este diccionario voy a colocar los resultados parciales de las
        # variables intervinientes para este indicador.
        myDict = {}

        #obtengo la lista de variables que participan de la
        #formula de un indicador para después, ir a buscar
        #sus valores.
        vars = getVariableList(formula)
        
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
            if(aleatorio!=0):
                #le pongo algún valor aleatorio
                rdoIndicador = rdoIndicador + random.random()*100

            rdoPonderado = db.getPonderacionIndicador(indicador,miFecha,rdoIndicador)[0][0]
            
            db.deleteIndicadoresValoresData(indicador,"",miFecha)
            db.insertIndicadoresValoresData(indicador,"",miFecha, rdoIndicador,0, rdoPonderado)

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

                if(aleatorio!=0):
                    #le pongo algún valor aleatorio
                    rdoIndicador = rdoIndicador + random.random()*100

                rdoPonderado = db.getPonderacionIndicador(indicador,miFecha,rdoIndicador)[0][0]
            
                db.deleteIndicadoresValoresData(indicador,g[0],miFecha)
                db.insertIndicadoresValoresData(indicador,g[0],miFecha, rdoIndicador,0, rdoPonderado)


    except Exception as error:
        print("Error en el calculo de indicador..",error)

def calcularIndicadores(miFecha = datetime.today()):
    try:
        print("------Calculando indicadores ----------------")
        records = db.getIndicadoresData()
        print("Total rows are:  ", len(records))
    
        for row in records:
            indicador = row[0]
            formula = row[2]
            agruparpor = row[3]

            # para cada indicador debo obtener el valor de cada variable
            # y reemplazarlo por su valor para finalmente evaluar toda la expresión

            print("---Id:{} Descripcion:{} \n---Formula: {}, agrupadopor: {}"
            .format(indicador,row[1],formula,agruparpor))
            calcularIndicador(indicador,formula,agruparpor,miFecha,1)

        print("----------Terminó de calcular indicadores ---------------")

    except Exception as error:
        print("Error calculating variables",error )

def deleteResultadosData():
    db.deleteResultadosData()

#db.createDb()
def cargarDatos():
    #calcular de enero hasta hoy. dia a día
    inicio = date(2021,1,1)
    fin    = date(2021,8,26)

    lista_fechas = [inicio + timedelta(days=d) for d in range((fin - inicio).days + 1)] 

    deleteResultadosData()
    calcularVariables()
    
    for fecha in lista_fechas:
        calcularIndicadores(fecha)

    # calcularValores()

def calcularValores(miFecha = date.today()):
    try:
        calcularVariables()
        calcularIndicadores(miFecha)
        # Tendría que llamar para hacer el pivot_table
        return "OK"
    except Exception as error:
        print("Error calculando valores",error )
        return "False"

    


#db.dbEjecutar("select count(1) as cant from variables;")
