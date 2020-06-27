const MercuryPlans = `
<div>

<div class="mt-5 row justify-content-center">
	<p class="mx-4">Monthly</p>

  <v-switch v-model="subscription_period_selected" class="mx-4 my-0" label=""
  style="color: #004b96;">
  </v-switch>

	<p class="mx-4">Annually</p>
    <br>
</div>

<!-- ____________________period switch end___________________ -->
<!-- ____________________N members starts____________________ -->

<div class="row justify-content-center inline">
	<!-- <div class="btn-toolbar shadow-lg" role="toolbar" aria-label="Toolbar with button groups">
		<div class="btn-group mr-2 border-1" id="" role="group">
			<button type="button" class="btn">1</button>
			<button type="button" class="btn">10</button>
			<button type="button" class="btn">50</button>
			<button type="button" class="btn">100</button>
		</div> 
  </div> -->

  <v-btn-toggle
  light
  tile
  prominent
  color="#004b96"
  v-model="group_type_selected" mandatory class="rounded">
  <v-btn v-for="group_type in group_types" :value="group_type" 
  style="background-color: white;">
      {{ group_type }}
  </v-btn>
</v-btn-toggle>



</div>

<!-- __________________cards container start_________________ -->
<div class="container mt-5 text-center">
		<div class="row d-flex justify-content-around">

		<div class="col-md-3">
			<div class="card text-center mb-4 shadow-sm elevation-4">
            <div class="card-header dark_blue_color text-light rounded shadow-lg">
            <h4 class="my-0 font-weight-normal">&#x20b9; {{ basic_plan_price }} </h4>
            </div>
            <div class="card-body justify-content-center">
            <!-- <h2 class="card-title pricing-card-title">BASIC</h2> -->
            <h3 style="letter-spacing: 3px;">BASIC</h3>
            <div class="justify-content-center w-100">
              <v-select
                class="mx-auto overflow-hidden"
                height="20"
                width="10"
                v-model="basic_product_name_selected"
                :items="get_basic_products"
                label="Select Investment Type"
                solo
                dense
              >
                <template v-slot:item="{item}" >
                    <span v-if="item == 'btst'">
                        {{ item.toUpperCase() }}
                    </span>
                    <span v-else>{{ item.charAt(0).toUpperCase() }}{{ item.slice(1).toLowerCase() }}
                    </span>
                </template>

                <template v-slot:selection="{item}" >
                    <span v-if="item == 'btst'">
                        {{ item.toUpperCase() }}
                    </span>
                    <span v-else>{{ item.charAt(0).toUpperCase() }}{{ item.slice(1).toLowerCase() }}
                    </span>
                </template>

              </v-select>
            </div>

            <ul class="list-unstyled list-inline text-center align-items-center">
              <li v-for="basic_product in get_basic_products" 
              class="pr-5">
                <span>
                  <div class="row">
                    <i v-if = "basic_product_name_selected == basic_product" class="fa fa-check mr-2" aria-hidden="true" 
                    style="font-size:20px;color:green">
                    </i>
                    <i v-else class="fa fa-close mr-4" aria-hidden="true" 
                    style="font-size:20px;color:red">
                    </i>
                    <span v-if="basic_product == 'btst'">
                      {{ basic_product.toUpperCase() }}
                    </span>
                    <span v-else>{{ basic_product.charAt(0).toUpperCase() }}{{ basic_product.slice(1).toLowerCase() }}
                    </span>
                  </div>
                </span>
              </li>
            </ul>
            <form method = "POST" action="/subscriptions/plan-data"> 
                <input type="hidden" name="csrfmiddlewaretoken" :value="get_csrf_token()" hidden> 
                <input class="periodcode" name = "period"  :value="$store.getters.state.subscription_period" hidden></input>
                <input class="plancode" name= "plancode"   :value="'basic'" hidden></input>
                <input class="planname" name= "planname"   :value='$store.getters.state.plan_name' hidden></input>
                <input class="groupcode" name= "groupcode" :value="group_type_selected_name" hidden></input>
              <button type="submit" class="btn btn-sm dark_blue_color text-light">Subscribe</button>
            </form>
            </div>
      </div>
      
    </div>
    
    <div class="col-md-3">
			<div class="card text-center mb-4 shadow-sm elevation-2">
          <div class="card-header bg-warning text-dark shadow-lg">
          <h4 class="my-0 font-weight-normal">&#x20b9; {{ premium_plan_price }} </h4>
          </div>
          <div class="card-body">
          
          <!-- <span style="position: relative;" class="mb-3">

                <img src="/static/img/premium_bg.svg" 
                class="yellow-banner"
                
                />

                <span style="position: relative;">
                  <h2>PREMIUM</h2>
                </span>
                
          </span> -->

          <div class="card-title text-dark border-1 rounded" style="">
            <h3 style="letter-spacing: 3px;">PREMIUM</h3>
          </div>
          <!-- <p>
            <small>*Includes all Investment Types</small>
          </p> -->
          <small>
            *Includes all Investment Types
          </small>
          <ul class="list-unstyled text-center" style="margin-top:45px;">
            <li v-for="premium_product in get_premium_products" class="pr-5">
              <div class="row">
                <i class="fa fa-check mr-4" aria-hidden="true" 
                style="font-size:20px;color:green">
                </i>
                {{ premium_product }}
              </div>
            </li>
          </ul>
          <form method = "POST" action="/subscriptions/plan-data"> 
            <input type="hidden" name="csrfmiddlewaretoken" :value="get_csrf_token()" hidden> 
            <input class="periodcode" name = "period"  :value='$store.getters.state.subscription_period' hidden></input>
            <input class="plancode" name= "plancode"   :value="'premium'" hidden></input>
            <input class="planname" name= "planname"   :value="'mercury'" hidden></input>
            <input class="groupcode" name= "groupcode" :value="group_type_selected_name" hidden></input>
            
            <button v-if="trial_apply" type="submit" class="btn btn-sm dark_blue_color text-light">Trial</button>
            
            <button v-else type="submit" class="btn btn-sm dark_blue_color text-light">Subscribe</button>
          </form>
          </div>
      </div>
      
		</div>
    
    <!-- row end below -->
    </div>
    <!-- container end below -->
	  </div>
	<!-- __________________cards container end_______________ -->



</div>
`




