const M_TRADE_MODAL = `
    <v-row justify="center">
      <v-dialog v-if = "item" v-model="show" persistent max-width="600px">        
        <v-card>
          <v-card-title class="text-center mx-auto">
            <span class="headline">{{item.ticker.toUpperCase()}}</span>
          </v-card-title>
          <v-card-text>
            <v-container style="font-size: 13px;">
              <v-row>
                <v-col cols="6" class="py-0">
                    <v-select
                        v-model="broker"
                        :items="['Zerodha', 'Upstox', 'HDFC Sec', 'Kotak Sec', 'ICIC Direct', 'Edelweiss']"                        
                        label="Broker"
                        data-vv-name="select"
                        required
                        readonly
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
                    <v-radio label="REG" value = "regular"></v-radio>
                    <v-radio label="BOO" value = "bo"></v-radio>
                    <v-radio label="CO" value = "co"></v-radio>
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
                            <v-radio label="MIS" value = "MIS"></v-radio>
                            <v-radio label="CNC" value = "CNC"></v-radio>                            
                        </v-radio-group>                        
                </v-col>
                <v-col cols="6" class="py-0 ">
                    <v-radio-group
                        v-model = "order_type"                        
                        mandatory
                        row
                        class="m-0" 
                        >
                            <v-radio label="MARKET" value = "MARKET"></v-radio>
                            <v-radio label="LIMIT" value = "LIMIT"></v-radio>                            
                        </v-radio-group>                        
                </v-col>                
              </v-row>
              <v-divider></v-divider>
              <v-row>
                    <v-col cols="6" class="py-0">
                        <v-text-field
                        label="Quantity"
                        :value = "quantity"
                        outlined
                        dense
                        ></v-text-field>
                    </v-col>
                    <v-col cols="6" class="py-0">
                        <v-text-field
                        label="Disclosed Quantity"
                        :value = "disclosed_quantity"
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
                        readonly
                        outlined
                        dense
                        ></v-text-field>
                    </v-col>
                    <v-col cols="6" class="py-0">
                        <v-text-field
                        label="Target Price"
                        :value = "item.target_price"
                        readonly
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
                        outlined
                        dense
                        ></v-text-field>
                    </v-col>
                    <v-col cols="4" class="py-0">
                        <v-text-field
                        label="SL"
                        :value = "item.stop_loss"
                        outlined
                        dense
                        ></v-text-field>
                    </v-col>
                    
                    <v-col cols="4" class="py-0">
                        <v-text-field
                        label="Trailing SL"
                        :value = "0"
                        outlined
                        dense
                        ></v-text-field>
                    </v-col>
                </v-row>
            </v-container>
            <small>*indicates required field</small>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" text @click="closed()">Close</v-btn>
            <v-btn id = "trade_action" color="blue darken-1" text @click="place_order()">{{item.signal.toUpperCase()}}</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-row>  
`



