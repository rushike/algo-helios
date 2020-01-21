var url=document.URL;
var stuff = url.split('/');
var id = stuff[stuff.length-1];
id = id.substring(1);
console.log(id);
var nav="nav"+id;
console.log(nav);

document.addEventListener("load",findActive(id,nav));


function findActive(x,nav)
{
    if(window.location.hash)
        scroll(0,0);
    
    if(x!="")
    {
    setTimeout(function(){scroll(0,0);},1);

    document.getElementById("Section1").classList.remove("active");
    document.getElementById("navSection1").classList.remove("active");

    document.getElementById(x).classList.add("active","in");
    document.getElementById(nav).classList.add("active");
    }
}
