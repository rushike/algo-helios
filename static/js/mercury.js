var data_table = `  <div id="table-wrapper" class="tab-content">
                        <div class="row table_details p-2">
                            <div class="col-md-2 col-xs-12">
                                <input type="text" id="{}_search" class="search form-control"
                                    placeholder="Search . . . " style="border-radius: 20px;">
                            </div>
                            <!-- <div class = "col-md-7 col-xs-12">
                                <div class = "row"> -->
                                    <div class="col-md-2 col-xs-6 count_display">
                                        <label class="param">Total Calls </label>
                                        <label class="value" id="{}_total_count">0</label>
                                    </div>
                                    <div class="col-md-2 col-xs-6 count_display">
                                        <label class="param">Hits </label>
                                        <label class="value" id="{}_hit_count">0</label>
                                    </div>
                                    <div class="col-md-2 col-xs-6 count_display">
                                        <a href="#" data-toggle="tooltip" data-placement="top"
                                            title="Partially Successful Calls, Hitting 60% of Target">
                                            <label class="param">Partial Hits </label>
                                            <label class="value" id="{}_partial_hit_count">0</label>
                                        </a>
                                    </div>
                                    <div class="col-md-2 col-xs-6 count_display">
                                        <label class="param">Miss </label>
                                        <label class="value" id="{}_miss_count">0</label>
                                    </div>
                                <!-- </div>
                            </div>-->
                            <div class="col-md-2 col-xs-12 text-center btn-group btn-group-lg ">
                                <span id = "{}_filter"><a href="#" data-toggle="tooltip" data-placement="top" title="Filter">
                                    <button class="btn filter get_filter"  data-toggle="modal" data-target="#{}_filter_modal">
                                        <small><span class="fa fa-filter"></span></small>
                                    </button>
                                </a></span>
                                <a href="#" data-toggle="tooltip" data-placement="top" title="Download">
                                    <button class="btn download" onclick='exportTableToCSV("{}")'>
                                        <small><span class="fa fa-download"></span></small>
                                    </button>
                                </a>
                                <a href="#" data-toggle="tooltip" data-placement="top" title="Refresh">
                                    <button class="btn refresh" onclick="location.reload()" title="Refresh">
                                        <small><span class="fa fa-refresh"></span></small>
                                    </button>
                                </a>
                            </div>
                        </div>

                        <hr style="margin-top: 10px; margin-bottom: 5px; border-top: 1px solid #ddd">

                        <!-- Modal -->
                        <div id="{}_filter_modal" class="modal" role="dialog">
                            <div class="modal-dialog">

                            <!-- Modal content-->
                            <div class="modal-content">
                                <div class="modal-header row">
                                <div class = "col-xs-3">
                                    <div id = "{}_clear_filter" style = "cursor : pointer;">
                                        <span class="fa-stack fa-2x" style="font-size:1.8rem;">
                                            <i class="fa fa-filter fa-stack-1x"></i>
                                            <i class="fa fa-ban fa-3x fa-stack-2x"></i>
                                        </span>
                                    </div>
                                </div>
                                <div class = "col-xs-5 text-center" style = "left:3rem">
                                    <h4 class="m-auto" >Filter</h4>
                                </div>
                                <div class = "col-xs-4">
                                    <button type="button" class="close" style = "margin-left : unset; opacity : 0.8" data-dismiss="modal" >&times;</button>                                
                                </div>
                                </div>
                                <div class="modal-body">
                                <form method  = "GET" action="/worker/apply-filters"  style="text-align: left;" id="{}_filter_form">
                                    <!--{% csrf_token %} -->
                                    <div class="form-group">
                                    <label>Tickers</label>
                                        <select name="tickers" class="tickers_filter" id="{}_tickers_filter" multiple="multiple">
                                        {{~~~~~|||~~~~~}}
                                        </select>
                                    </div>
                                    <div class="form-group">
                                    <div class="row">
                                        <div class="col-md-6" style="padding-bottom: 15px;">
                                        <label style="padding-right: 10px;">Side</label>
                                            <select name="sides" class="side_filter" id="{}_side_filter" multiple="multiple">
                                            <option value="BUY">BUY</option>
                                            <option value="SELL">SELL</option>
                                            </select>
                                        </div>
                                        <div class="col-md-6">
                                        <label style="padding-right: 10px; color: LightGray;">Signal Time</label>
                                            <select class="signal_time_filter" id="{}_signal_time_filter" multiple="multiple" disabled>
                                            <option>9.30 - 10.30</option>
                                            <option>10.30 - 11.30</option>
                                            <option>12.30 - 12.30</option>
                                            <option>12.30 - 01.30</option>
                                            <option>01.30 - 02.30</option>
                                            <option>02.30 - 03.30</option>
                                            </select>
                                        </div>
                                    </div>
                                    </div>
                                    <div class="form-group">
                                    <p>
                                        <label for="{}_rr_range">Risk Reward Range:</label>
                                        <input name="rr_range" class="rr_range_cls" type="text" id="{}_rr_range" style="border:0; color: #004B96; font-weight:bold;" readonly>
                                    </p>
                                    <div id="{}_rr_slider_range" class="rr_slider_range"></div>
                                    </div>
                                    <div class="form-group">
                                    <p>
                                        <label for="{}_profit_range">Profit % Range:</label>
                                        <input name="pp_range" class="profit_range_cls" type="text"
                                        id="{}_profit_range" style="border:0; color: #004B96; font-weight:bold;" readonly>
                                    </p>
                                    <div id="{}_profit_slider_range" class="profit_slider_range"></div>
                                    </div>
                                    <div class="form-group row text-center">
                                    <button type="button" class="filter_apply btn btn-default col-xs-8 col-xs-offset-2 light-blue-bg rounded-large">Apply</button>
                                    </div>
                                </form>
                                </div>
                            </div>

                            </div>
                        </div>

                        <table id="{}_data-table" class="table">
                            <thead>
                                <tr id="t-headers">
                                    <th>Ticker  <a><i class="fa fa-fw fa-sort"/></a></th>
                                    <th>LTP</a></th>
                                    <th>Signal  <a><i class="fa fa-fw fa-sort"/></a></th>
                                    <th>Signal Time  <a><i class="fa fa-fw fa-sort"/></a></th>
                                    <th>Signal Price  <a><i class="fa fa-fw fa-sort"/></a></th>
                                    <th>Target Price</a></th>
                                    <th>Stop Loss</th>
                                    <!-- <th><b>Risk/Reward</b>  <a><i class="fa fa-fw fa-sort"/></a></th> -->
                                    <th><a href="#" data-toggle="tooltip" data-placement="top"
                                    title="Expected Profit with respect to LTP if entered now">Profit %</a> <a><i class="fa fa-fw fa-sort"/></a></th>
                                    <th>Status <a><i class="fa fa-fw fa-sort"/></a></th>
                                    <!-- <th>Action</th> -->
                                    <!-- TODO: Display hit/miss number -->
                                </tr>
                            </thead>
                            <tbody id="{}_data-table-rows"/>
                        </table>
                    </div>`

