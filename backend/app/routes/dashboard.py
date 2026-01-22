from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User, Product, Sale, SaleItem, Expense, Asset, Liability, Equity, BudgetTarget, BusinessSettings, InventoryLog
from sqlalchemy import func, extract, and_
from datetime import datetime, timedelta
from decimal import Decimal

bp = Blueprint('dashboard', __name__)

@bp.route('/metrics', methods=['GET'])
@jwt_required()
def get_dashboard_metrics():
    """Get comprehensive dashboard metrics"""
    try:
        # Get query parameters for date filtering
        year = request.args.get('year', datetime.now().year, type=int)
        month = request.args.get('month', datetime.now().month, type=int)
        
        # Get all-time metrics
        all_time_sales = db.session.query(func.sum(Sale.total_amount)).scalar() or 0
        all_time_expenses = db.session.query(func.sum(Expense.amount)).scalar() or 0
        all_time_gross_profit = float(all_time_sales) - float(all_time_expenses)
        gross_profit_margin = (all_time_gross_profit / float(all_time_sales) * 100) if all_time_sales > 0 else 0
        
        # Today's metrics
        today = datetime.now().date()
        sales_today = db.session.query(func.sum(Sale.total_amount)).filter(
            func.date(Sale.sale_date) == today
        ).scalar() or 0
        
        items_sold_today = db.session.query(func.sum(SaleItem.quantity)).join(Sale).filter(
            func.date(Sale.sale_date) == today
        ).scalar() or 0
        
        expense_today = db.session.query(func.sum(Expense.amount)).filter(
            Expense.expense_date == today
        ).scalar() or 0
        
        # Monthly metrics
        monthly_sales = db.session.query(func.sum(Sale.total_amount)).filter(
            extract('year', Sale.sale_date) == year,
            extract('month', Sale.sale_date) == month
        ).scalar() or 0
        
        monthly_items_sold = db.session.query(func.sum(SaleItem.quantity)).join(Sale).filter(
            extract('year', Sale.sale_date) == year,
            extract('month', Sale.sale_date) == month
        ).scalar() or 0
        
        monthly_expenses = db.session.query(func.sum(Expense.amount)).filter(
            extract('year', Expense.expense_date) == year,
            extract('month', Expense.expense_date) == month
        ).scalar() or 0
        
        monthly_profit = float(monthly_sales) - float(monthly_expenses)
        
        # Get targets
        target = BudgetTarget.query.filter_by(year=year, month=month).first()
        sales_target = float(target.sales_target) if target and target.sales_target else 500000
        items_target = target.items_sold_target if target and target.items_sold_target else 750
        
        # Calculate progress
        sales_progress = (float(monthly_sales) / sales_target * 100) if sales_target > 0 else 0
        items_progress = (monthly_items_sold / items_target * 100) if items_target > 0 else 0
        
        # Inventory status
        in_stock = Product.query.filter(Product.current_stock > Product.low_stock_threshold).count()
        low_stock = Product.query.filter(
            and_(Product.current_stock > 0, Product.current_stock <= Product.low_stock_threshold)
        ).count()
        out_of_stock = Product.query.filter(Product.current_stock == 0).count()
        
        # Best selling items
        bestsellers = db.session.query(
            Product.name,
            func.sum(SaleItem.quantity).label('total_sold'),
            func.sum(SaleItem.line_total).label('total_revenue')
        ).join(SaleItem).join(Sale).filter(
            extract('year', Sale.sale_date) == year,
            extract('month', Sale.sale_date) == month
        ).group_by(Product.id, Product.name).order_by(func.sum(SaleItem.line_total).desc()).limit(5).all()
        
        bestsellers_data = [
            {
                'name': item[0],
                'quantity_sold': int(item[1]),
                'revenue': float(item[2])
            } for item in bestsellers
        ]
        
        # Top sales channels (mock data - can be extended with actual channel tracking)
        top_channels = [
            {'channel': 'Physical Store', 'sales': float(monthly_sales) * 0.4},
            {'channel': '2nd Branch', 'sales': float(monthly_sales) * 0.3},
            {'channel': 'Online Store', 'sales': float(monthly_sales) * 0.2},
            {'channel': 'Tiktok', 'sales': float(monthly_sales) * 0.07},
            {'channel': 'Shopify', 'sales': float(monthly_sales) * 0.03}
        ]
        
        # Expense distribution
        expense_breakdown = db.session.query(
            Expense.category,
            func.sum(Expense.amount).label('total')
        ).filter(
            extract('year', Expense.expense_date) == year,
            extract('month', Expense.expense_date) == month
        ).group_by(Expense.category).all()
        
        expense_distribution = [
            {
                'category': item[0].value if hasattr(item[0], 'value') else str(item[0]),
                'amount': float(item[1])
            } for item in expense_breakdown
        ]
        
        # Annual revenue target
        annual_target = db.session.query(func.sum(BudgetTarget.sales_target)).filter(
            BudgetTarget.year == year
        ).scalar() or 6000000
        
        annual_current = db.session.query(func.sum(Sale.total_amount)).filter(
            extract('year', Sale.sale_date) == year
        ).scalar() or 0
        
        annual_progress = (float(annual_current) / float(annual_target) * 100) if annual_target > 0 else 0
        
        return jsonify({
            'all_time': {
                'gross_profit': round(all_time_gross_profit, 2),
                'sales': round(float(all_time_sales), 2),
                'expenses': round(float(all_time_expenses), 2),
                'gross_profit_margin': round(gross_profit_margin, 0)
            },
            'today': {
                'sales': round(float(sales_today), 2),
                'items_sold': int(items_sold_today),
                'expenses': round(float(expense_today), 2)
            },
            'monthly': {
                'items_sold': int(monthly_items_sold),
                'items_target': items_target,
                'items_progress': round(items_progress, 0),
                'sales': round(float(monthly_sales), 2),
                'sales_target': sales_target,
                'sales_progress': round(sales_progress, 0),
                'expenses': round(float(monthly_expenses), 2),
                'profit': round(monthly_profit, 2)
            },
            'inventory': {
                'in_stock': in_stock,
                'low_stock': low_stock,
                'out_of_stock': out_of_stock
            },
            'bestsellers': bestsellers_data,
            'top_channels': top_channels,
            'expense_distribution': expense_distribution,
            'annual': {
                'current': round(float(annual_current), 2),
                'target': float(annual_target),
                'progress': round(annual_progress, 0)
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/sales-trend/daily', methods=['GET'])
@jwt_required()
def get_daily_sales_trend():
    """Get daily sales trend for the specified month"""
    try:
        year = request.args.get('year', datetime.now().year, type=int)
        month = request.args.get('month', datetime.now().month, type=int)
        
        # Get daily sales and expenses
        daily_data = db.session.query(
            func.date(Sale.sale_date).label('date'),
            func.sum(Sale.total_amount).label('sales')
        ).filter(
            extract('year', Sale.sale_date) == year,
            extract('month', Sale.sale_date) == month
        ).group_by(func.date(Sale.sale_date)).all()
        
        daily_expenses = db.session.query(
            Expense.expense_date.label('date'),
            func.sum(Expense.amount).label('expenses')
        ).filter(
            extract('year', Expense.expense_date) == year,
            extract('month', Expense.expense_date) == month
        ).group_by(Expense.expense_date).all()
        
        # Create lookup dictionaries
        sales_dict = {item[0].day: float(item[1]) for item in daily_data}
        expenses_dict = {item[0].day: float(item[1]) for item in daily_expenses}
        
        # Get days in month
        from calendar import monthrange
        days_in_month = monthrange(year, month)[1]
        
        trend_data = []
        for day in range(1, days_in_month + 1):
            trend_data.append({
                'day': day,
                'sales': sales_dict.get(day, 0),
                'expenses': expenses_dict.get(day, 0)
            })
        
        return jsonify(trend_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/sales-trend/monthly', methods=['GET'])
@jwt_required()
def get_monthly_sales_trend():
    """Get monthly sales trend for the specified year"""
    try:
        year = request.args.get('year', datetime.now().year, type=int)
        
        # Get monthly sales and expenses
        monthly_sales = db.session.query(
            extract('month', Sale.sale_date).label('month'),
            func.sum(Sale.total_amount).label('sales')
        ).filter(
            extract('year', Sale.sale_date) == year
        ).group_by(extract('month', Sale.sale_date)).all()
        
        monthly_expenses = db.session.query(
            extract('month', Expense.expense_date).label('month'),
            func.sum(Expense.amount).label('expenses')
        ).filter(
            extract('year', Expense.expense_date) == year
        ).group_by(extract('month', Expense.expense_date)).all()
        
        # Create lookup dictionaries
        sales_dict = {int(item[0]): float(item[1]) for item in monthly_sales}
        expenses_dict = {int(item[0]): float(item[1]) for item in monthly_expenses}
        
        month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                      'July', 'August', 'September', 'October', 'November', 'December']
        
        trend_data = []
        for month_num in range(1, 13):
            trend_data.append({
                'month': month_names[month_num - 1],
                'month_number': month_num,
                'sales': sales_dict.get(month_num, 0),
                'expenses': expenses_dict.get(month_num, 0)
            })
        
        return jsonify(trend_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/recent-activity', methods=['GET'])
@jwt_required()
def get_recent_activity():
    """Get recent business activity"""
    try:
        limit = request.args.get('limit', 10, type=int)
        
        # Recent sales
        recent_sales = Sale.query.order_by(Sale.sale_date.desc()).limit(limit).all()
        
        # Recent inventory changes
        recent_inventory = InventoryLog.query.order_by(InventoryLog.stock_date.desc()).limit(limit).all()
        
        # Recent expenses
        recent_expenses = Expense.query.order_by(Expense.expense_date.desc()).limit(limit).all()
        
        return jsonify({
            'recent_sales': [sale.to_dict() for sale in recent_sales],
            'recent_inventory': [log.to_dict() for log in recent_inventory],
            'recent_expenses': [expense.to_dict() for expense in recent_expenses]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
