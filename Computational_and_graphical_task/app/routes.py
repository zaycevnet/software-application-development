from flask import request, jsonify
from app import app, db
from app.models import Subscription
from datetime import datetime

@app.route('/subscriptions', methods=['POST'])
def add_subscription():
    data = request.get_json()

    # Валидация данных
    if not all(key in data for key in ['name', 'amount', 'periodicity', 'start_date', 'next_due_date']):
        return jsonify({'error': 'Missing required fields'}), 400

    subscription = Subscription(
        name=data['name'],
        amount=data['amount'],
        periodicity=data['periodicity'],
        start_date=datetime.strptime(data['start_date'], '%Y-%m-%d'),
        next_due_date=datetime.strptime(data['next_due_date'], '%Y-%m-%d')
    )
    
    db.session.add(subscription)
    db.session.commit()
    return jsonify({'message': 'Subscription added successfully'}), 201
