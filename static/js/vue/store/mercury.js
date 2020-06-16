Vue.use(Vuex);

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
axios.defaults.xsrfCookieName = "csrftoken"

const store = new Vuex.Store({
    strict: true,
    state: {
        // table : Table,
        state : STATE,
        items : [],
        selected_fields : [],
        fields : [],        
        filter : FILTER,
        tickers : [],
        meta : META,
        search : null,
        instruments : {},
        calls : {},
        loaded : false,
        filter_loaded : false,
        mobile_settings_toggle : false,
        drawer : false
    },
    getters: {
        state : (state, getters)=>{
            return state.state
        },
        items : (state, getters) =>{
            return state.items
        },
        fields : (state, getters) =>{
            return state.fields
        },
        selected_fields : (state, getters)=>{
            return state.selected_fields
        },
        search : function(state, getters){
            return state.search
        },
        filter : function(state, getters){
            return state.filter
        },
        meta : function(state, getters){
            return state.meta
        },
        tickers : function(state, getters){
            return state.tickers
        },
        instruments : function(state, getters){
            return state.instruments
        },
        calls : function(state, getters){
            return state.calls
        },
        loaded : function(state, getters){
            return state.loaded
        },
        mobile_toggle : function(state, getters){
            return state.mobile_settings_toggle
        },        
        drawer : function(state, getters){
            return state.drawer
        },
    },
    mutations: {
        /**
         * Structure : payload
         * payload = {
         *      key : value
         * }
         * key   =: which key state to update
         * value =: corresponding value
         */
        change_state : (state, state_dict)=>{        
            Object.entries(state_dict).forEach(([key, value])=>{
                state.state[key] = value;
            });
        },
        /**
         * Structure : payload
         * payload = object
         * adds 'object' of type 'signal' in table particular list based on state
         */
        add_entry : (state, signal)=>{
            // console.log("Vuex$mutations#add_entry =: mercury state : ", mstate, ", payload : ", payload);
            let table = state.items
            Vue.set(table, table.length, signal)
        },
        /**
         * Structure : payload
         * payload = [
         *      objects,
         *      ...
         * ]
         * refreshes entire table with list of objects['signals']
         * used when loading calls from db
         */
        refresh_table : (state, {calls, force_init = false})=>{
            var data_list = {} // this.data[STATE.market_type][STATE.market][STATE.type][portfolio_id].data
            var head = Table[STATE.market_type][STATE.market][STATE.type].header;
            // data_list.length = 0
            var start = true            
            var key = null, val = 0, v = 0
            data_list[OPTIONS] = {}
            data_list[STOCKS] = {}
            calls.forEach(value=>{
                if(!state.calls[value["call_id"]] || force_init){                
                    if(!value["active"]){
                        key = value["call_id"]
                        state.instruments[key] = {
                            ltp : new Tick(value.instrument_token, value.ltp || -1)
                        }
                        v++
                    }else {
                        key = value["instrument_token"]
                        if(state.instruments[key] && state.instruments[key].ltp) {
                            state.instruments[key].ltp.update(value.ltp)
                        }else{
                            if(!state.instruments[key])state.instruments[key] = {}
                            state.instruments[key].ltp = new Tick(value.instrument_token, value.ltp || -1)
                        }
                        val++
                    }
                    
                    var ltp = state.instruments[key].ltp
                    
                    if(value.product_type == STOCKS_PROD){
                        state.calls[value["call_id"]] = new Signal(
                            value["call_id"],
                            value["ticker"],
                            ltp,
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
                    }else if(value.product_type == OPTIONS_PROD){
                        state.calls[value["call_id"]] = new OptionsSignal(
                            value["call_id"],
                            value["underlying"],
                            value['expiry'],
                            value["strike"],            
                            value["ticker"],            
                            ltp,
                            value['signal'],
                            value["signal_time"],
                            value["price"],
                            value["target_price"],
                            value["stop_loss"],                            
                            value['risk_reward'],
                            value['status'],
                            value['active'],                        
                        )
                    }
                }
                else {
                    state.calls[value["call_id"]].update(
                        value["signal"],
                        value["status"],
                        value['active']
                    )
                }
                                
                if(!data_list[TYPE[value.product_type]][value["portfolio_id"]]){                    
                    data_list[TYPE[value.product_type]][value["portfolio_id"]] = Table[STATE.market_type][STATE.market][TYPE[value.product_type]][PORTFOLIOS[value["portfolio_id"]]].data
                    data_list[TYPE[value.product_type]][value["portfolio_id"]].length = 0
                }                
                data_list[TYPE[value.product_type]][value["portfolio_id"]].push(state.calls[value["call_id"]])
            })   
            console.log("active L : ", val, ", non active : ", v);     
            // console.log("setting mercury item : ",data_list, data_list[STATE.portfolio], STATE.portfolio)    
            // Vue.set(state, "items", data)
        },
        add_signal(state, {signal, portfolio_id, empty}){
            var mstate = state.state
            state.calls[signal.call_id] = signal
            var data_list = Table[mstate.market_type][mstate.market][mstate.type][portfolio_id].data            
            if(empty){
                data_list.length = 0
            }
            data_list.push(signal)
            
        },
        update_signal(state, signal_update){
            console.log("signal_update : ", signal_update)
            state.calls[signal_update.call_id].update(signal_update)
        },
        update_items : (state, items)=>{
            Vue.set(state, "items", items)
        },
        update_fields : (state, fields)=>{
            Vue.set(state, "fields", fields)
        },
        update_selected_fields : (state, selected_fields)=>{
            Vue.set(state, 'selected_fields', selected_fields)
        },
        update_meta :(state, meta)=>{
            meta = META.set(meta)
            Vue.set(state, "meta", meta)
        },
        update_search(state, value){
            // console.log("Vuex$mutations#update_search =: search value : ", value)
            // state.search = value
            Vue.set(state, "search", value)
        },
        update_filter(state, {filter, db_fetch}){
            // console.log("Vuex$mutations#update_search =: filter : ", filter, db_fetch)
            filter = FILTER.set(filter, db_fetch)
            Vue.set(state, "filter", filter)
            Vue.set(state.filter, 'loaded', true)
        },
        clear_filter(state){
            state.filter.init()
        },
        update_tickers(state, tickers){
            // console.log("Vuex$mutations#update_search =: filter : ", filter, db_fetch)
            Vue.set(state, "tickers", tickers)
        }, 
        update_loaded(state, value){
            Vue.set(state, "loaded", value)
        },
        update_instrument(state, {key, ltp, active, call_id}){
            // console.log("update instrument : ", key, ltp, active, call_id)
            if(!active){
                state.instruments[key] = {ltp : new Tick(key, ltp)}
            }
            else if(state.instruments[key] && state.instruments[key].ltp) {
                state.instruments[key].ltp.update(ltp)
            }else {
                if(!state.instruments[key]) {
                    state.instruments[key] = {}        
                }
                state.instruments[key].ltp = new Tick(key, ltp)
            } 
            return state.instruments[key].ltp
        },
        update_drawer(state, value){
            state.drawer = value
        },
        mobile_toggle(state){
            state.mobile_settings_toggle = !state.mobile_settings_toggle
        },
        do_from_store(state, {callback, params}){
            callback(state, params)
        }
    },
    actions: {
        async refresh_table(context, options){
            console.log("options : ", options)
            var {force = false, mercury = Mercury} = options
            var portfolios = force ? PORTFOLIOS.slice(2) : [context.getters.state.portfolio]
            var req_data = {portfolio_id : portfolios}
            console.log("portfolios refreshing data : ", portfolios);            
            var data_ = (await axios.post('/worker/calls-from-db2/', req_data)).data
            console.log("portfolios data : ", data_)
            context.commit('refresh_table', {calls : data_.calls, force_init : true})
            if(force){
                context.commit('update_loaded', true)
            }
            context.dispatch('change_state', {portfolio : context.getters.state.portfolio})
        },
        load_fields(context){
            // context.getters.fields
            let mstate = context.getters.state
            var head = Table[mstate.market_type][mstate.market][mstate.type].header
            var head_list = []                    
            Object.entries(head).forEach(([key, value]) => {
                head_list.push(
                    {
                        key : key,
                        value : key,
                        text : KEY_2_LABEL[key],                        
                        label : KEY_2_LABEL[key],
                        sortable : value.sortable || false,                        
                    }
                )
            });
            head_list.push({
                key : 'action', 
                value : 'action', 
                text : 'Action',
                label : 'Action',
                sortable : false,
            })
            context.commit('update_fields', head_list)
            context.commit('update_selected_fields', head_list)
        },
        load_meta(context){
            let mstate = context.getters.state
            var items = Table[mstate.market_type][mstate.market][mstate.type][mstate.portfolio].data
            var meta_ = items.reduce((meta, item) => {
                // console.log(meta, item)
                const {total = 0, partial_hit = 0, hit = 0, miss = 0} = meta;
                // if(TYPE[item.product_type] == OPTIONS) return {...meta, total: total + 1}
                if (item.status.toLowerCase() === 'partialhit') {
                    return {...meta, total: total + 1, partial_hit : partial_hit + 1};
                }else if (item.status.toLowerCase() === 'hit') {
                    return {...meta, total: total + 1, hit : hit + 1};
                }else if (item.status.toLowerCase() === 'miss') {
                    return {...meta, total: total + 1, miss : miss + 1};
                }return {...meta, total: total + 1}
            }, {});
            context.commit('update_meta', meta_)
        },
        load_items(context){
            let mstate = context.getters.state
            var items = Table[mstate.market_type][mstate.market][mstate.type][mstate.portfolio].data
            console.log("items for ", mstate.type, " i : ", items);
            
            context.commit('update_items', items)        
        },
        async load_all_tickers(context){ // this loads all filter for only particular market type
            let mstate = context.getters.state
            let table = Table[mstate.market_type][mstate.market][mstate.type]
            var response =  await axios.post('/worker/get-instruments-for-portfolios/', {})
            Object.entries(response.data).forEach(([key, value])=>{
                console.log(table[PORTFOLIOS[key]].tickers, PORTFOLIOS[key], key)
                table[PORTFOLIOS[key]]["tickers"] = value
            });
            context.dispatch('load_tickers')
        },
        load_tickers(context){
            let mstate = context.getters.state,
             db_fetch = true
            console.log("port : ",mstate, mstate.portfolio)
            let tickers = Table[mstate.market_type][mstate.market][mstate.type][mstate.portfolio].tickers
            // tickers = tickers.map(v=>{return {name : v}})
            context.commit('update_tickers', tickers)
        },
        async load_filters(context){ // this loads all filter for only particular market type
            let mstate = context.getters.state
            let table = Table[mstate.market_type][mstate.market][mstate.type]
            var response =  await axios.post('/worker/get-filters/', {})            
            // console.log("filters : ", response.data)
            Object.entries(response.data).forEach(([key, value])=>{
                table[key].filter.set(value, true)
            });            
            context.dispatch('propogate_state_change')
            // context.dispatch('load_filter')
        },
        load_filter(context){
            let mstate = context.getters.state,
             db_fetch = true            
            let filter = Table[mstate.market_type][mstate.market][mstate.type][mstate.portfolio].filter
            console.log("filter should change : ", filter)
            context.commit('update_filter', {filter, db_fetch})
        },
        clear_filter(context){
            context.commit("clear_filter")
        },
        change_state : (context, state_dict)=>{
            // console.log("Vuex$action#change_state =: context ", ", state_dict : ", state_dict)
            context.commit("change_state", state_dict);
            context.dispatch('propogate_state_change')
        },
        propogate_state_change(context){
            context.dispatch('load_filter')
            context.dispatch('load_fields')
            context.dispatch('load_items')
            context.dispatch('load_meta')
        },
        update_filter(context, filter_){
            let mstate = context.getters.state;
            let filter = Table[mstate.market_type][mstate.market][mstate.type][mstate.portfolio].filter;
            filter.set(filter_);
        },
        update_selected_fields(context, selected_fields){
            var selected_fields_ = []
            console.log("sellll : ", selected_fields);
            
            context.getters.fields.forEach(field =>{   
                console.log('e : ', field.text, field.key, selected_fields.some(e => e == field.text || e == field.key) , field.key == 'action')
                if(selected_fields.some(e => e == field.text || e == field.key) || field.key == 'action' ){
                    selected_fields_.push(field)
                }
            })
            console.log("selected fields : ", selected_fields, selected_fields_, context.getters.fields);
            context.commit('update_selected_fields', selected_fields_)
        },
        update_items(context, items){
            context.commit('update_items', items)
        },
        update_instrument(context, options){
            // options = {instrument_id, ltp, active, call_id}
            // console.log("options : ", options);
            
            var {key = null, ltp = null, active = true, call_id = null} = options
            key = options.instrument_id
            context.commit('update_instrument', {key, ltp, active, call_id})
        },
        insert_equity_call(context, data){
            var portfolio_id = PORTFOLIOS[data.portfolio_id || 2]
            // console.log("m data : ", this.data, ", m data data : ", this.data.data, portfolio_id);
            // console.log("signal data : ", data);
            // var ltp = this.data.update_tick(data.instrument_id, data.ltp || -1)
            var key = data.active ? data.instrument_id : data.call_id, ltp = data.ltp || -1;
            // console.log("instrument id : ", key, ", ltp : ", ltp)
            context.commit('update_instrument', {key, ltp})            
            // console.log("instrument id : ", key, ", ltp : ", ltp)
            var signal = new Signal(
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
            var empty = data.empty
            context.commit('add_signal', {signal, portfolio_id, empty})
        },
        update_equity_call(context, signal_update){
            context.commit("update_signal", signal_update)
        },
    }
});

const storex =  {
    table : Table,
    state : STATE,
    fields : [],
    items : []
}