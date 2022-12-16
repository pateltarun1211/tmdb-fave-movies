from functools import wraps
import secrets
from flask import request, jsonify, json, session
from movies_inventory.models import User
from flask_login import current_user
import decimal
import logging

def token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):

        token = current_user.token

        
        if not token:
            return jsonify({ 'message': 'Token is Missing!'}), 401
            
        return our_flask_function(token, *args, **kwargs)
    return decorated

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(JSONEncoder, self).default(obj)