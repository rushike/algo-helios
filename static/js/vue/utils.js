const helpers = {
    is_mobile(){
        return this.get.bodywidth() < 560  
    },
    converter : {
        vh2px(value) {
            var w = window,
            d = document,
            e = d.documentElement,
            g = d.getElementsByTagName('body')[0],
            x = w.innerWidth || e.clientWidth || g.clientWidth,
            y = w.innerHeight|| e.clientHeight|| g.clientHeight;
        
            var result = (y*value)/100;
            return result;
        },
        vw2px(value) {
            var w = window,
            d = document,
            e = d.documentElement,
            g = d.getElementsByTagName('body')[0],
            x = w.innerWidth || e.clientWidth || g.clientWidth,
            y = w.innerHeight|| e.clientHeight|| g.clientHeight;
        
            var result = (x*value)/100;
            return result;
        },

        percent2px(value, rootdivid = 'chess-board') {
            var g = document.getElementById(rootdivid);
            var x = g.clientWidth,
            y = g.clientHeight; 
            const result = {
                x : (x*value)/100,
                y : (y*value)/100
            };
            return result;
        },
    },
    get : {
        bodyheight(){
            var w = window,
            d = document,
            e = d.documentElement,
            g = d.getElementsByTagName('body')[0];
            return  g.clientHeight; // || w.innerHeight || e.clientHeight ||
        },
        bodywidth(){
            var w = window,
            d = document,
            e = d.documentElement,
            g = d.getElementsByTagName('body')[0];
            return g.clientWidth // || w.innerWidth || e.clientWidth ||
        },
        divheight(id){
            var div = document.getElementById(id)
            if(div){
                return div.offsetHeight
            }
        },
        divwidth(id){
            var div = document.getElementById(id)
            if(div){
                return div.offsetWidth
            }
        }
    }
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}