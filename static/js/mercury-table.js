

var loc = window.location;
var wsStart = 'ws://';
if (loc.protocol == "https:") {
    wsStart = 'wss://';
}
var endpoint = wsStart + loc.host + "/channel/";
var socket = new WebSocket(endpoint);
console.log("socket : coonn ,,, ", socket)

console.log(sessionStorage)


socket.onopen = function (e) {
    console.log("Web-socket conn opened ", e);
    socket.send(JSON.stringify({'load' : true}));
}


function getStatus(status) {
    if(status) {
        if(status.toLowerCase() == "partialhit") status = "Partial HIT"
        return status
    }
    return "Active"
}

function insert_new_row_for_options(source_table, data, position, status){
    
}

function insert_new_row_for_equity(source_table, data, position, status) {
    let newRow = source_table.getElementsByTagName("tbody")[0].insertRow(0);
    status = getStatus(status)
    newRow.innerHTML =
    `<td id="ticker" data-label="Ticker">`+data["ticker"]+`</td>
    <td id="ltp" data-label="LTP">`+data["price"]+`</td>
    <td id="signal" data-label="Signal"><button type="button" class="` + data['signal'] + `_btn trade " data-toggle="modal"
        data-target="#trade_modal">` + data["signal"] + `</button></td>
    <td id="signal_time" data-label="Signal Time">`+timeFormat(data["signal_time"], data["portfolio_id"])+`</td>
    <td id="price" data-label="Signal Price">`+data["price"]+`</td>
    <td id="target_price" data-label="TP">`+Math.abs(data["target_price"]).toFixed(2)+`</td>
    <td id="stop_loss" data-label="SL">`+Math.abs(data["stop_loss"]).toFixed(2)+`</td>
    <td id="profit_percent" data-label="Profit %">`+(data['profit_percent']).toFixed(2)+`</td>
    <td id="status" data-label="Status" class="call_status">`+ status +`</td>`;
    newRow.id = data["call_id"];
    newRow.setAttribute('class', data['instrument_token'])
    return newRow
}

