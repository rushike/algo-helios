/**
 * Trade Modal
 */
const MTradeModal = Vue.component('m-trade-modal', {
    props : ['item'],
    data : () =>{
        return {
            broker : 'Zerodha',
            instrument_name : 'Nifty 50',
            order_type : '',
            exec_type : '',
            quantity : 1,
            disclosed_quantity : 1,
            trailing_stop_loss : 0,
            trigger_price : 0,
            // quantity : 0,
            // show : this.item ? true : false
        }
    },
    computed : {
        show: {
            get(){
                return this.item ? true : false
            },
            set(value){
                
            }
        },
        trade_type:{
            get(){
                return this.$store.getters.state.portfolio == INTRADAY ? "MIS" : "CNC";
            },
            set(value){

            }
        },
    },
    methods : {
        closed(){
            this.$emit('closed')
        },
        place_order(){
            var self = this;
            console.log("self : ", self);
            function kite_warpper(self){    
                return function() {
                    // You can initialize multiple instances if you need
                    var kite = new KiteConnect("tpisubdoz4a7cskn"); // Initialize a new Kite instance
                    console.log("self : ", self);
                    
                    var trade_input = {
                        "tradingsymbol": self.item.ticker,//$('#trade_ticker').text(),
                        "exchange": "NSE",
                        "transaction_type": self.item.signal,//$('#trade_action2').text(),
                        "order_type": self.order_type, //$('input[name="order_type"]:checked').val(),
                        "product": self.trade_type ,//$('input[name="trade_type"]:checked').val(),
                        "price": parseFloat(self.item.price) ,// parseFloat($('input[name=price]').val()),
                        "quantity": parseFloat(self.quantity),//parseInt($('input[name=quantity]').val()),
                        "variety": self.exec_type,//$('input[name="exec_type"]:checked').val(),
                        "stoploss": parseFloat(self.item.stop_loss),//parseFloat($('input[name=stop_loss]').val()),
                        "squareoff": parseFloat(self.item.target_price),//parseFloat($('input[name=target_price]').val()),
                        "trailing_stoploss": parseFloat(self.trailing_stop_loss), //parseFloat($('input[name=trailing_stop_loss]').val()),
                        "trigger_price": parseFloat(self.trigger_price), //parseFloat($('input[name=trigger_price]').val()),
                        "disclosed_quantity": self.disclosed_quantity, //parseInt($('input[name=quantity]').val())
                    }
                    console.log(trade_input)
                    // Add a Bracket Order
                    kite.add(trade_input);

                    // Register an (optional) callback.
                    kite.finished(function(status, request_token) {
                        alert("Order Placed!! Status is " + status);
                    });

                    // Render the in-built button inside a given target
                    kite.link("#trade_action");
                }
            }
            KiteConnect.ready(kite_warpper(self))
        }
    },
    template : M_TRADE_MODAL,
});


/**
 * Stock Table
 */
