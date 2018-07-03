#!/usr/bin/ python
# -*- coding: UTF-8 -*-

from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views