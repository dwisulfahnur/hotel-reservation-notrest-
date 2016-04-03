from app.core.helper import create_app
from app.core.db import db
from app.hotel.views import hotel_views
from app.reservation.views import reservation_views
from app.user.views import user_views

from user.loginmanager import login_manager

from app.hotel.models import *
from app.reservation.models import *
from app.user.models import *


# Development Config
config = 'config.dev'
# Production Config
# config = 'config.Prod'

app = create_app(config)
db.init_app(app)
login_manager.init_app(app)

# register blue`t
app.register_blueprint(hotel_views)
app.register_blueprint(reservation_views)
app.register_blueprint(user_views)