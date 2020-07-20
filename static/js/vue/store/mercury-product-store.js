// const moduleA = {
//   state: () => ({ ... }),
//   mutations: { ... },
//   actions: { ... },
//   getters: { ... }
// }

Vue.use(Vuex);
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
axios.defaults.xsrfCookieName = "csrftoken"

const store = new Vuex.Store({
    state : {
        state : STATE,
        product_data :  PRODUCT_DATA
    },
    getters: {  

        state(state, getters){
            return state.state
        },
        product_data(state, getters){
            return state.product_data
        },
    
    },
    mutations: {    
        // uses commit 
        // updates in mutations
        update_state : (state, state_dict)=>{        
            state.state.update(state_dict)
        },

        update_product_data : (state, product_data_dict)=>{        
            state.product_data = product_data_dict
        },


    },

    actions: {
        /**
        context is store object 
        mutation is called by commit
        action is called by dispatch 
         */
        async load_product_data(context, props){
           var data = (await axios.post('/subscriptions/mercury-product-data/', {} )).data
           
           context.commit('update_product_data', data)
           // console.log('====================================');
           // console.log("data from DB", data);
           // console.log('====================================');
        }
    }
});