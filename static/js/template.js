const app = `
<div>



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

</div>
`

const timeline = 
`
<div class='container mt-4 mb-2'>
  <p class="text-center"><span class="max_font">
    One-stop shop for effective trading 
  </span></p>
<v-app>
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




</v-app>
</div>

`