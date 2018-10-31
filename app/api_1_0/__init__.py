#!/usr/bin/ python
# -*- coding: UTF-8 -*-

from flask import Blueprint

api = Blueprint('api', __name__)

from . import authentication, posts, users, comments, errors