const MStockTable = Vue.component("m-stocks-table", {    
    props : ['state', 'items', 'fields', 'headers'],
    data: () => {
        return {
            transProps: {
                // Transition name
                name: 'flip-list'
            },
            filterOn : [],
            trade_item : null,
            fields0 : "JUJ",
            show : false,
            search_fields : "",
        }
    },
    created(){
        console.log("stocks table created : ", this.fields);        
    },
    computed :{
        search : {
            get(){
                return this.$store.getters.search
            },
            set(value){
                console.log(value)
                this.$store.commit("update_search", value);
            }
        },
        filter : {
            get(){
                return this.$store.getters.filter
            },
            set(value){
                console.log(value)
                this.$store.commit("update_filter", value);
            }
        },
        filter_items(){
            return this.items.filter(d => {
                // if(TYPE[d.product_type] == OPTIONS) return true;
                if(Array.isArray(this.filter.profit_percentage) && 
                            this.filter.profit_percentage.length == 2 && 
                            !( this.filter.profit_percentage[0] <= d.profit * 100 && 
                            this.filter.profit_percentage[1] >= d.profit * 100 ))
                    return false
                else if(Array.isArray(this.filter.sides) && (this.filter.sides.length == 0 || !this.filter.sides.map(v=>v.toLowerCase()).includes(d.signal.toLowerCase())))
                    return false

                else if(Array.isArray(this.filter.tickers) && 
                        (this.filter.tickers.length == 0 || 
                        !this.filter.tickers.filter(v=>v).map(v=>v.toLowerCase()).includes(d.ticker.toLowerCase())))
                    return false
                
                else if(Array.isArray(this.filter.risk_reward) && 
                        this.filter.risk_reward.length == 2 && 
                        !( this.filter.risk_reward[0] <= d.risk_reward && 
                        this.filter.risk_reward[1] >= d.risk_reward))
                    return false
                return true
            })
        },
        selected_fields : {
            get(){                
                return this.$store.getters.selected_fields
            },
            set(selected_fields){
                this.$store.dispatch("update_selected_fields", selected_fields)
            }
        },
        fields_(){
            return this.$store.getters.fields.map(v=>v.text)
        },
        selected_fields_(){
            // console.log("?selght L  : ", this.$store.getters.selected_fields )
            return this.$store.getters.selected_fields.map(v=>v.text)
        },
        loading(){
            return this.filter_items.length == 0
        },
    },
    methods : {                
        forceRerender : function() {            
            this.tablekey += 1        
        },  
        onFiltered : function(filteredItems) {            
            this.totalRows = filteredItems.length
        }, 
        update_selected_fields(sel_fields){
            this.selected_fields = sel_fields;
        },
        row_class(group, index, item, items){
            var class_ = "hover-pointer "        
            var border = group ? "mx-1 follow_trade border " : ' ',
                active = item.active ? ' ' : 'disabled ', 
                group_highlight = (index == items.length - 1) ? ( index == 0 ? '' : 'border-top-0 '  ) : (index == 0 ? 'border-bottom-0 ' : 'border-top-0 border-bottom-0 ' )
            return class_ + border + active + group_highlight
             
        },
        follow_my_trade(item, follow){
            var callback = Signal.set_follow, params = {item, follow}
            this.$store.commit("do_from_store", {callback, params} )
        },
        delete_call(item){
            var callback = Signal.hide, params = {item}
            this.$store.commit("do_from_store", {callback, params} )
        },
        portfolio_filter(val, search, item, headers){
            if(search.length < 3 ){
                return true
            }
            console.log("VALUE : ", val);
            
            if(val.toString().toLowerCase().includes(search.toLowerCase())){     
                console.log("this.filter : ", this.filter)           
                return true
            }

            return false
        },        
        filter_on_search(val) {
            this.filter = this.$MultiFilters.updateFilters(this.filter, {search: val});
        },
        table_settings_toggle(){
            store.commit("mobile_toggle")
        },    
        is_mobile__class(){
            if(helpers.is_mobile()) 
                return 'table-settings--mobile'; 
            return 'table-settings--desktop';
        },
        show_trade_modal(item){
            this.show = !this.show
            if(this.trade_item){
                this.trade_item = null
            }else {
                this.trade_item = item
            }
        }
    },
    template : M_STOCKTABLE_TEMPLATE_STRING,
});


/**
 * Options Table
 */
const MOptionsTable = Vue.component("m-options-table", {    
    props : ['state', 'items', 'fields', 'headers'],
    data: () => {
        return {
            transProps: {
                // Transition name
                name: 'flip-list'
            },
            filterOn : [],
            fields0 : "JUJ",
        }
    },
    computed :{
        search : {
            get(){
                return this.$store.getters.search
            },
            set(value){
                console.log(value)
                this.$store.commit("update_search", value);
            }
        },
        filter : {
            get(){
                return this.$store.getters.filter
            },
            set(value){
                console.log(value)
                this.$store.commit("update_filter", value);
            }
        },
        filter_items(){
            return this.items.filter(d => {                
                if(Array.isArray(this.filter.profit_percentage) && 
                            this.filter.profit_percentage.length == 2 && 
                            !( this.filter.profit_percentage[0] < d.profit * 100 && 
                            this.filter.profit_percentage[1] > d.profit * 100 ))
                    return false                
                else if(Array.isArray(this.filter.sides) && this.filter.sides.length != 0 && !this.filter.sides.map(v=>v.toLowerCase()).includes(d.signal.toLowerCase()))
                    return false

                else if(Array.isArray(this.filter.tickers) && 
                        this.filter.tickers.length != 0 && 
                        !this.filter.tickers.map(v=>v.name.toLowerCase()).includes(d.ticker.toLowerCase()))
                    return false
                
                else if(Array.isArray(this.filter.risk_reward) && 
                        this.filter.risk_reward.length == 2 && 
                        !( this.filter.risk_reward[0] < d.risk_reward && 
                        this.filter.risk_reward[1] > d.risk_reward))
                    return false            
                return true
            })
        },
        loading(){
            return this.filter_items.length == 0
        },
    },
    methods : {                
        forceRerender : function() {            
            this.tablekey += 1        
        },  
        onFiltered : function(filteredItems) {            
            this.totalRows = filteredItems.length
        },
        
        filter_on_search(val) {
            this.filter = this.$MultiFilters.updateFilters(this.filter, {search: val});
        },
    },
    template : M_OPTIONSTABLE_TEMPLATE_STRING,
});


