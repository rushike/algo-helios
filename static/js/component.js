
const m_product_timeline = Vue.component('m-product-timeline', {
    name : 'm-product-timeline',
    template : timeline,
    data: () => ({
        reverse_ : true
    //   reverse: true,
    }),
    

    watch : {
        reverse_() { console.log("heyy") }
    }

    })

const _app = Vue.component('app', {
    name: 'App',
    components : { m_product_timeline },
    template : app
})
