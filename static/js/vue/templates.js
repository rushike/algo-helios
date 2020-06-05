
const M_STOCKTABLE_TEMPLATE_STRING_ = `
    <div>
    
    <b-row >
        <b-col cols = "12">
        <b-table
                id="mercury-table"            
                ref = "b_table"
                hover            
                outlined
                     
                head-variant= "light"
                :items="items"
                :fields="fields"
                :search="search"            
                :filterIncludedFields="filterOn"            
                @filtered="onFiltered"
                >

                <!-- Ticker -->
                <template v-slot:cell(ticker)="data">
                    <span>
                            {{ data.item.ticker }}
                    </span>        
                </template>

                <!-- LTP  -->
                <template v-slot:cell(ltp)="data">
                    <span>
                            {{ data.item.ltp }}
                    </span>
                </template>
                
                <!-- Signal  -->
                <template v-slot:cell(signal)="data">
                    <b-button  type="button" :class="data.item.signal + '_btn trade'"  data-toggle="modal" 
                            data-target="#trade_modal">
                            {{ data.item.signal }}
                    </b-button>        
                </template>

                <!-- Time -->
                <template v-slot:cell(time)="data">
                    <span>

                            {{ data.item.time }}
                    </span>
                </template>

                <!-- Signal Price -->
                <template v-slot:cell(price)="data">
                    <span>                       
                            {{ data.item.price }}
                    </span>
                </template>

                <!-- Target Price -->
                <template v-slot:cell(target_price)="data">
                    <span>                       
                            {{ data.item.target_price }}
                    </span>
                </template>

                <!-- Stop Loss -->
                <template v-slot:cell(stop_loss)="data">
                    <span>                       
                            {{ data.item.stop_loss }}
                    </span>
                </template>

                <!-- Profit Percentage -->
                <template v-slot:cell(profit)="data">
                    <span>                       
                            {{ data.item.profit }}
                    </span>
                </template>

                <!-- Status -->
                <template v-slot:cell(status)="data">
                    <b-badge pill variant="primary" :class = "'badge white ' + data.item.status.toLowerCase() + '_status'">
                        {{ data.item.status }}</b-badge>
                </template>
            </b-table>
        </b-col>
    </b-row>
    </div>
`

const M_STOCKTABLE_TEMPLATE_STRING = `
<!--
<v-layout column style="height: 90vh">
    <v-flex md12 style="overflow: auto"> -->
        <v-data-table
            
            :headers="headers"
            :items="items"     
            :items-per-page = "items.length"
            :search = "search"
            :custom-filter = "portfolio_filter"
            fixed-header
            height="80vh"
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
                <v-badge variant="primary" :class = "'badge white rounded  ' + item.status.toLowerCase() + '_status'">
                    {{ item.status }}
                </v-badge>
            </template>
        </v-data-table>
        <!--
    </v-flex>
</v-layout> -->

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
        
            <v-col
                
            </v-col>
        </v-row>
        <v-row
            class="mb-6"
            >
            <v-col cols ="3" >
                <v-text-field
                    v-model="search"
                    append-icon="mdi-magnify"
                    label="Search"
                    single-line
                    hide-details
                ></v-text-field>
                <!-- <v-form-group
                class="mb-0"
                >
                <v-input-group size="sm">
                    <v-form-input                    
                    v-model="search"
                    type="search"
                    id="filterInput"
                    placeholder="Search ..."
                    class = "rounded"
                    ></v-form-input>
                    <!--
                    <v-input-group-append>
                        <v-button :disabled="!search" @click="search = ''">Clear</v-button>
                    </v-input-group-append> 
                </v-input-group>
                </v-form-group> -->
            </v-col>
            
            <v-col cols ="6"  >
                <v-row >
                    <v-col cols = "7">
                        <v-row>
                            <v-col cols ="6">
                                <span class = "0.7rem"> Total</span>                        
                                <v-badge pill variant="primary" >150</v-badge>
                            </v-col>

                            <v-col cols ="6">
                                <span class = "0.7rem"> Partial HIT</span>                        
                                <v-badge pill variant="succes" class = "partialhit_status">0</v-badge>
                            </v-col>
                        </v-row>
                    </v-col>

                    <v-col cols = "5">
                        <v-row>
                            <v-col cols ="6">
                                <span class = "0.7rem">HIT</span>
                                <v-badge pill variant="succes" class = "hit_status">0</v-badge>
                            </v-col>

                            <v-col cols ="6">
                                <span class = "0.7rem"> MISS</span>
                                <v-badge pill variant="danger">0</v-badge>                        
                            </v-col>
                        </v-row>
                    </v-col>

                    
                    
                </v-row>
            </v-col>

            <v-col cols="3">                            
                    <span id = "filter">
                        <a href="#" data-toggle="tooltip" data-placement="top" title="Filter">
                            <button toggle = "filter-collapse" class="btn filter get_filter"  data-toggle="modal" data-target="#{}_filter_modal">
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

                    <span href="#" data-toggle="tooltip" data-placement="top" title="Notify">
                        <button v-on:click = "allow_notification()" class="btn refresh user-notify" title="Refresh">
                            <small v-if = "notification"><span class="fa fa-bell-slash notify"></span></small>
                            <small v-else><span class="fa fa-bell notify"></span></small>
                        </button>
                    </span>                
            </v-col>            
        </v-row>
        <!-- <div id="filter-collapse">
            <hr>
            <m-filter-inline></m-filter-inline>
        <div> -->
        </div>
`

