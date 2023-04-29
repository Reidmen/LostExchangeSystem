mod engine;
use engine::engine::{MatchingEngine, TradingPair};
use engine::orderbook::{BidOrAsk, Order, OrderBook};

fn main() {
    let buy_order_from_alice = Order::new(BidOrAsk::Bid, 5.5);
    let buy_order_from_bob = Order::new(BidOrAsk::Bid, 2.45);

    let mut orderbook = OrderBook::new();

    orderbook.add_order(4.4, buy_order_from_alice);
    orderbook.add_order(4.4, buy_order_from_bob);

    let sell_order_from_jhon = Order::new(BidOrAsk::Ask, 7.6);
    orderbook.add_order(20.0, sell_order_from_jhon);
    // println!("{:?}", orderbook);

    let mut engine = MatchingEngine::new();
    let pair = TradingPair::new("BTC".to_string(), "USD".to_string());
    engine.add_new_pair(pair.clone());

    let buy_order = Order::new(BidOrAsk::Bid, 6.5);
    //let eth_pair = TradingPair::new("ETH".to_string(), "USD".to_string());
    engine.place_limit_order(pair, 10.000, buy_order).unwrap();

}
