from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model):
    __tablename__= "user"
    user_id = db.Column(db.String(150), primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    first_name = db.Column(db.String(150),  nullable=False)
    last_name = db.Column(db.String(150))
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String, nullable=False ,unique=True)
    isflagged = db.Column(db.Boolean, default=0,nullable=False)
    pic_url = db.Column(db.String, nullable=False, default="https://thumbs.dreamstime.com/b/unisex-default-profile-picture-white-faceless-person-black-background-304887214.jpg")



class Sponsors(db.Model):
    __tablename__= "sponsor"
    sponsor_id = db.Column(db.String(150), db.ForeignKey('user.user_id'), nullable=False,primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    companyname = db.Column(db.String(50), nullable=False)
    industry = db.Column(db.String(150),nullable=False)

class Influencers(db.Model):
    __tablename__= "influencer"
    influencer_id = db.Column(db.String(150), db.ForeignKey('user.user_id'),primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(150),nullable=False)
    niche = db.Column(db.String(150),nullable=False)
    instagram = db.Column(db.Integer,nullable=False)
    facebook = db.Column(db.Integer,nullable=False)
    twitter = db.Column(db.Integer,nullable=False)

class Campaign(db.Model):
    __tablename__="campaign"
    campaign_id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(150),nullable=False)
    description = db.Column(db.String(500),nullable=False)
    category = db.Column(db.String(500),nullable=False)
    start_date = db.Column(db.Date,nullable=False)
    end_date = db.Column(db.Date,nullable=False)
    isprivate = db.Column(db.Boolean,default=False,nullable=False)
    goals = db.Column(db.String(250),nullable=False)
    budget = db.Column(db.Integer,nullable=False)
    isflagged = db.Column(db.Boolean, default=0,nullable=False)
    sponsor_id = db.Column(db.String(150), db.ForeignKey('sponsor.sponsor_id'))


class AdRequest(db.Model):
    __tablename__ = "adrequest"
    ad_id = db.Column(db.Integer,primary_key=True)
    campaign_id = db.Column(db.Integer,db.ForeignKey('campaign.campaign_id'),nullable=False)
    influencer_id = db.Column(db.String(150),db.ForeignKey('influencer.influencer_id'))
    messages = db.Column(db.String(1000),nullable=False)
    requirements = db.Column(db.String(750),nullable=False)
    payment_amount = db.Column(db.Integer,nullable=False)
    created_by = db.Column(db.String(10),nullable=False)
    updated_by = db.Column(db.String(10),nullable=False)
    status = db.Column(db.String(8),default="pending")

