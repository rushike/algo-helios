
class Tick{
    constructor(instrument_id = 129, tick = 12){
        this.instrument_id = instrument_id
        this.tick = tick
    }
    update(tick){
        this.tick = tick
        return this
    }
    toString(){
        return this.tick
    }
}

class Profit{
    constructor(instrument_id = 129, tick = 12, target_price, price){
        this.instrument_id = instrument_id
        this.tick = tick
        this.target_price = target_price
        this.price = price
    }
    update(tick, target_price, price){
        this.tick = tick
        this.target_price = target_price
        this.price = price
        return this
    }
    toString(){        
        return ((this.tick - this.target_price) / this.price).toFixed(2)
    }
}

class Signal{
    constructor(call_id, ticker, ltp, signal, time, price, target_price, stop_loss, status){        
        this.init(call_id, ticker, ltp, signal, time, price, target_price, stop_loss,  status)        
    }
    init(call_id, ticker, ltp, signal, time, price, target_price, stop_loss, status){
        var self = this
        this.call_id = call_id
        this.ticker = ticker
        this.ltp = ltp
        this.signal = signal
        this.time = time
        this.price = price
        this.target_price = target_price
        this.stop_loss = stop_loss
        this.profit = {
                    toString(){
                        return (Math.abs(self.ltp - self.target_price) / self.price).toFixed(2)
                    }
                }
        this.status = status
        this.isActive = true
    }
    update(signal, status){
        if(signal) this.signal = signal
        if(status) this.status = status
    }
}

class Data{
    constructor(){
        this.data = Table;
        this.fields = []
        this.items = []
        this.instruments = {}
        this.calls = {}
        
    }
    
    update_tick(instrument_id, ltp){
        if(this.instruments[instrument_id] && this.instruments[instrument_id].ltp) {
            this.instruments[instrument_id].ltp.update(ltp)
        }else if(!this.instruments[instrument_id]) this.instruments[instrument_id] = {}
        this.instruments[instrument_id].ltp = new Tick(instrument_id, ltp)
        return this.instruments[instrument_id].ltp
    }

    /**
     * dicts in data are in format specified from calls format in janus
     * @param {String} portfolio_id intraday, btst, positional, longterm
     * @param {String} nature equity, options
     * @param {Array} data list of calls dictionaries
     */
    load_calls(portfolio_id, type, data, mercury){
        // console.log("params :  portfolios_id : ", portfolio_id, ", type : ", type, ", data : ", data)
        var data_list = this.data[STATE.market_type][STATE.market][STATE.type][portfolio_id].data
        var head = this.data[STATE.market_type][STATE.market][STATE.type].header;
        data_list.length = 0

        data.forEach(value=>{
            if(!this.calls[value["call_id"]]){
                this.calls[value["call_id"]] = new Signal(
                    value["call_id"],
                    value["ticker"],
                    value["ltp"],
                    value["signal"],
                    value["time"],
                    value["price"],
                    value["target_price"],
                    value["stop_loss"],                    
                    value["status"]
                )
            }else {
                this.calls[value["call_id"]].update(
                    value["signal"],
                    value["status"]
                )
            }
            data_list.push(this.calls[value["call_id"]])
        })        
        // Vue.set(mercury.vue_mercury.$refs.stocktable, "items", data_list)
        Vue.set(mercury.vue_mercury, "items", data_list)
        // Vue.set(store, "items", data_list)

        // store.dispatch("refresh_table", data_list)
        // mercury.vue_mercury.refresh_table(data_list)        
    }
}

class MercuryTable{
    constructor(props = {id : "test"}){
        this.id = props.id;
        this.data = new Data();
        this.state = STATE    
    }

    get_portfolio(portfolio_id){    
        if(typeof portfolio_id == Number){
            return PORTFOLIOS[portfolio_id]
        }else if(typeof portfolio_id == String){
            if (PORTFOLIOS.includes(portfolio_id.lower())) return portfolio_id.lower()
        }
    }
    
    get_table_header(){
        var head = this.data.data.indian_market.equity[this.state.type].header
        console.log(head, this.data.data)        
        var head_list = []//this.data.fields
        Object.entries(head).forEach(([key, value]) => {
            head_list.push(
                {
                    key : key,
                    label : KEY_2_LABEL[key],
                    sortable : value.sortable || false
                }
            )
        });        
        storex.fields = head_list
        return head_list
    }

    insert_option_call(portfolio_id){
        portfolio_id = this.get_portfolio(portfolio_id)
    }
    insert_equity_call(portfolio_id){
        portfolio_id = this.get_portfolio(portfolio_id)
    }
    reinit(){
        document.getElementById(this.id).innerHTML = `<m-table-wrapper ref="stocktable" :items = "items" :fields = "fields" :headers = "headers" :state = "state" >{{fields}}</m-table-wrapper>`
        // document.getElementById(this.id).innerHTML = M_STOCKTABLE_TEMPLATE_STRING
    }
    render(){
        this.reinit()
        this.get_table_header()
            
        this.vue_mercury = new Vue({ 
            el: `#${this.id}`,
            store,
            vuetify: new Vuetify(),
            data : {
                state : storex.state,
                // items: storex.items,
                // fields: storex.fields,             
            }, 
            
            created() {
                // var head_list = this.$store.getters.fields
                // this.$store.commit('update_fields', head_list)                
                this.$store.dispatch('load_filters')
                this.$store.dispatch('load_fields')
            },
            computed: {
                sortOptions() {
                  // Create an options list from our fields
                  return this.fields
                    .filter(f => f.sortable)
                    .map(f => {
                      return { text: f.label, value: f.key }
                    })
                },
                items : {
                    get(){
                        return this.$store.getters.items
                    },
                    set(items_){
                        this.$store.commit("update_items", items_);
                    }
                },
                fields : {
                    get(){
                        return this.$store.getters.fields
                    },
                    set(fields_){
                        return this.$store.commit("update_fields", fields_);
                    }
                },
                headers : {
                    get(){
                        return this.$store.getters.fields
                    },
                    set(fields_){
                        return this.$store.commit("update_fields", fields_);
                    }
                }
              },
              mounted() {
                // Set the initial number of items
                this.totalRows = this.items.length
              },
            methods : {
                  onFiltered(filteredItems) {
                    // Trigger pagination to update the number of buttons/pages due to filtering
                    this.totalRows = filteredItems.length
                    this.currentPage = 1
                  }
            }
        });
    }
}