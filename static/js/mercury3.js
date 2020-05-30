
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
        // if(profit) this.profit = profit
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
        var data_list = [] //this.data[STATE.market_type][STATE.market][STATE.type][portfolio_id].data,
        var head = this.data[STATE.market_type][STATE.market][STATE.type].header;
        // data_list.length = 0

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
        // Vue.set(mercury.vue_mercury.$refs.b_table, "items", data_list)
        // store.dispatch("refresh_table", data_list)
        // mercury.vue_mercury.refresh_table(data_list)        
    }
}

class MercuryTable{
    constructor(props = {id : "test"}){
        this.id = props.id;
        this.data = new Data();
        this.nature = STOCKS;
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
        // Vue.set(vm.items[2], 'b' , 2)
        // head_list.length = 0
        Object.entries(head).forEach(([key, value]) => {
            head_list.push(
                {
                    key : key,
                    label : KEY_2_LABEL[key],
                    sortable : value.sortable || false
                }
            )
        });
        head_list.push({
            key: 'isActive',
            label: 'is Active',
            formatter: (value, key, item) => {
              return value ? 'Yes' : 'No'
            },
            sortable: true,
            sortByFormatted: true,
            filterByFormatted: true
          },)
        // this.vue_mercury.update_fields(data_list)
        // store.dispatch("update_fields", head_list)
        // Vue.set(mercury.vue_mercury.$refs.b_table, "fields", head_list)
        store.fields = head_list
        return head_list
    }

    insert_option_call(portfolio_id){
        portfolio_id = this.get_portfolio(portfolio_id)
    }
    insert_equity_call(portfolio_id){
        portfolio_id = this.get_portfolio(portfolio_id)
    }
    reinit(){
        // document.getElementById(this.id).innerHTML = `<m-data-table ref="stocktable" :items = "items" :fields = "fields" :state = "state" >{{fields}}</m-data-table>`
        document.getElementById(this.id).innerHTML = M_STOCKTABLE_TEMPLATE_STRING
    }
    render(){
        // this.reinit()
        // this.get_table_header()
            
        // this.vue_mercury = new Vue({ 
        //     el: `#${this.id}`,
        //     store,
        //     // props : ["state", "items", "fields"],
        //     data : {
        //         fields0 : "JUJ",
        //         transProps: {
        //             // Transition name
        //             name: 'flip-list'
        //         },
        //         state : store.state,
        //         items: store.items,
        //         fields: store.fields,
        //         filter: null,
        //         filterOn: [],
        //     }, 
        //     methods : {
        //         onFiltered : function(filteredItems) {
                
        //             console.log("filterd call : ", filteredItems, this.filter)
        //             // Trigger pagination to update the number of buttons/pages due to filtering
        //             // this.totalRows = filteredItems.length
        //             // this.currentPage = 1
        //         }
        //     }           
        //     // components: { 'm-data-table': MDataTable}
        // });

        new Vue({
            el : `#${this.id}`,
            data() {
                return {
                  items: [
                    { isActive: true, age: 40, name: { first: 'Dickerson', last: 'Macdonald' } },
                    { isActive: false, age: 21, name: { first: 'Larsen', last: 'Shaw' } },
                    {
                      isActive: false,
                      age: 9,
                      name: { first: 'Mini', last: 'Navarro' },
                      _rowVariant: 'success'
                    },
                    { isActive: false, age: 89, name: { first: 'Geneva', last: 'Wilson' } },
                    { isActive: true, age: 38, name: { first: 'Jami', last: 'Carney' } },
                    { isActive: false, age: 27, name: { first: 'Essie', last: 'Dunlap' } },
                    { isActive: true, age: 40, name: { first: 'Thor', last: 'Macdonald' } },
                    {
                      isActive: true,
                      age: 87,
                      name: { first: 'Larsen', last: 'Shaw' },
                      _cellVariants: { age: 'danger', isActive: 'warning' }
                    },
                    { isActive: false, age: 26, name: { first: 'Mitzi', last: 'Navarro' } },
                    { isActive: false, age: 22, name: { first: 'Genevieve', last: 'Wilson' } },
                    { isActive: true, age: 38, name: { first: 'John', last: 'Carney' } },
                    { isActive: false, age: 29, name: { first: 'Dick', last: 'Dunlap' } }
                  ],
                  fields: [
                    { key: 'name', label: 'Person Full name', sortable: true, sortDirection: 'desc' },
                    { key: 'age', label: 'Person age', sortable: true, class: 'text-center' },
                    {
                      key: 'isActive',
                      label: 'is Active',
                      formatter: (value, key, item) => {
                        return value ? 'Yes' : 'No'
                      },
                      sortable: true,
                      sortByFormatted: true,
                      filterByFormatted: true
                    },
                    { key: 'actions', label: 'Actions' }
                  ],
                  totalRows: 1,
                  currentPage: 1,
                  perPage: 5,
                  pageOptions: [5, 10, 15],
                  sortBy: '',
                  sortDesc: false,
                  sortDirection: 'asc',
                  filter: null,
                  filterOn: [],
                  infoModal: {
                    id: 'info-modal',
                    title: '',
                    content: ''
                  }
                }
              },
                   
              methods: {
                info(item, index, button) {
                  this.infoModal.title = `Row index: ${index}`
                  this.infoModal.content = JSON.stringify(item, null, 2)
                  this.$root.$emit('bv::show::modal', this.infoModal.id, button)
                },
                resetInfoModal() {
                  this.infoModal.title = ''
                  this.infoModal.content = ''
                },
                onFiltered(filteredItems) {
                  // Trigger pagination to update the number of buttons/pages due to filtering
                  this.totalRows = filteredItems.length
                  this.currentPage = 1
                }
              }
            }
        )
    }   
}
