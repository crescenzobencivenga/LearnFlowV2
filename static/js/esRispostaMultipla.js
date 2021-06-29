var data 
var es

function carica(jsondata,ex){
    data = jsondata
    es = ex
    var i = 1
    $.each(data[es].risposte, function(key,value){
        var el = document.createElement("h5")
        el.className = "my-auto"
        var id_elemento = "option"
        id_elemento = id_elemento.concat(i)
        i = i+1
        var t = document.createTextNode(value)
        var element = document.getElementById(id_elemento);
        el.appendChild(t)
        element.append(el);
    });
}


function controlla(){
        var corr = data[es].corretta
        console.log(corr)
        var fl = false
        for(var i = 0 ;i<4;i++){
            var id_elem = "radio"
            var a = i+1
            id_elem = id_elem.concat(a)
            console.log(document.getElementById(id_elem).checked)
            if(document.getElementById(id_elem).checked==true){
                if(a==corr)
                fl = true
                break
            }
        }
        if(fl){
            alert("brav")
        }else{
            alert("strunz")
        }
}


