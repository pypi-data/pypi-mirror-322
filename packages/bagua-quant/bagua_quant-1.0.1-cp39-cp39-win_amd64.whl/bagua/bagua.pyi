from enum import Enum, auto

class RunMode(Enum):
    """运行模式"""

    Backtest = auto()
    """回测模式"""
    Simulation = auto()
    """模拟交易"""
    Live = auto()
    """实盘交易"""

class TradeKind(Enum):
    """交易品种"""

    Spot = auto()
    """现货"""
    Future = auto()
    """永续合约"""

class TradeType(Enum):
    """交易类型"""

    Limit = auto()
    """限价单"""
    Market = auto()
    """市价单"""

class TradeSide(Enum):
    """交易方向"""

    Long = auto()
    """做多"""
    Short = auto()
    """做空"""

class OrderStatus(Enum):
    """订单状态"""

    Created = auto()
    """已创建"""
    Submitted = auto()
    """已提交"""
    PartialFilled = auto()
    """部分成交"""
    Filled = auto()
    """完全成交"""
    Canceled = auto()
    """已取消"""
    Rejected = auto()
    """已拒绝"""
