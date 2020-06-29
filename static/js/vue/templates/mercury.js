const M_TRADE_MODAL = `
    <v-row justify="center" >
      <v-dialog v-if = "item" v-model="show" persistent max-width="600px">        
        <v-card :class = "trade_wrapper_class(item.signal)">
          <v-card-title :class="'text-center mx-auto ' + trade_header_class(item.signal) ">
            <span class="headline font-weight-bold" style="font-size: 16px!important;">{{item.ticker.toUpperCase()}}</span>
          </v-card-title>
          <v-card-text class = "p-3 pt-0">
            <v-container style="font-size: 13px;">
              <v-row>
                <v-col cols="6" class="py-0">
                    <v-select
                        v-model="broker"
                        :items="[{text : 'Zerodha'}, { text : 'Upstox', disabled : true}, { text : 'HDFC Sec', disabled : true}, { text : 'Kotak Sec', disabled : true}, { text : 'ICIC Direct', disabled : true}, { text : 'Edelweiss', disabled : true}]"                        
                        label="Broker"
                        data-vv-name="select"
                        required
                        
                        class="m-0"
                  ></v-select>
                </v-col>
                <v-col cols="6" class="py-0" >
                    <v-radio-group
                        v-model = "exec_type"
                        mandatory
                        row 
                        class="m-0"              
                  >
                    <v-radio label="REG" :color = "bg_color(item.signal)" background-color = "bg_color(item.signal)" value = "regular"></v-radio>
                    <v-radio label="BO" :color = "bg_color(item.signal)" value = "bo"></v-radio>
                    <v-radio label="CO" :color = "bg_color(item.signal)" value = "co"></v-radio>
                  </v-radio-group>
                </v-col>
            </v-row>            
            <v-row>
                <v-col cols="6" class="py-0">
                        <v-radio-group
                        v-model = "trade_type"
                        disabled
                        mandatory
                        row 
                        class="m-0"                   
                        >
                            <v-radio label="MIS" :color = "bg_color(item.signal)" value = "MIS"></v-radio>
                            <v-radio label="CNC" :color = "bg_color(item.signal)" value = "CNC"></v-radio>                            
                        </v-radio-group>                        
                </v-col>
                <v-col cols="6" class="py-0 ">
                    <v-radio-group
                        v-model = "order_type"                        
                        mandatory
                        row
                        class="m-0" 
                        >
                            <v-radio label="MARKET" :color = "bg_color(item.signal)" value = "MARKET"></v-radio>
                            <v-radio label="LIMIT" :color = "bg_color(item.signal)" value = "LIMIT"></v-radio>                            
                        </v-radio-group>                        
                </v-col>                
              </v-row>
              <hr role="separator" aria-orientation="horizontal" class="mercury-divider" :style = "'margin-top:0px; background-color:' + bg_color(item.signal) + '; '">
              <v-row>
                    <v-col cols="6" class="py-0">
                        <v-text-field
                        label="Quantity"
                        :value = "quantity"
                        type = "number"
                        outlined
                        dense
                        ></v-text-field>
                    </v-col>
                    <v-col cols="6" class="py-0">
                        <v-text-field
                        label="Disclosed Quantity"
                        :value = "disclosed_quantity"
                        type = "number"
                        outlined
                        dense
                        ></v-text-field>
                    </v-col>
                </v-row>
                <v-row>
                    <v-col cols="6" class="py-0">
                        <v-text-field
                        label="Price"
                        :value = "item.price"
                        type = "number"                        
                        outlined
                        dense
                        ></v-text-field>
                    </v-col>
                    <v-col cols="6" class="py-0">
                        <v-text-field
                        label="Target Price"
                        :value = "item.target_price"
                        type = "number"                        
                        outlined
                        dense
                        ></v-text-field>
                    </v-col>
                </v-row>                
                <v-row v-if = "exec_type.toLowerCase() == 'bo'">
                    <v-col cols="4" class="py-0">
                        <v-text-field
                        label="TP"
                        :value = "item.target_price"
                        type = "number"
                        outlined
                        dense
                        ></v-text-field>
                    </v-col>
                    <v-col cols="4" class="py-0">
                        <v-text-field
                        label="SL"
                        :value = "item.stop_loss"
                        type = "number"
                        outlined
                        dense
                        ></v-text-field>
                    </v-col>
                    
                    <v-col cols="4" class="py-0">
                        <v-text-field
                        label="Trailing SL"
                        type = "number"
                        :value = "0"
                        outlined
                        dense
                        ></v-text-field>
                    </v-col>
                </v-row>
            </v-container>            
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" text @click="closed()">Close</v-btn>
            <button id = "trade_action" :class = "'btn ' + trade_btn_class(item.signal)" color="blue darken-1" text @click="place_order()">{{item.signal.toUpperCase()}}</button>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-row>  
`



