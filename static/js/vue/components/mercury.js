

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
            fields0 : "JUJ",
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
                if(Array.isArray(this.filter.profit_percentage) && 
                            this.filter.profit_percentage.length == 2 && 
                            !( this.filter.profit_percentage[0] < d.profit * 100 && 
                            this.filter.profit_percentage[1] > d.profit * 100 ))
                    return false
                else if(Array.isArray(this.filter.sides) && this.filter.sides.length != 0 && !this.filter.sides.map(v=>v.toLowerCase()).includes(d.signal.toLowerCase()))
                    return false

                else if(Array.isArray(this.filter.tickers) && 
                        this.filter.tickers.length != 0 && 
                        !this.filter.tickers.map(v=>v.toLowerCase()).includes(d.ticker.toLowerCase()))
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
        row_class(group, index, item, items){
            var class_ = "hover-pointer "
            var border = group ? "mx-1 follow_trade border " : ' ',
                active = item.active ? ' ' : 'disabled ',
                group_highlight = (index == items.length - 1) ? ( index == 0 ? '' : 'border-top-0'  ) : (index == 0 ? 'border-bottom-0' : 'border-top-0 border-bottom-0' )
            return class_ + border + active + group_highlight
             
        },
        follow_my_trade(item, follow){            
            item.set_follow(follow)
        },
        portfolio_filter(val, search, item, headers){
            if(search.length < 3 ){
                return true
            }
            
            if(val.toString().toLowerCase().includes(search.toLowerCase())){     
                console.log("this.filter : ", this.filter)           
                return true
            }

            return false
        },
        
        filter_on_search(val) {
            this.filter = this.$MultiFilters.updateFilters(this.filter, {search: val});
        },
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
                var selected_fields_ = []
                selected_fields.forEach(v=>{
                    var el = this.$store.getters.fields.find(element => element.key == v);
                    selected_fields_.push(el)
                });
                this.$store.dispatch("update_selected_fields", selected_fields_)
            }
        }
    },
    methods : {                
        forceRerender : function() {            
            this.tablekey += 1        
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
        async allow_notification(){
            var data =  (await axios.post('/user/toggle-notification/', {})).data
            this.notification = data['allow_notification']
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
    props : ['items', 'search', 'height'],
    data : ()=>{
        return {
            selected : [],
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
        },
        item_selected(item, value){
            // console.log("item, value : ", this.selected)
        }
    },
    watch : {
        selected(){
            this.$emit('change', this.selected.map(v=>v.name))
        }
    },
    template : M_MULTISELECT
})

const MFiterSidebar = Vue.component('m-filter-sidebar', {
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
            drawer : true,
        }
    },
    computed : {
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
                // console.log("values copmputed: ", this.filter.tickers)
                return this.filter.tickers || []
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
        apply_filters : _.debounce(async function(){
                await axios.post("/worker/apply-filters2/", {portfolio_id : STATE.portfolio, ...FILTER})
            }, 10000),
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
    template : M_FILTER_SIDEBAR,
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
        }
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
        }
    },
    methods : {                
        forceRerender : function() {            
            this.tablekey += 1        
        },  
    },
    template : M_APP,
    components: { 'm-data-table': MDataTable, 'm-data-table-info' : MDataTableInfo}
})