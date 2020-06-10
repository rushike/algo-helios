Vue.use(MultiFiltersPlugin)

class Data{
    constructor(){
        this.data = Table;
        this.fields = []
        this.items = []
        this.instruments = {}
        this.calls = {}
        
    }
    
    update_tick(instrument_id, ltp){
        // console.log("instrument id : ", instrument_id, ", ltp : ", ltp);
        
        if(this.instruments[instrument_id] && this.instruments[instrument_id].ltp) {
            this.instruments[instrument_id].ltp.update(ltp)
        }else if(!this.instruments[instrument_id]) {
            this.instruments[instrument_id] = {
                ltp : new Tick(instrument_id, ltp)
            }        
        }else if (!this.instruments[instrument_id].ltp){
            this.instruments[instrument_id].ltp = new Tick(instrument_id, ltp)
        }        
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
        var data_list = {}// this.data[STATE.market_type][STATE.market][STATE.type][portfolio_id].data
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
                    value["status"],
                    value['risk_reward'],
                    value['active'],
                    value["signal_time"],
                )
            }else {
                this.calls[value["call_id"]].update(
                    value["signal"],
                    value["status"],
                    value['active']
                )
            }
            
            if(!data_list[value["portfolio_id"]]){
                data_list[value["portfolio_id"]] = this.data[STATE.market_type][STATE.market][STATE.type][PORTFOLIOS[value["portfolio_id"]]].data
                data_list[value["portfolio_id"]].length = 0
            }
            data_list[value["portfolio_id"]].push(this.calls[value["call_id"]])
        })        
        console.log("setting mercury item : ", data_list[STATE.portfolio], STATE.portfolio)
         
    }
}

class MercuryTable{
    constructor(props = {id : "test"}){
        this.id = props.id;
        this.data = new Data();
        this.state = STATE    
    }

    get_portfolio(portfolio_id){        
        if(Number.isInteger(portfolio_id)){
            return PORTFOLIOS[portfolio_id]
        }else if(typeof portfolio_id == String){
            if (PORTFOLIOS.includes(portfolio_id.lower())) 
                return portfolio_id.lower()
            return 'intraday_'
        }
    }
    
    get_table_header(){
        var head = this.data.data.indian_market.equity[this.state.type].header
        // console.log(head, this.data.data)
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
    insert_equity_call(data = {}){
        var data_list = {};
        var portfolio_id = this.get_portfolio(data.portfolio_id || 2)
        // console.log("m data : ", this.data, ", m data data : ", this.data.data, portfolio_id);
        console.log("signal data : ", data);

        var ltp = this.data.update_tick(data.instrument_id, data.ltp || -1)

        this.data.calls[data.call_id] = new Signal(
                                                    data.call_id,
                                                    data.ticker,
                                                    ltp,
                                                    data.signal,
                                                    data.time,
                                                    data.price,
                                                    data.target_price,
                                                    data.stop_loss,
                                                    data.status,
                                                    data.risk_reward,
                                                    data.active,
                                                    data.signal_time,
                                                )
        var signal = this.data.calls[data.call_id], empty = data.empty
        store.commit('add_signal', {signal, portfolio_id, empty})
    }
    update_equity_signal(data = {}){
        if(this.data.calls[data.call_id]){
            this.data.calls[data.call_id].update(data.signal, data.status, data.active)
        }
    }
    update_tick(tick_data){
        this.data.update_tick(tick_data['instrument_token'], tick_data['last_price']);
    }
    reinit(){
        document.getElementById(this.id).innerHTML = `<m-app ref="stocktable" :items = "items" :fields = "fields" :headers = "headers" :state = "state" >{{fields}}</m-app>`
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
                var force = true, data = Mercury.data
                this.$store.dispatch('refresh_table', {force, data})
                this.$store.dispatch('load_filters')                
                this.$store.dispatch('load_fields')
                this.$store.dispatch('load_all_tickers')
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
                        return this.$store.getters.selected_fields
                    },
                    set(fields_){
                        return this.$store.commit("update_selected_fields", fields_);
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
                  },
            }
        });
    }
}