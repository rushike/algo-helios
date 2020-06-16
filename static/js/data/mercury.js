const STOCKS = 'stocks';
const OPTIONS = 'options';

const OPTIONS_PROD = "OPT"
const STOCKS_PROD = "EQ"

const NIFTY_50 = 256265

const NIFTY_BANK = 260105

const PORTFOLIOS = ['', 'nifty50', 'intraday', 'btst', 'positional', 'longterm'];

const TYPE = {};
TYPE[OPTIONS_PROD] = OPTIONS; TYPE[STOCKS_PROD] = STOCKS;

const KEY_2_LABEL = {
    ticker : "Ticker",
    ltp : "LTP",
    signal : "Signal",
    time : "Signal Time",
    signal_time : "Signal Time",
    signal_price : "Signal Price",
    price : "Signal Price",
    target_price : "Target Price",
    stop_loss :  "Stop Loss",
    profit : "Profit %",
    status : "Status",  
    underlying : "Underlying",
    expiry : "Expiry",
    strike : "Strike",
    risk_reward : "Risk Reward",
}

const STATE = {
    portfolio : PORTFOLIOS[2],
    type : STOCKS,
    market : "equity",
    market_type : "indian_market",
    update : true,
}

const META = {
    init(){
        this.total = 0
        this.partial_hit = 0
        this.hit = 0
        this.miss = 0
    },
    set(meta){
        this.init()        
        Object.entries(meta).forEach(([key, value])=>{
            this[key] = value
        });return this
    },
    update(value){
        this[value.toLowerCase()] += 1
        return this
    }    
};META.init();

class Filter{
    constructor(){
        this.init()
    }
    init(){
        this.tickers = null,  // null or list of ticker names
        this.sides = null, // null or BUY / SELL
        this.profit_percentage = null, // null or float
        this.risk_reward = null, // null or float
        this.search = null
        this.loaded = false
    }
    set(props, db_fetch = false){
        // console.log("props : ", props, db_fetch)        
        if(!props) return this
        if(props.tickers) this.tickers = props.tickers
        if(props.sides){ 
            this.sides = props.sides
            if(db_fetch) { 
                this.sides = props.sides.map(v=>v.toUpperCase())
            }
        }
        if(props.profit_percentage) this.profit_percentage = props.profit_percentage
        if(props.risk_reward) this.risk_reward = props.risk_reward
        if(props.search) this.search = props.search
        return this
    }
}

const FILTER = new Filter()

/**
 * Structure : 
 * {
 *      markert_type : {
 *          market :{
 *              market_categories : {
 *                  header : {
 *                      ...
 *                  }
 *                  product : {
 *                      data : [],
 *                      filter : {}
 *                      instrument : []
 *                  }
 *              }
 *          }
 *      }
 * }
 */

const Table = {
    indian_market : {
        equity : {
            stocks : {
                header : {
                    ticker : {sortable :true},
                    ltp : {},
                    signal : {sortable :true},
                    time : {sortable :true},
                    price : {sortable :true},
                    target_price : {},
                    stop_loss : {},
                    profit : {sortable : true},
                    status : {sortable :true},
                },
                intraday : {
                    data : [], // this will store data that will display by Bootstrap - Vue table,
                    filter : new Filter(),
                    tickers : [],
                },
                btst : {
                    data : [], 
                    filter : new Filter(),
                    tickers : [],
                },
                positional :{
                    data : [],
                    filter : new Filter(),
                    tickers : [],
                },
                longterm : {
                    data : [],
                    filter : new Filter(),
                    tickers : [],
                }
            }, 
            options : {
                header : {
                    // underlying : {},
                    expiry : {},
                    strike : {},
                    ticker : {},
                    ltp : {},
                    signal : {},
                    time : {},
                    price : {},
                    target_price : {},
                    stop_loss : {},
                    profit : {},
                    risk_reward : {},
                    status : {}
                },
                intraday : {
                    data : [],
                    filter : new Filter(),
                    tickers : [],
                },
                btst : {
                    data : [],
                    filter : new Filter(),   
                    tickers : [],                  
                }
            }, 
        },
        commodities : {},
        currencies : {},
    }

}

Number.prototype.round = function(places) {
    return +(Math.round(this + "e+" + places)  + "e-" + places);
}

