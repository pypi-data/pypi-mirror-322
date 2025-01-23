from eskmo.base.mvtype import *
from eskmo.const.event import *
from eskmo.const.skcom import *
from eskmo.skcom.function import *
from _typeshed import Incomplete
from datetime import datetime
from eskmo.internal.const import Order as Order, SmartOrder as SmartOrder
from eskmo.utils.misc import frozen_dataclass as frozen_dataclass

class DictableResult:
    def __getitem__(self, key): ...

class StockMarginInfo:
    stock_no: str
    financing_flag: int
    financing_limit: int
    financing_ratio: int
    short_selling_flag: int
    short_selling_limit: int
    short_selling_ratio: int
    day_trade_flag: int
    down_grade_flag: int
    flat_position_short_sell_flag: int
    full_settlement_flag: int
    warning_flag: int
    disposition_stock_flag: int
    watch_stock_flag: int
    restricted_stock_flag: int
    abnormal_promotion_flag: int
    special_abnormal_flag: int
    single_order_share_limit: int
    multiple_order_share_limit: int
    cash_security_precollection_ratio: int
    login_id: int
    account_no: int

class Quote:
    idx: tuple
    market: str
    decimal: int
    sector: int
    symbol: str
    name: str
    high: float
    open: float
    low: float
    close: float
    tick_qty: float
    ref: float
    bid: float
    bid_qty: float
    ask: float
    ask_qty: int
    bid_total_qty: int
    ask_total_qty: int
    future_oi: int
    qty_total: int
    qty_yesterday: int
    up: float
    down: float
    simulate: bool
    day_trade_type: int
    trading_day: str

class MITOrderResult(DictableResult):
    account: str
    symbol: str
    buysell: SmartOrder.MIT.ACTION
    price: float
    qty: int
    trigger_price: float
    trigger_dir: SmartOrder.MIT.TRIGGER_DIR
    order_flag: SmartOrder.MIT.ORDER_FLAG
    price_type: SmartOrder.MIT.PRICE_TYPE
    trade_type: SmartOrder.MIT.ORDER_TYPE
    is_pre_trade_risk_controlled: bool
    is_gtc_order: bool
    gtc_date: str
    gtc_end_by: SmartOrder.MIT.LONG_END_BY

class SendResult(DictableResult):
    state: str
    created: datetime
    callback_id: int
    thread_id: str

class PlaceResult(DictableResult):
    thread_id: str
    order: PlacedOrderResult

class MITPlaceResult(DictableResult):
    thread_id: str
    order: PlacedMITOrderResult

class CallbackResult(DictableResult):
    callbackId: int

class ErrorsResult(DictableResult):
    errors: list[str]
    error_code: str

class MITOrderSendStartResult(CallbackResult, MITOrderResult): ...
class MITOrderSendFailResult(ErrorsResult, CallbackResult, MITOrderResult): ...
class MITOrderSendSuccessResult(SendResult, MITOrderResult): ...
class MITOrderPlaceFailResult(ErrorsResult, MITPlaceResult): ...
class MITOrderPlaceSuccessResult(MITPlaceResult): ...

class OrderResult(DictableResult):
    account: str
    symbol: str
    exchange: Order.EXCHANGE
    period: Order.PERIOD
    order_flag: Order.FLAG
    buysell: Order.ACTION
    price: float
    qty: int
    price_type: Order.PRICE
    trade_type: Order.TRADE

class PlacedOrderResult(OrderResult):
    seq_no: str

class PlacedMITOrderResult(MITOrderResult):
    seq_no: str

class OrderSendStartResult(CallbackResult, OrderResult): ...
class OrderSendFailResult(ErrorsResult, CallbackResult, OrderResult): ...
class OrderSendSuccessResult(SendResult, OrderResult): ...
class OrderPlaceSuccessResult(PlaceResult): ...
class OrderPlaceFailResult(ErrorsResult, PlaceResult): ...

