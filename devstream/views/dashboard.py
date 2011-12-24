# -*- coding: utf-8 -*-

from flask import Blueprint, render_template


dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard')
def dashboard_home():
    return render_template('dashboard.html')
