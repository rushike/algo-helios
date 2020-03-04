import sys


session_filters = {}

portfolio_map = {
    'TEST': "intraday",
    '1': "intraday",
    '2': "btst",
    '3': "positional",
    '4': "longterm",
}


class SessionFilter:
    """
    Broad level filter for all the types of calls
    """

    def __init__(self):
        self.filters = dict()
        for call_type in set(portfolio_map.values()):
            self.filters[call_type] = CallFilter()
        self.filters['intraday'].lower_rr = 0.5

    def add_filters(self, request):
        call_type = request['call_type']
        self.filters.setdefault(call_type, CallFilter()).add_filters(request)

    def apply_filters(self, table):
        filtered_table = list()
        temp_data_dict = dict()
        for row in table:
            temp_data_dict['portfolio_id'] = row[11]
            temp_data_dict['orig_risk_reward'] = row[12]
            temp_data_dict['orig_profit_percent'] = row[13]
            temp_data_dict['ticker'] = row[0]
            temp_data_dict['signal'] = row[2]
            if self.filter(temp_data_dict):
                filtered_table.append(row)
            temp_data_dict.clear()
        return filtered_table

    def to_dict(self):
        dict_representation = {}
        for call_type, filter in self.filters.items():
            dict_representation[call_type] = filter.to_dict()
        return dict_representation

    def filter(self, data_dict):
        call_type = portfolio_map[str(data_dict['portfolio_id'])]
        if call_type not in self.filters:
            return True
        return self.filters[call_type].filter(data_dict)


class CallFilter:
    """
    A class to handle client filters
    """

    def __init__(self):
        self.tickers = set()
        self.sides = set()
        self.lower_rr, self.lower_profit_per = 0, 0
        self.upper_rr, self.upper_profit_per = sys.maxsize, sys.maxsize

    def add_filters(self, request):
        self.tickers = set(request.getlist('tickers'))
        self.sides = set(request.getlist('sides'))

        self.lower_rr = float(request['rr_range'].split(' - ')[0])
        upper_rr = float(request['rr_range'].split(' - ')[1])
        self.upper_rr = upper_rr if upper_rr < 5.0 else sys.maxsize

        self.lower_profit_per = float(request['pp_range'].split(' - ')[0])
        upper_profit_per = float(request['pp_range'].split(' - ')[1])
        self.upper_profit_per = upper_profit_per if upper_profit_per < 50 else sys.maxsize
        print("Added filters ", self.__dict__)

    def update_filters(self, tickers=set(), sides=set(), lower_rr=0,
                       upper_rr=sys.maxsize, lower_pp=0, upper_pp=sys.maxsize):
        self.tickers = tickers
        self.sides = sides
        self.lower_rr, self.lower_profit_per = lower_rr, lower_pp
        self.upper_rr, self.upper_profit_per = upper_rr, upper_pp

    def to_dict(self):
        return {"tickers": list(self.tickers), "sides": list(self.sides), "lower_rr": self.lower_rr,
                "upper_rr": self.upper_rr, "lower_pp": self.lower_profit_per, "upper_pp": self.upper_profit_per}

    def filter(self, data_dict):
        if (len(self.tickers) == 0 or (len(self.tickers) != 0 and data_dict['ticker'] in self.tickers)) and \
                (len(self.sides) == 0 or (len(self.sides) != 0 and data_dict['signal'] in self.sides)) and \
                self.lower_rr <= float(data_dict['orig_risk_reward']) <= self.upper_rr and \
                self.lower_profit_per <= float(data_dict['orig_profit_percent']) <= self.upper_profit_per:
            return True
