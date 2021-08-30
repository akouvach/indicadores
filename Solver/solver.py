import random
from datetime import date, datetime, timedelta

import Solver.db as db
from Solver.varios import getVariableList


def calcularVariables(miFecha = date.today()):
    try:
        records = db.getVariablesData()
        for row in records:
            variableId = row[0]
            variableDescripcion = row[1]
            formula = row[2]
            agrupadoPor = row[3]

            print("\nId: {} Descripción: {} Fórmula: {} Agrupación: {}\n".format(
                variableId, variableDescripcion, formula, agrupadoPor
            ))

            rdo = db.dbEjecutar(formula)
            
            # Se elimina el registro por si existía
            db.deleteVariablesValoresData(variableId, miFecha, "")

            if not agrupadoPor:
                # No tiene agrupamiento, se espera una sola fila y columna
                db.insertVariablesValoresData(variableId, miFecha, "", rdo[0][0], 0)
            else:
                # Hay que recorrer los resultados e insertar una fila por cada grupo
                for fila in rdo:
                    cols = len(fila)
                    valor = fila[cols-1]
                    grupo=';'.join(map(str, fila[:cols-1]))
                    db.insertVariablesValoresData(row[0],miFecha,grupo,valor, 0)
        print("--Cálculo de variables finalizado")

    except Exception as error:
        print("--Error while calcularVariables", error)


def calcularIndicadores(miFecha=datetime.today()):
    try:
        records = db.getIndicadoresAKData()  
        for row in records:
            indicador = row[0]
            formula = row[2]
            agruparPor = row[3]

            print("\nId: {} Descripción: {} Fórmula: {} Agrupación: {}\n".format(
                indicador, row[1], formula, agruparPor
            ))

            # Se utiliza el valor de cada variable para evaluar la expresión de cada indicador
            calcularIndicador(indicador, formula, agruparPor, miFecha, 0)

    except Exception as error:

        raise("Error calculating variables"+ error)


def calcularIndicador(indicador, formula, agruparPor, miFecha, aleatorio=0):
    try:
        myDict = {}

        # Se obtiene lista de variables que usa la fórmula de un indicador
        vars = getVariableList(formula)

        # Variable trae un sólo valor
        if not agruparPor:
            for v in vars:
                myDict[v]= db.getValorIndicador(v)[0][0]

            # Se procesa la fórmula con sus valores y se almacena su valor
            for v in myDict:
                formula = formula.replace("{" + v + "}", str(myDict[v]))
            
            rdoIndicador = eval(formula)
            if aleatorio:
                rdoIndicador = rdoIndicador + random.random()*100

            rdoPonderado = db.getPonderacionIndicador(indicador, miFecha, rdoIndicador)[0][0]
            
            db.deleteIndicadoresValoresData(indicador, "", miFecha)
            db.insertIndicadoresValoresData(indicador, "", miFecha, rdoIndicador, 0, rdoPonderado)

        # Indicador con variables asociadas agrupadas
        else:
            for v in vars:  
                print("--Analizando variable: ", v)
                rdo = db.getValorIndicador(v)

                # fila[0] tiene el grupo, fila[1] tiene el valor para la variable
                for fila in rdo:
                    myDict[v+fila[0]] = fila[1]

            # Diccionario actualizado, búsqueda de grupos para calcularles el valor del indicador
            grupos = db.getGruposIndicador(indicador)
            for g in grupos:
                formuAux = formula
                for v in vars:
                    auxGrupo = v + g[0]

                    # Si el grupo no existe, se crea con valor de 1
                    if not myDict.get(auxGrupo):
                        myDict[auxGrupo] = 1

                    formuAux = formuAux.replace("{" + v + "}", str(myDict[auxGrupo]))
                rdoIndicador = eval(formuAux)

                if aleatorio:
                    rdoIndicador = rdoIndicador + random.random()*100

                rdoPonderado = db.getPonderacionIndicador(indicador, miFecha, rdoIndicador)[0][0]
            
                db.deleteIndicadoresValoresData(indicador, g[0], miFecha)
                db.insertIndicadoresValoresData(indicador, g[0], miFecha, rdoIndicador, 0, rdoPonderado)

    except Exception as error:
        print("--Error while calcularIndicador", error)


def calcularValores(miFecha=date.today()):
    try:
        calcularVariables()
        calcularIndicadores(miFecha)
        # Tendría que llamar para hacer el pivot_table
        return "True"

    except Exception as error:
        raise("Error calculating variables: "+error )


#db.createDb()
def cargarDatos(fechahasta):
    try:
        #calcular de enero hasta hoy. dia a día
        inicio = date(2021,1,1)
        fin    = fechahasta

        lista_fechas = [inicio + timedelta(days=d) for d in range((fin - inicio).days + 1)] 

        deleteResultadosData()
        calcularVariables(inicio)
        
        for fecha in lista_fechas:
            try:
                print("calculando indicadores para:",fecha)
                calcularIndicadores(fecha)
            except Exception as error:
                raise("Error calculating variables" + error)

    except Exception as error:
        raise("Error calculating variables" + error)



def deleteResultadosData():
    db.deleteResultadosData()


# db.dbEjecutar("select count(1) as cant from variables;")