/**
 * Equity Table
 */
const MEquity = Vue.component("m-equity", {    
    props : ['state', 'items', 'fields', 'headers'],
    data: () => {
        return {
            transProps: {
                // Transition name
                name: 'flip-list'
            },
            fields0 : "JUJ",
        }
    },
    methods : {                
        forceRerender : function() {            
            this.tablekey += 1        
        },  
    },
    template : M_EQUITY_TEMPLATE_STRING,
    components: { 'm-stock-table': MStockTable}
});

/**
 * Mercury Indian Market
 */
const MIndianMarket = Vue.component("m-indian-market", {    
    props : ['state', 'items', 'fields', 'headers'],
    data: () => {
        return {
            transProps: {
                // Transition name
                name: 'flip-list',
                fields0 : "huhyf"
            },
        }
    },
    methods : {                
        forceRerender : function() {            
            this.tablekey += 1        
        },  
    },
    template : M_INDIAN_MARKET_TEMPLATE_STRING,
    components: { 'm-equity': MEquity}
});

const MDataTable = Vue.component('m-data-table', {   
    props : ['state', 'items', 'fields', 'headers'],   
    data: () => {
        return {
            transProps: {
                // Transition name
                name: 'flip-list'
            },
            fields0 : "JUJ",
        }
    },    
    methods : {                
        forceRerender : function() {            
            this.tablekey += 1        
        },  
    },
    template : M_DATA_TABLE,
    components: { 'm-indian-market': MIndianMarket}
})

/**
 * TableInfo
 */