// Number.prototype.toString = function() {
//     return this + "";
// }

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
        return (this.tick).toFixed(2)
    }
}

class Signal{
    constructor(call_id, ticker, ltp, signal, time, price, target_price, stop_loss, status, risk_reward, active, signal_time = null){        
        this.init(call_id, ticker, ltp, signal, time, price, target_price, stop_loss,  status, risk_reward, active, signal_time = signal_time)
    }
    init(call_id, ticker, ltp, signal, time, price, target_price, stop_loss, status, risk_reward, active, signal_time = null){
        var self = this
        this.product_type = STOCKS_PROD
        this.call_id = call_id
        this.ticker = ticker
        this.ltp = ltp
        this.signal = signal
        // signal_time = 2020-05-26T11:59:46.212353+05:30
        // time = 05/26/2020, 11:59:46        
        this.time = moment(signal_time, moment.ISO_8601).format('DD MMM YY, h:mm')
        this.price = price
        this.target_price = target_price.round(2)
        this.stop_loss = stop_loss.round(2)
        this.profit = {
                    toString(){                        
                        return (Math.abs(self.ltp - self.target_price) / self.price).toFixed(2)
                    }
                }
        this.status = status
        this.risk_reward = risk_reward
        this.active = active
        this.follow = false
        this.visible = true
    }
    update(data){
        console.log("signal update : ", data );        
        if(data.signal) this.signal = data.signal
        if(data.status) this.status = data.status
        if(data.active == true || data.active == false) this.active = data.active
    }
    static set_follow(state, params){
        var {item = null, follow = false} = params
        console.log("following : ", item ,follow);
        item.follow = follow
    } 
    static hide(state, params){
        var {item = null} = params
        console.log("hiding : ", item);
        item.visible = false
    }
    toString(){
        return `${this.ticker},${this.ltp}, ${this.signal}, ${this.time.replace(',', '  ')}, ` + 
                `${this.price}, ${this.target_price}, ${this.stop_loss}, ${this.profit}, ${this.status},`
    }
    
}


/**
*   underlying : {},
    expiry : {},
    strike : {},
    ticker : {},
    time : {},
    price : {},
    target_price : {},
    stop_loss : {},
    profit : {},
    risk_reward : {}
 */
class OptionsSignal{
    constructor(call_id, underlying, expiry, strike, ticker, ltp, signal, signal_time, price, target_price, stop_loss, profit, risk_reward, status, active){
        this.init(call_id, underlying, expiry, strike, ticker, ltp, signal, signal_time, price, target_price, stop_loss,  profit, risk_reward, status,active)
    }
    init(call_id, underlying, expiry, strike, ticker, ltp, signal, signal_time, price, target_price, stop_loss, risk_reward, status, active){
        var self = this
        this.product_type = OPTIONS_PROD
        this.call_id = call_id
        this.underlying = underlying
        this.expiry = moment(expiry, moment.ISO_8601).format('DD MMM')
        this.strike = strike
        this.ticker = ticker
        this.ltp = ltp
        this.signal = signal
        // signal_time = 2020-05-26T11:59:46.212353+05:30
        // time = 05/26/2020, 11:59:46        
        this.time = moment(signal_time, moment.ISO_8601).format('DD MMM YY, h:mm')
        this.price = price
        this.target_price = target_price.round(2)
        this.stop_loss = stop_loss.round(2)
        this.profit = {
                    toString(){                        
                        return (Math.abs(self.ltp - self.target_price) / self.price).toFixed(2)
                    }
                }        
        this.risk_reward = risk_reward
        this.status = status
        this.active = active
        this.follow = false
        this.visible = true 
    }
    update(data){
        console.log("signal update : ", data );        
        // if(data.signal) this.signal = data.signal
        // if(data.status) this.status = data.status
        if(data.active == true || data.active == false) this.active = data.active
    }
    static set_follow(state, params){
        var {item = null, follow = false} = params
        console.log("following : ", item ,follow);
        item.follow = follow
    } 
    static hide(state, params){
        var {item = null} = params
        console.log("hiding : ", item);
        item.visible = false
    }
    toString(){
        return `${this.ticker},${this.ltp}, ${this.signal}, ${this.time.replace(',', '  ')}, ` + 
                `${this.price}, ${this.target_price}, ${this.stop_loss}, ${this.profit}, ${this.status},`
    }
    
}
