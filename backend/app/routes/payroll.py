from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User, UserRole, PayrollRecord
from sqlalchemy import func, extract, and_
from datetime import datetime, date
from decimal import Decimal

bp = Blueprint('payroll', __name__)

def check_permission(user_id, required_roles):
    """Check if user has required role"""
    user = User.query.get(user_id)
    return user and user.role in required_roles


@bp.route('/employees', methods=['GET'])
@jwt_required()
def get_employees():
    """Get all employees"""
    try:
        user_id = get_jwt_identity()
        
        if not check_permission(user_id, [UserRole.ADMIN, UserRole.FINANCE_MANAGER]):
            return jsonify({'error': 'Insufficient permissions'}), 403
        
        employees = User.query.filter_by(is_active=True).order_by(User.last_name).all()
        
        return jsonify({
            'employees': [e.to_dict() for e in employees]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/records', methods=['GET'])
@jwt_required()
def get_payroll_records():
    """Get payroll records with filtering"""
    try:
        user_id = get_jwt_identity()
        
        if not check_permission(user_id, [UserRole.ADMIN, UserRole.FINANCE_MANAGER]):
            return jsonify({'error': 'Insufficient permissions'}), 403
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        employee_id = request.args.get('employee_id', type=int)
        year = request.args.get('year', type=int)
        month = request.args.get('month', type=int)
        
        query = PayrollRecord.query
        
        if employee_id:
            query = query.filter_by(employee_id=employee_id)
        
        if year:
            query = query.filter(extract('year', PayrollRecord.pay_period_start) == year)
        
        if month:
            query = query.filter(extract('month', PayrollRecord.pay_period_start) == month)
        
        query = query.order_by(PayrollRecord.pay_period_start.desc())
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'records': [r.to_dict() for r in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/records', methods=['POST'])
@jwt_required()
def create_payroll_record():
    """Create a payroll record"""
    try:
        user_id = get_jwt_identity()
        
        if not check_permission(user_id, [UserRole.ADMIN, UserRole.FINANCE_MANAGER]):
            return jsonify({'error': 'Insufficient permissions'}), 403
        
        data = request.get_json()
        
        required_fields = ['employee_id', 'pay_period_start', 'pay_period_end']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Check if employee exists
        employee = User.query.get(data['employee_id'])
        if not employee:
            return jsonify({'error': 'Employee not found'}), 404
        
        # Calculate payroll
        base_salary = Decimal(str(data.get('base_salary', 0)))
        hourly_rate = Decimal(str(data.get('hourly_rate', 0)))
        regular_hours = Decimal(str(data.get('regular_hours', 0)))
        overtime_hours = Decimal(str(data.get('overtime_hours', 0)))
        overtime_rate = hourly_rate * Decimal('1.5')
        
        regular_pay = base_salary + (hourly_rate * regular_hours)
        overtime_pay = overtime_rate * overtime_hours
        bonuses = Decimal(str(data.get('bonuses', 0)))
        
        gross_pay = regular_pay + overtime_pay + bonuses
        
        # Deductions
        tax_deductions = Decimal(str(data.get('tax_deductions', 0)))
        insurance_deductions = Decimal(str(data.get('insurance_deductions', 0)))
        other_deductions = Decimal(str(data.get('other_deductions', 0)))
        
        total_deductions = tax_deductions + insurance_deductions + other_deductions
        net_pay = gross_pay - total_deductions
        
        record = PayrollRecord(
            employee_id=data['employee_id'],
            pay_period_start=datetime.fromisoformat(data['pay_period_start']).date(),
            pay_period_end=datetime.fromisoformat(data['pay_period_end']).date(),
            base_salary=base_salary,
            hourly_rate=hourly_rate,
            regular_hours=regular_hours,
            overtime_hours=overtime_hours,
            overtime_rate=overtime_rate,
            regular_pay=regular_pay,
            overtime_pay=overtime_pay,
            bonuses=bonuses,
            gross_pay=gross_pay,
            tax_deductions=tax_deductions,
            insurance_deductions=insurance_deductions,
            other_deductions=other_deductions,
            total_deductions=total_deductions,
            net_pay=net_pay,
            is_paid=data.get('is_paid', False),
            payment_method=data.get('payment_method', 'bank_transfer'),
            notes=data.get('notes', '')
        )
        
        db.session.add(record)
        db.session.commit()
        
        return jsonify({
            'message': 'Payroll record created successfully',
            'record': record.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/records/<int:record_id>', methods=['PUT'])
@jwt_required()
def update_payroll_record(record_id):
    """Update a payroll record"""
    try:
        user_id = get_jwt_identity()
        
        if not check_permission(user_id, [UserRole.ADMIN, UserRole.FINANCE_MANAGER]):
            return jsonify({'error': 'Insufficient permissions'}), 403
        
        record = PayrollRecord.query.get(record_id)
        
        if not record:
            return jsonify({'error': 'Payroll record not found'}), 404
        
        if record.is_paid:
            return jsonify({'error': 'Cannot modify paid payroll record'}), 400
        
        data = request.get_json()
        
        # Update fields
        if 'base_salary' in data:
            record.base_salary = Decimal(str(data['base_salary']))
        if 'hourly_rate' in data:
            record.hourly_rate = Decimal(str(data['hourly_rate']))
        if 'regular_hours' in data:
            record.regular_hours = Decimal(str(data['regular_hours']))
        if 'overtime_hours' in data:
            record.overtime_hours = Decimal(str(data['overtime_hours']))
        if 'bonuses' in data:
            record.bonuses = Decimal(str(data['bonuses']))
        if 'tax_deductions' in data:
            record.tax_deductions = Decimal(str(data['tax_deductions']))
        if 'insurance_deductions' in data:
            record.insurance_deductions = Decimal(str(data['insurance_deductions']))
        if 'other_deductions' in data:
            record.other_deductions = Decimal(str(data['other_deductions']))
        if 'notes' in data:
            record.notes = data['notes']
        
        # Recalculate
        record.overtime_rate = record.hourly_rate * Decimal('1.5') if record.hourly_rate else Decimal('0')
        record.regular_pay = (record.base_salary or Decimal('0')) + ((record.hourly_rate or Decimal('0')) * (record.regular_hours or Decimal('0')))
        record.overtime_pay = (record.overtime_rate or Decimal('0')) * (record.overtime_hours or Decimal('0'))
        record.gross_pay = record.regular_pay + record.overtime_pay + (record.bonuses or Decimal('0'))
        record.total_deductions = (record.tax_deductions or Decimal('0')) + (record.insurance_deductions or Decimal('0')) + (record.other_deductions or Decimal('0'))
        record.net_pay = record.gross_pay - record.total_deductions
        
        db.session.commit()
        
        return jsonify({
            'message': 'Payroll record updated successfully',
            'record': record.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/records/<int:record_id>', methods=['DELETE'])
@jwt_required()
def delete_payroll_record(record_id):
    """Delete a payroll record"""
    try:
        user_id = get_jwt_identity()
        
        if not check_permission(user_id, [UserRole.ADMIN]):
            return jsonify({'error': 'Insufficient permissions'}), 403
        
        record = PayrollRecord.query.get(record_id)
        
        if not record:
            return jsonify({'error': 'Payroll record not found'}), 404
        
        if record.is_paid:
            return jsonify({'error': 'Cannot delete paid payroll record'}), 400
        
        db.session.delete(record)
        db.session.commit()
        
        return jsonify({'message': 'Payroll record deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/summary', methods=['GET'])
@jwt_required()
def get_payroll_summary():
    """Get payroll summary"""
    try:
        user_id = get_jwt_identity()
        
        if not check_permission(user_id, [UserRole.ADMIN, UserRole.FINANCE_MANAGER]):
            return jsonify({'error': 'Insufficient permissions'}), 403
        
        year = request.args.get('year', datetime.now().year, type=int)
        month = request.args.get('month', datetime.now().month, type=int)
        
        # Monthly totals
        monthly_records = PayrollRecord.query.filter(
            extract('year', PayrollRecord.pay_period_start) == year,
            extract('month', PayrollRecord.pay_period_start) == month
        ).all()
        
        total_gross = sum(float(r.gross_pay) for r in monthly_records)
        total_deductions = sum(float(r.total_deductions) for r in monthly_records)
        total_net = sum(float(r.net_pay) for r in monthly_records)
        
        pending_count = len([r for r in monthly_records if not r.is_paid])
        paid_count = len([r for r in monthly_records if r.is_paid])
        
        # Yearly totals
        yearly_records = PayrollRecord.query.filter(
            extract('year', PayrollRecord.pay_period_start) == year
        ).all()
        yearly_net = sum(float(r.net_pay) for r in yearly_records)
        
        # Monthly breakdown
        monthly_breakdown = db.session.query(
            extract('month', PayrollRecord.pay_period_start).label('month'),
            func.sum(PayrollRecord.gross_pay),
            func.sum(PayrollRecord.net_pay),
            func.count(PayrollRecord.id)
        ).filter(
            extract('year', PayrollRecord.pay_period_start) == year
        ).group_by(extract('month', PayrollRecord.pay_period_start)).all()
        
        return jsonify({
            'period': {'year': year, 'month': month},
            'monthly': {
                'total_employees': len(monthly_records),
                'total_gross_pay': round(total_gross, 2),
                'total_deductions': round(total_deductions, 2),
                'total_net_pay': round(total_net, 2),
                'pending': pending_count,
                'paid': paid_count
            },
            'yearly': {
                'total_net_pay': round(yearly_net, 2),
                'monthly_breakdown': [
                    {
                        'month': int(item[0]),
                        'gross_pay': round(float(item[1]), 2),
                        'net_pay': round(float(item[2]), 2),
                        'employees': int(item[3])
                    } for item in monthly_breakdown
                ]
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/pay/<int:record_id>', methods=['POST'])
@jwt_required()
def mark_as_paid(record_id):
    """Mark payroll record as paid"""
    try:
        user_id = get_jwt_identity()
        
        if not check_permission(user_id, [UserRole.ADMIN, UserRole.FINANCE_MANAGER]):
            return jsonify({'error': 'Insufficient permissions'}), 403
        
        record = PayrollRecord.query.get(record_id)
        
        if not record:
            return jsonify({'error': 'Payroll record not found'}), 404
        
        record.is_paid = True
        record.payment_date = date.today()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Payroll marked as paid',
            'record': record.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
