const PORTFOLIOS = ['', 'nifty50', 'intraday', 'btst', 'positional', 'longterm'];

const STOCKS = 'stocks';
const OPTIONS = 'options';

const KEY_2_LABEL = {
    ticker : "Ticker",
    ltp : "Last Price",
    signal : "Signal",
    time : "Signal Time",
    signal_time : "Signal Time",
    signal_price : "Signal Price",
    price : "Signal Price",
    target_price : "Target Price",
    stop_loss : "Stop Loss",
    profit : "Profit %",
    status : "Status",  
    underlying : "Underlying",
    expiry : "Expiry",
    strike : "Strike", 
}

const STATE = {
    portfolio : PORTFOLIOS[2],
    type : STOCKS,
    market : "equity",
    market_type : "indian_market",
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

const FILTER = {
    tickers : null, // null or list of ticker names
    sides : null, // null or BUY / SELL
    profit_percentage : null, // null or float
    risk_reward : null, // null or float
    search : null,
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
                    filter : {},
                    tickers : [],
                },
                btst : {
                    data : [], 
                    filter : {},
                    tickers : [],
                },
                positional :{
                    data : [],
                    filter : {},
                    tickers : [],
                },
                longterm : {
                    data : [],
                    filter : {},
                    tickers : [],
                }
            }, 
            options : {
                header : {
                    underlying : {},
                    expiry : {},
                    strike : {},
                    ticker : {},                                            
                    time : {},
                    price : {},
                    target_price : {},
                    stop_loss : {},
                    profit : {},
                    risk_reward : {}
                },
                intraday : {
                    data : [],
                    filter : {},
                    tickers : [],
                },
                btst : {
                    data : [],
                    filter : {},   
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