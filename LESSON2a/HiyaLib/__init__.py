from HiyaLib.common import *
from HiyaLib.Web import *
from flask import Flask, redirect, render_template, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from typing import Union, List, Tuple
