#from decimal import Decimal
from datetime import datetime, timezone

from nautilus_trader.adapters.binance.common.enums import BinanceAccountType
from nautilus_trader.adapters.binance.config import BinanceDataClientConfig
#from nautilus_trader.adapters.binance.config import BinanceExecClientConfig
from nautilus_trader.adapters.binance.factories import BinanceLiveDataClientFactory
#from nautilus_trader.adapters.binance.factories import BinanceLiveExecClientFactory
from nautilus_trader.common.config import ActorConfig
#from nautilus_trader.config import CacheConfig
#from nautilus_trader.config import DatabaseConfig
from nautilus_trader.config import InstrumentProviderConfig
from nautilus_trader.config import LiveExecEngineConfig
from nautilus_trader.config import LoggingConfig
from nautilus_trader.config import TradingNodeConfig
#from nautilus_trader.examples.strategies.volatility_market_maker import VolatilityMarketMaker
#from nautilus_trader.examples.strategies.volatility_market_maker import VolatilityMarketMakerConfig
from nautilus_trader.live.config import LiveDataEngineConfig
from nautilus_trader.live.data_engine import LiveDataEngine
from nautilus_trader.live.node import TradingNode
from nautilus_trader.model.data import BarType, Bar
from nautilus_trader.model.identifiers import InstrumentId, ClientId
from nautilus_trader.model.identifiers import TraderId
from nautilus_trader.common.actor import Actor
#from nautilus_trader.adapters.binance.futures.types import BinanceFuturesMarkPriceUpdate


class MyActorConfig(ActorConfig):
    bar_type: BarType
    instrument_id: InstrumentId


class MyActor(Actor):
    def __init__(self, config: MyActorConfig):
        super().__init__(config)
        self.bar_type = config.bar_type
        self.instrument_id = config.instrument_id

    def on_start(self) -> None:
        self.log.info("Actor started, waiting for data...")

        #self.subscribe_data(
        #    data_type=DataType(BinanceFuturesMarkPriceUpdate, metadata={"instrument_id": self.instrument.id}),
        #    client_id=ClientId("BINANCE"),
        #)
        self.request_bars(self.config.bar_type, client_id=ClientId("BINANCE"))
        self.subscribe_bars(self.config.bar_type, client_id=ClientId("BINANCE"))

    def on_bar(self, bar: Bar) -> None:
        timestamp = datetime.fromtimestamp(bar.ts_event / 1e9, tz=timezone.utc)
        self.log.info(f"Bar received at {timestamp}: O={bar.open}, H={bar.high}, L={bar.low}, C={bar.close}, V={bar.volume}")

# Configure the trading node
config_node = TradingNodeConfig(
    trader_id=TraderId("TESTER-001"),
    logging=LoggingConfig(log_level="INFO"),
    exec_engine=LiveExecEngineConfig(
        reconciliation=True,
        reconciliation_lookback_mins=1440,
    ),
    #data_engine=LiveDataEngineConfig(
    #    time_bars_timestamp_on_close=False,  # Use opening time as `ts_event`, as per IB standard
    #    validate_data_sequence=True
    #),

    #cache=CacheConfig(
    #    database=DatabaseConfig(),  # default redis
    #    buffer_interval_ms=100,
    #),
    data_clients={
        "BINANCE": BinanceDataClientConfig(
            api_key="",
            api_secret="",
            account_type=BinanceAccountType.SPOT,
            instrument_provider=InstrumentProviderConfig(load_all=True),
        ),
    },
#    exec_clients={
#        "BINANCE": BinanceExecClientConfig(
#            # api_key=os.getenv("BINANCE_FUTURES_API_KEY"),
#            # api_secret=os.getenv("BINANCE_FUTURES_API_SECRET"),
#            account_type=BinanceAccountType.USDT_FUTURE,
#            instrument_provider=InstrumentProviderConfig(load_all=True),
#            max_retries=3,
#            retry_delay=1.0,
#        ),
#    },
    timeout_connection=30.0,
    timeout_reconciliation=10.0,
    timeout_portfolio=10.0,
    timeout_disconnection=10.0,
    timeout_post_stop=5.0,
)

# Instantiate the node with a configuration
node = TradingNode(config=config_node)
#engine = LiveDataEngine()

# Configure your strategy
strat_config = MyActorConfig(
    instrument_id=InstrumentId.from_str("ETHUSDT.BINANCE"),
    bar_type=BarType.from_str("ETHUSDT.BINANCE-1-MINUTE-LAST-EXTERNAL"),
)
# Instantiate your strategy
#strategy = VolatilityMarketMaker(config=strat_config)
actor = MyActor(config=strat_config)

# Add your strategies and modules
#node.trader.add_strategy(strategy)
node.trader.add_actor(actor)

# Register your client factories with the node (can take user-defined factories)
node.add_data_client_factory("BINANCE", BinanceLiveDataClientFactory)
#node.add_exec_client_factory("BINANCE", BinanceLiveExecClientFactory)
node.build()


# Stop and dispose of the node with SIGINT/CTRL+C
if __name__ == "__main__":
    try:
        node.run()
    finally:
        node.dispose()
