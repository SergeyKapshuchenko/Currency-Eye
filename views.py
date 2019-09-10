from app import app
from functools import wraps
from flask import request, abort
from config import IP_LIST
import controllers


def check_ip(func):
    @wraps(func)
    def checker(*args, **kwargs):
        if request.remote_addr not in IP_LIST:
            return abort(403)
        return func(*args, **kwargs)
    return checker


@app.route("/")
def hello():
    return "Hello everyone"


@app.route("/xrates")
def view_rates():
    return controllers.ViewAllRates().call()


@app.route("/api/xrates/<fmt>")
def api_rates(fmt):
    return controllers.GetApiRates().call(fmt)


@app.route("/update/<int:from_currency>/<int:to_currency>")
@app.route("/update/all")
def update_xrates(from_currency=None, to_currency=None):
    return controllers.UpdateRates().call(from_currency, to_currency)


@app.route("/logs/<log_type>")
@check_ip
def view_logs(log_type):
    return controllers.ViewLog().call(log_type)


@app.route("/edit/<int:from_currency>/<int:to_currency>", methods=["GET", "POST"])
@check_ip
def edit_xrate(from_currency, to_currency):
    return controllers.EditRate().call(from_currency, to_currency)
