// const BASE_API="http://localhost:5000/";

const BASE_API=(window.location.host=="localhost:5000")?"http://localhost:5000/":"https://powermykpi.azurewebsites.net/";

console.log(window.location.host);
function ui_mostrarTabla(lugar,datos){
    let myDiv = document.getElementById(lugar);
    
    let mensaje = "<table class='w3-table w3-bordered'>";
    // console.log(datos.data);


    // hago un ciclo para colocar los titulos
    let titulos = datos.data[0];
    mensaje += "<thead><tr>";
    for(var j in titulos){
        mensaje += "<th>" + j + "</th>";
    }
    mensaje += "</tr></thead>";

    mensaje+="<tbody>";
           
    //ahora recorro todos los elementos del vector para poner los datos
    for (var i in datos.data) {
        mensaje += "<tr>";
        if(datos.data.hasOwnProperty(i)){
            let miObj = datos.data[i];
            for(var j in miObj){
                mensaje += "<td>" + miObj[j] + "</td>";
            }
        } 
        mensaje += "</tr>";
    }

    mensaje+="</tbody>";
    mensaje += "</table>";
    myDiv.innerHTML = mensaje;

}
function ui_mostrarDatos(lugar){

    let miTabla = document.getElementById("misSources").value;
    if(miTabla != "Seleccione una tabla para visualizar"){
        //Imprimo
        //Traigo los datos de la tabla
        let rdo = obtener("sources/"+miTabla,lugar,ui_mostrarTabla)
    } else {
        document.getElementById(lugar).innerHTML="..."
    }



}

function ui_mostrarSources(lugar,data){
    let myDiv= document.getElementById(lugar);
    // console.log(data);
    let rdo=data.data.reduce((acum,valor)=>{
        return acum+"<option>"+valor.tabla+"</option>";
    },"<select id='misSources' onchange='ui_mostrarDatos(" + String.fromCharCode(34) + "resultados" + String.fromCharCode(34) + ");'><option selected>Seleccione una tabla para visualizar</option>")+"</select>";
    myDiv.innerHTML=rdo;
}

function obtener(myUrl, lugar, funcion){
    let rdo = fetch(BASE_API+myUrl)
    .then(response=>response.json())
    .then(data=>funcion(lugar,data))
}

function mostrarSources(myDiv){
    document.getElementById(myDiv).innerHTML="Cargando...";
    //Obtengo los Nombres de las tablas
    let mySources = obtener("sources","sources", ui_mostrarSources)

}

function inicializar(){
    mostrarSources('sources');
}