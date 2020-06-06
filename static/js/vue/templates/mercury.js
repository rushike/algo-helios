const M_STOCKTABLE_TEMPLATE_STRING = `

    <v-data-table
        
        :headers="fields"
        :items="filter_items"     
        :items-per-page = "items.length"
        :search = "search"
        :loading = 'loading'
        loading-text="Loading... Please wait"
        :disable-pagination = "true"
        :group-desc = "true"
        group-by = "follow"
        
        height="70vh"
        class="elevation-1"        
        style="max-height: calc(100vh ); backface-visibility: hidden;"
        hide-default-footer
        fixed-header>
        
        
        <template v-slot:group.header="{group, groupBy}" >
              {{group}} {{groupBy}}
        </template>

        <template v-slot:group="{group, options, items, headers}" >             
            
                <tr v-for = "(item, index) in items" :class = "row_class(group, index, item, items) + ' ' + (item.ltp.instrument_id)" >
                    <td v-for = "header in headers" >
                        <span v-if = "header.key == 'signal'">
                            <button rounded type="button" :class="item.signal + '_btn trade'"  data-toggle="modal" 
                                data-target="#trade_modal">
                                <span >            
                                    {{ item.signal }}
                                </span>
                            </button>
                        </span>
                        <span v-else-if = "header.key == 'status'">
                            <span :class = "'badge rounded  ' + item.status + '_status'">
                                {{ item.status }}
                            </span>
                        </span>
                        <span v-else-if = "header.key == 'action'">
                            <span v-if = "item.follow">                                            
                                <img class = "px-1 fa-2x" v-on:click="follow_my_trade(item, true)" src="/static/img/pin-slash.svg" style = "cursor:pointer; opacity : 0.4; height : 30%;" aria-hidden="true"></img>
                                <img class = "px-1 fa-2x" v-on:click="follow_my_trade(item, false)" src="/static/img/bin.svg" style = "cursor:pointer; height : 30%;" aria-hidden="true" ></img>
                            </span>
                            <span v-else>
                                <img class = "px-1 fa-2x" v-on:click="follow_my_trade(item, true)" src="/static/img/pin.svg" style = "cursor:pointer; height : 30%;" aria-hidden="true" ></img>
                                <img class = "px-1 fa-2x" v-on:click="follow_my_trade(item, false)" src="/static/img/bin.svg" style = "cursor:pointer; opacity : 0.4; height : 30%;" aria-hidden="true" ></img>
                            </span>
                            

                        </span>
                        <span v-else>                        
                            {{item[header.key]}}
                        </span>
                    </td>
                </tr>

        </template> 



       
    </v-data-table>  
</v-responsive>
`

const M_OPTIONSTABLE_TEMPLATE_STRING = `
    <v-data-table
        :headers="headers"
        :items="filter_items"     
        :items-per-page = "items.length"
        :search = "search"        
        loading = 'loading'
        loading-text="Loading... Please wait"
        fixed-header
        :disable-pagination = "true"
        hide-default-footer
        height="70vh"
        class="elevation-1"        
        style="max-height: calc(100vh ); backface-visibility: hidden;">
        
    </v-data-table>  
`

const M_EQUITY_TEMPLATE_STRING = `
<div>
<m-stocks-table v-if = "state.type == 'stocks'" ref="m_stocktable" :items = "items" :fields = "fields" :headers = "headers" :state = "state" >
</m-stocks-table>
<m-stocks-table v-if = "state.type == 'options'" ref="m_stocktable" :items = "items" :fields = "fields" :headers = "headers" :state = "state" >
</m-stocks-table>
</div>
`

const M_INDIAN_MARKET_TEMPLATE_STRING = `
<m-equity ref="m_equity" :items = "items" :fields = "fields" :headers = "headers" :state = "state" >
</m-equity>
`
const M_DATA_TABLE = `
<m-indian-market ref="m_indian_market" :items = "items" :fields = "fields" :headers = "headers" :state = "state" >
</m-indian-market>
`

