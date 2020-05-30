

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
                else if(Array.isArray(this.filter.sides) && this.filter.sides.length != 0 && !this.filter.sides.map(v=>v.side.toLowerCase()).includes(d.signal.toLowerCase()))
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
        }
    },
    methods : {                
        forceRerender : function() {            
            this.tablekey += 1        
        },  
        onFiltered : function(filteredItems) {            
            this.totalRows = filteredItems.length
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


            // Its time to run all created filters.
            // Will be executed in the order thay were defined.
            
        },
        
        filter_on_search(val) {
            this.filter = this.$MultiFilters.updateFilters(this.filter, {search: val});
        },
    },
    template : M_STOCKTABLE_TEMPLATE_STRING,
});


/**
 * Stock Table
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
            lsearch : this.filter
        }
    },
    computed : {
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
        ])
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
            options: [
                {	language: 'JavaScript', name: 'Vue.js' },
                { language: 'JavaScript', name: 'Vue-Multiselect' },
                { language: 'JavaScript', name: 'React' },
                { language: 'JavaScript', name: 'Go' },
                { language: 'JavaScript', name: 'PHP' }
            ],
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
                // console.log("ticks valuess :", this.filter.tickers, value);
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
    methods : {                
        forceRerender : function() {            
            this.tablekey += 1        
        },  
    },
    template : M_APP,
    components: { 'm-data-table': MDataTable, 'm-data-table-info' : MDataTableInfo}
})