String.prototype.format = function () {
    var i = 0, args = arguments;
    return this.replace(/{}/g, function () {
    return typeof args[0] != 'undefined' ? args[0] : '';
    });
};

function option_tag_list(list){
    var op_str = "";
    for(var i = 0; i < list.length; i++){
        op_str += "<option value" + list[i] + ">" + list[i] + "</option>"
    }return op_str
}


$(document).ready(function() {

        $.ajax({
            type: "GET",
            url: "/worker/get-filters",
            // data: {},
            data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
            success: function(data)
            {
                $.each(data, function(tab_to_consider, filter_data) {
                    console.log("Filter data recieved from database for portfolio : ", tab_to_consider, ", Data ", filter_data)
                    tab_id = "#" + tab_to_consider
                    $( tab_id + "_rr_range" ).val(filter_data['risk_reward'][0] + " - " + filter_data['risk_reward'][1]);
                    $( tab_id + "_profit_range" ).val(filter_data['profit_percentage'][0] + " - " + filter_data['profit_percentage'][1]);
                    $( tab_id + "_tickers_filter").multiselect('select', filter_data['tickers']);
                    $( tab_id + "_side_filter").multiselect('select', filter_data['sides']);
                    $( tab_id + "_rr_slider_range" ).slider( "option", "values", [ filter_data['risk_reward'][0], filter_data['risk_reward'][1] ] );
                    $( tab_id + "_profit_slider_range" ).slider( "option", "values", [ filter_data['profit_percentage'][0], filter_data['profit_percentage'][1] ] );
                });
            },
            error: function(request, status, error)
            {
                alert(request.responseText);
            }
        });

        function getEligibleTab(portfolioId) {
            if (portfolioId == 1  || portfolioId == "TEST") {
                return "intraday"
            }
            else if (portfolioId == 2) {
                return "btst"
            }
            else if (portfolioId == 3) {
                return "positional"
            }
            else if (portfolioId == 4) {
                return "longterm"
            }
            return "intraday"
        }
    function fetch_instruments_for_portfolio(portfolio){
        var data = $.ajax({
            type: "POST",
            async: false,
            url: "/worker/get-instrument-from-portfolio",           
            data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value, 'portfolio_id' : portfolio},
            success: function(data)
            {
                return option_tag_list(data);
            },
            error: function(request, status, error)
            {
                alert(request.responseText);
            }
        });
        return option_tag_list(data.responseJSON)
    }

    $.each([ "intraday", "btst", "positional", "longterm" ], function( index, value ) {
        $("#" + value + "_content").html(data_table.format(value).replace("{{~~~~~|||~~~~~}}", fetch_instruments_for_portfolio(value)));

        $( "#" + value + "_rr_slider_range" ).slider({
                range: true,
                min: 0,
                max: 5,
                step: 0.1,
                values: [1, 5],
                slide: function( event, ui ) {
                $( "#" + value + "_rr_range" ).val( ui.values[ 0 ] + " - " + ui.values[ 1 ] );
                }
        });

        $("#" + value + "_clear_filter").click(()=>{
            $.ajax({
                type: "POST",
                async: false,
                url: "/worker/clear-filter/",           
                data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value, 'portfolio_id' : value},
                success: function(data)
                {
                    console.log("filter cleared")
                    location.reload();
                },
                error: function(request, status, error)
                {
                    alert(request.responseText);
                }
            });
        });

        $( "#" + value + "_rr_range" ).val($( "#" + value + "_rr_slider_range" ).slider( "values", 0 ) +
            " - " + $( "#" + value + "_rr_slider_range" ).slider( "values", 1 ) );

            $( "#" + value + "_profit_slider_range" ).slider({
                range: true,
                min: 0,
                max: 50,
                step: 0.1,
                values: [0, 50],
                slide: function( event, ui ) {
                    $( "#" + value + "_profit_range" ).val( ui.values[ 0 ] + " - " + ui.values[ 1 ] );
                }
        });

        $( "#" + value + "_rr_slider_range" ).draggable();
        $( "#" + value + "_profit_slider_range" ).draggable();

        $( "#" + value + "_profit_range" ).val($( "#" + value + "_profit_slider_range" ).slider( "values", 0 ) +
            " - " + $( "#" + value + "_profit_slider_range" ).slider( "values", 1 ) );
    });

    $('.tickers_filter').multiselect({
        includeSelectAllOption: true,
        enableFiltering: true,
        enableCaseInsensitiveFiltering: true,
        includeFilterClearBtn: false,
        dropRight: true,
        buttonWidth: '80%'
    });

    $('.side_filter').multiselect({
        buttonWidth: '30%',
        nonSelectedText:'None',
        allSelectedText:'All',
    });

    $('.signal_time_filter').multiselect({
        includeSelectAllOption: true,
        buttonWidth: '50%',
        allSelectedText: 'Trading session'
    });

    const getCellValue = (tr, idx) => tr.children[idx].innerText || tr.children[idx].textContent;

    const comparer = (idx, asc) => (a, b) => ((v1, v2) =>
        v1 !== '' && v2 !== '' && !isNaN(v1) && !isNaN(v2) ? v1 - v2 : v1.toString().localeCompare(v2)
        )(getCellValue(asc ? a : b, idx), getCellValue(asc ? b : a, idx));

    document.querySelectorAll('th').forEach(th => th.addEventListener('click', (() => {
        const table = document.getElementById($('.nav-tabs .active').attr("id") + "_data-table");
        const tbody = table.children[1];
        Array.from(tbody.querySelectorAll('tr:nth-child(n+1)'))
            .sort(comparer(Array.from(th.parentNode.children).indexOf(th), this.asc = !this.asc))
            .forEach(tr => tbody.appendChild(tr));
    })));

    function isTouchDevice(){
        return true == ("ontouchstart" in window || window.DocumentTouch && document instanceof DocumentTouch);
    }

    if (isTouchDevice()===false) {
        $('[data-toggle="tooltip"]').tooltip({
                'delay': { show: 1000 }, trigger: "hover"
        });
    }

    $('.table').on('load change DOMNodeInserted', '.call_status', function(e){
        var closest_tr = $(this).closest('tr')
        status = closest_tr.find('td:eq(8)').html()
        badge_template = 'active_status'
        if (status == 'MISS') {
            badge_template = 'miss_status'
        } else if (status == 'HIT') {
            badge_template = 'hit_status'
        } else if (status == 'Inactive') {
            badge_template = 'inactive_status'
        } else if (status == 'Active') {
            badge_template = 'active_status'
        } else if (status == 'Partial HIT') {
            badge_template = 'partialhit_status'
        } else {
            return
        }

        new_html = `<span class="badge white ` + badge_template + `">` + status + `</span>`;
        closest_tr.find('td:eq(8)').html(new_html)
    });

    $('.table').on('click', '.trade', function(e) {
        $('#trade_action').remove();
        activeTab = $('.nav-tabs .active').attr("id")

        if (activeTab == "intraday") {
            $("input[name=trade_type][value='MIS']").prop("checked",true).trigger('change');
            $("input[name=exec_type][value='bo']").prop("checked",true).trigger('change');
            $("input[name=order_type][value='LIMIT']").prop("checked",true).trigger('change');
        } else {
            $("input[name=trade_type][value='CNC']").prop("checked",true).trigger('change');
            $("input[name=exec_type][value='regular']").prop("checked",true).trigger('change');
        }
        var closest_tr = $(this).closest('tr')

        var id = closest_tr.attr("id")
        var ticker = closest_tr.find('td:eq(0)').html()
        var ltp = closest_tr.find('td:eq(1)').html()
        var signal = closest_tr.find('td:eq(2)').text()
        var tp = closest_tr.find('td:eq(5)').html()
        var sl = closest_tr.find('td:eq(6)').html()

        $('#trade_ticker').text(ticker);
        $('input[name=price]').val(ltp);
        $('input[name=target_price]').val(Math.round(Math.abs(tp - ltp) * 10) / 10);
        $('input[name=stop_loss]').val(Math.round(Math.abs(sl - ltp) * 10) / 10);
        $('input[name=trigger_price]').val(sl);

        var trade_action_btn = $('<button id="trade_action2" type="button" class= "trade_action col-md-offset-2 col-md-8 btn btn-rounded rounded-large">');
        trade_action_btn.attr("data-name", signal);
        console.log("trade_action : ", trade_action_btn, ", signal : ", signal)
        trade_action_btn.text(signal);
        if (signal == "BUY") {
            trade_action_btn.removeClass("SELL_btn");
            $('#trade_header').removeClass("SELL_header");
        } else {

            trade_action_btn.removeClass("BUY_btn");
            $('#trade_header').removeClass("BUY_header");
        }
        trade_action_btn.addClass(signal + "_btn");
        $('#trade_header').addClass(signal + "_header");
        $("#trade_action2").remove()
        $("#buttonView").append(trade_action_btn);

        $('.trade_action').on('mousedown', function(e){
            KiteConnect.ready(function() {
                // You can initialize multiple instances if you need
                var kite = new KiteConnect("tpisubdoz4a7cskn"); // Initialize a new Kite instance

                var trade_input = {
                    "tradingsymbol": $('#trade_ticker').text(),
                    "exchange": "NSE",
                    "transaction_type": $('#trade_action2').text(),
                    "order_type": $('input[name="order_type"]:checked').val(),
                    "product": $('input[name="trade_type"]:checked').val(),
                    "price": parseFloat($('input[name=price]').val()),
                    "quantity": parseInt($('input[name=quantity]').val()),
                    "variety": $('input[name="exec_type"]:checked').val(),
                    "stoploss": parseFloat($('input[name=stop_loss]').val()),
                    "squareoff": parseFloat($('input[name=target_price]').val()),
                    "trailing_stoploss": parseFloat($('input[name=trailing_stop_loss]').val()),
                    "trigger_price": parseFloat($('input[name=trigger_price]').val()),
                    "disclosed_quantity": parseInt($('input[name=quantity]').val())
                }
                console.log(trade_input)
                // Add a Bracket Order
                kite.add(trade_input);

                // Register an (optional) callback.
                kite.finished(function(status, request_token) {
                    alert("Order Placed!! Status is " + status);
                });

                // Render the in-built button inside a given target
                kite.link("#trade_action2");
            });
        });

        $('.trade_action').on('click', function(e){
            console.log("trade action clicked")
            $('#trade_modal').modal('toggle');
        });
    });

    $('input[name=exec_type]').on('change', function(){
            exec_type = $('input[name=exec_type]:checked').val();

            if (exec_type == "bo" || exec_type == "co") {
            $("input[name=trade_type][value='MIS']").prop("checked",true);
            $("input[name=trade_type]").prop('disabled', true);

            if (exec_type == "bo") {
                $("input[name=order_type][value='LIMIT']").prop("checked",true);
                $("input[name=order_type]").prop('disabled', true);
                $("input[name=trigger_price]").prop('disabled', true);

                $("#trade_bo_params").prop('hidden', false);

                $("input[name=target_price]").prop('disabled', false);
                $("input[name=stop_loss]").prop('disabled', false);
                $("input[name=trailing_stop_loss]").prop('disabled', false);
            } else {
                $("input[name=order_type][value='LIMIT']").prop("checked",true);
                $("input[name=order_type]").prop('disabled', false);

                $("#trade_bo_params").prop('hidden', true);

                $("input[name=trigger_price]").prop('disabled', false);
                $("input[name=target_price]").prop('disabled', true);
                $("input[name=stop_loss]").prop('disabled', true);
                $("input[name=trailing_stop_loss]").prop('disabled', true);
            }
            } else {
            $("input[name=trade_type]").prop('disabled', false);
            $("input[name=order_type]").prop('disabled', false);
            $("input[name=trigger_price]").prop('disabled', true);

            $("#trade_bo_params").prop('hidden', true);

            $("input[name=target_price]").prop('disabled', true);
            $("input[name=stop_loss]").prop('disabled', true);
            $("input[name=trailing_stop_loss]").prop('disabled', true);
            }
    });

    $('input[name=order_type]').on('change', function(){
        order_type = $('input[name=order_type]:checked').val();
        if (order_type == "MARKET") {
            $("input[name=price]").prop('disabled', true);
        } else {
            $("input[name=price]").prop('disabled', false);
        }
    });

    $(".search").on('keyup', function () {
        var value = $(this).val().toLowerCase();
        $("#" + $('.nav-tabs .active').attr("id") + "_data-table-rows tr").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });

    $("input[name=quantity]").on('keyup', function () {
        $("input[name=disclosed_quantity]").val($(this).val());
    });

    $(".filter_apply").on('click', function () {
        var current_tab = $('.nav-tabs .active').attr("id")
        console.log("Data to be send", $('#' + current_tab + "_filter_form").serialize(), $('#' + current_tab + "_filter_form") )
        $.ajax({
            type: "GET",
            url: "/worker/apply-filters/",
            data: $('#' + current_tab + "_filter_form").serialize()  + '&call_type=' + current_tab,
            success: function(data)
            {
                console.log("Filter applied successfully!");
                location.reload();
            },
            error: function(request, status, error)
            {
                location.reload()
            }
        });
    });

    $(".product-tabs").on('click', function () {
        console.log($('.nav-tabs li.active a').attr("href"))
        $("meta[name=active-tab]").attr("content", $('.nav-tabs li.active a').attr("href"));
    });

        $('.nav-tabs a[href="#' + $('meta[name=active-tab]').attr("content") + '"]').tab('show');
});

