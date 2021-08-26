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

console.log(window.location.host);

const RESULTADOS = "resultados";
let cantxpagina=50;


function ui_mostrarDatosidIndicador(id,lugar){
    console.log("mostrarDatosIdIndicador...",id, lugar);

    let miIndicador = document.getElementById(id).value;

    console.log(miIndicador);

    // if(miTabla != "Seleccione para visualizar"){
    //     //Imprimo
    //     //Traigo los datos de la tabla
    //     let rdo = obtener("sources/"+miTabla+"/",id, "resultados",ui_mostrarTabla)
    // } else {
    //     document.getElementById(lugar).innerHTML="..."
    // }
}

function ui_mostrarDatosidVariable(id,lugar){
    console.log("mostrarDatosIdVariable...",id, lugar);

    let miIndicador = document.getElementById(id).value;

    console.log(miIndicador);

    // if(miTabla != "Seleccione para visualizar"){
    //     //Imprimo
    //     //Traigo los datos de la tabla
    //     let rdo = obtener("sources/"+miTabla+"/",id, "resultados",ui_mostrarTabla)
    // } else {
    //     document.getElementById(lugar).innerHTML="..."
    // }
}



function ui_mostrarSelectIndicadores(id, lugar,data){
    console.log("mostrarndo select...",lugar,id, data);
    let myDiv= document.getElementById(lugar);
    // console.log(data);
    let rdo=data.data.reduce((acum,valor)=>{
        return acum+"<option value='"+valor.id+"'>"+valor.descripcion+"</option>";
    },"<select id='"+id+"' onchange='ui_mostrarDatos" + id + "(" + String.fromCharCode(34) + id + String.fromCharCode(34) + "," + String.fromCharCode(34) + lugar + String.fromCharCode(34) + ");'><option selected>Seleccione para visualizar</option>")+"</select>";
    myDiv.innerHTML=rdo;
}

function ui_mostrarSelectVariables(id, lugar,data){
    console.log("mostrarndo select...",lugar,id, data);
    let myDiv= document.getElementById(lugar);
    // console.log(data);
    let rdo=data.data.reduce((acum,valor)=>{
        return acum+"<option value='"+valor.id+"'>"+valor.descripcion+"</option>";
    },"<select id='"+id+"' onchange='ui_mostrarDatos" + id + "(" + String.fromCharCode(34) + id + String.fromCharCode(34) + "," + String.fromCharCode(34) + lugar + String.fromCharCode(34) + ");'><option selected>Seleccione para visualizar</option>")+"</select>";
    myDiv.innerHTML=rdo;
}

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

function ui_mostrarTabla(id, lugar, datos, pagina=1){
    // console.log("entro",Date.UTC())
    let datosTabla = JSON.parse(sessionStorage.getItem("datosTabla"));

    if(id==""){
        console.log("session..",datosTabla);
        id = datosTabla.id;
        lugar = datosTabla.lugar;
        datos = datosTabla.datos;
    }
    
    let myDiv = document.getElementById(lugar);
    // console.log("mostrando tabla",datos, datos.data.length)
    
    let mensaje = "<table class='w3-table w3-bordered'>";

    // hago un ciclo para colocar los titulos
    let titulos = datos.data[0];
    mensaje += "<thead><tr><th>Nro</th>";
    for(var j in titulos){
        mensaje += "<th>" + j + "</th>";
    }
    mensaje += "</tr></thead>";

    mensaje+="<tbody>";
           
    //ahora recorro todos los elementos del vector para poner los datos
    for(let r=(pagina-1);r<((pagina-1)+cantxpagina);r++){
    // for (var i in datos.data) {
        mensaje += "<tr><td>"+r+"</td>";
        if(datos.data.hasOwnProperty(r)){
            let miObj = datos.data[r];
            for(var j in miObj){
                mensaje += "<td>" + miObj[j] + "</td>";
            }
        } 
        mensaje += "</tr>";
    }

    mensaje+="</tbody>";
    mensaje+="<tfoot><tr><td colspan='"+Object.keys(titulos).length+"'>Filas procesadas:" + datos.data.length + " | " ;

    if(datos.data.length > cantxpagina){
        //debo realizar paginación
        if(pagina>1){
            //agrego un botón para bajar la página
            mensaje+="<button><</button>";
        }
        if(pagina*cantxpagina<datos.data.length){
            //le agrego uno para la siguiente página
            mensaje+="<button onclick='ui_mostrarTabla("+ 
            String.fromCharCode(34)+String.fromCharCode(34)+","+
            String.fromCharCode(34)+String.fromCharCode(34)+","+
            String.fromCharCode(34)+String.fromCharCode(34)+","+
            ++pagina + ")';>></button>";
        }
    }

    mensaje+="</td></tr></tfoot>";
    
    mensaje += "</table>";
    myDiv.innerHTML = mensaje;
    

}


async function ui_mostrarDatosSources(valor){
    console.log("cargando datos de", valor);
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
        ui_mostrarTabla("",RESULTADOS,data);

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
    },"<select id='"+id+"' onchange='ui_mostrarDatosSources(this.value);'><option selected value='Seleccione'>----Seleccione----</option>")+"</select>";
// },"<select id='"+id+"' onchange='ui_mostrarDatos" + id + "(this)" + String.fromCharCode(34) + id + String.fromCharCode(34) + "," + String.fromCharCode(34) + lugar + String.fromCharCode(34) + ");'><option selected>Seleccione para visualizar</option>")+"</select>";
    myDiv.innerHTML=rdo;
}

function mostrarIndicadores(id,myDiv){
    document.getElementById(myDiv).innerHTML="Cargando...";
    //Obtengo los Indicadores
    obtener("sources/indicadores/",id, myDiv, ui_mostrarSelectIndicadores)

}

function mostrarVariables(id,myDiv){
    document.getElementById(myDiv).innerHTML="Cargando...";
    //Obtengo los Indicadores
    obtener("sources/variables/",id, myDiv, ui_mostrarSelectVariables)

}

function inicializar(){
    mostrarSources('idSource','sources');
    let f = new Date();
    let mes = ((f.getMonth()+1)<10?"0":"")+(f.getMonth()+1);
    let anio= f.getFullYear();
    let dia = (f.getDate()<10?"0":"")+f.getDate();
    let miFecha = anio+"-"+ mes+"-"+dia;
    console.log("efe:",f, miFecha);
    document.getElementById("fecha").value = miFecha;

    // mostrarIndicadores('idIndicador','indicadores');
    // mostrarVariables('idVariable','variables');
    
}

async function calcularIndicadores(){
    let fecha = document.getElementById("fecha").value;
    console.log(fecha);
    let data = await enviar("calcularvalores/" + fecha + "/",{});
    alert(data);

}