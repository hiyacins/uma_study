from HiyaLib.common import ReadJsonFromFile, FileReader
from HiyaLib.Web import login_required, wraps
from flask import Flask, redirect, render_template, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from typing import Union, List, Tuple