const M_DATA_TABLE_INFO = `
    <div class = "pb-1">
    <v-row
        class="mx-3"
        no-gutters
        >
        <v-col cols="12" md = "3" >
                <v-select
                class = "px-1 pt-4"
                v-model="type"
                :items="equity_type"
                menu-props="auto"
                label="Select"
                hide-details          
                single-line
                dense
                solo            
                ></v-select>
        </v-col>
        
        <v-col cols ="12" md = "6" class = "text-center">
            <v-row >
                <v-col cols = "12" md = "6" class = "text-center">
                    <v-row>
                        <v-col cols ="6" class = "text-center">                            
                            <v-badge pill variant="primary" color="blue" :content = "'Total'" class = "blue--text darken-4--text font-weight-bold headline">{{meta.total}}</v-badge>
                        </v-col>

                        <v-col cols ="6" class = "text-center">                                                  
                            <v-badge pill color="green accent-3" :content = "'Partial HIT'" class = "light-green--text accent-3--text font-weight-bold headline">{{meta.partial_hit}}</v-badge>
                        </v-col>
                    </v-row>
                </v-col>

                <v-col cols = "12" md = "6" class = "text-center">
                    <v-row>
                        <v-col cols ="6" class = "text-center">
                            <v-badge pill color="green lighten-1"  :content = "'HIT'" class = "green--text darken-4--text font-weight-bold headline">{{meta.hit}}</v-badge>
                        </v-col>

                        <v-col cols ="6" class = "text-center">
                            <v-badge pill color="red" :content = "'MISS'" class = "deep-orange--text darken-4--text font-weight-bold headline">{{meta.miss}}</v-badge>                        
                        </v-col>
                    </v-row>
                </v-col>
            </v-row>
        </v-col>

        <v-col cols="12" md="3" class = "pt-3" >
            <v-row align="center" justify="center" class = "float-right">
            <v-col cols = "12" >
                <!-- <span id = "filter">
                    <a data-toggle="tooltip"  data-placement="top" title="Filter">
                        <button data-toggle = "collapse" data-target = "#filter-collapse" class="btn filter get_filter"  aria-expanded="false" aria-controls="filter-collapse">
                            <small><span class="fa fa-filter"></span></small>
                        </button>
                    </a>
                </span> -->

                <span id = "download">
                    <a href="#" data-toggle="tooltip" data-placement="top" title="Download">
                        <button class="btn download" v-on:click='download_as_csv()'>
                            <small><span class="fa fa-download"></span></small>
                        </button>
                    </a>
                </span>
                <span >
                    <a href="#" data-toggle="tooltip" data-placement="top" title="Refresh">
                        <button class="btn refresh" v-on:click = "refresh_table()" id = "refresh"  title="Refresh">
                            <small><span class="fa fa-refresh"></span></small>
                        </button>
                    </a>
                </span>

                <span href="#" data-toggle="tooltip" data-placement="top" title="Notify">
                    <button class="btn refresh user-notify" v-on:click = "allow_notification()" title="notify">
                        <small v-if = "notification" ><span class="fa fa-bell-slash notify"></span></small>
                        <small v-else><span class="fa fa-bell notify"></span></small>
                    </button>
                </span>    
                </v-col>
                </v-row>            
        </v-col>            
    </v-row>
    <v-row
        class="mx-3"
        no-gutters
        >
        <v-col cols = "12" md = "3">        
            <v-text-field
                v-model="search"
                class = "px-1"
                append-icon="mdi-magnify"
                label="Search"
                single-line
                hide-details
            ></v-text-field>
        </v-col>
        <v-spacer></v-spacer>
        <v-col cols = "12" md = "4" class = "pt-2">
            <v-select
                class = "px-1"
                v-model="selected_fields"
                :items="fields"
                menu-props="auto"
                label="Select"
                multiple
                hide-details
                dense
                solo
                single-line
            >
                <template v-slot:selection="{ item, index }">
                    <v-chip v-if="index < 2">
                        <span>{{ item.text }}</span>
                    </v-chip>
                    <span
                        v-if="index === 2"
                        class="grey--text caption"
                        >(+{{ selected_fields.length - 1 }} others)</span>
                </template>
            
            </v-select>
        </v-col>
    </v-row>
    </div>
`

const M_FILTER_INLINE = `
<div class = "p-3" style = "position : sticky; z-index: 100;">
    <v-row>
        <v-col>
            <multiselect 
                v-model="ticker_values" 
                :options="ticker_options"
                :multiple="true"
                track-by="name"
                :custom-label="ticker_name"            
                placeholder = "Select Tickers   "
                >
                    <div
                    class="selection-count"
                    slot="selection"
                    slot-scope="{ values, search, isOpen, remove }"
                    >
                        <template v-if="!isOpen && values.length">
                            {{ (values.slice(0, 1).map((value) => value.name)).toString() + ((values.length - 1) ? " ... " : "")}}                                 
                            <span class="badge badge-secondary">{{((values.length - 1) ? " +" : "") + ((values.length - 1) || "")}}</span> 
                            <b>{{((values.length - 1) ? " more" : "")}} </b>
                        </template>
                    </div>
            </multiselect>
        </V-col>

        <v-col>
            <multiselect 
                v-model="side_values" 
                :options="side_options"
                :multiple="true"
                track-by="side"
                :custom-label="side_name"                
                >
                    <div
                    class="selection-count"
                    slot="selection"
                    slot-scope="{ values, search, isOpen, remove }"
                    >
                        <template v-if="!isOpen && values.length">                                
                            <span v-if = "values.map((v)=>v.side).includes('BUY')" class = "BUY_btn trade">
                                BUY
                            </span>                           
                            <span v-if = "values.map((v)=>v.side).includes('SELL')" class = "SELL_btn trade">
                                SELL
                            </span> 
                        </template>
                    </div>
            </multiselect>
        </v-col>
            
        <v-col>
            <div>    
                <v-range-slider                                        
                    v-model = "pp_range"                                    
                    :min="min__profit_percentage"
                    :max="max__profit_percentage"
                    label="Profit %"                                        
                    ></v-range-slider>
            </div>
        </v-col>

        <v-col>
            <div>
                <v-range-slider
                    v-model = "rr_range"
                    :min="min__risk_reward"
                    :max="max__risk_reward"
                    step = 0.1
                    label="Risk $"
                    ></v-range-slider>
            </div>
        </v-col>
    </v-row>
</div>
`