class ReplyPrice:
    price: str
    numerator: str
    denominator: str

class ReplyCommodity:
    com_id: str
    year_month: str
    strike_price: str

class Reply:
    num: int
    key_no: str
    market: str
    type: str
    status: str
    broker: str
    cust_no: str
    buysell_info: str
    exchange_id: str
    symbol: str
    strike_price: str
    book_no: str
    price: str
    numerator: str
    denominator: str
    price_lags: list[ReplyPrice]
    volume: int
    before_qty: int
    after_qty: int
    date_str: str
    time_str: str
    ok_seq: str
    sub_id: str
    sale_no: str
    agent: str
    trade_date: str
    msg_no: str
    pre_order: str
    commodity_lags: list[ReplyCommodity]
    execution_no: str
    price_symbol: str
    reserved: str
    order_effective: str
    call_put: str
    order_seq: str
    error_msg: str
    cancel_order_mark_by_exchange: str
    exchange_tandem_msg: str
    seq_no: str
    buysell: str
    trade_type: str
    order_type: str
    price_type: str

class SmartReply:
    user_id: str
    trade_kind: str
    market: str
    type: str
    exchange_code: str
    smart_key_no: str
    pub_seq_no: str
    broker: str
    account: str
    sub_account: str
    exchange_id: str
    seq_no: str
    o_seq_no: str
    order_no: str
    symbol: str
    buysell_str: str
    order_type: str
    order_price_mark: str
    order_price: str
    price_type: str
    order_cond: str
    qty: str
    trigger_price: str
    trigger_time: str
    trigger_dir: str
    day_trade: str
    created: datetime
    sale_no: str
    user_ip: str
    trade_source: str
    status: str
    error_msg: str
    message: str
    updated: datetime
    universal_msg: str
    base_price: str
    market_deal_trigger: str
    num: int
    buysell: str

class OrderStatus:
    reply: Reply
    is_closed: bool
    price: str
    volume: int
    volume_remain: int
    volume_cancel: int
    volume_deal: int

class SmartOrderStatus:
    reply: SmartReply
    is_closed: bool
    price: str
    volume: int
    volume_remain: int
    volume_cancel: int
    volume_deal: int

class OrderNotifyResult(DictableResult):
    count: int
    order: OrderStatus

class SmartOrderChangedResult(DictableResult):
    count: int
    order: SmartOrderStatus

class MITOrderNotifyResult(SmartOrderChangedResult): ...

class OrderCancelFailResult(ErrorsResult):
    order_class: str
    cancel_action: str
    seq_no: str
    is_already_cancelled: bool

class SubscribeStartResult(DictableResult):
    event: str
    symbol: str

class SubscribeFailResult(DictableResult):
    event: str
    symbol: str
    error_code: str
    errors: list[str]

class SubscribeSuccessResult(DictableResult):
    event: str
    symbol: str
    messages: list[str]

class UnsubscribeStartResult(DictableResult):
    event: str
    symbol: str

class UnsubscribeFailResult(DictableResult):
    event: str
    symbol: str
    error_code: str
    errors: list[str]

class UnsubscribeSuccessResult(DictableResult):
    event: str
    symbol: str
    messages: list[str]

class APIExecuteErrorResult(DictableResult):
    event: str
    phase: str
    function: str
    error_code: str
    errors: list[str]

class LoginFailResult(DictableResult):
    event: str
    auto_relogin: bool
    userId: str
    error_code: str
    errors: list[str]

class LoginStartResult(DictableResult):
    event: str
    type: str
    connection: int

class LoginSuccessResult(DictableResult):
    event: str
    api: str
    userId: str

class LoginProgressNotifyResult(DictableResult):
    event: str
    progress: int
    description: str