const app = `

<v-app>

<mercury-plans>
</mercury-plans>




<div class="container-fluid pt-5">
  
<!-- <div class="row"> -->
  <p class="text-center"><span class="max_font2">Features</span></p>
<!-- </div>   -->

  <div class="row text-center">
    
    <div class="col-md-3 mt-3">
      <img src="/static/img/high_hit_rate.png" class="img-fluid img_resize"><br>
      <p class="mt-3">High Hit Rate</p>
    </div>

    <div class="col-md-3">
      <img src="/static/img/superior_returns.png" class="img-fluid img_resize"><br>
      <p class="mt-3">Superior Returns</p>
    </div>

    <div class="col-md-3 mt-2">
      <img src="/static/img/real_time_notif.png" class="img-fluid img_resize"><br>
      <p class="mt-3">Real Time Notifications</p>
    </div>

    <div class="col-md-3 mt-4">
      <img src="/static/img/algo_gen_calls.png" class="img-fluid algo_gen_calls"><br>
      <p class="mt-2">Algo Generated Calls</p>
    </div>

  </div>
</div>

<m-product-timeline>
</m-product-timeline>


</v-app>
`

const timeline = 
`
<div class='container mt-5 mb-5'>
  <p class="text-center"><span class="max_font2">
    One-stop shop for effective trading 
  </span></p>
    <v-timeline :dense="$vuetify.breakpoint.smAndDown"> 
      <v-timeline-item :small="true">
        <span slot="opposite">
            <v-card class="elevation-0">
            <v-card-title class=" font-weight-bold">Customize & Analyse</v-card-title>
            <v-card-text class="text-dark time_line_font_sm">
            <span class="float-left">Filter calls as per your convenience and download data for analysis</span>
            </v-card-text>
            </v-card>
        </span>
        <v-card class="elevation-2">
          <v-img src="/static/img/custom.png"></v-img>
          <div class="hide_this_desktop">
          <v-card-text class="pb-0">
              <h5 class="font-weight-bold">Customize & Analyse<h5>
          </v-card-text>
          <v-card-text class="text-dark time_line_font_sm">
            Filter calls as per your convenience and download data for analysis
          </v-card-text>
          </div>
        </v-card>
      </v-timeline-item>

      <v-timeline-item :small="true">
        <span slot="opposite">
            <v-card class="elevation-0">
                <v-card-title class=" font-weight-bold">One Click Order</v-card-title>
                <v-card-text class="text-dark time_line_font_sm">
                <span class="float-left">Place your order through your preferred borker with just one click.</span>
                </v-card-text>
            </v-card>
        </span>
        <v-card class="elevation-2">
        <v-img src="/static/img/oneclick.png"></v-img>
        <div class="hide_this_desktop">
          <v-card-text class="pb-0">
              <h5 class="font-weight-bold">One Click Order<h5>
          </v-card-text>
          <v-card-text class="text-dark time_line_font_sm">
            Place your order through your preferred borker with just one click.
          </v-card-text>
          </div>
        </v-card>
      </v-timeline-item>

      <v-timeline-item :small="true">
        <span slot="opposite">
            <v-card class="elevation-0">
                <v-card-title class=" font-weight-bold">Real Time Notifications</v-card-title>
                <v-card-text class="text-dark time_line_font_sm">
                <span class="float-left">Stay updated with real time notifications of calls</span>
                </v-card-text>
            </v-card>
        </span>
        <v-card class="elevation-2">
        <v-img src="/static/img/realtime.png"></v-img>
        <div class="hide_this_desktop">
          <v-card-text class="pb-0">
            <h5 class="font-weight-bold">Real Time Notifications<h5>
          </v-card-text>
          <v-card-text class="text-dark time_line_font_sm">
            Stay updated with real time notifications of calls
          </v-card-text>
          </div>
        </v-card>
      </v-timeline-item>


      <v-timeline-item :small="true">
        <span slot="opposite">
            <v-card class="elevation-0">
                <v-card-title class=" font-weight-bold">Multiple Investment Types</v-card-title>
                <v-card-text class="text-dark time_line_font_sm">
                <span class="float-left">
                    Diversify your investments with our multiple investment types
                </span>
                </v-card-text>
            </v-card>
        </span>
        <v-card class="elevation-2">
        <v-img src="/static/img/multi.png"></v-img>
        <div class="hide_this_desktop">
          <v-card-text class="pb-0">
              <h5 class="font-weight-bold">Multi Investment Types<h5>
          </v-card-text>
          <v-card-text class="text-dark time_line_font_sm">
            Diversify your investments with our multiple investment types
          </v-card-text>
          </div>
        </v-card>
      </v-timeline-item>

    </v-timeline>


<div class="container mt-5">  

<!-- <div class="mx-auto mt-5 mb-5">
  Experience all these Features<br>
  <button class="btn btn-md text-light mt-5 dark_blue_color">
		  Start Your Free Trial  
	</button> 
</div> -->
<!-- 
<div class="row justify-content-center text-center">
    <div class="col-md-6 d-flex text-center justify-content-center">
        <span class="text-dark">HELLO</span>
        <button class="btn btn-md text-light dark_blue_color">
            Start Your Free Trial  
        </button>
    </div>
</div> -->

<!-- 
<v-container class="mx-auto">
    <span class="text-dark text-center">HELLO</span>
    <button class="btn btn-md text-light dark_blue_color">
        Start Your Free Trial  
    </button>
</v-container> -->

<p class="text-center mt-4 ">
  <span class="font-weight-bold">Experience all these Features
</span>
</p>
<div class="row justify-content-center mt-5 mb-5">
  <button class="btn btn-md text-light dark_blue_color text-center justify-content-center">
      Start Your Free Trial  
  </button>
</div>

<p class="text-center mt-5"><span class="max_font2 mt-5">FAQ</span></p>

    <!-- <v-expansion-panels popout blue elevation="0">
      <v-expansion-panel
        v-for="(item,i) in 5"
        :key="i"
        flat
      >
        <v-expansion-panel-header class="">Item</v-expansion-panel-header>
        <v-expansion-panel-content>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels> -->
</div>
</div>

`