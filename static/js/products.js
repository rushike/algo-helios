var url=document.URL;
var stuff = url.split('/');
var id = stuff[stuff.length-1];
var id=id.substring(1);
console.log(id);
var nav = id + "Nav";
console.log(nav);

document.addEventListener("load",findActive(id,nav));

function findActive(id,nav){
    
    if(window.location.hash)
        scroll(0,0);

    if(id!=""){
        setTimeout(function(){scroll(0,0);},1);
        if(id=="portfolio"){

            document.getElementById("callsgenNav").classList.remove("active");
            document.getElementById("callsgen").classList.remove("active","in");
            
            document.getElementById(id).classList.add("in","active");
            document.getElementById(nav).classList.add("active");
        }
    }
}