const M_STOCKTABLE_TEMPLATE_STRING = `
<div>
    <m-trade-modal :item = "trade_item" @closed = "show_trade_modal()"></m-trade-modal>
    <v-bottom-sheet v-model="sheet" persistent>
        
        <!-- <v-sheet class="text-center"> -->
        <v-btn
            class="mt-6"
            text
            color="white"
            @click="show_details()"
            style="font-size: 2rem;"
        >×</v-btn>
        <v-list v-if = "detail_item">
            <v-list-item two-line>
                <v-list-item-content>
                  <v-list-item-title class="text-left" style="font-size: 16px;">{{detail_item.ticker.toUpperCase()}}</v-list-item-title>
                  <v-list-item-subtitle>
                    <v-row>
                        <v-col cols= "3">
                                
                                    <img 
                                            v-if = "detail_item.follow"
                                            class = "px-1 fa-2x" 
                                            v-on:click="follow_my_trade(detail_item, false)" 
                                            src="/static/img/pin-slash.svg"
                                            style = "cursor:pointer; height : 12px;" 
                                            ></img>
                                            
                                    <img 
                                        v-else
                                        class = "px-1 fa-2x" 
                                        v-on:click="follow_my_trade(detail_item, true)" 
                                        src="/static/img/pin.svg"                                     
                                        style = "cursor:pointer; height : 12px;" 
                                        aria-hidden="true"                                     
                                        ></img>    
                                
                                <span>
                                    Pin
                                </span>
                        </v-col>
                        <v-col cols= "3">
                            
                                <img                                     
                                class = "px-1 fa-2x" 
                                v-on:click="delete_call(detail_item)" 
                                src="/static/img/bin.svg" 
                                data-toggle="tooltip" data-placement="top" title="Delete Call"
                                style = "cursor:pointer; height : 12px;"                             
                                ></img> 
                            
                            <span>
                                Delete
                            </span>
                        </v-col>                            
                    </v-row>

                  </v-list-item-subtitle>
                </v-list-item-content>
                <v-list-item-action>
                    <button rounded type="button"  :class="detail_item.signal + '_btn trade elevation-7 ' + (detail_item.active ? ' ' : 'inactive ')"  data-toggle="modal" 
                                    data-target="#trade_modal" @click = "show_trade_modal(detail_item)">
                        <span >            
                            {{ detail_item.signal }}
                        </span>
                    </button>
                  </v-list-item-action>
              </v-list-item>
              <div class="card px-3 border-bottom-0" style="font-size: 11px;font-weight: 500;">
                <v-row>
                    <v-col class="py-1">
                        <span class="float-left">
                            <span >Targert Price : </span>
                            <span>{{detail_item.target_price}}</span>
                        </span>
                    </v-col>
                    <v-col class="py-1">
                        <span class="float-right">
                            <span >LTP : </span>
                            <span>{{detail_item.ltp}}</span>
                        </span>
                    </v-col>
                </v-row>                
                <v-row>
                    <v-col class="py-1">
                        <span class="float-left">
                            <span >Stop Loss : </span>
                            <span>{{detail_item.stop_loss}}</span>
                        </span>
                    </v-col>
                    <v-col class="py-1">
                        <span class="float-right">
                            <span >Signal Price : </span>
                            <span>{{detail_item.price}}</span>
                        </span>
                    </v-col>
                </v-row>
                <v-row>
                    <v-col class="py-1">
                        <span class="float-left">
                            <span >Signal Time : </span>
                            <span>{{detail_item.time}}</span>
                        </span>
                    </v-col>
                    <v-col class="py-1">
                        <span class="float-right">
                            <span >Profit % : </span>
                            <span>{{detail_item.profit}}</span>
                        </span>
                    </v-col>
                </v-row>
            </div>
        </v-list>

        <!-- </v-sheet> -->
    </v-bottom-sheet>
    <div
        v-dragscroll
    >
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
        mobile-breakpoint = "500"
        height="70vh"
        class="elevation-1"        
        style="max-height: calc(100vh ); backface-visibility: hidden;"
        hide-default-footer
        fixed-header>

        <template v-slot:header.action="{header}" >
        <span >
            Action
            <!-- <span style="position: relative;"> -->
            <span v-on:click = "table_settings_toggle()" class = "pl-2" style = "font-size : 1rem; cursor : pointer; position: absolute; top: 15%;right: -5px;">   
                <v-menu bottom left>
                    <template v-slot:activator="{ on, attrs }">
                    <v-btn
                        dark
                        icon
                        v-bind="attrs"
                        v-on="on"
                    >
                    <v-tooltip top>
                        <template v-slot:activator="{ on, attrs }">
                            <img 
                                src = "/static/img/edit-pencil.svg"
                                class = "fa-2x" 
                                style = "color:rgb(0, 0, 0, 0.6);height:30%"  
                                v-bind="attrs"
                                v-on="on"                              
                            ></img>
                        </template>
                        <span>Customize Table</span>
                    </v-tooltip>
                  
                    </v-btn>
                    </template>
                
                    <v-container fluid class = "white">
                        
                        <m-multiselect
                            :search = "search"
                            :items = "fields_"
                            :selected_all = "selected_fields_"
                            @change = "update_selected_fields"
                            >
                        </m-multiselect>
                    </v-container>

                </v-menu>
            </span>
        </span>
            <!-- </span> -->
        </template>
        
        <template v-slot:group.header="{group, groupBy}" >

        </template>

        <template v-if = "is_mobile()"  v-slot:group="{group, options, items, headers}">
            <v-card v-for = "(item, index) in items" v-if = "is_mobile() && item.visible" :class="row_class(group, index, item, items) + ' border p-2 '" @click = "show_details(item)">   
                    <v-container fluid style="font-size: 12px;">                 
                        <v-row  >
                            <v-col cols = "2" class = "p-1"  @click = "show_trade_modal(item)">
                                <button rounded type="button"  :class="item.signal + '_btn trade elevation-7 ' + (item.active ? ' ' : 'inactive ')"  data-toggle="modal" 
                                    data-target="#trade_modal">
                                    <span >            
                                        {{ item.signal }}
                                    </span>
                                </button>
                            </v-col>
                            <v-col cols = "3" class = "p-1">
                                {{item.ticker.toUpperCase()}}
                            </v-col>
                            <v-spacer></v-spacer>
                            <v-col cols = "2" class = "p-1 pr-0">
                                <span class="float-right">{{item.ltp}}</span>
                            </v-col>
                            <v-col cols = "2" class = "p-1">
                                <span :class = "'badge elevation-7 ' + item.status.toLowerCase() + '_status float-right '">
                                    {{ item.status }}
                                </span>
                            </v-col>
                        </v-row>
                        <v-row>
                            <v-col cols = "3"  class = "p-1">
                                TP : {{item.target_price}}
                            </v-col>
                            <v-col cols = "3"  class = "p-1">
                                SL : {{item.stop_loss}}
                            </v-col>
                            <v-spacer></v-spacer>                            
                            <v-col cols = "3" class = "p-1">
                                <span class="float-right">{{item.time}}</span>
                            </v-col>
                        </v-row>
                    </v-container>
                </v-card>
        </template>        
        <template v-else v-slot:group="{group, options, items, headers}" >
                <tr v-for = "(item, index) in items" v-if = "item.visible" :class = "row_class(group, index, item, items) + (item.ltp.instrument_id)" :id = "item.call_id">
                    <td  v-for = "header in headers" >
                        <span v-if = "header.key == 'signal'" @click = "show_trade_modal(item)">
                            <button rounded type="button"  :class="item.signal + '_btn trade shadow ' + (item.active ? ' ' : 'inactive ')"  data-toggle="modal" 
                                data-target="#trade_modal">
                                <span >            
                                    {{ item.signal }}
                                </span>
                            </button>
                        </span>
                        <span v-else-if = "header.key == 'status'">
                            <span :class = "'badge shadow ' + item.status.toLowerCase() + '_status'">
                                {{ item.status }}
                            </span>
                        </span>
                        <span v-else-if = "header.key == 'ticker'">
                            <span v-if = "item.product_type == 'OPT'">
                                <span class="options-ticker">{{ item.underlying.toUpperCase() }}</span> 
                                <span class="option-type badge badge-warning px-1">{{(item.option_type ? item.option_type.toUpperCase() : "CE")}}</span>
                                <!-- <span class="">@</span> -->
                                <br>
                                <span class="options-strike">{{ item.strike }}</span> 
                                <!-- <span class="">@</span> -->
                                <span class="options-expiry">{{item.expiry}}</span>
                                <!-- <span class="">@</span> -->
                                
                            </span>                        
                            <span v-else>
                                {{item.ticker}}
                            </span>
                        </span>
                         <span v-else-if = "header.key == 'action'" style = "width : '3rem'">                            
                            <v-tooltip top>
                                <template v-slot:activator="{ on, attrs }">
                                    <img 
                                        v-if = "item.follow"
                                        class = "px-1 fa-2x" 
                                        v-on:click="follow_my_trade(item, false)" 
                                        src="/static/img/pin-slash.svg" 
                                        data-toggle="tooltip" data-placement="top" title="Pin Call" style = "cursor : pointer; height : 30%;" 
                                        aria-hidden="true"
                                        v-bind="attrs"
                                        v-on="on"
                                        ></img>
                                        
                                    <img 
                                        v-else
                                        class = "px-1 fa-2x" 
                                        v-on:click="follow_my_trade(item, true)" 
                                        src="/static/img/pin.svg" 
                                        data-toggle="tooltip" data-placement="top" title="Pin Call"
                                        style = "cursor:pointer; height : 30%;" 
                                        aria-hidden="true" 
                                        v-bind="attrs"
                                        v-on="on"
                                        ></img>
                                </template>
                                <span>Pin Call</span>
                            </v-tooltip>
                            <v-tooltip top>
                                <template v-slot:activator="{ on, attrs }">
                                    <img                                     
                                        class = "px-1 fa-2x" 
                                        v-on:click="delete_call(item)" 
                                        src="/static/img/bin.svg" 
                                        data-toggle="tooltip" data-placement="top" title="Delete Call"
                                        style = "cursor:pointer; height : 30%;" 
                                        aria-hidden="true" 
                                        v-bind="attrs"
                                        v-on="on"
                                        ></img>                                
                                </template>
                                <span>Delete Call</span>
                              </v-tooltip>
                            
                        </span> 
                        <span v-else>                        
                            {{item[header.key]}}
                        </span>
                    </td>
                </tr>      
        </template>        
    </v-data-table>  
</div>
</div>
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
            :style="'max-height: calc(100vh ); backface-visibility: hidden; '">
            
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
        <v-col v-if = "!is_mobile()"  cols="12" md = "5"  class="p-0">
            <v-row >
                <v-col cols = "6" md = "6" class = " p-3">
                    <span class = "head-tickers px-2">
                        NIFTY 50
                    </span>
                    <span class = "head-ticks px-2">{{nifty_50_tick()}}</span>
                </v-col>
                <v-col cols = "6" md = "6" class = " p-3">
                    <span class = "head-tickers px-2">
                        NIFTY BANK
                    </span>
                    <span class = "head-ticks px-1">{{nifty_bank_tick()}}</span>
                </v-col>
            </v-row>
        </v-col>
        
        <v-col cols ="7" md = "7" class = "text-center p-0 stats-wrapper">
            <v-row class="p-1">
                <v-col cols ="3" class = "text-center p-0">                            
                    <span pill variant="primary" color="blue" :content = "'Total'" class = "total--text font-weight-bold stats-head">{{meta.total}}</span><br v-if = "is_mobile()">
                    <span class = "total--text  meta-text"> Total</span>
                </v-col>

                <v-col cols ="3" class = "text-center p-0">                                                  
                    <span pill color="green accent-3" :content = "'Partial HIT'" class = "partialhit_status--text font-weight-bold stats-head">{{meta.partial_hit}}</span><br v-if = "is_mobile()">
                    <span class = "partialhit_status--text  meta-text"> Partial Hits</span>
                </v-col>
                <v-col cols ="3" class = "text-center p-0">
                    <span pill color="green lighten-1"  :content = "'HIT'" class = "hit_status--text font-weight-bold stats-head">{{meta.hit}}</span><br v-if = "is_mobile()">
                    <span class = "hit_status--text  meta-text">Hits</span>
                </v-col>

                <v-col cols ="3" class = "text-center p-0">
                    <span pill color="red" :content = "'MISS'" class = "miss_status--text font-weight-bold stats-head">{{meta.miss}}</span><br v-if = "is_mobile()">
                    <span class = "miss_status--text  meta-text"> Miss</span>
                </v-col>                    
            </v-row>
        </v-col>
        <v-col v-if = "is_mobile()" cols = "5"  >
            <v-row align="center" justify="center" :class = "is_mobile() ? 'text-center ' : 'float-right center pt-3' " >
                <v-col cols = "12" class = "p-1" >
                                <a href="#" data-toggle="tooltip" data-placement="top" title="Download" >
                                    <button class="btn download" v-on:click='download_as_csv()' style="margin: 0px;">
                                        <small><span class="fa fa-download notify" style="font-size: 16px;"></span></small>
                                    </button>
                                </a>                            
                    </span>
                    <span >                      
                                <a href="#" data-toggle="tooltip" data-placement="top" title="Refresh"  >
                                    <button class="btn refresh" v-on:click = "refresh_table()" id = "refresh"  title="Refresh" style="margin: 0px;">
                                        <small><span class="fa fa-refresh notify" style="font-size: 16px;"></span></small>
                                    </button>
                                </a>                           
                    </span>
                    <span>                       
                                <span href="#" data-toggle="tooltip" data-placement="top" title="Notify" >
                                    <button class="btn refresh user-notify" v-on:click = "allow_notification()" title="notify" style="margin: 0px;">
                                        <small v-if = "notification" ><span class="fa fa-bell-slash notify" style="font-size: 1rem;"></span></small>
                                        <small v-else><span class="fa fa-bell notify" style="font-size: 16px;"></span></small>
                                    </button>
                                </span>                           
                    </span>
                </v-col>
            </v-row>      
        </v-col>
    </v-row>
    
    <v-row
        class="mx-3"
        no-gutters
        >
        <v-col cols = "6" md = "3" lg = "3" class = "px-1">
            <v-text-field
                v-model="search"
                class = "px-1 p-1  blue lighten-5"
                rounded
                append-icon="mdi-magnify"
                label="Search"
                single-line
                hide-details
                dense
                :style=" is_mobile() ? ' font-size: 10px;' : ' font-size:13px' "
            ></v-text-field>
        </v-col>
        
        <v-col cols = "6" md = "3" lg = "3" class = "px-1">    
            <v-select
                class = "mx-1 shadow"
                v-model="type"
                :items="equity_type"
                menu-props="auto"
                label="Select"
                hide-details          
                single-line
                dense
                solo     
                :style=" is_mobile() ? ' font-size: 10px;' : ' font-size:13px' "
                >
            </v-select>    
        </v-col>        
        <v-spacer></v-spacer>
        <v-col v-if = "!is_mobile()" md = "4"  >
            <v-row align="center" justify="center" :class = "is_mobile() ? 'text-center ' : 'float-right ' ">
                <v-col cols = "12" class = "p-1" >
                    <!-- <span id = "filter">
                        <a data-toggle="tooltip"  data-placement="top" title="Filter">
                            <button data-toggle = "collapse" data-target = "#filter-collapse" class="btn filter get_filter"  aria-expanded="false" aria-controls="filter-collapse">
                                <small><span class="fa fa-filter"></span></small>
                            </button>
                        </a>
                    </span> -->

                    <span id = "download">
                        <v-tooltip top>
                            <template v-slot:activator="{ on, attrs }">
                                <a href="#" data-toggle="tooltip" data-placement="top" title="Download" v-bind="attrs" v-on="on">
                                    <button class="btn download" v-on:click='download_as_csv()'>
                                        <small><span class="fa fa-download notify" style="font-size: 1rem;"></span></small>
                                    </button>
                                </a>
                            </template>
                            <span>Download</span>
                        </v-tooltip>
                    </span>
                    <span >
                        <v-tooltip top>
                            <template v-slot:activator="{ on, attrs }">
                                <a href="#" data-toggle="tooltip" data-placement="top" title="Refresh"  v-bind="attrs" v-on="on">
                                    <button class="btn refresh" v-on:click = "refresh_table()" id = "refresh"  title="Refresh">
                                        <small><span class="fa fa-refresh notify" style="font-size: 1rem;"></span></small>
                                    </button>
                                </a>
                            </template>
                            <span>Refresh</span>
                        </v-tooltip>
                    </span>
                    <span>
                        <v-tooltip top>
                            <template v-slot:activator="{ on, attrs }">
                                <span href="#" data-toggle="tooltip" data-placement="top" title="Notify" v-bind="attrs" v-on="on">
                                    <button class="btn refresh user-notify" v-on:click = "allow_notification()" title="notify">
                                        <small v-if = "notification" ><span class="fa fa-bell-slash notify" style="font-size: 1rem;"></span></small>
                                        <small v-else><span class="fa fa-bell notify" style="font-size: 1rem;"></span></small>
                                    </button>
                                </span>
                            </template>
                            <span>Notify</span>
                        </v-tooltip>
                    </span>
                </v-col>
            </v-row>      
        </v-col>
    </v-row>
    <!-- <div :id = "is_mobile__class()" :class = "show_table_settings__class()">
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
    </div> -->

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
            @toggle-select-all = 'item_selected'  
            >
        </v-data-table>        
</div>
`