const M_STOCKTABLE_TEMPLATE_STRING = `
<div>
    <m-trade-modal :item = "trade_item" @closed = "show_trade_modal()"></m-trade-modal>
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
              {{group}} {{groupBy}}
        </template>

        <template v-slot:group="{group, options, items, headers}" >             
                <tr v-for = "(item, index) in items" v-if = "item.visible" :class = "row_class(group, index, item, items)  + (item.ltp.instrument_id)" :id = "item.call_id">
                    <td  v-for = "header in headers" >
                        <span v-if = "header.key == 'signal'" @click = "show_trade_modal(item)">
                            <button rounded type="button"  :class="item.signal + '_btn trade elevation-7 ' + (item.active ? ' ' : 'inactive ')"  data-toggle="modal" 
                                data-target="#trade_modal">
                                <span >            
                                    {{ item.signal }}
                                </span>
                            </button>
                        </span>
                        <span v-else-if = "header.key == 'status'">
                            <span :class = "'badge elevation-7 ' + item.status.toLowerCase() + '_status'">
                                {{ item.status }}
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
        <v-col cols="12" md = "5"  class="p-0">
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
        
        <v-col cols ="12" md = "7" class = "text-center p-0">
            <v-row >
                <v-col cols = "12" md = "6" class = "text-center p-0">
                    <v-row>
                        <v-col cols ="6" class = "text-center">                            
                            <span pill variant="primary" color="blue" :content = "'Total'" class = "total--text font-weight-bold headline">{{meta.total}}</span>
                            <span class = "total--text px-2 meta-text"> Total</span>
                        </v-col>

                        <v-col cols ="6" class = "text-center">                                                  
                            <span pill color="green accent-3" :content = "'Partial HIT'" class = "partialhit_status--text font-weight-bold headline">{{meta.partial_hit}}</span>
                            <span class = "partialhit_status--text px-2 meta-text"> Partial Hits</span>
                        </v-col>
                    </v-row>
                </v-col>

                <v-col cols = "12" md = "6" class = "text-center p-0">
                    <v-row>
                        <v-col cols ="6" class = "text-center">
                            <span pill color="green lighten-1"  :content = "'HIT'" class = "hit_status--text font-weight-bold headline">{{meta.hit}}</span>
                            <span class = "hit_status--text px-2 meta-text">Hits</span>
                        </v-col>

                        <v-col cols ="6" class = "text-center">
                            <span pill color="red" :content = "'MISS'" class = "miss_status--text font-weight-bold headline">{{meta.miss}}</span>
                            <span class = "miss_status--text px-2 meta-text"> Miss</span>
                        </v-col>
                    </v-row>
                </v-col>
            </v-row>
        </v-col>
    </v-row>
    
    <v-row
        class="mx-3"
        no-gutters
        >
        <v-col cols = "12" md = "3" lg = "2" class = "mx-1">    
            <v-select
                class = "mx-1 elevation-1"
                v-model="type"
                :items="equity_type"
                menu-props="auto"
                label="Select"
                hide-details          
                single-line
                dense
                solo            
                >
            </v-select>    
        </v-col>        
        <v-col cols = "12" md = "4" lg = "3" class = "mx-1">
            <v-text-field
                v-model="search"
                class = "px-1 p-1  blue lighten-5 elevation-3"
                rounded
                append-icon="mdi-magnify"
                label="Search"
                single-line
                hide-details
                dense
            ></v-text-field>
        </v-col>
        <v-spacer></v-spacer>
        <v-col cols = "12" md = "4"  >
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
                    <span class = "float-right text-danger" v-on:click = "clear_filter()" style = "cursor:pointer">Clear</span>
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
        <v-item-group
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
                        <v-item v-slot:default="{ active, toggle }" active-class="active-head" class = "p-4" :value = "n - 1">
                            <v-card                                
                                
                                @click="toggle"
                                no-gutters
                                dense
                                class="align-center py-2 text-center mx-2 temp-white"

                                style="cursor: pointer;"

                            >
                            <span class = "title text-center" >{{portfolios[n-1].toUpperCase()}} </span>
                            </v-card>
                        </v-item>
                    </v-col>
                </v-row>
            </v-container>
        </v-item-group>    
`

const M_NAVBAR = `
<v-card class="overflow-hidden">
    <v-app-bar
      absolute
      color="white"
      elevate-on-scroll
      scroll-target="#scrolling-techniques-7"
    >
        <v-app-bar-nav-icon></v-app-bar-nav-icon>

        <v-toolbar-title>Title</v-toolbar-title>

        <v-spacer></v-spacer>

        <v-btn icon>
            <v-icon>mdi-magnify</v-icon>
        </v-btn>

        <v-btn icon>
            <v-icon>mdi-heart</v-icon>
        </v-btn>

        <v-btn icon>
            <v-icon>mdi-dots-vertical</v-icon>
        </v-btn>
        </v-app-bar>
        <v-sheet
        id="scrolling-techniques-7"
        class="overflow-y-auto"
        max-height="600"
        >
        <v-container style="height: 1500px;">

        </v-container>
        </v-sheet>
  </v-card>
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
      elevate-on-scroll
      scroll-target="#scrolling-techniques-7"
    >
        <a class="navbarlogo" href="/">
            <img id="logo" src="/static/algotext.png" width="130px" height="auto">
        </a>
            
            <v-spacer></v-spacer>
            <v-toolbar-title class= "font-weight-bold">MERCURY</v-toolbar-title>
            <v-spacer></v-spacer>        
            
            <v-menu
                class="mx-2 p-1"
                v-for="([text, rounded], index) in [['Removed', '0'],]"
                :key="text"
                :rounded="rounded"
                offset-y
                max-width = "20%"
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
                    style="min-width: 7rem;text-align: center;"
                >
                    {{ user.first_name }}
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
            max-height="100vh"
        >

            <v-container fluid class = " blue lighten-5 container-fluid" style="min-width: 100vh;max-width: 10000px;">
                <v-row>
                    <v-col
                        v-if="!is_mobile()"
                        style="width: 21%; flex: 1 0 21%;max-width:22%;" 
                    >

                    </v-col>
                    <v-col class="p-0">
                        <m-navigator class = "p-0"></m-navigator>
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
                    <v-col :cols= "is_mobile() ? '12' : ''"> 
                        <m-table-wrapper class = "white elevation-13"  style = "border-radius : 0.7rem" ref="stocktable" :items = "items" :fields = "fields" :headers = "headers" :state = "state" >{{fields}}</m-table-wrapper>    
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