let protocol = "http";
if(window.location.host=="powermykpi.azurewebsites.net"){
    protocol+="s";
}
protocol+="://";

const BASE_API = protocol + window.location.host+"/";
// switch (myHost){
//     case "localhost:5000":
//         const BASE_API=myHost
// }
// const BASE_API=(window.location.host=="localhost:5000")?"http://localhost:5000/":"https://powermykpi.azurewebsites.net/";

console.log(BASE_API);

const RESULTADOS = "resultados";
let cantxpagina=100;



function obtener(myUrl){
    console.log("obteniendo..",BASE_API+myUrl);
    let rdo = fetch(BASE_API+myUrl)
    .then(response=>response.json())
    .then(data=>data);
    return rdo

}

function enviar(myUrl,data){
    console.log("enviando..",BASE_API+myUrl);
    let rdo = fetch(BASE_API+myUrl,{method:'POST', body:JSON.stringify(data)})
    .then(response=>response.json())
    .then(data=>data);
    return rdo
}

async function verEstimaciones(indicador,grupo){
    //Actualizo los valores
    document.getElementById("estimationsDetail").innerHTML="Loading...";
    let data = await obtener("predicciones/"+indicador+"/"+grupo+"/")

    if (data.data.length >0){
        ui_mostrarTabla("estimaciones","estimationsDetail",data);
    } else {
        document.getElementById("estimationsDetail").innerHTML="No data found..."
    }


    document.getElementById("estimationHeader").innerHTML = "Indicator:" + indicador + " Group:" + grupo;
    
    
    document.getElementById('id01').style.display='block';

}


function ui_mostrarTablaIndicadores(id, lugar, datos, pagina=1){
    // console.log("entro",Date.UTC())
    
    let myDiv = document.getElementById(lugar);
    // console.log("mostrando tabla",datos, datos.data.length)
    
    let mensaje = "<table class='w3-table-all w3-hoverable w3-border'>";

    // hago un ciclo para colocar los titulos
    let titulos = datos.data[0];
    mensaje += "<thead><tr class='w3-orange'><th>Nro</th>";
    for(var j in titulos){
        mensaje += "<th>" + j + "</th>";
    }
    mensaje += "<th>Est.</th>";
    mensaje += "</tr></thead>";

    mensaje+="<tbody>";
           
    //ahora recorro todos los elementos del vector para poner los datos
    for(let r=0;r<datos.data.length;r++){
    // for (var i in datos.data) {
        if(datos.data[r]){
            mensaje += "<tr><td>"+r+"</td>";
            miIndicador=0;
            miGrupo = "--";
            if(datos.data.hasOwnProperty(r)){
                let miObj = datos.data[r];
                for(var j in miObj){
                    if(j=="indicadorId"){
                        miIndicador=miObj[j]
                    }
                    if(j=="grupo"){
                        miGrupo=miObj[j]
                    }
                    
                    mensaje += "<td>" + miObj[j] + "</td>";
                }
            } 
            mensaje += "<td><button onclick=" + 
            String.fromCharCode(34) +
            "verEstimaciones(" + miIndicador + ", '" + miGrupo + "');" + 
            String.fromCharCode(34) +
            ">...</button></td>";
            mensaje += "</tr>";
        } else {
            break;
        }
    }

    mensaje+="</tbody>";
    mensaje+="<tfoot><tr><td colspan='"+Object.keys(titulos).length+"'>Rows:" + datos.data.length + " | " ;

    mensaje+="</td></tr></tfoot>";
    
    mensaje += "</table>";
    myDiv.innerHTML = mensaje;
    

}

function ui_mostrarTabla(id, lugar, datos, pagina=1){
    // console.log("entro",Date.UTC())



    let myDiv = document.getElementById(lugar);
    // console.log("mostrando tabla",datos, datos.data.length)
    
    let mensaje = "<table class='w3-table-all w3-hoverable w3-border'>";

    // hago un ciclo para colocar los titulos
    let titulos = datos.data[0];
    mensaje += "<thead><tr class='w3-orange'><th>Nro</th>";
    for(var j in titulos){
        mensaje += "<th>" + j + "</th>";
    }
    mensaje += "</tr></thead>";

    mensaje+="<tbody>";
           
    //ahora recorro todos los elementos del vector para poner los datos
    for(let r=0;r<datos.data.length;r++){
    // for (var i in datos.data) {
        if(datos.data[r]){
            mensaje += "<tr><td>"+r+"</td>";
            if(datos.data.hasOwnProperty(r)){
                let miObj = datos.data[r];
                for(var j in miObj){
                    mensaje += "<td>" + miObj[j] + "</td>";
                }
            } 
            mensaje += "</tr>";
        } else {
            break;
        }
    }

    mensaje+="</tbody>";
    mensaje+="<tfoot><tr><td colspan='"+Object.keys(titulos).length+"'>Rows:" + datos.data.length + " | " ;

    mensaje+="</td></tr></tfoot>";
    
    mensaje += "</table>";
    myDiv.innerHTML = mensaje;
    

}