const M_FILTER_SIDEBAR = `
<v-card >
    <v-container>
        <v-row dense>
            <v-col>
                <h5 class = "p-1">
                    <span class = "font-weight-bold"> Filters </span>
                    <span class = "float-right text-danger h6" v-on:click = "clear_filter()" style = "cursor:pointer">Clear</span>
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
                        :selected_all = "ticker_values"
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
<div
>
<v-navigation-drawer
        v-model="drawer"        
        fixed

        temporary        
        height = "100vh"
        width = "80vw"
        
      >
        <v-list-item        
            >
            <v-list-item-content >

                ${M_FILTER_SIDEBAR}
            </v-list-item-content>
        </v-list-item>   
        <v-list-item
            link
            >
            <v-list-item-content class = "text-center">
                <a class="navbarlogo" href="{%url 'index'%}">
                    <img id="logo" src="/static/algonauts.png" width="80vh" height="auto">
                </a>
            </v-list-item-content>
        </v-list-item> 
</v-navigation-drawer>
</div>

`

const M_NAVIGATOR = `
<v-container class="px-3" >
    <v-row v-if = "is_mobile()">
        <v-col class="px-3">
            <v-select
                v-model = "active_portfolio"
                class="px-3"
                :items="portfolios.map(v=>v.toUpperCase())"
                label="Solo field"
                dense
                solo
          ></v-select>
        </v-col>
    </v-row>
    <v-item-group
            v-else
            v-model="toggle_exclusive"            
            mandatory
            @change="change_state" 
        >
            <v-container>
                
                <v-row>
                    <v-col                
                    cols="12"
                    md="3"
                    v-for = "n in 4" 
                    class="py-0"
                    >
                    <div v-if="false"> loop starts with 1 </div>
                        <v-item v-slot:default="{ active, toggle }" active-class="active-head" class = "p-2 shadow-2" :value = "n - 1" :disabled = "true"> 
                            <v-card                                
                                :disabled = "portfolio_clickable(n-1)"
                                @click="toggle"
                                no-gutters
                                dense
                                class="align-center py-2 text-center mx-2 temp-white"

                                style="cursor: pointer;"

                            >
                            <span class = "text-center title-mercury" >{{portfolios[n-1].toUpperCase()}} </span>
                            </v-card>
                        </v-item>
                    </v-col>
                </v-row>

            </v-container>
    </v-item-group>    
</v-container>        
`



