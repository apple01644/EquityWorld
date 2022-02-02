import enum
from dataclasses import dataclass


class Main:
    main_obj = None


class EquityState(enum.Enum):
    normal = '정상'
    translate_stop = '거래중지'
    price_max_limit = '상한가'
    price_min_limit = '하한가'


@dataclass
class EquityBase:
    name: str
    price: int = 1000
    state: EquityState = EquityState.normal
    delta: float = 1

    @property
    def yesterday_price(self) -> int:
        main_obj = Main.main_obj
        if main_obj.bf_crdt not in main_obj.equity_logs:
            return self.price

        return main_obj.equity_logs[main_obj.bf_crdt][self.name].price

    @property
    def increment_per(self) -> float:
        return round(100 * 1e2 * (self.price - self.yesterday_price) / self.yesterday_price) * 1e-2

    def json(self):
        return {
            'name': self.name,
            'price': self.price,
            'state': self.state.value,
            'increment_per': self.increment_per,
            'increment': self.price - self.yesterday_price,
        }
