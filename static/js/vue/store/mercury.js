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
        instruments : [],
        meta : META,
        search : null,
        loaded : false,
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
        instruments : function(state, getters){
            return state.instruments
        },
        loaded : function(state, getters){
            return state.loaded
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
        refresh_table : (state, {calls, mercury})=>{
            var data_list = {} // this.data[STATE.market_type][STATE.market][STATE.type][portfolio_id].data
            var head = mercury.data.data[STATE.market_type][STATE.market][STATE.type].header;
            // data_list.length = 0
            var start = true
            calls.forEach(value=>{
                if(!mercury.data.calls[value["call_id"]]){
                    // mercury.insert_equity_call({
                    //     call_id : value["call_id"],
                    //     ticker : value["ticker"],
                    //     ltp : value["ltp"],
                    //     signal : value["signal"],
                    //     time : value["time"],
                    //     price : value["price"],
                    //     target_price : value["target_price"],
                    //     stop_loss : value["stop_loss"],
                    //     status : value["status"],
                    //     risk_reward : value["risk_reward"],
                    //     active : value["active"],
                    //     signal_time : value["signal_time"],
                    //     portfolios : value["portfolio_id"],
                    //     instrument_id : value["instrument_token"],
                    //     empty : start,
                    // })
                    // start = false
                    var ltp = mercury.data.update_tick(value.instrument_token, value.ltp || -1)
                    mercury.data.calls[value["call_id"]] = new Signal(
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
                }
                else {
                    data.calls[value["call_id"]].update(
                        value["signal"],
                        value["status"],
                        value['active']
                    )
                }
                
                if(!data_list[value["portfolio_id"]]){
                    data_list[value["portfolio_id"]] = mercury.data.data[STATE.market_type][STATE.market][STATE.type][PORTFOLIOS[value["portfolio_id"]]].data
                    data_list[value["portfolio_id"]].length = 0
                }
                data_list[value["portfolio_id"]].push(mercury.data.calls[value["call_id"]])
            })        
            // console.log("setting mercury item : ",data_list, data_list[STATE.portfolio], STATE.portfolio)    
            // Vue.set(state, "items", data)
        },
        add_signal(state, {signal, portfolio_id, empty}){
            var mstate = state.state
            var data_list = Table[mstate.market_type][mstate.market][mstate.type][portfolio_id].data
            console.log("dsta list : ", data_list);
            if(empty){
                data_list.length = 0
            }
            data_list.push(signal)
            console.log("dsta list : ", data_list);
            
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
        },
        update_instruments(state, instruments){
            // console.log("Vuex$mutations#update_search =: filter : ", filter, db_fetch)
            Vue.set(state, "instruments", instruments)
        }, 
        update_loaded(state, value){
            Vue.set(state, "loaded", value)
        }
    },
    actions: {
        async refresh_table(context, options){
            console.log("options : ", options)
            var {force = false, mercury = Mercury} = options
            var portfolios = force ? PORTFOLIOS.slice(2) : [context.getters.state.portfolio]
            var req_data = {portfolio_id : portfolios}
            console.log("portfolios refreshing data : ", portfolios);            
            var data_ = (await axios.post('/worker/calls-from-db/', req_data)).data
            console.log("portfolios data : ", data_)
            context.commit('refresh_table', {calls : data_.calls, mercury : mercury})
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
                text : 'Follow',
                label : 'Follow',
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
            context.commit('update_items', items)        
        },
        async load_all_instruments(context){ // this loads all filter for only particular market type
            let mstate = context.getters.state
            let table = Table[mstate.market_type][mstate.market][mstate.type]
            var response =  await axios.post('/worker/get-instruments-for-portfolios/', {})
            Object.entries(response.data).forEach(([key, value])=>{
                console.log(table[PORTFOLIOS[key]].tickers, PORTFOLIOS[key], key)
                table[PORTFOLIOS[key]]["tickers"] = value
            });
            context.dispatch('load_instruments')
        },
        load_instruments(context){
            let mstate = context.getters.state,
             db_fetch = true
            console.log("port : ",mstate, mstate.portfolio)
            let instruments = Table[mstate.market_type][mstate.market][mstate.type][mstate.portfolio].tickers
            // instruments = instruments.map(v=>{return {name : v}})
            context.commit('update_instruments', instruments)
        },
        async load_filters(context){ // this loads all filter for only particular market type
            let mstate = context.getters.state
            let table = Table[mstate.market_type][mstate.market][mstate.type]
            var response =  await axios.post('/worker/get-filters/', {})            
            // console.log("filters : ", response.data)
            Object.entries(response.data).forEach(([key, value])=>{
                table[key].filter = value
            });
            context.dispatch('load_filter')
        },
        load_filter(context){
            let mstate = context.getters.state,
             db_fetch = true            
            let filter = Table[mstate.market_type][mstate.market][mstate.type][mstate.portfolio].filter
            console.log("filter should change : ", filter)
            context.commit('update_filter', {filter, db_fetch})
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
        update_selected_fields(context, selected_fields){
            var selected_fields_ = []
            context.getters.fields.forEach(field =>{                
                if(selected_fields.some(e => e.key == field.key)){
                    selected_fields_.push(field)
                }
            })
            context.commit('update_selected_fields', selected_fields_)
        },
        update_items(context, items){
            context.commit('update_items', items)
        }
    }
});

const storex =  {
    table : Table,
    state : STATE,
    fields : [],
    items : []
}