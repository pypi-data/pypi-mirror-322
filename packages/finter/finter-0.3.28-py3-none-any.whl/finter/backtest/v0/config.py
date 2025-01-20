from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

import pandas as pd
from typing_extensions import Literal

from finter.data.data_handler.main import DataHandler

AVAILABLE_RESAMPLE_PERIODS = Literal[None, "W", "M", "Q"]
AVAILABLE_REBALANCING_METHODS = Literal["auto", "W", "M", "Q", "by_position"]
AVAILABLE_CORE_TYPES = Literal["basic", "id_fund", "vn"]
AVAILABLE_DIVIDEND_TYPES = Literal[None, "cash", "reinvest"]


@dataclass(slots=True)
class DataConfig:
    position: pd.DataFrame = field(default_factory=pd.DataFrame)
    price: pd.DataFrame = field(default_factory=pd.DataFrame)
    volume: pd.DataFrame = field(default_factory=pd.DataFrame)
    dividend_ratio: pd.DataFrame = field(default_factory=pd.DataFrame)
    exchange_rate: pd.DataFrame = field(default_factory=pd.DataFrame)


@dataclass(slots=True)
class DateConfig:
    start: int = 20150101  # e.g. 20200101
    end: int = int(datetime.now().strftime("%Y%m%d"))  # e.g. 20201231


@dataclass(slots=True)
class CostConfig:
    # unit: basis point
    buy_fee_tax: float = 0.0
    sell_fee_tax: float = 0.0
    slippage: float = 0.0
    dividend_tax: float = 0.0


@dataclass(slots=True)
class ExecutionConfig:
    initial_cash: float = 1e8
    volume_capacity_ratio: float = 0.0

    resample_period: AVAILABLE_RESAMPLE_PERIODS = None
    rebalancing_method: AVAILABLE_REBALANCING_METHODS = "auto"

    core_type: AVAILABLE_CORE_TYPES = "basic"

    drip: AVAILABLE_DIVIDEND_TYPES = None


@dataclass(slots=True)
class OptionalConfig:
    # todo: currency, seperate dividend
    # adj_dividend: bool = False
    debug: bool = False


@dataclass(slots=True)
class CacheConfig:
    data_handler: Optional[DataHandler] = None
    timeout: int = 300
    maxsize: int = 5


@dataclass(slots=True)
class FrameConfig:
    shape: tuple[int, int] = field(default_factory=tuple)
    common_columns: list[str] = field(default_factory=list)
    common_index: list[str] = field(default_factory=list)


@dataclass(slots=True)
class SimulatorConfig:
    date: DateConfig
    cost: CostConfig
    execution: ExecutionConfig
    optional: OptionalConfig
    cache: CacheConfig
    frame: FrameConfig

    def __repr__(self) -> str:
        date_info = f"Date: {self.date.start} -> {self.date.end}"
        cost_info = "Cost: " + ", ".join(
            f"{slot}: {getattr(self.cost, slot) * 10000:.1f}bp"
            for slot in self.cost.__slots__
        )
        execution_info = "Execution: " + ", ".join(
            f"{slot}: {getattr(self.execution, slot)}"
            for slot in self.execution.__slots__
        )
        frame_info = f"Frame: {self.frame.shape}"

        return (
            "┌─────────────────────────────────────\n"
            f"│ {date_info}\n"
            f"│ {cost_info}\n"
            f"│ {execution_info}\n"
            f"│ {frame_info}\n"
            "└─────────────────────────────────────"
        )
