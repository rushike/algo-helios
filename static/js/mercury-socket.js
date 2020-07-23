

var loc = window.location;
var wsStart = 'ws://';
if (loc.protocol == "https:") {
    wsStart = 'wss://';
}
var endpoint = wsStart + loc.host + "/channel/";
var socket = new WebSocket(endpoint);
// console.log(moment.tz(moment(), 'Asia/Kolkata').format('DD/MM/YYYY HH:mm'),  " socket : connection ", socket)

// console.log(sessionStorage)


socket.onopen = function (e) {
    console.log(moment.tz(moment(), 'Asia/Kolkata').format('DD/MM/YYYY HH:mm'), " Web-socket conn opened ", e);
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
    // // console.log("message ", e);

    var data_dict = JSON.parse(e['data']);
    
    
    if (typeof data_dict == 'undefined' || data_dict.length <= 0) {
        // the array is defined and has at least one element
        return;
    }

    dataType = data_dict["dtype"]    
    if (dataType == "signal_update") {
        data_dict.instrument_id = data_dict.instrument_token
        // Mercury.update_equity_signal(data_dict)
        store.dispatch("update_equity_call", data_dict)
    }
    else if (dataType == 'signal'){
        console.log("signal : ", data_dict);        
        data_dict.instrument_id = data_dict.instrument_token
        if(data_dict.product_type == OPTIONS_PROD){
            store.dispatch("insert_options_call", {...data_dict, instrument_id : data_dict.instrument_token})
        }else {
            store.dispatch("insert_equity_call", {...data_dict, instrument_id : data_dict.instrument_token})
        }
        
    }
    else if (dataType == "tick"){                    
        if (data_dict.data && Array.isArray(data_dict.data)){
            // if dictionary of tick
            data_dict.data.forEach(value =>{
                store.dispatch("update_instrument", {instrument_id : value.instrument_token, ltp : value.last_price})
            })
        }
        else if(data_dict.constructor == Object) {
            store.dispatch("update_instrument",  {instrument_id : value.instrument_token, ltp : value.last_price})
        }
    }
}

socket.onerror = function (e) {
    console.log(moment.tz(moment(), 'Asia/Kolkata').format('DD/MM/YYYY HH:mm'), " : error", e);
}

socket.onclose = function (e) {
    console.log(moment.tz(moment(), 'Asia/Kolkata').format('DD/MM/YYYY HH:mm'), "close", e);
}

window.onbeforeunload = function () {
    this.socket.close();
}
