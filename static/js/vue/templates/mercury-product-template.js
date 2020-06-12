const MercuryPlans = `
<div>

<div class="mt-5 row justify-content-center">
	<p class="mx-4">Monthly</p>

  <!-- <v-switch v-model="multiple" class="mx-4 my-0" label=""></v-switch> -->
  <v-switch v-model="subscription_period_selected" class="mx-4 my-0" label=""></v-switch>

	<!-- <div class="custom-control custom-switch">
		<input type="checkbox" class="custom-control-input mx-5" id="customSwitch1" checked>
		<label class="custom-control-label" for="customSwitch1"></label>
	</div> -->

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
  <v-btn-toggle v-model="group_type_selected" mandatory>
  <v-btn v-for="group_type in group_types" :value="group_type">
      {{ group_type }}
  </v-btn>
</v-btn-toggle>



</div>

<!-- __________________cards container start_________________ -->
<div class="container mt-5 justify-content-center">
		<div class="row d-flex justify-content-center">
		<div class="col-md-7">
		  <div class="card-deck mb-3 text-center" style="">
		
			<div class="card mb-4 shadow-sm">
			  <div class="card-header dark_blue_color text-light rounded shadow-lg">
				<h4 class="my-0 font-weight-normal">&#x20b9; {{ basic_plan_price }} <small class="text">/ mo</small></h4>
			  </div>
			  <div class="card-body justify-content-center">
        <h1 class="card-title pricing-card-title">BASIC</h1>
        <div class="justify-content-center w-100">
          <v-select
            v-model="basic_product_name_selected"
            :items="get_basic_products"
            label="Any One"
            solo
          ></v-select>
        </div>

				<ul class="list-unstyled mt-3 mb-4">
				  <li v-for="basic_product in get_basic_products">
            {{ basic_product }}
          </li>
        </ul>
        

        <form method = "POST" action="/subscriptions/plan-data"> 
            <input type="hidden" name="csrfmiddlewaretoken" :value="get_csrf_token()" hidden> 
            <input class="periodcode" name = "period"  :value="subscription_period_selected" hidden></input>
            <input class="plancode" name= "plancode"   :value="'basic'" hidden></input>
            <input class="planname" name= "planname"   :value='basic_product_name_selected' hidden></input>
            <input class="groupcode" name= "groupcode" :value="group_type_selected_name" hidden></input>
          <button type="submit" class="btn btn-sm dark_blue_color text-light">Subscribe</button>
        </form>

			  </div>
			</div>
		
			<div class="card mb-4 shadow-sm">
			  <div class="card-header dark_blue_color text-light rounded shadow-lg">
				<h4 class="my-0 font-weight-normal">&#x20b9; {{ premium_plan_price }} <small class="text">/ mo</small></h4>
			  </div>
			  <div class="card-body">
				<h1 class="card-title pricing-card-title">PREMIUM</h1>
				<ul class="list-unstyled mt-3 mb-4">
				  <li v-for="premium_product in get_premium_products">
              {{ premium_product }}
          </li>
				</ul>
				<button class="btn btn-sm dark_blue_color text-light">Subscribe</button>
			  </div>
			</div>
		
		  </div>
		</div>
		</div>
	  </div>
	<!-- __________________cards container end_______________ -->



</div>
`




const app = `

<v-app>

<mercury-plans>
</mercury-plans>




<div class="container-fluid pt-4">
  
<!-- <div class="row"> -->
  <p class="text-center"><span class="max_font">Features</span></p>
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
<div class='container mt-4 mb-2'>
  <p class="text-center"><span class="max_font">
    One-stop shop for effective trading 
  </span></p>
    <v-timeline :dense="$vuetify.breakpoint.smAndDown"> 

      <v-timeline-item>
        <span slot="opposite">Customize & Analyse
        </span>
        <v-card class="elevation-2">
          <v-img src="/static/img/custom.png"></v-img>
          <v-card-title class="headline">Customize & Analyse</v-card-title>
          <v-card-text>
            Filter calls as per your convenience and download data for analysis
          </v-card-text>
        </v-card>
      </v-timeline-item>

      <v-timeline-item>
        <span slot="opposite">One Click Order</span>
        <v-card class="elevation-2">
        <v-img src="/static/img/oneclick.png"></v-img>
          <v-card-title class="headline">One Click Order</v-card-title>
          <v-card-text>
            Place your order through your preferred borker with just one click.
          </v-card-text>
        </v-card>
      </v-timeline-item>

      <v-timeline-item>
        <span slot="opposite">Real Time Notifications</span>
        <v-card class="elevation-2">
        <v-img src="/static/img/realtime.png"></v-img>
          <v-card-title class="headline">Real Time Notifications</v-card-title>
          <v-card-text>
            Stay updated with real time notifications of calls
          </v-card-text>
        </v-card>
      </v-timeline-item>


      <v-timeline-item>
        <span slot="opposite">Multiple Investment Types</span>
        <v-card class="elevation-2">
        <v-img src="/static/img/multi.png"></v-img>
          <v-card-title class="headline">Multiple Investment Types</v-card-title>
          <v-card-text>
            Diversify your investments with our multiple investment types
          </v-card-text>
        </v-card>
      </v-timeline-item>

    </v-timeline>


<div class="container">  



<p class="text-center"><span class="max_font">FAQ</span></p>

<ul class="accordion" style="list-style: none;">
	<li>
		<a>What happens when my free trials expires ?</a>
		<p> text </p>
	</li>
	<li>
		<a>Do you offer Discounts ?</a>
		<p>text</p>
	</li>
	<li>
		<a>Can I pay for my Team ?</a>
		<p>text</p>
	</li>
  	<li>
	<a>Which payment methods are available ?</a>
		<p>text</p>
	</li>
  	<li>
	<a>Can I unsubscribe anytime in between?</a>
		<p>text</p>
	</li>
  	<li>
	<a>Can I get extended trial period ?</a>
		<p>text</p>
	</li>
</ul> <!-- / accordion -->


</div>
</div>

`