const MDataTableInfo = Vue.component('m-data-table-info', {       
    data: () => {
        return {
            lsearch : this.filter,
            equity_type : [
                "STOCKS",
                "OPTIONS",
            ],
            notification : true,
            mobile_settings_toggle : false,
        }
    },
    computed : {

        type : {
            get(){
                return this.$store.state.state.type.toUpperCase()
            },
            set(value){
                var type = value.toLowerCase()
                // console.log("radio toggle | value : ", value, ", type : ", type)
                this.$store.dispatch('change_state', {'type' : type})
            }
        },
        search : {
            get(){
                return this.$store.getters.search
            },
            set(value){
                this.$store.commit("update_search", value);
            }
        },
        filter : {
            get(){
                return this.$store.getters.filter
            },
            set(filter){                
                let db_fetch = false
                this.$store.commit("update_filter", {filter, db_fetch});
            }
        },
        meta : {
            get(){
                return this.$store.getters.meta
            },
            set(meta){                                
                this.$store.commit("update_meta", meta);
            }
        },
        fields(){
            return this.$store.getters.fields
        },
        selected_fields : {
            get(){
                return this.$store.getters.selected_fields
            },
            set(selected_fields){
                console.log("selected fileds : ", selected_fields);
                
                // var selected_fields_ = []
                // selected_fields.forEach(v=>{
                //     var el = this.$store.getters.fields.find(element => element.key == v);
                //     selected_fields_.push(el)
                // });
                this.$store.dispatch("update_selected_fields", selected_fields)
            }
        }
    },
    methods : {                
        forceRerender : function() {            
            this.tablekey += 1        
        },
        nifty_50_tick(){
            return this.$store.getters.instruments[NIFTY_50] ? this.$store.getters.instruments[NIFTY_50].ltp : "0000.00"
        },
        nifty_bank_tick(){
            return this.$store.getters.instruments[NIFTY_BANK] ? this.$store.getters.instruments[NIFTY_BANK].ltp  : "0000.00"
        },
        filter_on_search(val) {
            this.filters = this.$MultiFilters.updateFilters(this.filters, {search: val});
        },
        ...Vuex.mapMutations([
            'update_search',
        ]), 
        download_as_csv(){
            var fields = this.$store.getters.fields, items = this.$store.getters.items, portfolio = this.$store.getters.state.portfolio
            var d = new Date();
            var filename = "AlgonautsCalls_" + portfolio + '_' + d.getFullYear() + '' + (d.getMonth()+1) + '' + d.getDate() + ".csv"
            var csv = ['Ticker, Last Price, Signal, Signal Time, Signal Price, Target Price, Stop Loss, Profit %, Status'];        
            items.forEach(item => {
				csv.push(item.toString())
            })
            var csv_string = csv.join("\n")

            var csvFile = new Blob([csv_string], {type: "text/csv"});   // CSV file
            var downloadLink = document.createElement("a");             // Download link
            downloadLink.download = filename;                           // File name
            downloadLink.href = window.URL.createObjectURL(csvFile);    // Create a link to the file
            downloadLink.style.display = "none";                        // Hide download link
            document.body.appendChild(downloadLink);                    // Add the link to DOM
            downloadLink.click();                                       // Click download link
        },
        async refresh_table(){
            var force = false, mercury = Mercury
            this.$store.dispatch('refresh_table', {force, mercury})
        },
        allow_notification :  _.throttle(async function(){
            // this.notification = !this.notification
            var data =  (await axios.post('/user/toggle-notification/', {})).data
            this.notification = data['allow_notification']
        }, 3000),       
        show_table_settings__class(){
            var mobile_settings_toggle = store.getters.mobile_toggle
            if(helpers.is_mobile() || mobile_settings_toggle){                
                return "table-settings--visible";
            }else{
                return "table-settings--invisible"
            }
        },
        is_mobile(){
            return helpers.is_mobile()
        },
        is_mobile__class(){
            if(helpers.is_mobile()) 
                return 'table-settings--mobile'; 
            return 'table-settings--desktop';
        },
    },
    template : M_DATA_TABLE_INFO,
    // components: { 'm-indian-market': MIndianMarket}
})


const MFILTER_INLINE = Vue.component('m-filter-inline', {
    data(){
        return {                        
            min__profit_percentage : 0,
            max__profit_percentage : 50,
            min__risk_reward : 0,
            max__risk_reward : 5,
            side_options : [
                {
                    side : "BUY",                    
                },
                {
                    side : "SELL"
                }
            ],
        }
    },
    computed : {
        filter : {
            get(){
                return this.$store.getters.filter
            },
            set(filter){
                let db_fetch = false
                this.$store.commit("update_filter", {filter, db_fetch});
            }
        },
        ticker_options : {
            get(){
                return this.$store.getters.instruments
            },
            set(value){
                console.log("Filter set value : ", value)
            }
        },
        ticker_values:{
            get(){
                // console.log("values copmputed: ", this.filter, Object.keys(this.filter) ,this.filter.sides, this.$store.getters.filter.sides)
                return this.filter.tickers
            },
            set(value){
                console.log("ticks valuess :", this.filter.tickers, value);
                let filter = {"tickers" : value,}
                Vue.set(this, 'filter', filter)
            }
        },
        side_values:{
            get(){
                // console.log("values copmputed: ", this.filter, Object.keys(this.filter) ,this.filter.sides, this.$store.getters.filter.sides)
                return this.filter.sides
            },
            set(value){
                // console.log(this.filter.sides, value[0], value[1] ? value[1].side :value[1] , value[2] ? value[2].side :value[2]);
                let filter = {"sides" : value,}
                Vue.set(this, 'filter', filter)
            }
        },
        pp_range:{
            get(){
                return this.filter.profit_percentage || [0, 50]
            },
            set(value){
                let filter = {"profit_percentage" : value}
                Vue.set(this, 'filter', filter)
            }
        },
        rr_range:{
            get(){
                return this.filter.risk_reward || [0, 5]
            },
            set(value){
                let filter = {"risk_reward" : value}
                Vue.set(this, 'filter', filter)
            }
        },
    },
    methods : {
        select (option) {
            option.selected = !option.selected
        },
        ticker_name(option){
            return option.name
        },
        side_name(option){
            return option.side
        },
    },
    template : M_FILTER_INLINE,
    components: {
        Multiselect: window.VueMultiselect.default
        
    },

})

