Vue.use(Vuex);

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
axios.defaults.xsrfCookieName = "csrftoken"

const store = new Vuex.Store({
    strict: true,
    state: {
        // table : Table,
        state : STATE,
        items : [],
        fields : [],        
        filter : FILTER,
        instruments : [],
        meta : META,
        search : null,
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
        refresh_table : (state, data)=>{            
            Vue.set(state, "items", data)
        },
        update_items : (state, items)=>{
            Vue.set(state, "items", items)
        },
        update_fields : (state, fields)=>{
            Vue.set(state, "fields", fields)
        },
        update_meta :(state, meta)=>{
            console.log("meta setting : ", meta)
            meta = META.set(meta)
            console.log("after : ", meta)
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
        }
    },
    actions: {
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
                        sortable : value.sortable || false
                    }
                )
            });
            context.commit('update_fields', head_list)
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
            instruments = instruments.map(v=>{return {name : v}})
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
            // console.log("Vuex$action#change_state =: context ", context, ", state_dict : ", state_dict)
            context.commit("change_state", state_dict);
            context.dispatch('propogate_state_change')
        },
        propogate_state_change(context){
            context.dispatch('load_filter')
            context.dispatch('load_fields')
            context.dispatch('load_items')
            context.dispatch('load_meta')
        }
        // add_entry : (context, payload)=>{
        //     console.log("Vuex$action#add_entry =: context ", context, ", payload : ", payload)
        //     context.commit("add_entry", payload);
        // },
        // refresh_table : (context, payload)=>{
        //     console.log("Vuex$action#refresh_table =: context ", context, ", payload : ", payload)
        //     context.commit("refresh_table", payload);
        // },
        // update_fields : (context, payload)=>{
        //     console.log("Vuex$action#refresh_table =: context ", context, ", payload : ", payload)
        //     context.commit("update_fields", payload);
        // },
    }
});

const storex =  {
    table : Table,
    state : STATE,
    fields : [],
    items : []
}