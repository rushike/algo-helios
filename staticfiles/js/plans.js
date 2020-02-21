const header = ["", "MERCURY", "SERVICES"  ]
const urls = ["", "#plans", "#services"]
const hlen = header.length
var head = 1
var active = "head-individual";
$(document).ready(function(){
    l = (head + hlen - 1) % hlen
    c = head; 
    r = (head + 1) % hlen
    $("#ah-left-a").html(header[l]);
    $("#ah-center-a").html(header[c]);
    $("#ah-right-a").html(header[r]);

    $("#ah-left").click(function(){
        // $("div.header a").click(function (e) {
        //     e.preventDefault();  
        //         $(this).tab('show');
        // });

        content = $("#ah-left-a").text()
        console.log("clicked on text ", content, $("#ah-left-a").toArray()) 

        head = (head + hlen - 1) % hlen
        l = (head + hlen - 1) % hlen
        c = head; 
        r = (head + 1) % hlen

        $("#ah-left-a").html(header[l]);
        $("#ah-center-a").html(header[c]);
        $("#ah-right-a").html(header[r]);

        $("#ah-left-a").attr("href", urls[l])
        $("#ah-center-a").attr("href", urls[c])
        $("#ah-right-a").attr("href", urls[r])
    });

    $("#ah-center").click(function(){
        console.log("center clicked");
    });

    $("#ah-right").click(function(){

        content = $("#ah-right-a").text()
        console.log("clicked on text ", content, $("#ah-right-a").toArray())    
        head = (head  + 1) % hlen
        l = (head + hlen - 1) % hlen 
        c = head; 
        r = (head + 1) % hlen

        $("#ah-left-a").html(header[l]);
        $("#ah-center-a").html(header[c]);
        $("#ah-right-a").html(header[r]);

        $("#ah-left-a").attr("href", urls[l])
        $("#ah-center-a").attr("href", urls[c])
        $("#ah-right-a").attr("href", urls[r])
    });

});