const M_MULTISELECT =  `
<div>
    <v-data-table
        v-model="selected"
        :headers="headers"
        :items="__m_items"
        :search = "search"
        :height = "__m_height"
        :loading = "loading"
        loading-text="Loading... Please wait"
        mobile-breakpoint = 0
        disable-pagination
        item-key="name"
        show-select
        dense
        clipped
        fixed-header
        :class="this.$vuetify.theme.dark "
        hide-default-footer
        @click:row = "row_clicked"
        @item-selected="item_selected"        
        >
    </v-data-table>
</div>
`

const M_FILTER_SIDEBAR = `
<v-card>
    <v-container>
        <v-row dense>
            <v-col>
                <h5 class = "p-1">
                    <span class = "font-weight-bold"> Filters </span>
                    <span class = "float-right text-danger">Clear</span>
                </h5> 
            </v-col>
        </v-row>
        <v-row 
            class = "px-3"
            dense
            >
            <v-col
                class = "mt-2"
                dense
            >
                    <span class = "align-bottom font-weight-bold" style = "font-size : 14px">
                        Tickers
                    </span>             
            </v-col>
            <v-col
                cols  = "8"
                dense
                >
                <span class = "float-right">
                    <v-text-field 
                        v-model="search"
                        append-icon="mdi-magnify"
                        label="Search"
                        single-line
                        hide-details
                        dense
                    ></v-text-field>
                </span>
            </v-col>        
        </v-row>
        <v-row >
            <v-col class = "py-0">
                <v-container fluid>
                    <m-multiselect
                        :search = "search"
                        :items = "ticker_options"
                        @change = "update_selected_tickers"
                        >
                    </m-multiselect>
                </v-container>
            </v-col>
        </v-row>

        <v-row dense>
            <v-col
                class = "py-0 mt-2"
                dense>   
                <h6 class = "px-3">  
                    <span class = "align-bottom font-weight-bold">
                        Sides
                    </span>
                </h6>
            </v-col>
        </v-row>
        <v-row>
            <v-col 
            class = "py-0"
                dense
                >
                    <v-row class = "px-3">
                        <v-col dense
                        class = "py-0"
                        >
                        <v-checkbox v-model = "side_values" class = "as_radio mt-0" value = "BUY">
                            <template v-slot:label>
                                <span class = "BUY_btn trade">
                                    BUY
                                </span> 
                            </template>
                        </v-checkbox>
                        </v-col>
                        <v-col dense
                        class = "py-0"
                        >
                        <v-checkbox v-model = "side_values" class = "as_radio mt-0" value = "SELL">
                            <template v-slot:label>
                                <span class = "SELL_btn trade">
                                    SELL
                                </span> 
                            </template>
                        </v-checkbox>
                        </v-col>
                    </v-row>
            
            </v-col>        
        </v-row>

        
    <v-row dense>
        <v-col
            dense>   
            <h6 class = "px-3">  
                <span class = "align-bottom font-weight-bold">
                    Risk Reward Range
                </span>
            </h6>
        </v-col>
    </v-row>
    
    <v-row class = "px-5">
        <v-col 
            class = "pb-0"
            dense
            >
                <v-range-slider
                    v-model = "rr_range"
                    :min="min__risk_reward"
                    :max="max__risk_reward"
                    thumb-label="always"
                    :thumb-size="18"
                    step = 0.1
                    ticks
                    >
                </v-range-slider>
                <!--
                <v-row>
                    <v-col cols = "5">
                    <v-row class = "float-left">
                        <v-col col = "6" >Min : </v-col>
                        <v-col col = "6">
                            <v-text-field
                                v-model = "rr_range[0]"
                                label="min__risk_reward"
                                disable
                                solo
                                dense
                            ></v-text-field>
                        </v-col>
                    </v-row>
                    </v-col>
                    <v-spacer></v-spacer>
                    <v-col cols = "5">
                    <v-row class = "float-right">
                        <v-col col = "6">Max</v-col>
                        <v-col col = "6">
                            <v-text-field
                                v-model = "rr_range[1]"
                                label="min__risk_reward"
                                disable
                                solo
                                dense
                            ></v-text-field>
                        </v-col>
                    </v-row>
                    </v-col>
                </v-row> -->
        </v-col>        
    </v-row>

    
    

    <v-row dense>
        <v-col
            class = "py-0"
            dense>   
            <h6 class = "px-3">  
                <span class = "align-bottom font-weight-bold">
                    Profit Percent Range
                </span>
            </h6>
        </v-col>
    </v-row>
    
    <v-row class = "px-5">
        <v-col 
            dense
            >
                <v-range-slider
                    v-model = "pp_range"
                    :min="min__profit_percentage"
                    :max="max__profit_percentage"
                    thumb-label="always"
                    :thumb-size="18"
                    step = 1                    
                    ticks
                    >
                </v-range-slider>
                <!--
                <v-row>
                    <v-col cols = "5">
                        <v-row class = "float-left">
                            <v-col cols = "6" >Min : </v-col>
                            <v-col cols = "6">
                                <v-text-field
                                    v-model = "pp_range[0]"
                                    label="min__profit_percentage"
                                    disable
                                    solo
                                    dense
                                ></v-text-field>
                            </v-col>
                        </v-row>
                    </v-col>
                    <v-spacer></v-spacer>
                    <v-col cols = "5">
                        <v-row class = "float-right">
                            <v-col cols = "6">Max</v-col>
                            <v-col cols = "6">
                                <v-text-field
                                    v-model = "pp_range[1]"
                                    label = "max__profit_percentage"
                                    disable
                                    solo
                                    dense
                                ></v-text-field>
                            </v-col>
                        </v-row>
                    </v-col>
                </v-row> -->
        </v-col>        
    </v-row>



    </v-container>


</v-card>
`

