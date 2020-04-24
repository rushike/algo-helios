class Lander{
    constructor(props = {}){
        this.anim_min_height = 10
        this.anim_max_height = 50

        this.id = ("id" in props) ? props.id : "test";
        this.height = ("height" in props) ? props.height : 374;
        this.width =  ("width" in props) ? props.width : 347;
        this.fill_the_div();
        this.fire_rocket();
        this.start_animation();
        this.style = ("style" in props) ? props.style : "margin-top : 20vh;";
        this.after_div_classes = ("after_div_classes" in props) ? props.after_div_classes : "containerm";
        document.getElementById(`${this.id}`).setAttribute("style", this.style);
        this.svg = document.getElementById(`${this.id}-svg` );
        // setTimeout(() => {
        //     this.fly_up();
        // }, 3000);
    }

    fill_the_div(){
        var div = document.getElementById(this.id)
        div.innerHTML = this.svg_img()
    }

    fire_rocket(svg){
        var svg = svg ? svg : document.getElementById(`${this.id}-svg` )
        for(var i = 0; i < 27; i++){
            var stick = (i % 9) + 1 ;
            var fire = parseInt(i / 9) + 1;
            var fire_stick = svg.getElementById('fire-' + stick + fire);
            fire_stick.setAttribute("y2", parseInt(fire_stick.getAttribute("y1")) +  Math.floor(Math.random()*this.anim_max_height) + this.anim_min_height)
        }
    }

    
    fly_up(){
        var divwrapper = document.getElementById(this.id);
        var style = divwrapper.currentStyle || window.getComputedStyle(divwrapper);
        var margin = style.marginTop
        clearInterval(this.start_anim)
        this.fire_rocket() 
        let mod_margin = parseFloat(margin) / 7;
        this.fire_rocket()
        let subtract_margin = mod_margin
        let new_mt = parseFloat(margin)
        this.fire_rocket()
        var svg =  document.getElementById(`${this.id}-svg` )
        this.fire_rocket()
        var width = parseFloat(svg.getAttribute("width"))
        this.fire_rocket()
        var height = parseFloat(svg.getAttribute("height"))
        this.fire_rocket()
        var x = 0;
        this.end_anim = setInterval(()=>{
            this.fire_rocket.bind(this)
            new_mt = new_mt - mod_margin;
            divwrapper.setAttribute('style', `margin-top : ${new_mt}px`);
            mod_margin *= 2.2
            height *= 0.95
            width *= 0.85
            x += 0.09
            svg.setAttribute("height", `${height}`)
            svg.setAttribute("width",`${width}` )
            this.fire_rocket.bind(this)
            document.querySelector(`.${this.after_div_classes}`).style.opacity = x
        }, 40)

        setTimeout(()=>{
            clearInterval(this.end_anim);
            svg.setAttribute("style", "display:none")
            divwrapper.setAttribute('style', 'display:none')
            document.querySelector(`.${this.after_div_classes}`).style.opacity = 1
        }, 1000)
    }

    start_animation(){
        this.start_anim = setInterval(this.fire_rocket.bind(this), 70)
    }

    svg_img(){
        return `
            <svg id = "${this.id}-svg" width="${this.width}" height="${this.height}" viewBox="0 0 347 374" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M19 144H14V302H19V144Z" fill="#585959"/>
                <path d="M18.5 144.5H14.5V301.5H18.5V144.5Z" stroke="#707070"/>
                <path d="M33 150H0V278H33V150Z" fill="#004B96"/>
                <path d="M334 144H328V302H334V144Z" fill="#585959"/>
                <path d="M333.5 144.5H328.5V301.5H333.5V144.5Z" stroke="#707070"/>
                <path d="M347 150H314V278H347V150Z" fill="#004B96"/>
                <path d="M59 111H54V282H59V111Z" fill="#585959"/>
                <path d="M58.5 111.5H54.5V281.5H58.5V111.5Z" stroke="#707070"/>
                <path d="M73 118H39V257H73V118Z" fill="#7DDCFF"/>
                <path d="M98 77H93V266H98V77Z" fill="#585959"/>
                <path d="M97.5 77.5H93.5V265.5H97.5V77.5Z" stroke="#707070"/>
                <path d="M112 83H79V242H112V83Z" fill="#004B96"/>
                <path d="M137 32H132V229H137V32Z" fill="#585959"/>
                <path d="M136.5 32.5H132.5V228.5H136.5V32.5Z" stroke="#707070"/>
                <path d="M151 38H118V205H151V38Z" fill="#7DDCFF"/>
                <path d="M176 0H171V212H176V0Z" fill="#585959"/>
                <path d="M175.5 0.5H171.5V211.5H175.5V0.5Z" stroke="#707070"/>
                <path d="M190 7H157V188H190V7Z" fill="#004B96"/>
                <path d="M216 32H211V229H216V32Z" fill="#585959"/>
                <path d="M215.5 32.5H211.5V228.5H215.5V32.5Z" stroke="#707070"/>
                <path d="M230 38H196V205H230V38Z" fill="#7DDCFF"/>
                <path d="M255 77H250V266H255V77Z" fill="#585959"/>
                <path d="M254.5 77.5H250.5V265.5H254.5V77.5Z" stroke="#707070"/>
                <path d="M269 83H236V242H269V83Z" fill="#004B96"/>
                <path d="M294 111H289V282H294V111Z" fill="#585959"/>
                <path d="M293.5 111.5H289.5V281.5H293.5V111.5Z" stroke="#707070"/>
                <path d="M308 118H275V257H308V118Z" fill="#7DDCFF"/>
                <line id = "fire-11" x1="9.5" y1="312" x2="9.5" y2="323" stroke="black" stroke-width="3"/>
                <line id = "fire-12" x1="18.5" y1="312" x2="18.5" y2="374" stroke="black" stroke-width="3"/>
                <line id = "fire-13" x1="27.5" y1="312" x2="27.5" y2="350" stroke="black" stroke-width="3"/>
                <line id = "fire-21" x1="48.5" y1="292" x2="48.5" y2="354" stroke="black" stroke-width="3"/>
                <line id = "fire-22" x1="57.5" y1="292" x2="57.5" y2="319" stroke="black" stroke-width="3"/>
                <line id = "fire-23" x1="66.5" y1="292" x2="66.5" y2="302" stroke="black" stroke-width="3"/>
                <line id = "fire-31" x1="88.5" y1="276" x2="88.5" y2="292" stroke="black" stroke-width="3"/>
                <line id = "fire-32" x1="97.5" y1="276" x2="97.5" y2="338" stroke="black" stroke-width="3"/>
                <line id = "fire-33" x1="106.5" y1="276" x2="106.5" y2="312" stroke="black" stroke-width="3"/>
                <line id = "fire-41" x1="127.5" y1="239" x2="127.5" y2="276" stroke="black" stroke-width="3"/>
                <line id = "fire-42" x1="136.5" y1="239" x2="136.5" y2="308" stroke="black" stroke-width="3"/>
                <line id = "fire-43" x1="145.5" y1="239" x2="145.5" y2="257" stroke="black" stroke-width="3"/>
                <line id = "fire-51" x1="166.5" y1="222" x2="166.5" y2="298" stroke="black" stroke-width="3"/>
                <line id = "fire-52" x1="175.5" y1="222" x2="175.5" y2="239" stroke="black" stroke-width="3"/>
                <line id = "fire-53" x1="184.5" y1="222" x2="184.5" y2="261" stroke="black" stroke-width="3"/>
                <line id = "fire-61" x1="205.5" y1="239" x2="205.5" y2="271" stroke="black" stroke-width="3"/>
                <line id = "fire-62" x1="214.5" y1="239" x2="214.5" y2="298" stroke="black" stroke-width="3"/>
                <line id = "fire-63" x1="223.5" y1="239" x2="223.5" y2="258" stroke="black" stroke-width="3"/>
                <line id = "fire-71" x1="245.5" y1="276" x2="245.5" y2="338" stroke="black" stroke-width="3"/>
                <line id = "fire-72" x1="254.5" y1="276" x2="254.5" y2="294" stroke="black" stroke-width="3"/>
                <line id = "fire-73" x1="263.5" y1="276" x2="263.5" y2="318" stroke="black" stroke-width="3"/>
                <line id = "fire-81" x1="284.5" y1="292" x2="284.5" y2="328" stroke="black" stroke-width="3"/>
                <line id = "fire-82" x1="293.5" y1="292" x2="293.5" y2="350" stroke="black" stroke-width="3"/>
                <line id = "fire-83" x1="302.5" y1="292" x2="302.5" y2="310" stroke="black" stroke-width="3"/>
                <line id = "fire-91" x1="323.5" y1="312" x2="323.5" y2="323" stroke="black" stroke-width="3"/>
                <line id = "fire-92" x1="332.5" y1="312" x2="332.5" y2="367" stroke="black" stroke-width="3"/>
                <line id = "fire-93" x1="341.5" y1="312" x2="341.5" y2="350" stroke="black" stroke-width="3"/>
            </svg>
        `
    }
}
    