function mostrarIndicadorDetalles(indicador, variables, lugar, ultimosValores){
    let myDiv = document.getElementById(lugar);
    let tabla = `
    <div class='w3-container'>
        <div class="w3-card-4">

            <header class="w3-container w3-blue">
            <h1>
            <span class="w3-badge w3-red">${ indicador[0].id }</span>
            ${ indicador[0].descripcion }
            </h1>
            </header>
            
            <div class="w3-container">
            <p><b>Formula:</b> ${ indicador[0].formula }</p>            
            <p><b>Group by:</b> ${ indicador[0].agrupadopor }</p>
            </div>
            
            <footer class="w3-container w3-blue">
            <h5>Variables</h5>
            </footer>

            <div class="w3-container">
            <p>${ variables.reduce( (acum, data) => acum + 
                "<p><b>" + data.id + "</b></p>" +
                "<p>" + data.formula + "</p>" +
                "<p>" + data.agrupadopor + "</p>","") }
            </p>            
            </div>

            <footer class="w3-container w3-blue">
            <h5>Last values</h5>
            </footer>

            <div class="w3-container" id="ultimosValoresIndicador">
            </div>
            
        </div>

    </div>`;
    // console.log(ultimosValores)


    myDiv.innerHTML = tabla;
    ui_mostrarTabla(indicador, 'ultimosValoresIndicador', ultimosValores)
            
}

async function ui_mostrarDatosSources(valor){
    if(valor != "Seleccione"){
        //Traigo los datos de la tabla
        document.getElementById(RESULTADOS).innerHTML="cargando...";
        let data = await obtener("sources/"+valor+"/")

        //Almaceno los datos para paginar después
        let datosTabla = {};
        datosTabla.id = "";
        datosTabla.lugar = RESULTADOS;
        datosTabla.datos = data;
        sessionStorage.setItem("datosTabla",JSON.stringify(datosTabla));
        if(valor == "current_indicator_value"){
            ui_mostrarTablaIndicadores("",RESULTADOS,data);
        } else{
            ui_mostrarTabla("",RESULTADOS,data);
        }
    } else {
        document.getElementById(RESULTADOS).innerHTML="..."
    }
}

async function ui_mostrarDatosIndicador(valor){
    // console.log("cargando datos de", valor);
    if(valor != "Seleccione"){
        //Traigo los datos de la tabla
        document.getElementById(RESULTADOS).innerHTML="cargando...";
        // window.open(BASE_API+"indicador/" + valor);
        
        let indicador = await obtener("indicadores/"+valor+"/")
        let variables = await obtener("indicadores/"+valor+"/variables/")
        let ultimos = await obtener("resultados/"+valor+"/ultimos/")


        mostrarIndicadorDetalles(indicador.data, variables.data, RESULTADOS, ultimos);

    } else {
        document.getElementById(RESULTADOS).innerHTML="..."
    }
}

async function mostrarSources(id,lugar){
    let myDiv= document.getElementById(lugar);
    myDiv.innerHTML = "Cargando...";
    //Obtengo los Nombres de las tablas
    let tablas = await obtener("sources")
    // console.log(data);
    let rdo = tablas.data.reduce((acum,valor)=>{
        return acum+"<option value='"+valor.tabla+"'>"+valor.tabla+"</option>";
    },"<select  class=" + String.fromCharCode(34) + 
    "w3-input" + String.fromCharCode(34) + " id='"+id+
    "' onchange='ui_mostrarDatosSources(this.value);'><option selected value='Seleccione'>----Seleccione----</option>")+"</select>";
    myDiv.innerHTML=rdo;
}

async function mostrarIndicadores(id,lugar){
    document.getElementById(lugar).innerHTML="Cargando...";
    let myDiv= document.getElementById(lugar);
    myDiv.innerHTML = "Cargando...";
    //Obtengo los Nombres de las tablas
    let indicadores = await obtener("sources/indicadores/")
    // console.log(indicadores);
    let rdo = indicadores.data.reduce((acum,valor)=>{
        return acum+"<option value='"+valor.id+"'>"+valor.descripcion+"</option>";
    },"<select  class=" + String.fromCharCode(34) + 
    "w3-input" + String.fromCharCode(34) + 
    " id='"+id+"' onchange='ui_mostrarDatosIndicador(this.value);'><option selected value='Seleccione'>----Seleccione----</option>")+"</select>";
    myDiv.innerHTML=rdo;

}


async function calcularIndicadores(){
    let fecha = document.getElementById("fecha").value;
    let data = await enviar("calcularvalores/" + fecha + "/",{});
    alert(data);

}

async function calcularAttrition(){
    let data = await enviar("attrition", {});
    alert(data);

}

async function calcularFuturo(){
    let data = await enviar("kpi-prediction",{});
    alert(data);

}

function inicializar(){
    mostrarSources('idSource','sources');
    mostrarIndicadores('idIndicador','indicadores');


    let f = new Date();
    let mes = ((f.getMonth()+1)<10?"0":"")+(f.getMonth()+1);
    let anio= f.getFullYear();
    let dia = (f.getDate()<10?"0":"")+f.getDate();
    let miFecha = anio+"-"+ mes+"-"+dia;
    // console.log("efe:",f, miFecha);
    document.getElementById("fecha").value = miFecha;

    // mostrarIndicadores('idIndicador','indicadores');
    // mostrarVariables('idVariable','variables');
    
}