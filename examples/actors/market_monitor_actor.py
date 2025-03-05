from nautilus_trader.live.engine import LiveEngine, LiveEngineConfig
from nautilus_trader.config import LoggingConfig
from nautilus_trader.model.identifiers import TraderId

engine_config = LiveEngineConfig(
    trader_id=TraderId("MONITOR-LIVE-001"),
    logging=LoggingConfig(log_level="INFO"),
)

engine = LiveEngine(config=engine_config)


from nautilus_trader.model.enums import OmsType, AccountType
from nautilus_trader.model.currencies import USDT
from nautilus_trader.model.identifiers import Venue

engine.add_venue(
    venue=Venue("BINANCE"),
    oms_type=OmsType.NETTING,
    account_type=AccountType.CASH,
    base_currency=USDT,
)

from nautilus_trader.model.identifiers import InstrumentId, Symbol
from nautilus_trader.model.instruments.spot import SpotInstrument

BTCUSDT = SpotInstrument(
    instrument_id=InstrumentId(Symbol("BTCUSDT"), Venue("BINANCE")),
    base_currency="BTC",
    quote_currency="USDT",
    price_precision=2,
    size_precision=6,
    multiplier=1.0,
    lot_size=0.000001,
    min_trade_amount=10.0,
    maker_fee=0.001,
    taker_fee=0.001,
)
engine.add_instrument(BTCUSDT)

from nautilus_trader.common.actor import Actor, ActorConfig
from nautilus_trader.model.data import Bar, BarType

class LiveMonitorConfig(ActorConfig):
    instrument_id: InstrumentId
    bar_type: BarType

class LiveMonitor(Actor):
    def __init__(self, config: LiveMonitorConfig):
        super().__init__(config)
        self.bar_count = 0

    def on_start(self):
        # Подписка на данные (например, свечи)
        self.subscribe_bars(self.config.bar_type)
        self.log.info(f"Подписан на данные свечей: {self.config.bar_type}")

    def on_bar(self, bar: Bar):
        self.bar_count += 1
        print(f"Получен бар: {bar.ts_event} цена закрытия: {bar.close}")

monitor_config = LiveMonitorConfig(
    instrument_id=BTCUSDT.id,
    bar_type=BarType.from_str("BTCUSDT.BINANCE-1-MINUTE-LAST-EXTERNAL"),
)

monitor_actor = LiveMonitor(monitor_config)
engine.add_actor(monitor_actor)

# Настройка подключения к Binance (предварительно установи nautilus_trader[binance])
from nautilus_trader.adapters.binance.spot.client import BinanceSpotClientFactory
from nautilus_trader.adapters.binance.spot.data_client import BinanceSpotDataClientConfig

binance_config = BinanceSpotDataClientConfig(api_key='', api_secret='')  # публичные данные API-ключи не обязательны
client = BinanceSpotClientFactory.create(client_id='BINANCE_SPOT', config=binance_config)

engine.add_data_client(client)

engine.run()