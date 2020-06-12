// for mercury product page 

const YEARLY = "yearly"
const MONTHLY = "monthly"

/**
STATE will keep a track of user interaction 
 */

const STATE = {
    group_type : 1, //max number in group
    plan_type : null , // either basic or premium
    subscription_period : "monthly" , // either monthly / annually
    product_name : "intraday", //can be list mercury#intraday, (btst), (positional), (longterm), (premium)
    plan_name : "mercury#intraday", // can be string
    init(){
        this.group_type = 1
        this.plan_type = null
        this.subscription_period = "monthly"
        this.product_name = "intraday"
        this.plan_name = "mercury#intraday"
    },
    update(props){
        if(!props) return this
        if(props.group_type) this.group_type = props.group_type
        if(props.plan_type) this.plan_type = props.plan_type
        if(props.subscription_period) this.subscription_period = props.subscription_period
        if(props.product_name) this.product_name = props.product_name
        if(props.plan_name) this.plan_name = props.plan_name
        return this
    }

}

// const PRODUCT_DATA = {
//     group_type : {
//             plan_type : {
//                 plan_name : { 
//                     data : []
//                     price_per_month
//                     price_per_year
//                 }
//             }
//         }
//     }

// all plans data will be loaded 
var PRODUCT_DATA = null


// class Product {
//     constructor(product_name) {
//         this.product_name = product_name
//     }
//     toString() {
//         return this.product_name.split('#')[1] //removes # 
//     }
// }