const M_FILTER_INLINE = `
    <div class = "p-3" style = "position : sticky; z-index: 100;">
        <v-row>
            <v-col>
                <multiselect 
                    v-model="ticker_values" 
                    :options="options"
                    :multiple="true"
                    track-by="library"
                    :custom-label="ticker_name"
                    :class="{invalid:myValue === null}"
                    placeholder = "Select Tickers   "
                    >
                        <div
                        class="selection-count"
                        slot="selection"
                        slot-scope="{ values, search, isOpen, remove }"
                        >
                            <template v-if="!isOpen && values.length">
                                {{ (values.slice(0, 1).map((value) => value.library)).toString() + ((values.length - 1) ? " ... " : "")}}                                 
                                <b-badge pill variant="secondary">{{((values.length - 1) ? " +" : "") + ((values.length - 1) || "")}}</b-badge> 
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
                    :class="{invalid:myValue === null}"
                    >
                        <div
                        class="selection-count"
                        slot="selection"
                        slot-scope="{ values, search, isOpen, remove }"
                        >
                            <template v-if="!isOpen && values.length">                                
                                <b-badge v-if = "values.map((v)=>v.side).includes('BUY')" variant="dark">
                                    BUY
                                </b-badge> 
                                <b-badge v-if = "values.map((v)=>v.side).includes('SELL')" variant="info">
                                    SELL
                                </b-badge> 
                            </template>
                        </div>
                </multiselect>
            </v-col>
                
            <v-col>
                <div>    
                    <v-form inline>
                        <label class="sr-only" for="range-1">Profit %</label>
                        <input                        
                        id="range-1" 
                        class="mb-2 mr-sm-2 mb-sm-0"
                        v-model="profit_percentage" type="range" min="0" max="5" step="0.5"
                        ></input>
                    </v-form-inline>
                </div>
            </v-col>

            <v-col>
                <div>
                    <v-form inline>
                        <label class="sr-only" for="range-2">Risk Reward</label>
                        <input                        
                            id="range-2"                             
                            class="mb-2 mr-sm-2 mb-sm-0"
                            v-model="risk_reward" type="range" min="0" max="5" step="0.5"
                        ></input>
                    </v-form-inline>
                </div>
            </b-col>
        </b-row>
    </div>
`

const M_TABLE_WRAPPER = `
    <div class = "border">
        
        <m-data-table-info></m-data-table-info> 
        <m-data-table ref="stocktable" :items = "items" :fields = "fields" :headers = "headers" :state = "state" ></m-data-table>
    </div>
`
