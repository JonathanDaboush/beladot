
# ------------------------------------------------------------------------------
# analysis.py
# ------------------------------------------------------------------------------
# Utility functions for analyzing order trends, revenue, and profit in sales data.
# Provides daily, weekly, and monthly aggregation for reporting and dashboards.
# ------------------------------------------------------------------------------

def analyze_units_sold_trends(orders, period='daily'):
    """
    Analyze trends in units sold over a given period.
    Args:
        orders (list): List of order objects with 'created_at' and 'order_items'.
        period (str): Aggregation period ('daily', 'weekly', 'monthly').
    Returns:
        dict: Trends, average per period, and original orders.
    """
    from collections import defaultdict
    trends = defaultdict(int)
    for order in orders:
        date = getattr(order, 'created_at', None)
        if not date:
            continue
        if period == 'daily':
            key = date.date()
        elif period == 'weekly':
            key = date.isocalendar()[1]
        elif period == 'monthly':
            key = (date.year, date.month)
        else:
            key = date.date()
        for item in getattr(order, 'order_items', []):
            trends[key] += item.quantity
    if not trends:
        return {'trends': {}, 'average_per_period': 0, 'orders': orders}
    avg = sum(trends.values()) / len(trends)
    return {'trends': dict(trends), 'average_per_period': avg, 'orders': orders}

def analyze_revenue_profit_trends(orders, period='daily', fee_rate=0.1, shipping_cost=0, ad_cost=0):
    """
    Analyze revenue and profit trends over a given period.
    Args:
        orders (list): List of order objects with 'created_at' and 'total_amount'.
        period (str): Aggregation period ('daily', 'weekly', 'monthly').
        fee_rate (float): Platform fee rate as a decimal.
        shipping_cost (float): Shipping cost per order.
        ad_cost (float): Advertising cost per order.
    Returns:
        dict: Revenue/profit trends, averages, and original orders.
    """
    from collections import defaultdict
    revenue_trends = defaultdict(float)
    profit_trends = defaultdict(float)
    for order in orders:
        date = getattr(order, 'created_at', None)
        if not date:
            continue
        if period == 'daily':
            key = date.date()
        elif period == 'weekly':
            key = date.isocalendar()[1]
        elif period == 'monthly':
            key = (date.year, date.month)
        else:
            key = date.date()
        revenue = getattr(order, 'total_amount', 0)
        fees = revenue * fee_rate
        profit = revenue - fees - shipping_cost - ad_cost
        revenue_trends[key] += revenue
        profit_trends[key] += profit
    avg_revenue = sum(revenue_trends.values()) / len(revenue_trends) if revenue_trends else 0
    avg_profit = sum(profit_trends.values()) / len(profit_trends) if profit_trends else 0
    return {
        'revenue_trends': dict(revenue_trends),
        'profit_trends': dict(profit_trends),
        'average_revenue_per_period': avg_revenue,
        'average_profit_per_period': avg_profit,
        'orders': orders
    }

def analyze_order_count_trends(orders, period='daily'):
    """
    Analyze order count trends over a given period.
    Args:
        orders (list): List of order objects with 'created_at'.
        period (str): Aggregation period ('daily', 'weekly', 'monthly').
    Returns:
        dict: Order count trends, average per period, and original orders.
    """
    from collections import defaultdict
    trends = defaultdict(int)
    for order in orders:
        date = getattr(order, 'created_at', None)
        if not date:
            continue
        if period == 'daily':
            key = date.date()
        elif period == 'weekly':
            key = date.isocalendar()[1]
        elif period == 'monthly':
            key = (date.year, date.month)
        else:
            key = date.date()
        trends[key] += 1
    avg = sum(trends.values()) / len(trends) if trends else 0
    return {'order_count_trends': dict(trends), 'average_orders_per_period': avg, 'orders': orders}
