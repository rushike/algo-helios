const m_product_timeline = Vue.component('m-product-timeline', {
    name : 'm-product-timeline',
    template : timeline,
    data: () => {
        return {}
    },

    watch : {
        reverse_(){

        }
    }

})


const mercury_plans = Vue.component('mercury-plans', {
    template : MercuryPlans,
    created() {
        
        this.$store.dispatch('load_product_data', {})
        
    },
    data : () => {
        return {}
    },
    computed : {
                
        group_types(){
            x = this.$store.getters.product_data

            return x ? Object.keys(x) : [];
        },

        trial_apply(){
            var current_state = this.$store.getters.state; 
            var product_data = this.$store.getters.product_data;
            return product_data ? product_data[current_state.group_type].eligible_for_trial && product_data[current_state.group_type].premium.trial_applicable : false
        },


        group_type_selected : {
            get() {
                return this.$store.getters.state.group_type
            },
            set(value){
                
                this.$store.commit('update_state',{
                    // group_type : parseInt(this.group_types[value])
                    group_type : value
                })
            }
        },
        
        group_type_selected_name () {
            var current_state = this.$store.getters.state; 
            var product_data = this.$store.getters.product_data;
            return product_data ? product_data[current_state.group_type].group_type : 'individual'
        },

        subscription_period_selected : {
            get() {
                return this.$store.getters.state.subscription_period == MONTHLY ? false : true
            },
            set(value){
                if ( value ) 
                { 
                        this.$store.commit('update_state',{
                        subscription_period : YEARLY
                    })
                
                }

                else 
                {
                        this.$store.commit('update_state',{
                        subscription_period : MONTHLY
                    })
                }
            }
        },

        basic_plan_price() {
            var current_state = this.$store.getters.state 
            var product_data = this.$store.getters.product_data
            
            if (!product_data)
                return 0

            if (current_state.subscription_period == MONTHLY )
                return product_data[current_state.group_type].basic[current_state.plan_name].monthly_price

            else if (current_state.subscription_period == YEARLY )
                return product_data[current_state.group_type].basic[current_state.plan_name].yearly_price
        },


        premium_plan_price() {
            var current_state = this.$store.getters.state 
            var product_data = this.$store.getters.product_data
            
            if (!product_data)
                return 0

            if (current_state.subscription_period == MONTHLY )
                return product_data[current_state.group_type].premium.mercury.monthly_price

            else if (current_state.subscription_period == YEARLY )
                return product_data[current_state.group_type].premium.mercury.yearly_price
        },


        get_premium_products() {
            var current_state = this.$store.getters.state 
            var product_data = this.$store.getters.product_data
            
            if (!product_data)
                { return [] }

            return product_data[current_state.group_type].premium.mercury.data.map(v=>v.split('#')[1]).filter(v=>v)
        },

        get_basic_products() {
            var current_state = this.$store.getters.state 
            var product_data = this.$store.getters.product_data
            
            if (!product_data)
                { return [] }

            // console.log('====================================');
            // console.log(Object.keys(product_data[current_state.group_type].basic).map(v=>v.split('#')[1]));
            // console.log('====================================');

            return Object.keys(product_data[current_state.group_type].basic).map(v=>v.split('#')[1]).filter(v=>v)
        },

        basic_product_name_selected : {
            get() {
                return this.$store.getters.state.plan_name.split('#')[1]
            },
            set(value){
                this.$store.commit('update_state',{
                    plan_name : "mercury#"+value , product_name : "mercury#"+value
                })
            }
        },    
    },

    watch : {
        reverse_(){

        }
    },

    methods : {
        get_csrf_token(){
            // // console.log(document.getElementById("csrf_token").innerHTML)
            // return document.getElementById("csrf_token").innerHTML
            return $("input[name='csrfmiddlewaretoken']").val()
    
        },

        isMobile() {
            if(/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) 
            {
                return true
            } 
            else 
            {
                return false
            }
        }


    }

})






const _app = Vue.component('app', {
    name: 'App',
    // components : {  },
    template : app
})
