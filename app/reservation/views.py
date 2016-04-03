import datetime
from flask import Blueprint, render_template, request, views, abort
from models import Reservation
from app.reservation.models import Hotels, Reservation
from app.user.loginmanager import roles_required

reservation_views = Blueprint('reservation', __name__, template_folder='../templates')

@reservation_views.route("/reservation/<int:id>/", methods=["GET", "POST"])
@roles_required('user')
def reservation(id):
	hotel = Hotels.query.get(id)
	if request.method == "POST":
		checkin_date = request.form.get('checkin')
		checkout_date = request.form.get('checout')
		room_number = request.form.get('room_number')
		room = request.form.get('room')
		adult = request.form.get('adult')
		amount = request.form.get('amount')
		night = request.form.get('night')
		return
	return render_template("reservation.html", **locals())