const MTableWrapper = Vue.component('m-table-wrapper', {   
    props : ['state', 'items', 'fields', 'headers'],
    data: () => {
        return {
            transProps: {
                // Transition name
                name: 'flip-list'
            },
            fields0 : "JUJ",
        }
    },
    methods : {                
        forceRerender : function() {            
            this.tablekey += 1        
        },  
    },
    template : M_TABLE_WRAPPER,
    components: { 'm-data-table': MDataTable, 'm-data-table-info' : MDataTableInfo}
})

const MNavigator = Vue.component('m-navigator', {       
    data: () => {
        return {
            transProps: {
                // Transition name
                name: 'flip-list'
            },
            fields0 : "JUJ",
            active_ : 0,            
        }
    },    
    computed : {
        toggle_exclusive : {
            get(){
                return this.active_
            },
            set(value){
                console.log("Value active in tab : ", value)
                this.active_ = value
            }
        }, 
        portfolios(){
            return PORTFOLIOS.slice(2)
        }
    },
    methods : {   
        forceRerender(){            
            this.tablekey += 1
        },  
        change_state(){
            var portfolio = PORTFOLIOS[this.active_ + 2]
            console.log("portfolio changed to : ", portfolio)
            this.$store.dispatch('change_state', {"portfolio" : portfolio})
        },
    },
    template : M_NAVIGATOR,
    components: { 'm-data-table': MDataTable, 'm-data-table-info' : MDataTableInfo}
})

const MMultiselect = Vue.component('m-multiselect', {
    props : ['items', 'search', 'height', 'selected_all', 'wait'],
    data : ()=>{
        
        return {
            selected: [],
            emit : false,
            headers : [
                {
                    key : "name",
                    label : "Select All",
                    text : "Select All",
                    sortable : false,
                    value : "name"
                }
            ],
        }
    },
    async created (){    
        while(this.wait){
            await sleep(500)
        }
        if(Array.isArray(this.selected_all)) this.selected = this.selected_all.filter(v=>v).map(v=>{return{name : v}})
    },
    computed : {
        __m_items(){            
            return this.items.map(v => {return {"name" : v}})
        },
        __m_height(){
            return this.height ? this.height : "160"
        },
        loading(){
            return this.__m_items.length == 0
        },
    },
    methods :{
        row_clicked(item){            
            // this.$emit("item-selected", {item : item, value : true})
            // this.selected.push(item.name)        

            this.emit = true
            if(this.selected.some(v => v.name == item.name)){
                this.selected = this.selected.filter(v=> v.name != item.name)
            }else{
                this.selected.push(item)
            }
            

            console.log("row click item ", item, item.name, this.selected);
            
        },
        item_selected(item, value){
            // console.log("item, value : ", this.selected)                        
            this.emit = true
            if(Array.isArray(item)){
                Vue.set(this, 'selected', item)
            }
        }
    },
    watch : {
        selected(){
            if(this.emit){         
                console.log("watch : selected change : ", this.selected);
                       
                this.$emit('change', this.selected.filter(v=>v).map(v=>v.name))
            }
        },
        selected_all(){
            if(Array.isArray(this.selected_all)) {
                this.emit = false 
                this.selected = this.selected_all.map(v=>{return{name : v}})  
            }
            
        }
    },
    template : M_MULTISELECT
})

