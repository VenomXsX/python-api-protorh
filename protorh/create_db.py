from database import Base, engine

# these imports r required
from models import User, RequestRH, Event, Department


Base.metadata.create_all(engine)