// PUSH Notifications

const registerSw = async () => {
    if ('serviceWorker' in navigator) {
        console.log("Will initialte sw.js NOTIFICATION")
        const reg = await navigator.serviceWorker.register('/static/js/sw.js');
        initialiseState(reg)
        console.log("initialted sw.js with reg : ", reg)

    } else {
        console.log("Not eligible for push notifications!!")
    }
};

const initialiseState = (reg) => {
    if (!reg.showNotification) {
        console.log('Showing notifications isn\'t supported');
        return
    }
    if (Notification.permission === 'denied') {
        console.log('You prevented us from showing notifications');
        return
    }
    if (!'PushManager' in window) {
        console.log("Push isn't allowed in your browser");
        return
    }
    subscribe(reg);
}

function urlB64ToUint8Array(base64String) {
    const padding = '='.repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding)
        .replace(/\-/g, '+')
        .replace(/_/g, '/');

    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);
    const outputData = outputArray.map((output, index) => rawData.charCodeAt(index));

    return outputData;
}

const subscribe = async (reg) => {
    const subscription = await reg.pushManager.getSubscription();
    console.log("Subscribe : subscriptions : ", subscription)
    if (subscription) {
        sendSubData(subscription);
        return;
    }

    const vapidMeta = document.querySelector('meta[name="vapid-key"]');
    const key = vapidMeta.content;

    const options = {
        userVisibleOnly: true, 
        // ...(key && {applicationServerKey: urlB64ToUint8Array(key)})// if key exists, create applicationServerKey property 
    };
    if(key) {
        options.applicationServerKey = urlB64ToUint8Array(key)
    }
    const sub = await reg.pushManager.subscribe(options);
    sendSubData(sub)
};

// TODOs
// Get all products subscribed from backend
// You get the list of products
const sendSubData = async (subscription) => {
    const browser = navigator.userAgent.match(/(firefox|msie|chrome|safari|trident)/ig)[0].toLowerCase();
    groups = await fetch('/worker/user_channel_groups/')
        .then(async (response) => {
            return await response.json();
        })


    console.log("Groups await from channels are : ", groups, groups.length)
    // Subscribe based on the groups eligible
    for(var i = 0; i < groups.length; i++){
        const data = {
            status_type: 'subscribe',
            subscription: subscription.toJSON(),
            browser: browser,
            group: groups[i],
        };
        console.log("Data to Webpush Save : ", data);
        const res = await fetch('/webpush/save_information', {
            method: 'POST',
            body: JSON.stringify(data),
            headers: {
                'content-type': 'application/json'
            },
            credentials: "include"
        });

        console.log("sendSubData res : is :  ", res)

        handleResponse(res);
    }
};

const handleResponse = (res) => {
    console.log(res.status);
};

registerSw();
