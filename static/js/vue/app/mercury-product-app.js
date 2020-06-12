

function start_app() {
    new Vue({
    el: '#app',
    store, 
    vuetify: new Vuetify(),
    created(){
        console.log('====================================');
        console.log(this);
        console.log(this.$store);
        console.log('====================================');
    }
    })
}