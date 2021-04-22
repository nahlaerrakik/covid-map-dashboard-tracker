__author__ = 'nahla.errakik'

from . import db
import pandas as pd


class Country(db.Model):
    __tablename__ = 'countries'

    id = db.Column('id', db.String, primary_key=True)
    name = db.Column(db.String)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    population = db.Column(db.Integer)

    def to_dict(self):
        return dict(id=self.id,
                    name=self.name,
                    latitude=self.latitude,
                    longitude=self.longitude,
                    population=self.population)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all_countries():
        return db.session.query(Country).all()


class Case(db.Model):
    __tablename__ = 'cases'

    id = db.Column('id', db.Integer, primary_key=True)
    country = db.Column(db.String, db.ForeignKey('countries.id'))
    new_confirmed = db.Column(db.Integer)
    new_deaths = db.Column(db.Integer)
    all_confirmed = db.Column(db.Integer)
    all_deaths = db.Column(db.Integer)
    all_recovered = db.Column(db.Integer)
    all_critical = db.Column(db.Integer)
    last_updated_at = db.Column(db.DateTime)

    def to_dict(self):
        return dict(country=self.country,
                    new_confirmed=self.new_confirmed,
                    new_deaths=self.new_deaths,
                    all_confirmed=self.all_confirmed,
                    all_deaths=self.all_deaths,
                    all_recovered=self.all_recovered,
                    all_critical=self.all_critical,
                    last_updated_at=self.last_updated_on)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        case = Case.query.filter_by(country=self.country).first()
        if case is None:
            return False

        case.new_confirmed = self.new_confirmed
        case.new_deaths = self.new_deaths
        case.all_confirmed = self.all_confirmed
        case.all_deaths = self.all_deaths
        case.all_recovered = self.all_recovered
        case.all_critical = self.all_critical
        case.last_updated_at = self.last_updated_at
        db.session.commit()

        return True

    @staticmethod
    def get_all_cases():
        cases = db.session.query(Country, Case).join(Country, Country.id == Case.country).order_by(Case.all_confirmed.desc())
        statement = cases.statement
        df = pd.read_sql(statement, db.engine)
        return df

    @staticmethod
    def get_last_update():
        return db.session.query(Case.last_updated_at).order_by(Case.last_updated_at).first()

    @staticmethod
    def get_kpi():
        return db.session.query(db.func.sum(Case.all_confirmed),
                                db.func.sum(Case.all_recovered),
                                db.func.sum(Case.all_deaths),
                                db.func.sum(Case.all_critical)).first()




db.create_all()
db.session.commit()