const M_APP = `
<v-app     
    v-touch="{
        left: () => swipe('left'),
        right: () => swipe('right'),
        up: () => swipe('up'),
        down: () => swipe('down')
    }"
    style="min-height: 50vh;">
    <v-app-bar
      
      color="white"                  
    >
        <a class="navbarlogo" href="/">
            <img id="logo" src="/static/algotext.png" width="130px" height="auto">
        </a>
            
            <v-spacer></v-spacer>
            <v-toolbar-title class= "font-weight-bold">MERCURY</v-toolbar-title>
            <v-spacer></v-spacer>        
            <span v-if="false">
                <v-menu
                
                    class="mx-2 p-1"
                    v-for="([text, rounded], index) in [['Removed', '0'],]"
                    :key="'notification-key'"
                    :rounded="rounded"
                    offset-y
                    :max-width = "is_mobile() ? '20%' : '80%'"
                >
                    <template v-slot:activator="{ attrs, on }">
                    <span
                        v-bind="attrs"
                        v-on="on"
                        style="min-width: 2rem;text-align: center;"
                    >
                        <v-badge
                            bordered
                            color="error"
                            :content = "notifications.length"
                            link           
                            >
                            <span class="fa fa-bell notify" style="font-size: 1rem;"></span>
                        </v-badge>
                    </span>
                    </template>
            
                    <v-list three-line>
                        <template v-for="(item, index) in notifications">
                            
                            <v-subheader
                                v-if="item.header"
                                :key="item.header"
                                v-text="'Today'"
                            ></v-subheader>
                
                            <v-divider
                                v-else-if="item.divider"
                                :key="index"
                                :inset="item.inset"
                            ></v-divider>
                    
                            <v-list-item
                                v-else
                                :key="item.title"
                                @click=""
                            >
                                <v-list-item-content>
                                    
                                    <v-list-item-title v-html="item.title"></v-list-item-title>
                                    <v-list-item-subtitle v-html="item.subtitle"></v-list-item-subtitle>                                
                                </v-list-item-content>
                            </v-list-item>
                        </template>
                    </v-list>
                </v-menu>
            </span>
            <v-menu
                class="mx-2 p-1"
                v-for="([text, rounded], index) in [['Removed', '0'],]"
                :key="text"
                :rounded="rounded"
                offset-y                
            >
                <template v-slot:activator="{ attrs, on }">
                <span
                    v-bind="attrs"
                    v-on="on"
                    style="min-width: 6rem;text-align: center;"
                >
                    {{ user.first_name }}
                    <i class="fa fa-caret-down pl-2" aria-hidden="true"></i>
                </span>            
                </template>
        
                <v-list>
                <v-list-item             
                    link
                    href = "/user/profile/info/" tag = "div"
                >
                    <v-list-item-title v-text="'Dashboard'" ></v-list-item-title>
                </v-list-item>
                <v-list-item link href = "/user/feedback/" tag = "div">
                    <v-list-item-title v-text="'Feedback'" ></v-list-item-title>
                </v-list-item>
                <v-list-item link  href = "/worker/mercury" tag = "div">
                    <v-list-item-title v-text="'Mercury'"></v-list-item-title>
                </v-list-item>
                <form method="post" id="logout" action="/accounts/logout/">
                    <input type="hidden" name="csrfmiddlewaretoken" :value="get_csrf_token()" hidden> 
                    <v-list-item link type = submit onclick="this.closest('form').submit();return false;" class = "link-unstyled dark-gray">
                        
                        <v-list-item-title v-text="'Sign Out'" >
                        </v-list-item-title>
                    </v-list-item>
                </form>
                </v-list>
            </v-menu>
        </v-app-bar>
        
        <v-sheet
            id="scrolling-techniques-7"
            class="overflow-y-auto"
            max-height="90vh"
            max-width = "100vw"
        >

            <v-container fluid class = " blue lighten-5 container-fluid" style="min-width: 100vw;max-width: 10000px;">
                <v-row>
                    <v-col
                        v-if="!is_mobile()"
                        style="width: 21%; flex: 1 0 21%;max-width:22%;" 
                    >

                    </v-col>
                    <v-col class="p-0">
                        <m-navigator class = "p-0" style="min-width: 2px; max-height: 10%;"></m-navigator>
                    </v-col>
                </v-row>
                <v-row>    
                    <v-col 
                        v-if = "!is_mobile()"
                        style="width: 21%; flex: 1 0 21%;max-width:22%;" 
                        class = "p-0">
                        <v-row>
                            <v-col cols = "12" md = "11" class = "float-left">
                                <m-filter-sidebar class = "elevation-7" style = "border-radius : 0.7rem" ></m-filter-sidebar>
                            </v-col>
                        </v-row>
                    </v-col>
                    <v-col v-else>
                        <m-filter-sidebar ></m-filter-sidebar>
                    </v-col>
                    <v-col :cols= "is_mobile() ? '12' : ''" :style=" is_mobile() ? ' margin-top: -15%; ' : ' '"> 
                        <m-table-wrapper class = "white elevation-13"  style = "border-radius : 0.7rem;max-height: 90%;" ref="stocktable" :items = "items" :fields = "fields" :headers = "headers" :state = "state" >{{fields}}</m-table-wrapper>    
                    </v-col>
                </v-row>
                <!-- <m-filter-sidebar :drawer = "drawer"></m-filter-sidebar>
                <div style = "margin-left : 5vw !important;">
                    <m-navigator ></m-navigator>
                    <m-table-wrapper ref="stocktable" :items = "items" :fields = "fields" :headers = "headers" :state = "state" >{{fields}}</m-table-wrapper>    
                </div> -->
            </v-container>
        </v-sheet>
</v-app>
`