function timeFormat(signal_time, portfolioId){
    if (portfolioId == 1  || portfolioId == "TEST") {
        return new Date(signal_time).toLocaleString("en-GB", {hour: '2-digit', minute: '2-digit'})
    }
    else if (portfolioId == 2) {
        return new Date(signal_time).toLocaleString("en-GB", {day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit'})
    }
    else if (portfolioId == 3) {
        return new Date(signal_time).toLocaleString("en-GB", {day: 'numeric', month: 'short', year: '2-digit', hour: '2-digit', minute: '2-digit'})
    }
    else if (portfolioId == 4) {
        return new Date(signal_time).toLocaleString("en-GB", {day: 'numeric', month: 'short', year: '2-digit', hour: '2-digit', minute: '2-digit'})
    }
    return new Date(signal_time).toLocaleString("en-GB", {day: 'numeric', month: 'short', year: '2-digit', hour: '2-digit', minute: '2-digit'})
}

function getEligibleTab(portfolioId) {
    if (portfolioId == 2  || portfolioId == "TEST") {
        return "intraday"
    }
    else if (portfolioId == 3) {
        return "btst"
    }
    else if (portfolioId == 4) {
        return "positional"
    }
    else if (portfolioId == 5) {
        return "longterm"
    }
    return "intraday"
}

function updateCount(activeTab) {
    var total_count = -1;
    var hit_count = 0;
    var miss_count = 0;
    var partial_count = 0;
    var table = document.getElementById(activeTab + "_data-table");
    for (var i = 0, row; row = table.rows[i]; i++) {
        status = row.cells[8].innerText
        total_count += 1
        if (status == 'HIT') {
            hit_count += 1
        }
        else if (status == 'MISS') {
            miss_count += 1
        }
        else if (status == 'Partial HIT') {
            partial_count += 1
        }
    }

    document.getElementById(activeTab + '_total_count').innerHTML = total_count;
    document.getElementById(activeTab + '_hit_count').innerHTML = hit_count;
    document.getElementById(activeTab + '_miss_count').innerHTML = miss_count;
    document.getElementById(activeTab + '_partial_hit_count').innerHTML = partial_count;
}

function update_the_tick(data_dict){
    class_name = data_dict['instrument_token']
    instruments = document.getElementsByClassName(class_name)
    for(var i = 0; i < instruments.length; i++){
        inst = instruments[i]
        if(data_dict["last_price"]) inst.cells.namedItem("ltp").innerHTML = data_dict["last_price"];

        if(data_dict["profit_percent"]) {
            inst.cells.namedItem("profit_percent").innerHTML = (data_dict["profit_percent"]).toFixed(2);
        }else{
            inst.cells.namedItem("profit_percent").innerHTML = ((parseFloat(inst.cells.namedItem("ltp").innerHTML) - inst.cells.namedItem("target_price").innerHTML) / inst.cells.namedItem("price").innerHTML * 100).toFixed(2)
        }        
    };
        
}

socket.onmessage = function (e) {
    // console.log("message ", e);

    var data_dict = JSON.parse(e['data']);
    if (typeof data_dict == 'undefined' || data_dict.length <= 0) {
        // the array is defined and has at least one element
        return;
    }
    dataType = data_dict["dtype"]
    if (dataType == "signal" || dataType == "tick" || dataType == "signal_update") {
        var status = data_dict['status']
        var active = data_dict['active']
        call_id = data_dict["call_id"];
        portfolioId = data_dict["portfolio_id"];
        var activeTab = getEligibleTab(portfolioId);
        var dataTable = document.getElementById(activeTab + "_data-table")

        var rowId = call_id
        var row = dataTable.rows.namedItem(rowId)
        if (dataType == "signal") {
            console.debug("data recieved : ", data_dict)
            let data;
            data = data_dict;
            if (existing = row) {
                // A new signal with different side is received, ignore signal with same side
                if (row.cells.namedItem("signal").innerHTML != data['signal']){
                    row = document.getElementById(rowId);
                    row.className = "disabled";
                    if (row.cells.namedItem("status").innerHTML == "Active") {
                        row.cells.namedItem("status").innerHTML = "Inactive";
                    }
                    
                    status = getStatus(status)
                    row = insert_new_row_for_equity(dataTable, data, 0, status)
                    if(!active){
                        console.log("Will disable row with call id in --signal: ", call_id)
                        row.className = "disabled";
                        
                    }
                }
            }
            else {
                status = getStatus(status)
                row = insert_new_row_for_equity(dataTable, data, 0, status);
                if (!active) {
                    console.log("Will disable row with call id : ", call_id)
                    row.className = "disabled";
                }
            }
        }
        else if (dataType == "signal_update"){
            console.debug("data recieved : ", data_dict)
            console.log("Signal Update : data_dict = ", data_dict)
            if (dataTable && row) {
                
                if(data_dict['last_price']) 
                    row.cells.namedItem("ltp").innerHTML = data_dict["last_price"];
                if(data_dict['profit_percent']) 
                    row.cells.namedItem("profit_percent").innerHTML = data_dict['profit_percent'];
                if(data_dict['status']) 
                    row.cells.namedItem("status").innerHTML = getStatus(status);
                if(data_dict['signal']) 
                    row.cells.namedItem("signal").innerHTML = `<button type="button" class="` + data_dict['signal'] + `_btn trade btn-xs" data-toggle="modal"
                                                                                    data-target="#trade_modal">` + data_dict["signal"] + `</button>`
                if(data_dict['price']) 
                    row.cells.namedItem("price").innerHTML = data_dict['price'];
                
                if (!active) {
                    console.log("Will disable row with call id : ", call_id)
                    row.className = "disabled";
                }
            }
        }
        else if(dataType == "tick"){            
            if (data_dict.data && Array.isArray(data_dict.data)){
                // if dictionary of tick
                data_dict.data.forEach(value =>{
                    update_the_tick(value)
                })
            }
            else if(data_dict.constructor == Object) {
                update_the_tick(data_dict)
            }
        }
    }

    updateCount(activeTab)
}

socket.onerror = function (e) {
    console.log("error", e);
}

socket.onclose = function (e) {
    console.log("close", e);
}

window.onbeforeunload = function () {
    this.socket.close();
}
