const M_STOCKTABLE_TEMPLATE_STRING = `

    <v-data-table
        
        :headers="headers"
        :items="filter_items"     
        :items-per-page = "items.length"
        :search = "search"
        :custom-filter = "portfolio_filter"
        fixed-header
        height="70vh"
        class="elevation-1"        
        style="max-height: calc(100vh ); backface-visibility: hidden;">
        
        
        <template v-slot:item.ticker="{ item }">
            <span>
                {{ item.ticker }}
            </span>
        </template>

        <template v-slot:item.signal="{ item }">
            <button rounded type="button" :class="item.signal + '_btn trade'"  data-toggle="modal" 
                data-target="#trade_modal">
                {{ item.signal }}
            </button> 
        </template>

        <template v-slot:item.status="{ item }">
            <span class = "'badge white rounded  ' + item.status.toLowerCase() + '_status'">
                {{ item.status }}
            </span>
        </template>
    </v-data-table>  
</v-responsive>
`

const M_EQUITY_TEMPLATE_STRING = `
<m-stocks-table ref="m_stocktable" :items = "items" :fields = "fields" :headers = "headers" :state = "state" >
</m-stocks-table>
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
    <div>
    <v-row
        class="m-3"
        no-gutters
        >
        <v-col cols ="12" md = "3" >
            <v-text-field
                v-model="search"
                append-icon="mdi-magnify"
                label="Search"
                single-line
                hide-details
            ></v-text-field>
            
                <!--
                <v-input-group-append>
                    <v-button :disabled="!search" @click="search = ''">Clear</v-button>
                </v-input-group-append> 
            </v-input-group>
            </v-form-group> -->
        </v-col>
        
        <v-col cols ="12" md = "6">
            <v-row >
                <v-col cols = "12" md = "6">
                    <v-row>
                        <v-col cols ="6" class = "text-center">                            
                            <v-badge pill variant="primary" color="blue" :content = "meta.total + ''">Total</v-badge>
                        </v-col>

                        <v-col cols ="6" class = "text-center">                                                  
                            <v-badge pill color="green accent-3" :content = "meta.partial_hit + ''">Partial Hit</v-badge>
                        </v-col>
                    </v-row>
                </v-col>

                <v-col cols = "6">
                    <v-row>
                        <v-col cols ="6" class = "text-center">
                            <v-badge pill color="green lighten-1"  :content = "meta.hit + ''">HIT</v-badge>
                        </v-col>

                        <v-col cols ="6" class = "text-center">
                            <v-badge pill color="red" :content = "meta.miss + ''">MISS</v-badge>                        
                        </v-col>
                    </v-row>
                </v-col>
            </v-row>
        </v-col>

        <v-col cols="12" md="3">
            <v-row align="center" justify="center">
            <v-col cols = "12" class = "text-center">
                <span id = "filter">
                    <a data-toggle="tooltip"  data-placement="top" title="Filter">
                        <button data-toggle = "collapse" data-target = "#filter-collapse" class="btn filter get_filter"  aria-expanded="false" aria-controls="filter-collapse">
                            <small><span class="fa fa-filter"></span></small>
                        </button>
                    </a>
                </span>

                <span id = "download">
                    <a href="#" data-toggle="tooltip" data-placement="top" title="Download">
                        <button class="btn download" onclick='exportTableToCSV("{}")'>
                            <small><span class="fa fa-download"></span></small>
                        </button>
                    </a>
                </span>
                <span >
                    <a href="#" data-toggle="tooltip" data-placement="top" title="Refresh">
                        <button class="btn refresh" id = "{}-refresh"  title="Refresh">
                            <small><span class="fa fa-refresh"></span></small>
                        </button>
                    </a>
                </span>

                <span href="#" data-toggle="tooltip" onclick="make_notification_ajax_call()" data-placement="top" title="Notify">
                    <button class="btn refresh user-notify"  title="Refresh">
                        <small><span class="fa fa-bell-slash notify"></span></small>
                    </button>
                </span>    
                </v-col>
                </v-row>            
        </v-col>            
    </v-row>
    <div id="filter-collapse" class = "collapse">
        <hr>
        <m-filter-inline></m-filter-inline>
    </div>
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

const M_TABLE_WRAPPER = `
    <div class = "border">
        <m-data-table-info></m-data-table-info> 
        <m-data-table ref="stocktable" :items = "items" :fields = "fields" :headers = "headers" :state = "state" ></m-data-table>
    </div>
`
const M_NAVIGATOR = `
<div>

    <v-card
    flat
    class=""
    >
        <v-card-text>
            <v-row
                align="center"
                justify="center"
            >
                <v-btn-toggle
                    v-model="toggle_exclusive"            
                    mandatory
                    rounded

                    @change="change_state"
                >
                    <v-btn active-class="active-head" >
                        Intraday
                    </v-btn>
                    <v-btn active-class="active-head">
                        BTST
                    </v-btn>
                    <v-btn active-class="active-head">
                        Positional
                    </v-btn>
                    <v-btn active-class="active-head">
                        Longterm
                    </v-btn>
                </v-btn-toggle>
            </v-row>
        </v-card-text>
    </v-card>
</div>
`

const M_APP = `
<v-app>
<div>
    <m-navigator></m-navigator>
    <m-table-wrapper ref="stocktable" :items = "items" :fields = "fields" :headers = "headers" :state = "state" >{{fields}}</m-table-wrapper>    
</div>
</v-app>
`