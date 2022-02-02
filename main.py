import copy
import datetime
import math
import random
import time
from typing import Dict, Optional

import requests

from equity_datatype import EquityBase, EquityState, Main
from format import format_date, format_korean

main_obj: Optional['ChartManager'] = None


class ChartManager:
    equity_bases: Dict[str, EquityBase] = {
        k.name: k for k in [
            EquityBase(name='승호건설', delta=0.45),
            EquityBase(name='한국화약', delta=0.4),
            EquityBase(name='대마도', delta=0.1),
            EquityBase(name='모건스탠리', delta=0.03),

            EquityBase(name='호반전자', delta=0.2),
            EquityBase(name='해성에너지', delta=0.3),
            EquityBase(name='SC하이닉스', delta=0.5),
            EquityBase(name='호반전자(우)', delta=0.6),
            EquityBase(name='GAYJOYGO', delta=0.7),
            EquityBase(name='마차이', delta=0.8),
            EquityBase(name='지완무역', delta=0.9),
            EquityBase(name='신라자원', delta=0.9),
            EquityBase(name='대한물류', delta=1.1),
            EquityBase(name='비트비트원', delta=1.3),
        ]
    }
    Crdt = str
    equity_logs: Dict[Crdt, Dict[str, EquityBase]] = {}

    def __init__(self):
        self.virtual_date = datetime.datetime(year=2022, month=1, day=1)
        self.virtual_date += datetime.timedelta(days=-1)
        self.day = 0
        self.crdt: str = ''
        self.bf_crdt: str = ''

    @property
    def yesterday(self):
        return self.virtual_date - datetime.timedelta(days=1)

    def start(self):
        while True:
            self.loop()
            time.sleep(0.5)

    def log_equity(self):
        for eq_base in self.equity_bases.values():
            if eq_base.state == EquityState.translate_stop:
                continue
            eq_base.price += round(random.uniform(-1, +1) * eq_base.price * eq_base.delta)

        self.verify_equity()

        self.equity_logs[format_date(self.virtual_date)] = {
            k: copy.copy(v) for k, v in self.equity_bases.items()
        }
        self.sync()
        for eq_base in self.equity_bases.values():
            print(format_korean(eq_base.name + '({:s})'.format(eq_base.state.value), 20), '::', '%4s' % eq_base.price,
                  end='')
            print(
                ', 증감',
                '%7s' % (
                    '{:+4.2f}%'.format(eq_base.increment_per)
                ),
            )

    def verify_equity(self):
        for eq_base in self.equity_bases.values():
            if eq_base.price <= 10:
                eq_base.price = 10
                eq_base.state = EquityState.translate_stop
                continue

            if eq_base.state in (EquityState.price_max_limit, EquityState.price_min_limit):
                eq_base.state = EquityState.normal

            if eq_base.price > eq_base.yesterday_price * (1 + .3):
                eq_base.price = int(math.floor(eq_base.yesterday_price * (1 + .3)))
                eq_base.state = EquityState.price_max_limit
            elif eq_base.price < eq_base.yesterday_price * (1 - .3):
                eq_base.price = int(math.ceil(eq_base.yesterday_price * (1 - .3)))
                eq_base.state = EquityState.price_min_limit

    def sync(self):
        base_url = 'https://equityworld-5c018-default-rtdb.asia-southeast1.firebasedatabase.app'
        res = requests.put(
            f'{base_url}/main.json',
            json={
                'crdt': self.crdt,
                'equity_logs': {crdt: {
                    k: eq_base.json() for k, eq_base in enumerate(eq_bases.values())
                } for crdt, eq_bases in self.equity_logs.items()},
                'equity_bases': {k: eq_base.json() for k, eq_base in enumerate(self.equity_bases.values())}
            }
        )
        assert res.status_code == 200, res.status_code

    def loop(self):
        self.virtual_date += datetime.timedelta(days=1)
        self.crdt = format_date(self.virtual_date)
        self.bf_crdt = format_date(self.yesterday)

        print('\n' * 10)
        print('== 기준일자 [{:=^0}]'.format(self.crdt))
        self.log_equity()


if __name__ == '__main__':
    Main.main_obj = ChartManager()
    Main.main_obj.start()
