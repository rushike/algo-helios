

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
                this.$store.commit("update_search", value);
            }
        }
    },
    methods : {                
        forceRerender : function() {            
            this.tablekey += 1        
        },  
        onFiltered : function(filteredItems) {            
            this.totalRows = filteredItems.length            
        }, 
        portfolio_filter(items, filters, filter, headers){
            // console.log("this.$MultiFilters : ", this.$MultiFilters)
            const cf = new this.$MultiFilters(items, filters, filter, headers);

            // cf.registerFilter('search', function (searchWord, items) {
            //     if (searchWord.trim() === '') return items;
      
            //     return items.filter(item => {
            //       return item.name.toLowerCase().includes(searchWord.toLowerCase());
            //     }, searchWord);
      
            // });

            cf.registerFilter('tickers_search', function (tickers, items) {                
                    // if (added_by.trim() === '') return items;        
                    return items.filter(item => {
                        return tickers.map(value=>value.toLowerCase()).includes(item.ticker.toLowerCase())
                    }, tickers);            
            });

            cf.registerFilter('side_search', function (sides, items) {
                // if (added_by.trim() === '') return items;
                return items.filter(item => {
                    return sides.map(value=>value.toLowerCase()).includes(item.ticker.toLowerCase())
                }, sides);
            });
        }
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
        }
       
    },
    methods : {                
        forceRerender : function() {            
            this.tablekey += 1        
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
            side_values: [],
            ticker_values : [],
            options: [
                {	language: 'JavaScript', library: 'Vue.js' },
                { language: 'JavaScript', library: 'Vue-Multiselect' },
                { language: 'JavaScript', library: 'React' },
                { language: 'JavaScript', library: 'Go' },
                { language: 'JavaScript', library: 'PHP' }
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
            set(value){
                this.$store.commit("update_filter", value);
            }
        },
        ticker_options : {
            get(){
                let ticker = []
                (this.filter.tickers || []).forEach(value=>{
                    ticker.push({
                        name : value
                    })
                });
                return ticker
            },
            set(value){
                // console.log("Filter set value : ", value)
            }
        },
        // sides_options(){            
        //     return this.filter.sides
        // },
        pp_range(){
            return this.filter.profit_percentage
        },
        rr_range(){
            return this.filter.risk_reward
        }
    },
    methods : {
        select (option) {
            option.selected = !option.selected
        },
        ticker_name(option){
            return option.library
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