const MFilterSidebar = Vue.component('m-filter-sidebar', {
    props : [],
    data: () => {
        return {
            transProps: {
                // Transition name
                name: 'flip-list'
            },
            fields0 : "JUJ",            
            search : "",
            selected_tickers: [],
            min__profit_percentage : 0,
            max__profit_percentage : 50,
            min__risk_reward : 0,
            max__risk_reward : 5,            
        }
    },
    computed : {
        drawer : {
            get(){
                return this.$store.getters.drawer
            },
            set(value){
                this.$store.commit("update_drawer", value);
            }
        },
        
        filter : {
            get(){
                return this.$store.getters.filter
            },
            set(filter){
                let db_fetch = false
                // console.log("Changes filter value ", filter, db_fetch)
                this.$store.commit("update_filter", {filter, db_fetch});
                this.apply_filters()
                
            }
        },
        ticker_options () {            
                return this.$store.getters.tickers
        },
        ticker_values:{
            get(){                
                return (this.filter.tickers || this.ticker_options).filter(v=>v)
            },
            set(value){
                // console.log("ticks valuess :", this.filter.tickers, value);
                let filter = {"tickers" : value,}
                Vue.set(this, 'filter', filter)
            }
        },
        side_values:{
            get(){
                // console.log("values copmputed: ", this.filter, Object.keys(this.filter) ,this.filter.sides, this.$store.getters.filter.sides)
                return this.filter.sides || ["SELL", "BUY"]
            },
            set(value){
                // console.log("value : ", value);
                let filter = {"sides" : value}
                Vue.set(this, 'filter', filter)
            }
        },
        pp_range:{
            get(){
                return this.filter.profit_percentage || [0, 50]
            },
            set(value){
                let filter = {"profit_percentage" : value}
                Vue.set(this, 'filter', filter)
            }
        },
        rr_range:{
            get(){
                return this.filter.risk_reward || [0, 5]
            },
            set(value){
                let filter = {"risk_reward" : value}
                Vue.set(this, 'filter', filter)
            }
        },
    },
    methods : {                
        forceRerender : function() {            
            this.tablekey += 1        
        },        
        update_selected_tickers(sel_tickers){            
            this.ticker_values = sel_tickers
        },
        async clear_filter(){
            await axios.post("/worker/clear-filter2/", {portfolio_id : STATE.portfolio})
            this.$store.dispatch("clear_filter")
        },
        apply_filters(){
            this.$store.dispatch('update_filter', FILTER)
            return _.debounce(async function(){
                await axios.post("/worker/apply-filters2/", {portfolio_id : STATE.portfolio, type : STATE.type, ...FILTER})
            }, 10000)
        },
        select (option) {
            option.selected = !option.selected
        },
        ticker_name(option){
            return option.name
        },
        side_name(option){
            return option.side
        },
        is_mobile(){
            return helpers.is_mobile()
        },
        show_drawer(){
            console.log("drawer show : ", this.drawer);
            this.drawer = true
        },
    },
    watch : {
        drawer() {
            console.log("drawer changed :  ", this.drawer);
        }
    },
    template : helpers.is_mobile() ? M_DRAWER_FILTER : M_FILTER_SIDEBAR,
    // components: { 'm-data-table': MDataTable, 'm-data-table-info' : MDataTableInfo}
})

const MApp = Vue.component('m-app', {   
    props : ['state', 'items', 'fields', 'headers'],
    data: () => {
        return {
            transProps: {
                // Transition name
                name: 'flip-list'
            },
            fields0 : "JUJ",
            drawer : false,
        }
    },
    created(){
        this.$store.dispatch("load_notifications")
    },
    computed : {
        type : {
            get(){
                return this.$store.state.state.type.toUpperCase()
            },
            set(value){
                var type = value.toLowerCase()
                console.log("radio toggle | value : ", value, ", type : ", type)
                this.$store.dispatch('change_state', {'type' : type})
            }
        },
        user (){
            return User
        },
        notifications (){
            var notis = this.$store.getters.notifications.data
            var displayers = []
            notis.forEach(v=>{
                var display = {}
                display.title = PORTFOLIOS[v.portfolio_id].toUpperCase() +  '- ' + " - " + v.ticker.toUpperCase() + " - " + v.signal
                display.subtitle = `<span class='text--primary'>${v.status.toUpperCase()}</span> &mdash; Price : ${v.price}, Target Price : ${v.target_price}, Stop Loss : ${v.stop_loss}`
                displayers.push(display)
            })
            return displayers
        },        
    },
    methods : {                
        notifications_ (){
            console.log(Notifications.data)
            return Notifications.data
        },
        forceRerender : function() {            
            this.tablekey += 1        
        },
        is_mobile(){
            return helpers.is_mobile()
        },            
        swipe(direction){
            console.log("swipe direction : ", direction);            
            if(direction=='right'){
                this.$store.commit("update_drawer", true)
            }
            if(direction=='left'){
                this.$store.commit("update_drawer", false)
            }
        },
        get_csrf_token(){
            return $("input[name='csrfmiddlewaretoken']").val()
    
        },
    },
    template : M_APP,
    components: { 'm-data-table': MDataTable, 'm-data-table-info' : MDataTableInfo}
})