const M_TABLE_WRAPPER = `
    <div class = "border" >
        <m-data-table-info ></m-data-table-info> 
        <m-data-table ref="stocktable" :items = "items" :fields = "fields" :headers = "headers" :state = "state" ></m-data-table>
    </div>
`

const M_DRAWER_FILTER = `

<v-navigation-drawer
        v-model="drawer"
        :expand-on-hover="true"
        :permanent="true"
        width = "30vw"
        absolute
        style = "z-index:100;"
        floating
      >
        <v-list-item
            link
            >
            <v-list-item-icon class = "mr-1">
              <v-icon class="fa fa-filter blue--text darken-4--text" aria-hidden="true"></v-icon>
            </v-list-item-icon>
            <v-list-item-content collapse>

                ${M_FILTER_SIDEBAR}
            </v-list-item-content>
        </v-list-item>   
    
</v-navigation-drawer>
`

const M_NAVIGATOR = `
    <v-card
    flat
    class="m-0 p-0"
    style= "background : transparent"
    >
            <v-row
                align="center"
                justify="center"
            >                
                <v-btn-toggle
                    v-model="toggle_exclusive"            
                    mandatory                    
                    @change="change_state"
                    rounded
                    
                    class = "mb-1"
                >
                    <v-btn active-class="active-head" class = "p-4">
                        
                                <span class = "title" > Intraday </span>
                    </v-btn>
                    <v-btn active-class="active-head" class = "p-4">
                        <span class = "title" > BTST </span>
                    </v-btn>
                    <v-btn active-class="active-head" class = "p-4">
                        <span class = "title" > Positional </span>
                    </v-btn>
                    <v-btn active-class="active-head" class = "p-4">
                        <span class = "title" > Longterm </span>
                    </v-btn>
                </v-btn-toggle>
            </v-row>
        
    </v-card>
`

const M_APP = `
<v-app>
<v-container fluid class = "blue lighten-5">
    <m-navigator class = "p-0"></m-navigator>
    <v-row>
        <v-col cols = "12" md = "3" class = "p-0">
            <v-row>
                <v-col cols = "12" md = "11" class = "float-left">
                    <m-filter-sidebar class = "elevation-7" style = "border-radius : 0.7rem" ></m-filter-sidebar>
                </v-col>
            </v-row>
         </v-col>
        <v-col cols = "12" md = "9"> 
            <m-table-wrapper class = "white elevation-13"  style = "border-radius : 0.7rem" ref="stocktable" :items = "items" :fields = "fields" :headers = "headers" :state = "state" >{{fields}}</m-table-wrapper>    
         </v-col>
    </v-row>
    <!-- <m-filter-sidebar ></m-filter-sidebar>
    <div style = "margin-left : 5vw !important;">
        <m-navigator ></m-navigator>
        <m-table-wrapper ref="stocktable" :items = "items" :fields = "fields" :headers = "headers" :state = "state" >{{fields}}</m-table-wrapper>    
    </div> -->
</v-container>
</v-app>
`