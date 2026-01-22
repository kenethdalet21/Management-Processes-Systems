from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models import Sale, Expense, Asset, Liability, Equity, CashFlow, Product, SaleItem, PayrollRecord
from app.models.financial import ExpenseCategory
from sqlalchemy import func, extract
from datetime import datetime
from decimal import Decimal

bp = Blueprint('financial', __name__)

@bp.route('/statements', methods=['GET'])
@jwt_required()
def get_financial_statements():
    """Get consolidated financial statements"""
    try:
        year = request.args.get('year', datetime.now().year, type=int)
        
        # Revenue calculations
        sales_revenue = db.session.query(func.sum(Sale.total_amount)).filter(
            extract('year', Sale.created_at) == year
        ).scalar() or 0
        
        # COGS - Cost of products sold
        cogs = db.session.query(
            func.sum(Product.item_cost * SaleItem.quantity)
        ).join(SaleItem, Product.id == SaleItem.product_id).join(
            Sale, Sale.id == SaleItem.sale_id
        ).filter(extract('year', Sale.created_at) == year).scalar() or 0
        
        # Payroll expenses
        payroll_expenses = db.session.query(func.sum(PayrollRecord.gross_pay)).filter(
            extract('year', PayrollRecord.pay_period_start) == year,
            PayrollRecord.is_paid == True
        ).scalar() or 0
        
        # Other expenses
        other_expenses = db.session.query(func.sum(Expense.amount)).filter(
            extract('year', Expense.expense_date) == year
        ).scalar() or 0
        
        total_revenue = float(sales_revenue)
        cost_of_goods_sold = float(cogs)
        gross_profit = total_revenue - cost_of_goods_sold
        operating_expenses = float(payroll_expenses) + float(other_expenses)
        operating_income = gross_profit - operating_expenses
        net_income = operating_income
        
        # Balance Sheet
        inventory_value = db.session.query(
            func.sum(Product.item_cost * Product.current_stock)
        ).filter(Product.track_inventory == True).scalar() or 0
        
        assets = Asset.query.all()
        current_assets_db = sum(a.book_value for a in assets if a.asset_type == 'current')
        non_current_assets = sum(a.book_value for a in assets if a.asset_type != 'current')
        
        liabilities = Liability.query.all()
        current_liabilities = sum(float(l.current_balance) for l in liabilities if l.liability_type == 'current')
        long_term_liabilities = sum(float(l.current_balance) for l in liabilities if l.liability_type == 'long_term')
        
        # Accrued payroll (unpaid)
        accrued_payroll = db.session.query(func.sum(PayrollRecord.net_pay)).filter(
            PayrollRecord.is_paid == False
        ).scalar() or 0
        
        equity_records = Equity.query.all()
        shareholders_equity = sum(float(e.amount) for e in equity_records)
        
        # Cash estimate (revenue - paid expenses)
        cash = total_revenue - cost_of_goods_sold - float(payroll_expenses) - float(other_expenses)
        
        current_assets = float(inventory_value) + max(0, cash) + current_assets_db
        total_assets = current_assets + non_current_assets
        total_liabilities = current_liabilities + long_term_liabilities + float(accrued_payroll)
        
        # Cash Flow
        cash_from_sales = total_revenue
        inventory_purchases = float(cogs)  # Simplified
        operating_cash_flow = cash_from_sales - float(payroll_expenses) - float(other_expenses)
        investing_cash_flow = -inventory_purchases
        net_cash_change = operating_cash_flow + investing_cash_flow
        
        return jsonify({
            'income_statement': {
                'total_revenue': round(total_revenue, 2),
                'sales_revenue': round(float(sales_revenue), 2),
                'service_revenue': 0,
                'cost_of_goods_sold': round(cost_of_goods_sold, 2),
                'gross_profit': round(gross_profit, 2),
                'operating_expenses': round(operating_expenses, 2),
                'payroll_expenses': round(float(payroll_expenses), 2),
                'other_expenses': round(float(other_expenses), 2),
                'operating_income': round(operating_income, 2),
                'other_income': 0,
                'net_income': round(net_income, 2)
            },
            'balance_sheet': {
                'current_assets': round(current_assets, 2),
                'cash': round(max(0, cash), 2),
                'accounts_receivable': 0,
                'inventory_value': round(float(inventory_value), 2),
                'non_current_assets': round(non_current_assets, 2),
                'total_assets': round(total_assets, 2),
                'current_liabilities': round(current_liabilities + float(accrued_payroll), 2),
                'accounts_payable': 0,
                'accrued_payroll': round(float(accrued_payroll), 2),
                'long_term_liabilities': round(long_term_liabilities, 2),
                'total_liabilities': round(total_liabilities, 2),
                'shareholders_equity': round(shareholders_equity + net_income, 2)
            },
            'cash_flow': {
                'net_income': round(net_income, 2),
                'cash_from_sales': round(cash_from_sales, 2),
                'payroll_payments': round(float(payroll_expenses), 2),
                'operating_cash_flow': round(operating_cash_flow, 2),
                'inventory_purchases': round(inventory_purchases, 2),
                'investing_cash_flow': round(investing_cash_flow, 2),
                'net_cash_change': round(net_cash_change, 2)
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/ratios', methods=['GET'])
@jwt_required()
def get_financial_ratios():
    """Calculate all financial ratios"""
    try:
        year = request.args.get('year', datetime.now().year, type=int)
        
        # Get data for calculations
        sales_revenue = db.session.query(func.sum(Sale.total_amount)).filter(
            extract('year', Sale.created_at) == year
        ).scalar() or 0
        
        cogs = db.session.query(
            func.sum(Product.item_cost * SaleItem.quantity)
        ).join(SaleItem, Product.id == SaleItem.product_id).join(
            Sale, Sale.id == SaleItem.sale_id
        ).filter(extract('year', Sale.created_at) == year).scalar() or 0
        
        inventory_value = db.session.query(
            func.sum(Product.item_cost * Product.current_stock)
        ).filter(Product.track_inventory == True).scalar() or 0
        
        payroll = db.session.query(func.sum(PayrollRecord.gross_pay)).filter(
            extract('year', PayrollRecord.pay_period_start) == year
        ).scalar() or 0
        
        expenses = db.session.query(func.sum(Expense.amount)).filter(
            extract('year', Expense.expense_date) == year
        ).scalar() or 0
        
        revenue = float(sales_revenue)
        cogs_val = float(cogs)
        gross_profit = revenue - cogs_val
        operating_expenses = float(payroll) + float(expenses)
        net_income = gross_profit - operating_expenses
        
        # Balance sheet values
        assets = Asset.query.all()
        current_assets_db = sum(a.book_value for a in assets if a.asset_type == 'current')
        total_assets = sum(a.book_value for a in assets) + float(inventory_value)
        
        liabilities = Liability.query.all()
        current_liabilities = sum(float(l.current_balance) for l in liabilities if l.liability_type == 'current')
        total_liabilities = sum(float(l.current_balance) for l in liabilities)
        
        equity = sum(float(e.amount) for e in Equity.query.all())
        total_equity = equity + net_income if equity > 0 else net_income
        
        current_assets = float(inventory_value) + current_assets_db + max(0, revenue - cogs_val - operating_expenses)
        
        # Ensure we don't divide by zero
        safe_div = lambda n, d: round(n / d, 4) if d > 0 else 0
        
        return jsonify({
            'liquidity': {
                'current_ratio': safe_div(current_assets, current_liabilities) if current_liabilities > 0 else 2.0,
                'quick_ratio': safe_div(current_assets - float(inventory_value), current_liabilities) if current_liabilities > 0 else 1.5,
                'cash_ratio': safe_div(max(0, revenue - cogs_val - operating_expenses), current_liabilities) if current_liabilities > 0 else 1.0,
                'working_capital': round(current_assets - current_liabilities, 2)
            },
            'profitability': {
                'gross_margin': safe_div(gross_profit, revenue),
                'operating_margin': safe_div(gross_profit - operating_expenses, revenue),
                'net_margin': safe_div(net_income, revenue),
                'roe': safe_div(net_income, total_equity) if total_equity > 0 else 0,
                'roa': safe_div(net_income, total_assets) if total_assets > 0 else 0
            },
            'leverage': {
                'debt_to_equity': safe_div(total_liabilities, total_equity) if total_equity > 0 else 0,
                'debt_ratio': safe_div(total_liabilities, total_assets) if total_assets > 0 else 0,
                'equity_ratio': safe_div(total_equity, total_assets) if total_assets > 0 else 1
            },
            'efficiency': {
                'asset_turnover': safe_div(revenue, total_assets) if total_assets > 0 else 0,
                'inventory_turnover': safe_div(cogs_val, float(inventory_value)) if inventory_value > 0 else 0,
                'days_sales_outstanding': round(safe_div(0, revenue) * 365, 1) if revenue > 0 else 0
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/income-statement', methods=['GET'])
@jwt_required()
def get_income_statement():
    """Generate Income Statement (Profit and Loss Statement)"""
    try:
        year = request.args.get('year', datetime.now().year, type=int)
        month = request.args.get('month', type=int)
        
        # Revenue (Sales)
        revenue_query = db.session.query(func.sum(Sale.total_amount))
        if month:
            revenue = revenue_query.filter(
                extract('year', Sale.sale_date) == year,
                extract('month', Sale.sale_date) == month
            ).scalar() or 0
        else:
            revenue = revenue_query.filter(
                extract('year', Sale.sale_date) == year
            ).scalar() or 0
        
        # Expenses by category
        expense_query = db.session.query(
            Expense.category,
            func.sum(Expense.amount)
        ).group_by(Expense.category)
        
        if month:
            expenses = expense_query.filter(
                extract('year', Expense.expense_date) == year,
                extract('month', Expense.expense_date) == month
            ).all()
        else:
            expenses = expense_query.filter(
                extract('year', Expense.expense_date) == year
            ).all()
        
        expense_breakdown = {
            item[0].value if hasattr(item[0], 'value') else str(item[0]): float(item[1])
            for item in expenses
        }
        
        total_expenses = sum(expense_breakdown.values())
        profit_loss = float(revenue) - total_expenses
        profit_margin = (profit_loss / float(revenue) * 100) if revenue > 0 else 0
        
        return jsonify({
            'period': {
                'year': year,
                'month': month
            },
            'revenue': round(float(revenue), 2),
            'expenses': {
                'breakdown': expense_breakdown,
                'total': round(total_expenses, 2)
            },
            'profit_loss': round(profit_loss, 2),
            'profit_margin': round(profit_margin, 2)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/balance-sheet', methods=['GET'])
@jwt_required()
def get_balance_sheet():
    """Generate Balance Sheet"""
    try:
        as_of_date = request.args.get('date', datetime.now().date())
        
        # Assets
        assets = Asset.query.all()
        current_assets = sum(asset.book_value for asset in assets if asset.asset_type == 'current')
        fixed_assets = sum(asset.book_value for asset in assets if asset.asset_type == 'fixed')
        intangible_assets = sum(asset.book_value for asset in assets if asset.asset_type == 'intangible')
        total_assets = current_assets + fixed_assets + intangible_assets
        
        # Liabilities
        liabilities = Liability.query.all()
        current_liabilities = sum(float(lib.current_balance) for lib in liabilities if lib.liability_type == 'current')
        long_term_liabilities = sum(float(lib.current_balance) for lib in liabilities if lib.liability_type == 'long_term')
        total_liabilities = current_liabilities + long_term_liabilities
        
        # Equity
        equity_records = Equity.query.all()
        total_equity = sum(float(eq.amount) for eq in equity_records)
        
        # Check balance
        total_liabilities_equity = total_liabilities + total_equity
        is_balanced = abs(total_assets - total_liabilities_equity) < 0.01
        
        return jsonify({
            'as_of_date': str(as_of_date),
            'assets': {
                'current_assets': round(current_assets, 2),
                'fixed_assets': round(fixed_assets, 2),
                'intangible_assets': round(intangible_assets, 2),
                'total': round(total_assets, 2)
            },
            'liabilities': {
                'current_liabilities': round(current_liabilities, 2),
                'long_term_liabilities': round(long_term_liabilities, 2),
                'total': round(total_liabilities, 2)
            },
            'equity': {
                'total': round(total_equity, 2)
            },
            'total_liabilities_equity': round(total_liabilities_equity, 2),
            'is_balanced': is_balanced
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/cash-flow-statement', methods=['GET'])
@jwt_required()
def get_cash_flow_statement():
    """Generate Cash Flow Statement"""
    try:
        year = request.args.get('year', datetime.now().year, type=int)
        month = request.args.get('month', type=int)
        
        query = CashFlow.query
        if month:
            query = query.filter(
                extract('year', CashFlow.transaction_date) == year,
                extract('month', CashFlow.transaction_date) == month
            )
        else:
            query = query.filter(extract('year', CashFlow.transaction_date) == year)
        
        cash_flows = query.all()
        
        # Categorize cash flows
        operating_in = sum(float(cf.amount) for cf in cash_flows if cf.flow_type == 'in' and cf.category == 'operating')
        operating_out = sum(float(cf.amount) for cf in cash_flows if cf.flow_type == 'out' and cf.category == 'operating')
        
        investing_in = sum(float(cf.amount) for cf in cash_flows if cf.flow_type == 'in' and cf.category == 'investing')
        investing_out = sum(float(cf.amount) for cf in cash_flows if cf.flow_type == 'out' and cf.category == 'investing')
        
        financing_in = sum(float(cf.amount) for cf in cash_flows if cf.flow_type == 'in' and cf.category == 'financing')
        financing_out = sum(float(cf.amount) for cf in cash_flows if cf.flow_type == 'out' and cf.category == 'financing')
        
        net_operating = operating_in - operating_out
        net_investing = investing_in - investing_out
        net_financing = financing_in - financing_out
        
        net_cash_flow = net_operating + net_investing + net_financing
        
        return jsonify({
            'period': {
                'year': year,
                'month': month
            },
            'operating_activities': {
                'inflows': round(operating_in, 2),
                'outflows': round(operating_out, 2),
                'net': round(net_operating, 2)
            },
            'investing_activities': {
                'inflows': round(investing_in, 2),
                'outflows': round(investing_out, 2),
                'net': round(net_investing, 2)
            },
            'financing_activities': {
                'inflows': round(financing_in, 2),
                'outflows': round(financing_out, 2),
                'net': round(net_financing, 2)
            },
            'net_cash_flow': round(net_cash_flow, 2)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
