from eskmo.const.skcom import *
from dataclasses import dataclass
from eskmo.base.interface import UserReferable as UserReferable

@dataclass
class PnLUnrealizedSummary(UserReferable):
    stock_name: str
    symbol_code: str
    currency: str
    trade_type: str
    position: str
    mark_price: str
    price_changed_today: str
    market_value: str
    nav: str
    pnl: str
    avg_price: str
    cost: str
    deal_price: str
    fee: str
    fee_estimated: str
    tax: str
    tax_estimated: str
    margin_funds: str
    collateral: str
    dividend_estimated: str
    dividend: str
    return_estimated: str
    unknown_stock_qty: str
    note: str
    has_details: str
    sorting_id: str
    trade_type_code: str
    breakeven: str
    login_id: str
    account_no: str
    def init(self, user) -> None: ...
    def update(self, pnl: dict): ...
    def __init__(self, stock_name, symbol_code, currency, trade_type, position, mark_price, price_changed_today, market_value, nav, pnl, avg_price, cost, deal_price, fee, fee_estimated, tax, tax_estimated, margin_funds, collateral, dividend_estimated, dividend, return_estimated, unknown_stock_qty, note, has_details, sorting_id, trade_type_code, breakeven, login_id, account_no) -> None: ...
