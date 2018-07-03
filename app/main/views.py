#!/usr/bin/ python
# -*- coding: UTF-8 -*-

from flask import render_template
from . import main


@main.route('/')
def index():
    return render_template('index.html')