class MarginLimitResult(DictableResult):
    symbol: str
    margin_purchase: str
    margin_purchase_limit: str
    margin_purchase_ratio: str
    short_sale: str
    short_sale_limit: str
    short_sale_ratio: str
    day_trade: str
    down_grade: str
    flat_short: str
    fullcash_delivery: str
    alerting: str
    disposition: str
    attention: str
    restricted: str
    unusally_recommended: str
    specific_abnormally: str
    single_order_qty_limit: str
    multiple_order_qty_limit: str
    advance_collection_ratio: str
    login_id: str
    margin_account: str

class Tick:
    count: int
    date_str: str
    time_str: str
    ms_str: str
    timestamp: float
    time: datetime
    symbol: str
    bid: float
    ask: float
    close: float
    qty: int
    simulate: bool

class OrderBookLevel:
    price: float
    qty: int

class Best5:
    code: str
    bid: list[OrderBookLevel]
    ask: list[OrderBookLevel]
    simulate: bool

class PnLUnrealizedSummaryResult:
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

class PnLUnrealizedDetailsResult:
    stock_name: str
    symbol_code: str
    deal_date: str
    trade_type: str
    purchase: str
    offsetable: str
    avg_price: str
    deal_price: str
    pnl: str
    return_rate: str
    fee: str
    fee_estimated: str
    tax: str
    tax_estimated: str
    margin_funds: str
    collateral: str
    lending_interest: str
    short_fee: str
    payment: str
    dividend: str
    note: str
    book_no: str
    trade_type_code: str
    login_id: str
    account_no: str

class PnLRealizedSummaryResult:
    trade_type: str
    trade_type_code: str
    date: str
    subsidiary_code: str
    account: str
    stock_no: str
    qty: str
    price: str
    pnl: str
    return_rate: str
    note: str
    has_details: str
    book_no_sell: str
    seq_no_sell: str
    stock_name: str
    currency: str
    investment: str
    login_id: str

class PnLRealizedDetailsResult:
    date: str
    trade_type: str
    stock_no: str
    stock_name: str
    book_no: str
    buysell: str
    qty: str
    avg_price: str
    deal_price: str
    fee: str
    tax: str
    margin_funds: str
    collateral: str
    margin_interest: str
    short_fee: str
    payment: str
    offset_qty: str
    note: str
    trade_type_code: str
    login_id: str
    account_no: str

class PnLRealizedStockSummaryResult:
    trade_type: str
    trade_type_code: str
    subsidiary_code: str
    account: str
    symbol_code: str
    qty: str
    pnl: str
    return_rate: str
    currency: str
    login_id: str

class PnLRealizedTotalInverstmentResult:
    subsidiary_code: str
    account: str
    investment_twd: str
    pnl_twd: str
    return_twd: str
    investment_rmb: str
    pnl_rmb: str
    return_rmb: str
    login_id: str

class PnLDayTradeSummaryResult:
    num: str
    stock_name: str
    symbol_code: str
    currency_zh: str
    offset_qty: str
    pending_offset_qty: str
    pending_buy_qty: str
    pending_sell_qty: str
    offset_available_qty: str
    market_price: str
    updown_today: str
    market_value: str
    nav: str
    pnl_unrealized: str
    pnl_realized: str
    pnl_total: str
    avg_price: str
    cost: str
    deal_price: str
    fee: str
    fee_estimated: str
    tax: str
    tax_estimated: str
    return_estimated: str
    note: str
    has_details: str
    currency: str
    login_id: str
    account_no: str

class PnLDayTradeDetailsResult:
    stock_name: str
    book_no: str
    qty: str
    offset_qty: str
    avg_price: str
    deal_price: str
    fee: str
    fee_estimated: str
    tax: str
    tax_estimated: str
    payment: str
    symbol_code: str
    buysell: str
    login_id: str
    account_no: str

class EventDataParser:
    loginCnt: Incomplete
    mapping: Incomplete
    def __init__(self) -> None: ...
    def parse(self, event, data): ...
    def parseQuote(event: str, data: dict) -> Quote: ...
    @staticmethod
    def parseStockMarginInfo(data: dict) -> StockMarginInfo: ...
