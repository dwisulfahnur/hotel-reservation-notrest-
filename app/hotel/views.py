import datetime
from flask import Blueprint, render_template, request, redirect, url_for, abort, views, flash
from models import Hotels, Country, Province, City, HotelsFacility, HotelRoom
from sqlalchemy.exc import IntegrityError
from app.core.db import db
from flask.ext.login import current_user, login_required
from app.user.loginmanager import roles_required

hotel_views = Blueprint('hotel', __name__, static_folder='../statics', template_folder='../templates')

@hotel_views.route("/")
def index():
    return redirect(url_for('.hotel_view'))

@hotel_views.route("/hotel/", defaults={'id':None})
@hotel_views.route("/hotel/<int:id>", methods=["GET"])
def hotel_view(id):
    if id:
        if not Hotels.query.get(id):
            return abort(404)
    if id is None:
        hotels = Hotels.query.all()
        return render_template('hotels.html', **locals())
    hotel = Hotels.query.get(id)
    hotel_facility = HotelsFacility.query.filter_by(hotels_id=id).first()
    facilities = []
    facilities.append("Garage") if hotel_facility.garage is True else None
    facilities.append("Car Ports") if hotel_facility.carports is True else None
    facilities.append("Swimming Pool") if hotel_facility.swimmingpool is True else None

    hotels_room = HotelRoom.query.filter_by(hotels_id=hotel.id).all()
    return render_template('hotel.html', **locals())


## Hotel View
@hotel_views.route("/delete_hotel/", defaults={'id':None})
@hotel_views.route("/delete_hotel/<int:id>", methods=["GET"])
@roles_required('admin')
def delete_hotel(id):
    if not id:
        for hotel in Hotels.query.all():
            hotel_ = Hotels.query.get(hotel.id)
            db.session.delete(hotel_)
        db.session.commit()
        flash("Hotels data successfully deleted")
        return redirect(url_for('.hotel_view'))
    hotel = Hotels.query.get(id)
    if not hotel:
        return abort(404)

    hotel_name = hotel.name
    db.session.delete(hotel)
    db.session.commit()
    flash("%s successfully deleted"%hotel_name)
    return redirect(url_for('.hotel_view'))


## New Hotel
@hotel_views.route("/new_hotel/", methods=["GET","POST"])
@roles_required('admin')
def new_hotel():
    if request.method == "POST":
        name = request.form.get("name")
        address = request.form.get("address")
        zipcode = request.form.get("zipcode")
        country_id = int(request.form.get("country"))
        province_id = int(request.form.get("province"))
        city_id = int(request.form.get("city"))
        
        #Validate Form 
        errors = []
        def empty_error(field):
            if field == "":
                empty = "field can't empty"
                if  empty not in errors:
                    errors.append(empty)
        if country_id is 0:
            errors.append("Country is invalid")
        if province_id is 0:
            errors.append("Province is invalid")
        if city_id is 0:
            errors.append("City is invalid")
        empty_error(name)
        empty_error(address)
        empty_error(zipcode)

        if len(errors) == 0:
            hotel = Hotels(name=name,
                           address=address,
                           zipcode=zipcode,
                           country_id=country_id, 
                           province_id=province_id,
                           city_id=city_id)
            db.session.add(hotel)
            db.session.commit()

            garage = request.form.get(("garage"))
            carports = request.form.get(("carports"))
            swimmingpool = request.form.get(("swimmingpool"))
            hotel_facility = HotelsFacility(hotels_id=hotel.id,
                                            garage=bool(garage),
                                            carports=bool(carports),
                                            swimmingpool=bool(swimmingpool))
            db.session.add(hotel_facility)
            db.session.commit()
            flash("Hotel successfully created")
    cities = City.query.all()
    provincies = Province.query.all()
    countries = Country.query.all()
    return render_template('new_hotel.html', **locals())

#Hotel Update
@hotel_views.route("/update_hotel/<int:id>", methods=["POST", "GET"])
@roles_required('admin')
def update_hotel(id):
    hotel = Hotels.query.get(id)
    if not hotel:
        return abort(404)
    if request.method == "POST":
        name = request.form.get("name")
        address = request.form.get("address")
        zipcode = request.form.get("zipcode")
        country_id = int(request.form.get("country"))
        province_id = int(request.form.get("province"))
        city_id = int(request.form.get("city"))
        errors = []
        def empty_error(field):
            if field == "":
                empty ="field can't empty"
                if  empty not in errors:
                    errors.append(empty)

        empty_error(name)
        empty_error(address)
        empty_error(zipcode)
            
        if country_id is 0:
            errors.append("Country is invalid")
        if province_id is 0:
            errors.append("Province is invalid")
        if city_id is 0:
            errors.append("City is invalid")

        if len(errors) == 0:
            hotel.name=name,
            hotel.address=address,
            hotel.zipcode=zipcode,
            hotel.country_id=country_id, 
            hotel.province_id=province_id,
            hotel.city_id=city_id

            garage = bool(request.form.get(("garage")))
            carports = bool(request.form.get(("carports")))
            swimmingpool = bool(request.form.get(("swimmingpool")))

            facility = HotelsFacility.query.filter_by(hotels_id=hotel.id).first()
            facility.garage = garage
            facility.carports = carports
            facility.swimmingpool = swimmingpool

            db.session.commit()
            flash("Hotel successfully updated")

    cities = City.query.all()
    provincies = Province.query.all()
    countries = Country.query.all()
        
    
    facility = HotelsFacility.query.filter_by(hotels_id=hotel.id).first()
    if facility.garage is True:
        facility.garage =  "%d checked"%facility.garage
    if facility.carports is True:
        facility.carports = "%d checked"%facility.carports
    if facility.swimmingpool is True:
        facility.swimmingpool = "%d checked"%facility.swimmingpool

    return render_template("update_hotel.html", **locals())