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

const FILTER = {
    tickers : null, // null or list of ticker names
    action : null, // null or BUY / SELL
    profit : null, // null or float
    risk_reward : null, // null or float

    set(props){
        if(props.tickers) this.tickers = tickers
        if(props.action) this.action = this.action
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
 *                      data : []
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
                },
                btst : {
                    data : [], 
                    filter : {},
                },
                positional :{
                    data : [],
                    filter : {},
                },
                longterm : {
                    data : [],
                    filter : {},
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
                },
                btst : {
                    data : [],
                    filter : {},                     
                }
            }, 
        },
        commodities : {},
        currencies : {},
    }

}