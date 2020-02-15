const header = ["", "MERCURY", "SERVICES \n & \nCONSULTANCY"  ]
const hlen = header.length
var head = 1
var active = "head-individual";
$(document).ready(function(){
    l = (head + hlen - 1) % hlen
    c = head; 
    r = (head + 1) % hlen
    $("#ah-left").html(header[l]);
    $("#ah-center").html(header[c]);
    $("#ah-right").html(header[r]);

    $("#ah-left").click(function(){
        head = (head + hlen - 1) % hlen
        l = (head + hlen - 1) % hlen
        c = head; 
        r = (head + 1) % hlen
        $("#ah-left").html(header[l]);
        $("#ah-center").html(header[c]);
        $("#ah-right").html(header[r]);
    });

    $("#ah-center").click(function(){
        console.log("center clicked");
    });

    $("#ah-right").click(function(){
        head = (head  + 1) % hlen
        l = (head + hlen - 1) % hlen 
        c = head; 
        r = (head + 1) % hlen

        $("#ah-left").html(header[l]);
        $("#ah-center").html(header[c]);
        $("#ah-right").html(header[r]);
    });

});