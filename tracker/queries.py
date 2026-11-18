"""
Django ORM queries for tracker analytics and reports.
"""

from decimal import Decimal, ROUND_HALF_UP
from django.db.models import Sum, Count, Value, DecimalField
from django.db.models.functions import Coalesce
from .models import Transaction

CENT = Decimal('0.01')

def _money(value):
    """
    Normalizes numeric values to exact 2-decimal-place currency amounts.
    """
    if value is None:
        return Decimal('0.00')
    if isinstance(value, Decimal):
        return value.quantize(CENT, rounding=ROUND_HALF_UP)
    return Decimal(str(value)).quantize(CENT, rounding=ROUND_HALF_UP)

def get_monthly_spending_summary(user_id, start_date, end_date):
    """
    Calculates total spending and transaction count within a date range
    for the given user using Django ORM aggregations.
    """
    agg = Transaction.objects.filter(
        user_id=user_id,
        tx_date__gte=start_date,
        tx_date__lte=end_date,
    ).aggregate(
        total_spent=Coalesce(
            Sum('amount'),
            Value(Decimal('0.00'), output_field=DecimalField(max_digits=10, decimal_places=2))
        ),
        tx_count=Count('id')
    )
    return {
        'total_spent': _money(agg['total_spent']),
        'tx_count': int(agg['tx_count']),
    }

def get_monthly_category_breakdown(user_id, start_date, end_date, total_spent=None):
    """
    Aggregates spending by category for a user during a date window
    using Django ORM grouping and annotations.
    """
    qs = Transaction.objects.filter(
        user_id=user_id,
        tx_date__gte=start_date,
        tx_date__lte=end_date,
    ).values(
        'category_id',
        'category__name',
        'category__color'
    ).annotate(
        category_total=Coalesce(
            Sum('amount'),
            Value(Decimal('0.00'), output_field=DecimalField(max_digits=10, decimal_places=2))
        ),
        tx_count=Count('id')
    ).order_by('-category_total', 'category__name')

    rows = list(qs)

    if total_spent is not None and total_spent > 0:
        total = _money(total_spent)
    else:
        total = sum((_money(r['category_total']) for r in rows), Decimal('0.00'))

    breakdown = []
    for r in rows:
        cat_total = _money(r['category_total'])
        pct = float((cat_total / total) * 100) if total > 0 else 0.0
        breakdown.append({
            'category_id': r['category_id'],
            'name': r['category__name'],
            'color': r['category__color'],
            'total': cat_total,
            'tx_count': int(r['tx_count']),
            'percentage': round(pct, 1),
        })

    return breakdown

def get_recent_transactions(user_id, limit=5):
    """
    Retrieves the most recent transactions for a user joined with category metadata.
    """
    qs = Transaction.objects.filter(
        user_id=user_id
    ).select_related('category').order_by('-tx_date', '-id')[:limit]

    recent = []
    for tx in qs:
        recent.append({
            'id': tx.id,
            'amount': _money(tx.amount),
            'tx_date': tx.tx_date,
            'note': tx.note,
            'category_name': tx.category.name,
            'category_color': tx.category.color,
        })
    return recent

def get_filtered_transactions(user_id, category_id=None, start_date=None, end_date=None, search=None):
    """
    Retrieves all transactions for a user matching optional filter parameters
    using Django ORM filter chaining.
    """
    qs = Transaction.objects.filter(user_id=user_id).select_related('category')

    if category_id:
        qs = qs.filter(category_id=category_id)

    if start_date:
        qs = qs.filter(tx_date__gte=start_date)

    if end_date:
        qs = qs.filter(tx_date__lte=end_date)

    if search:
        search_term = search.strip()
        if search_term:
            qs = qs.filter(note__icontains=search_term)

    qs = qs.order_by('-tx_date', '-id')

    transactions = []
    for tx in qs:
        transactions.append({
            'id': tx.id,
            'amount': _money(tx.amount),
            'tx_date': tx.tx_date,
            'note': tx.note,
            'category_id': tx.category_id,
            'category_name': tx.category.name,
            'category_color': tx.category.color,
        })
    return transactions
