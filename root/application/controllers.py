from flask import redirect,url_for,render_template,request,session
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
from flask import current_app as app
from application.database import User, Sponsors,Influencers,Campaign,AdRequest
from application.database import db
from sqlalchemy import func
from flask_restful import Api,Resource


USER = None
api = Api(app)

nic=["Machine learning", "Neural networks", "Natural language processing","Threat analysis", "Penetration testing", "Network security","Frontend", "Backend", "Full-stack", "Frameworks","Diet planning", "Food science", "Supplements","Exercise routines", "Strength training", "Cardiovascular health","Therapy", "Mindfulness", "Stress management","Stocks", "bonds", "real estate","Budgeting", "saving", "debt management","Bitcoin", "Ethereum", "blockchain technology","Curriculum development", "Classroom management", "Educational technology","University programs", "Research", "Academic advising","E-learning platforms", "MOOCs", "Distance education","Genres", "Reviews", "Film production","Genres", "Artists", "Production techniques","Video games", "Board games", "Game design","Popular tourist spots", "Off-the-beaten-path locations","Packing", "Safety", "Cultural etiquette","Itinerary creation", "Budgeting", "Accommodations","Cooking techniques", "Meal ideas", "Dietary preferences","Reviews", "Cuisine types", "Dining experiences","Regional specialties", "Food history", "Culinary traditions","Football", "Basketball", "Soccer","Tennis", "Golf", "Swimming","Performance analysis", "Injury prevention", "Training techniques","Genetics", "Ecology", "Microbiology","Quantum mechanics", "Astrophysics", "Classical mechanics","Organic chemistry", "Inorganic chemistry", "Physical chemistry","Painting", "Sculpture", "Photography","Theatre", "Dance", "Music performance","Genres", "Authors", "Literary analysis","Makeup","Skincare","Haircare","Fashion","Nails","Beauty Trends"]



@app.route('/')
def base():
    return render_template('base.html',prof1=USER)


@app.route('/signupcr' ,methods=["GET","POST"])
def signupcr():
    if request.method == "POST":
        firstname = request.form.get('firstname').strip()
        lastname = request.form.get('lastname').strip()
        category = request.form.get('category').strip()
        niche = request.form.get('niche').strip()
        instagram = request.form.get('instagram').strip()
        facebook = request.form.get('facebook').strip()
        twitter = request.form.get('twitter').strip()
        username = request.form.get('username').strip()
        email = request.form.get('email').strip()
        password = request.form.get('password').strip()
        cpassword = request.form.get('cpassword').strip()


        if len(firstname) < 3 :
            return(render_template('error.html',first=True,prof1=USER))
        elif int(instagram) < 1 or int(facebook) < 1 or int(twitter) < 1:
            return(render_template('error.html',fol=True,prof1=USER))
        elif len(username) < 4:
            return(render_template('error.html',uname=True,prof1=USER))
        elif "@" not in email or ".com" not in email:
            return(render_template('error.html',valid=True,prof1=USER))
        elif len(password) < 8 and len(password) > 12 :
            return(render_template('error.html',length=True,prof1=USER))
        elif password != cpassword:
            #flash('Password and Confirm Password mismatch.', category='error')
            return(render_template('error.html',mismatch=True,prof1=USER))
        else:
            count = User.query.count() + 1
            userid = "in" + str(count)
            newuser = User(user_id = userid,first_name=firstname,last_name=lastname,username=username,email = email,password=generate_password_hash(password,method='scrypt'))

            newinfluencer = Influencers(influencer_id = userid,name= firstname+" "+lastname,category=category,niche=niche,instagram=instagram,facebook=facebook,twitter=twitter)

            db.session.add(newuser)
            db.session.add(newinfluencer)
            db.session.commit()

            return render_template('login.html',prof1=USER)
    else:
        cat= ["Technology","Health","Finance","Education","Entertainment","Travel","Food","Sports","Science","Arts","Beauty"]
        return render_template('signupcr.html',categories=cat,niches=nic,prof1=USER)
    
@app.route('/signupbr', methods=["GET","POST"])
def signupbr():
    if request.method == "POST":
        firstname = request.form.get('firstname').strip()
        lastname = request.form.get('lastname').strip()
        companyname = request.form.get('company').strip()
        industry = request.form.get('industry').strip()
        username = request.form.get('username').strip()
        email = request.form.get('email').strip()
        password = request.form.get('password').strip()
        cpassword = request.form.get('cpassword').strip()

        user = User.query.filter_by(username=username).first()
        if user:
            return(render_template('error.html',us=True,prof1=USER))
        elif len(firstname) < 3 :
            return(render_template('error.html',first=True,prof1=USER))
        elif len(companyname) < 3 :
            return(render_template('error.html',cname=True,prof1=USER))
        elif len(username) < 4:
            return(render_template('error.html',uname=True,prof1=USER))
        elif "@" not in email or ".com" not in email:
            return(render_template('error.html',valid=True,prof1=USER))
        elif len(password) < 8 and len(password) > 12 :
            return(render_template('error.html',length=True,prof1=USER))
        elif password != cpassword:
            return(render_template('error.html',mismatch=True,prof1=USER))
        else:
            count = User.query.count() + 1
            userid = "sp" + str(count)
            newuser = User(user_id = userid,first_name=firstname,last_name=lastname,username=username,email = email,password=generate_password_hash(password,method='scrypt'))

            newsponsor = Sponsors(sponsor_id = userid,name= firstname+' '+lastname,companyname=companyname,industry=industry)

            db.session.add(newuser)
            db.session.add(newsponsor)
            db.session.commit()

            return render_template('login.html',prof1=USER)
    else:
        
        ind=["Technology","Health","Finance","Education","Entertainment","Travel","Food","Sports","Science","Arts","Beauty"]
        return render_template('signupbr.html',industries=ind,prof1=USER)
    
@app.route('/login', methods=["GET","POST"])
def login():
    if request.method=="POST":
        username = request.form.get('username')
        pas = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if 'adm' in user.user_id:
            return render_template('error.html',adm=True,prof1=user)

        if user:
            if check_password_hash(user.password,pas):
                session['user'] = user.user_id
                if "in" in user.user_id:
                    prof2 = Influencers.query.filter_by(influencer_id = user.user_id).first()

                    addata = AdRequest.query.filter_by(influencer_id=session['user']).all()

                    data= Sponsors.query.join(Campaign,Sponsors.sponsor_id==Campaign.sponsor_id).join(AdRequest,AdRequest.campaign_id== Campaign.campaign_id).with_entities(Sponsors.name.label("Sponsor_name"), Sponsors.companyname, Sponsors.industry, Campaign.budget,Campaign.name.label("Campaign_name"), Campaign.description,Campaign.category, Campaign.start_date, Campaign.end_date,Campaign.goals, AdRequest.ad_id, AdRequest.influencer_id, AdRequest.messages,AdRequest.requirements, AdRequest.payment_amount, AdRequest.status,AdRequest.created_by,AdRequest.updated_by).all()
     
                    return render_template('home.html', prof1= user, prof2=prof2 ,data=data)
                
                elif "sp" in user.user_id :
                    prof2 = Sponsors.query.filter_by(sponsor_id = user.user_id).first()
                    campaigndata = Campaign.query.filter_by(sponsor_id=session['user']).all()[-3:]
                    categories=["Technology","Health","Finance","Education","Entertainment","Travel","Food","Sports","Science","Arts","Beauty"]

                    adcampdata = AdRequest.query.join(Campaign,Campaign.campaign_id==AdRequest.campaign_id).with_entities(AdRequest.ad_id,AdRequest.campaign_id.label('campaign_id'),AdRequest.influencer_id,AdRequest.messages,AdRequest.requirements,AdRequest.payment_amount,AdRequest.created_by,AdRequest.updated_by,AdRequest.status,Campaign.name.label("campaign_name"),Campaign.description,Campaign.category,Campaign.start_date,Campaign.end_date,Campaign.isprivate,Campaign.goals,Campaign.budget,Campaign.sponsor_id)

                    return render_template('home.html', prof1= user, prof2=prof2,campaigndata = campaigndata,categories=categories,adcampdata=adcampdata)  
            else:
                return render_template('error.html',pas=True,prof1=USER)
        else:
            return render_template('error.html', user=True,prof1=USER) , 400
    else:
        return render_template("login.html", prof1=USER)
    
@app.route('/admin_login', methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):

            pending_count = AdRequest.query.filter_by(status='pending').count()
            accepted_count = AdRequest.query.filter_by(status='accepted').count()
            rejected_count = AdRequest.query.filter_by(status='rejected').count()
            user_count = User.query.count()
            camp_count = Campaign.query.count()
            ad_count = AdRequest.query.count()
            influ_count = Influencers.query.count()

            total_count = pending_count + accepted_count + rejected_count
            if total_count > 0:
                pending_percentage = (pending_count / total_count) * 100
                accepted_percentage = (accepted_count / total_count) * 100
                rejected_percentage = (rejected_count / total_count) * 100
            else:
                pending_percentage = accepted_percentage = rejected_percentage = 0


            categories = [
                {'name': 'Technology', 'count': Campaign.query.filter_by(category='Technology').count()},
                {'name': 'Health', 'count': Campaign.query.filter_by(category='Health').count()},
                {'name': 'Finance', 'count': Campaign.query.filter_by(category='Finance').count()},
                {'name': 'Education', 'count': Campaign.query.filter_by(category='Education').count()},
                {'name': 'Entertainment', 'count': Campaign.query.filter_by(category='Entertainment').count()},
                {'name': 'Travel', 'count': Campaign.query.filter_by(category='Travel').count()},
                {'name': 'Food', 'count': Campaign.query.filter_by(category='Food').count()},
                {'name': 'Sports', 'count': Campaign.query.filter_by(category='Sports').count()},
                {'name': 'Science', 'count': Campaign.query.filter_by(category='Science').count()},
                {'name': 'Arts', 'count': Campaign.query.filter_by(category='Arts').count()},
                {'name': 'Beauty', 'count': Campaign.query.filter_by(category='Beauty').count()},
            ]

            max_count = max(category['count'] for category in categories) if categories else 1

            total_users = User.query.count()
            total_sponsors = Sponsors.query.count()
            total_influencers = Influencers.query.count()

            sponsor_percentage = (total_sponsors / total_users) * 100 if total_users > 0 else 0
            influencer_percentage = (total_influencers / total_users) * 100 if total_users > 0 else 0


            top_influencers = (
                db.session.query(
                    Influencers.influencer_id,
                    Influencers.name,
                    Influencers.category,
                    Influencers.niche,
                    User.first_name,
                    User.last_name,
                    User.email,
                    User.pic_url,
                    func.count(AdRequest.ad_id).label('accepted_count')
                )
                .join(User, User.user_id == Influencers.influencer_id)
                .join(AdRequest, AdRequest.influencer_id == Influencers.influencer_id)
                .filter(AdRequest.status == "accepted")
                .group_by(
                    Influencers.influencer_id,
                    Influencers.name,
                    Influencers.category,
                    Influencers.niche,
                    User.first_name,
                    User.last_name,
                    User.email,
                    User.pic_url
                )
                .order_by(func.count(AdRequest.ad_id).desc())
                .limit(3)
                .all()
            )


            top_sponsors = (
                db.session.query(
                    User.first_name,
                    User.last_name,
                    User.email,
                    User.pic_url,
                    Sponsors.companyname,
                    Sponsors.industry,
                    func.count(Campaign.campaign_id).label('campaign_count')
                )
                .join(Sponsors, User.user_id == Sponsors.sponsor_id)
                .join(Campaign, Sponsors.sponsor_id == Campaign.sponsor_id)
                .group_by(Sponsors.sponsor_id)
                .order_by(func.count(Campaign.campaign_id).desc())
                .limit(3)
                .all()
            )


            top_campaigns = (
            db.session.query(
                Campaign.name,
                db.func.count(AdRequest.ad_id).label('accepted_count')
            )
            .join(AdRequest, AdRequest.campaign_id == Campaign.campaign_id)
            .filter(AdRequest.status == "accepted")
            .group_by(Campaign.campaign_id)
            .order_by(db.func.count(AdRequest.ad_id).desc())
            .limit(5)
            .all()
            )

            public_campaigns_count = Campaign.query.filter_by(isprivate=0).count()
            private_campaigns_count = Campaign.query.filter_by(isprivate=1).count()


            public_percentage = (public_campaigns_count / camp_count) * 100 if camp_count > 0 else 0
            private_percentage = (private_campaigns_count / camp_count) * 100 if camp_count > 0 else 0


            average_budget = db.session.query(db.func.avg(Campaign.budget)).scalar() or 0


            campaign_durations = db.session.query(db.func.avg(db.func.julianday(Campaign.end_date) - db.func.julianday(Campaign.start_date))).scalar() or 0
            average_duration = round(campaign_durations) if campaign_durations else 0


            total_instagram_reach = db.session.query(db.func.sum(Influencers.instagram)).scalar() or 0
            total_facebook_reach = db.session.query(db.func.sum(Influencers.facebook)).scalar() or 0
            total_twitter_reach = db.session.query(db.func.sum(Influencers.twitter)).scalar() or 0


            avg_instagram_reach = total_instagram_reach / influ_count if influ_count > 0 else 0
            avg_facebook_reach = total_facebook_reach / influ_count if influ_count > 0 else 0
            avg_twitter_reach = total_twitter_reach / influ_count if influ_count > 0 else 0


            flagged_users_count = User.query.filter_by(isflagged=True).count()

            flagged_campaign_count = Campaign.query.filter_by(isflagged=True).count()

            session['user'] = user.user_id

            return render_template(
                'home.html',
                prof1=user,
                pending_count=pending_count,
                user_count=user_count,
                camp_count=camp_count,
                ad_count=ad_count,
                accepted_count=accepted_count,
                rejected_count=rejected_count,
                top_influencers=top_influencers,
                top_sponsors=top_sponsors,
                pending_percentage=pending_percentage,
                accepted_percentage=accepted_percentage,
                rejected_percentage=rejected_percentage,
                max_count=max_count,
                sponsor_percentage=sponsor_percentage,
                influencer_percentage=influencer_percentage,
                categories=categories,
                public_percentage=public_percentage,
                private_percentage=private_percentage,
                average_budget=average_budget,
                average_duration=average_duration,
                top_campaigns=top_campaigns,
                total_instagram_reach=total_instagram_reach,
                total_facebook_reach=total_facebook_reach,
                total_twitter_reach=total_twitter_reach,
                avg_instagram_reach=avg_instagram_reach,
                avg_facebook_reach=avg_facebook_reach,
                avg_twitter_reach=avg_twitter_reach,
                flagged_users_count=flagged_users_count,
                flagged_campaign_count=flagged_campaign_count
                )
        else:
                return render_template('error.html',pas=True,prof1=USER,user=True)
    else:
        return render_template("admin_login.html",prof1=USER)

@app.route('/users')
def users():
    admin = User.query.filter_by(user_id= session['user']).first()
    users = User.query.all()
    spon = Sponsors.query.all()
    influ = Influencers.query.all()


    return render_template('users.html', prof1=admin, users= users,spon=spon,influ=influ)

@app.route('/flag_user/<userid>')
def flag(userid):
    admin = User.query.filter_by(user_id= session['user']).first()
    user = User.query.filter_by(user_id=userid).first()
    users = User.query.all()
    spon = Sponsors.query.all()
    influ = Influencers.query.all()

    if user.isflagged == 0:

        user.isflagged = 1
    elif user.isflagged == 1:

        user.isflagged = 0

    db.session.commit()
    
    return render_template('users.html', prof1=admin, users= users,spon=spon,influ=influ)

@app.route('/flag_campaign/<id>')
def flagcampaign(id):
    admin = User.query.filter_by(user_id= session['user']).first()
    campaigns = Campaign.query.all()
    campaign = Campaign.query.filter_by(campaign_id=id).first()

    if campaign.isflagged == 0:

        campaign.isflagged = 1
    elif campaign.isflagged == 1:

        campaign.isflagged = 0

    db.session.commit()
    
    return render_template('campaignadmin.html', prof1=admin,campaigns=campaigns)

@app.route('/campaignadmin')
def campaignadmin():
    admin = User.query.filter_by(user_id= session['user']).first()

    campaigns = Campaign.query.all()

    return render_template('campaignadmin.html', prof1=admin,campaigns=campaigns)

@app.route('/logout')
def logout():
  
    if 'admin' in session['user']:
        session.pop('user')
        return redirect('/admin_login')
    else:
        session.pop('user')
        return redirect(url_for('login'))

@app.route('/profile')
def profile():
    user = User.query.filter_by(user_id=session['user']).first()
    if "admin" in user.user_id:
        # Calculate statistics
        pending_count = AdRequest.query.filter_by(status='pending').count()
        accepted_count = AdRequest.query.filter_by(status='accepted').count()
        rejected_count = AdRequest.query.filter_by(status='rejected').count()
        user_count = User.query.count()
        camp_count = Campaign.query.count()
        ad_count = AdRequest.query.count()
        influ_count = Influencers.query.count()

        total_count = pending_count + accepted_count + rejected_count
        if total_count > 0:
            pending_percentage = (pending_count / total_count) * 100
            accepted_percentage = (accepted_count / total_count) * 100
            rejected_percentage = (rejected_count / total_count) * 100
        else:
            pending_percentage = accepted_percentage = rejected_percentage = 0

        categories = [
            {'name': 'Technology', 'count': Campaign.query.filter_by(category='Technology').count()},
            {'name': 'Health', 'count': Campaign.query.filter_by(category='Health').count()},
            {'name': 'Finance', 'count': Campaign.query.filter_by(category='Finance').count()},
            {'name': 'Education', 'count': Campaign.query.filter_by(category='Education').count()},
            {'name': 'Entertainment', 'count': Campaign.query.filter_by(category='Entertainment').count()},
            {'name': 'Travel', 'count': Campaign.query.filter_by(category='Travel').count()},
            {'name': 'Food', 'count': Campaign.query.filter_by(category='Food').count()},
            {'name': 'Sports', 'count': Campaign.query.filter_by(category='Sports').count()},
            {'name': 'Science', 'count': Campaign.query.filter_by(category='Science').count()},
            {'name': 'Arts', 'count': Campaign.query.filter_by(category='Arts').count()},
            {'name': 'Beauty', 'count': Campaign.query.filter_by(category='Beauty').count()},
        ]

        max_count = max(category['count'] for category in categories) if categories else 1

        total_users = User.query.count()
        total_sponsors = Sponsors.query.count()
        total_influencers = Influencers.query.count()

        sponsor_percentage = (total_sponsors / total_users) * 100 if total_users > 0 else 0
        influencer_percentage = (total_influencers / total_users) * 100 if total_users > 0 else 0  

        top_influencers = (
            db.session.query(
                Influencers.influencer_id,
                Influencers.name,
                Influencers.category,
                Influencers.niche,
                User.first_name,
                User.last_name,
                User.email,
                User.pic_url,
                func.count(AdRequest.ad_id).label('accepted_count')
            )
            .join(User, User.user_id == Influencers.influencer_id)
            .join(AdRequest, AdRequest.influencer_id == Influencers.influencer_id)
            .filter(AdRequest.status == "accepted")
            .group_by(
                Influencers.influencer_id,
                Influencers.name,
                Influencers.category,
                Influencers.niche,
                User.first_name,
                User.last_name,
                User.email,
                User.pic_url
            )
            .order_by(func.count(AdRequest.ad_id).desc())
            .limit(3)
            .all()
        )

        top_sponsors = (
            db.session.query(
                User.first_name,
                User.last_name,
                User.email,
                User.pic_url,
                Sponsors.companyname,
                Sponsors.industry,
                func.count(Campaign.campaign_id).label('campaign_count')
            )
            .join(Sponsors, User.user_id == Sponsors.sponsor_id)
            .join(Campaign, Sponsors.sponsor_id == Campaign.sponsor_id)
            .group_by(Sponsors.sponsor_id)
            .order_by(func.count(Campaign.campaign_id).desc())
            .limit(3)
            .all()
        )

        # Campaigns with the highest number of accepted ad requests
        top_campaigns = (
            db.session.query(
                Campaign.name,
                db.func.count(AdRequest.ad_id).label('accepted_count')
            )
            .join(AdRequest, AdRequest.campaign_id == Campaign.campaign_id)
            .filter(AdRequest.status == "accepted")
            .group_by(Campaign.campaign_id)
            .order_by(db.func.count(AdRequest.ad_id).desc())
            .limit(5)
            .all()
        )
        # Campaign stats
        public_campaigns_count = Campaign.query.filter_by(isprivate=0).count()
        private_campaigns_count = Campaign.query.filter_by(isprivate=1).count()

         # Percentages
        public_percentage = (public_campaigns_count / camp_count) * 100 if camp_count > 0 else 0
        private_percentage = (private_campaigns_count / camp_count) * 100 if camp_count > 0 else 0

        # Average budget of campaigns
        average_budget = db.session.query(db.func.avg(Campaign.budget)).scalar() or 0

        # Average duration of campaigns
        campaign_durations = db.session.query(db.func.avg(db.func.julianday(Campaign.end_date) - db.func.julianday(Campaign.start_date))).scalar() or 0
        average_duration = round(campaign_durations) if campaign_durations else 0

        # Influencer reach
        total_instagram_reach = db.session.query(db.func.sum(Influencers.instagram)).scalar() or 0
        total_facebook_reach = db.session.query(db.func.sum(Influencers.facebook)).scalar() or 0
        total_twitter_reach = db.session.query(db.func.sum(Influencers.twitter)).scalar() or 0

        # Average social media reach per influencer
        avg_instagram_reach = total_instagram_reach / influ_count if influ_count > 0 else 0
        avg_facebook_reach = total_facebook_reach / influ_count if influ_count > 0 else 0
        avg_twitter_reach = total_twitter_reach / influ_count if influ_count > 0 else 0

        # Number of flagged users
        flagged_users_count = User.query.filter_by(isflagged=True).count()

        flagged_campaign_count = Campaign.query.filter_by(isflagged=True).count()

        return render_template('home.html', 
            prof1=user, 
            pending_count=pending_count, 
            user_count=user_count, 
            camp_count=camp_count, 
            ad_count=ad_count, 
            accepted_count=accepted_count, 
            rejected_count=rejected_count, 
            top_influencers=top_influencers, 
            top_sponsors=top_sponsors, 
            sponsor_percentage=sponsor_percentage, 
            influencer_percentage=influencer_percentage, 
            max_count=max_count, 
            pending_percentage=pending_percentage, 
            accepted_percentage=accepted_percentage, 
            rejected_percentage=rejected_percentage,
            categories=categories,
            public_percentage=public_percentage,
            private_percentage=private_percentage,
            average_budget=average_budget,
            average_duration=average_duration,
            top_campaigns=top_campaigns,
            total_instagram_reach=total_instagram_reach,
            total_facebook_reach=total_facebook_reach,
            total_twitter_reach=total_twitter_reach,
            avg_instagram_reach=avg_instagram_reach,
            avg_facebook_reach=avg_facebook_reach,
            avg_twitter_reach=avg_twitter_reach,
            flagged_users_count=flagged_users_count,
            flagged_campaign_count=flagged_campaign_count
            )
    elif "in" in user.user_id:
        prof2 = Influencers.query.filter_by(influencer_id = user.user_id).first()

        data= Sponsors.query.join(Campaign,Sponsors.sponsor_id==Campaign.sponsor_id).join(AdRequest,AdRequest.campaign_id== Campaign.campaign_id).with_entities(Sponsors.name.label("Sponsor_name"), Sponsors.companyname, Sponsors.industry, Campaign.budget,Campaign.category,Campaign.name.label("Campaign_name"), Campaign.description, Campaign.start_date, Campaign.end_date,Campaign.goals, AdRequest.ad_id, AdRequest.influencer_id, AdRequest.messages,AdRequest.requirements, AdRequest.payment_amount, AdRequest.status,AdRequest.created_by,AdRequest.updated_by).all()
        
        categories=["Technology","Health","Finance","Education","Entertainment","Travel","Food","Sports","Science","Arts","Beauty"]
        return render_template('home.html', prof1= user, prof2=prof2 ,data=data,categories=categories,nic=nic)
    
    elif "sp" in user.user_id :

        prof2 = Sponsors.query.filter_by(sponsor_id = user.user_id).first()
        campaigndata = Campaign.query.filter_by(sponsor_id=session['user']).all()[-3:]

        adcampdata = AdRequest.query.join(Campaign,Campaign.campaign_id==AdRequest.campaign_id).with_entities(AdRequest.ad_id,AdRequest.campaign_id.label('campaign_id'),AdRequest.influencer_id,AdRequest.messages,AdRequest.requirements,AdRequest.payment_amount,AdRequest.created_by,AdRequest.updated_by,AdRequest.status,Campaign.name.label("campaign_name"),Campaign.description,Campaign.category,Campaign.start_date,Campaign.end_date,Campaign.isprivate,Campaign.goals,Campaign.budget,Campaign.sponsor_id)

        categories=["Technology","Health","Finance","Education","Entertainment","Travel","Food","Sports","Science","Arts","Beauty"]

        return render_template('home.html', prof1= user, prof2=prof2,campaigndata = campaigndata,categories=categories,adcampdata=adcampdata,nic=nic)

@app.route('/edit_profile', methods=['POST'])
def edit_profile():
    if 'user' in session:
        user_id = session['user']
        first_name = request.form.get('first_name').strip()
        last_name = request.form.get('last_name').strip()
        email = request.form.get('email').strip()
        profile_picture_url = request.form.get('pic_url').strip()

        user = User.query.filter_by(user_id=user_id).first()

        if not user:
            return redirect(url_for('login'))

        # Update the user's profile
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        if email is not None:
            user.email = email
        if profile_picture_url is not None:
            user.pic_url = profile_picture_url

        if 'sp' in session['user']:

            industry = request.form.get('industry').strip()
            companyname = request.form.get('companyname').strip()

            # Fetch the current user data 
            sponsor = Sponsors.query.filter_by(sponsor_id=user_id).first()
           
            if industry is not None:
                sponsor.industry = industry
            if companyname is not None:
                sponsor.companyname = companyname
            
            sponsor.name = first_name+' '+last_name
            
            db.session.commit()

            return redirect(url_for('profile'))
        elif 'in' in session['user']:
            category = request.form.get('category').strip()
            niche = request.form.get('niche').strip()
            insta = request.form.get('instagram').strip()
            facebook = request.form.get('facebook').strip()
            twitter = request.form.get('twitter').strip()

            influencer = Influencers.query.filter_by(influencer_id= user_id).first()

            if category is not None:
                influencer.category = category
            if niche is not None:
                influencer.niche = niche
            if insta is not None:
                influencer.category = category
            if facebook is not None:
                influencer.facebook = facebook
            if twitter is not None:
                influencer.twitter = twitter
            
            influencer.name = first_name+' '+last_name

            db.session.commit()

            return redirect(url_for('profile'))

    return redirect(url_for('login'))

@app.route('/change_password', methods=['POST'])
def change_password():
    if 'user' in session:
        user_id = session['user']
        current_password = request.form.get('currentPassword').strip()
        new_password = request.form.get('newPassword').strip()
        confirm_password = request.form.get('confirmPassword').strip()

        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            return redirect(url_for('login'))

        if not check_password_hash(user.password, current_password):

            return "Current Password is Incorrect"

        if new_password != confirm_password:

            return "new password and confirm password are not same"

        user.password = generate_password_hash(new_password)
        db.session.commit()

        return redirect(url_for('login'))

    return redirect(url_for('login'))

@app.route('/create-campaign',methods=["GET","POST"])
def createcampaign():
    user = User.query.filter_by(user_id=session['user']).first()
    prof2 = Sponsors.query.filter_by(sponsor_id = session['user']).first()
    categories=["Technology","Health","Finance","Education","Entertainment","Travel","Food","Sports","Science","Arts","Beauty"]
    if request.method == "POST":
        name = request.form.get('name')
        description = request.form.get('description')
        category = request.form.get('category')
        startdate = request.form.get('start_date')
        start = datetime.strptime(startdate, "%Y-%m-%d")
        enddate = request.form.get('end_date')
        end = datetime.strptime(enddate, "%Y-%m-%d")
        isprivate = request.form.get('isprivate')
        goals = request.form.get('goals')
        budget= request.form.get('budget')
        id = session['user']

        if isprivate:
            private=1       
        else:
            private=0

        newcampaign= Campaign(name=name,
                                description=description,
                                budget=budget,
                                category=category,
                                start_date = start,
                                end_date = end,
                                isprivate= private ,
                                goals=goals,
                                sponsor_id=id)        
        db.session.add(newcampaign)
        db.session.commit()
        return render_template('create-campaign.html',prof1=user,prof2=prof2,categories=categories)
    else:

        return render_template('create-campaign.html',prof1=user,prof2=prof2,categories=categories)
    
@app.route('/campaign')
def campaign():
    user = User.query.filter_by(user_id=session['user']).first()
    prof2 = Sponsors.query.filter_by(sponsor_id = session['user']).first()
    campaigndata = Campaign.query.filter_by(sponsor_id=session['user']).all()
    categories=["Technology","Health","Finance","Education","Entertainment","Travel","Food","Sports","Science","Arts","Beauty"]
    distinct_cat = db.session.query(Campaign.category).distinct().filter_by(sponsor_id=session['user']).with_entities(Campaign.category).all()
    addata= AdRequest.query.join(Campaign,AdRequest.campaign_id==Campaign.campaign_id)
    influ = Influencers.query.all()
    return render_template('campaign.html',prof1=user,prof2=prof2,campaigndata=campaigndata,addata=addata,categories=categories,distinct_cat=distinct_cat,influ=influ)

@app.route("/update_campaign/<camp_id>", methods=["POST"])
def update_campaign(camp_id):
    campaign = Campaign.query.get(camp_id)

    if campaign:
        campaign_name = request.form.get("campaign_name")
        description = request.form.get("description")
        start_date_str = request.form.get("start_date")
        end_date_str = request.form.get("end_date")
        category= request.form.get('category')
        goals = request.form.get("goals")
        budget = request.form.get('budget')

        if campaign_name is not None:
            campaign.name = campaign_name
        if description is not None:
            campaign.description = description
        if category is not None:
            campaign.category = category
        if budget is not None:
            campaign.budget = budget
        if start_date_str:
            try:
                campaign.start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            except ValueError:
                return "Invalid start date format. Please use YYYY-MM-DD.", 400

        if end_date_str:
            try:
                campaign.end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            except ValueError:
                return "Invalid end date format. Please use YYYY-MM-DD.", 400
        if goals is not None:
            campaign.goals = goals
        # Commit the changes to the database
        db.session.commit()

        # Redirect to the profile or another page after updating
        return redirect('/profile')

    # Handle the case where the campaign doesn't exist
    return "Campaign not found", 404

@app.route("/delete_campaign/<camp_id>", methods=["POST"])
def del_camp(camp_id):
    if request.method=="POST":
        AdRequest.query.filter_by(campaign_id=camp_id).delete()
        Campaign.query.filter_by(campaign_id=camp_id).delete()
        db.session.commit()
        return redirect('/profile')


@app.route('/campbycat', methods=["GET","POST"])
def campbycat():
    selected_cat = request.form.get('selected_cat').strip()
    user = User.query.filter_by(user_id=session['user']).first()
    prof2 = Sponsors.query.filter_by(sponsor_id = session['user']).first()
    campaigndata = Campaign.query.filter_by(sponsor_id=session['user']).all()
    categories=["Technology","Health","Finance","Education","Entertainment","Travel","Food","Sports","Science","Arts","Beauty"]
    addata= AdRequest.query.join(Campaign,AdRequest.campaign_id==Campaign.campaign_id)

    category_camp = Campaign.query.filter_by(category=selected_cat).all()
    distinct_cat = db.session.query(Campaign.category).distinct().filter_by(sponsor_id=session['user']).all()

    return render_template('campaign.html',prof1=user,prof2=prof2,campaigndata=campaigndata,addata=addata,categories=categories,distinct_cat=distinct_cat,category_camp=category_camp,selected_cat=selected_cat)

@app.route('/adrequest')
def adrequest():
    user = User.query.filter_by(user_id=session['user']).first()
    # addata = AdRequest.query.join(Campaign,AdRequest.campaign_id==Campaign.campaign_id)
    addata = AdRequest.query.join(Campaign,Campaign.campaign_id==AdRequest.campaign_id).with_entities(AdRequest.ad_id,AdRequest.campaign_id.label('campaign_id'),AdRequest.influencer_id,AdRequest.messages,AdRequest.requirements,AdRequest.payment_amount,AdRequest.created_by,AdRequest.updated_by,AdRequest.status,Campaign.name.label("campaign_name"),Campaign.description,Campaign.category,Campaign.start_date,Campaign.end_date,Campaign.isprivate,Campaign.goals,Campaign.budget,Campaign.isflagged,Campaign.sponsor_id)
    influ = Influencers.query.all()

    if 'sp' in session['user']:
        prof2 = Sponsors.query.filter_by(sponsor_id = session['user']).first()

        return render_template('adrequest.html',prof1=user,prof2=prof2,addata=addata,influ=influ)
    else :
        prof2 = Influencers.query.filter_by(influencer_id= session['user']).first()

        return render_template('adrequest.html',prof1=user,prof2=prof2,addata=addata,influ=influ)


@app.route('/create_adrequest/<campaignid>' , methods=["GET","POST"])
def create_adrequest(campaignid):
    user = User.query.filter_by(user_id=session['user']).first()
    prof2 = Sponsors.query.filter_by(sponsor_id = session['user']).first()
    influ = Influencers.query.all()
    campaigndata = Campaign.query.filter_by(sponsor_id=session['user']).all()

    if request.method == "POST":
        influencerid = request.form.get('influencer_id')
        msg = request.form.get('messages')
        req = request.form.get('requirements')
        payment = request.form.get('payment_amount')
        created_by = session['user']
        updated_by = session['user']
        camp_id = campaignid

        newadrequest = AdRequest(campaign_id=camp_id,
                                    influencer_id = influencerid,
                                    messages=msg,
                                    requirements=req,
                                    created_by=created_by,
                                    updated_by=updated_by,
                                    payment_amount=payment)

        db.session.add(newadrequest)
        db.session.commit()

        return redirect(url_for('campaign'))
    else:
        return render_template('create_adrequest.html',prof1 =user,prof2=prof2 ,influ=influ)
    
@app.route('/update_adrequest/<int:adId>', methods=['GET', 'POST'])
def update_ad(adId):
    ad = AdRequest.query.get_or_404(adId)
    if request.method == 'POST':
        influencerid= request.form.get('influencer_id')
        messages = request.form.get('message')
        requirements = request.form.get('requirement')
        payment_amount = request.form.get('payment_amount')

        try:
            if influencerid:
                ad.influencer_id = influencerid
            if messages:
                ad.messages = messages
            if requirements:
                ad.requirements = requirements
            if payment_amount:
                ad.payment_amount = float(payment_amount)

            # Commit the changes to the database
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return 'Error updating ad request!'

        # Redirect to a page, e.g., the campaign detail page or list page
        if 'sp' in session['user']:
            return redirect('/adrequest')
        if 'in' in session['user']:
            return redirect('/adrequest')

    # Render the template with current ad request and campaign data
    return redirect('/profile')
    
@app.route('/send_adrequest/<Id>' , methods=["POST"])
def send_request(Id):
    user = User.query.filter_by(user_id=session['user']).first()

    if request.method == "POST":
        if 'sp' in session['user']:
            prof2 = Sponsors.query.filter_by(sponsor_id = session['user']).first()
            influencer_id = Id
            campaign_id = request.form.get('campaign_id')
            messages = request.form.get('messages')
            requirements = request.form.get('requirements')
            payment = request.form.get('payment_amount')
            created_by = session['user']
            updated_by = session['user']

            if campaign_id == 'Select':
                return render_template('error.html',campaign=True,prof1=user)

            newadrequest = AdRequest(campaign_id=campaign_id,
                                        influencer_id = influencer_id,
                                        messages=messages,
                                        requirements=requirements,
                                        created_by=created_by,
                                        updated_by=updated_by,
                                        payment_amount=payment)

            db.session.add(newadrequest)
            db.session.commit()

            return redirect('/profile')
        
        elif 'in' in session['user']:
            prof2 = Influencers.query.filter_by(influencer_id = session['user']).first()

            # print("Id:", Id)
            # print("Request form data:", request.form)

            influencer_id= session['user']
            campaign_id = Id
            messages = request.form.get('messages')
            requirements = request.form.get('requirements')
            payment = request.form.get('payment_amount')
            created_by = session['user']
            updated_by = session['user']

            newadrequest = AdRequest(campaign_id=campaign_id,
                                        influencer_id = influencer_id,
                                        messages=messages,
                                        requirements=requirements,
                                        created_by=created_by,
                                        updated_by=updated_by,
                                        payment_amount=payment)

            db.session.add(newadrequest)
            db.session.commit()

            return redirect('/adrequest')

@app.route("/send_adrequestwithnone/<adId>", methods=["GET"])
def send_adrequestwithnone(adId):
    ad = AdRequest.query.get_or_404(adId)
    if ad:
        ad.influencer_id = session['user']
        ad.updated_by = session['user']
        db.session.commit()

        return redirect('/adrequest')

@app.route("/update_status/<Ad_id>/<string>", methods=["POST"])
def update_status(Ad_id,string):
    if request.method=="POST":
        ad = AdRequest.query.filter_by(ad_id=Ad_id).first()
        if ad is None:
            # Handle the case where the ad is not found
            return "Ad not found", 404  # Or redirect to an error page
        ad.status=string
        db.session.commit()
        return redirect('/profile')
    
@app.route('/delete_adrequest/<int:adId>', methods=['POST'])
def delete_ad(adId):
    ad = AdRequest.query.filter_by(ad_id=adId)
    if ad:
        try:
            ad.delete()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return 'Error!' , 404
    return redirect('/campaign')

@app.route('/negotiate_adrequest/<adId>', methods=["POST"])
def negotiate(adId):
    ad = AdRequest.query.filter_by(ad_id=adId).first()
    payment= request.form.get('payment_amount')
    requirement = request.form.get('requirements')

    if payment:
        ad.payment_amount = int(payment)
        ad.updated_by = session['user']
    if requirement:
        ad.requirements = requirement
        ad.updated_by = session['user']

    db.session.commit()

    return redirect('/adrequest')


@app.route('/search', methods=['GET'])
def search():
   
    query = request.args.get("query", "").strip()

    categories_dict = {"Technology":["Machine learning", "Neural networks", "Natural language processing","Threat analysis", "Penetration testing", "Network security","Frontend", "Backend", "Full-stack", "Frameworks"],"Health": ["Diet planning", "Food science", "Supplements","Exercise routines", "Strength training", "Cardiovascular health","Therapy", "Mindfulness", "Stress management"],"Finance": ["Stocks", "bonds", "real estate","Budgeting", "saving", "debt management","Bitcoin", "Ethereum", "blockchain technology"],"Education": ["Curriculum development", "classroom management", "educational technology","University programs", "research", "academic advising","E-learning platforms", "MOOCs", "distance education"],"Entertainment": ["Genres", "reviews", "film production","Genres", "artists", "production techniques","Video games", "board games", "game design"],"Travel": ["Popular tourist spots", "off-the-beaten-path locations","Packing", "safety", "cultural etiquette","Itinerary creation", "budgeting", "accommodations"],"Food": ["Cooking techniques", "meal ideas", "dietary preferences","Reviews", "cuisine types", "dining experiences","Regional specialties", "food history", "culinary traditions"],"Sports": ["Football", "basketball", "soccer","Tennis", "golf", "swimming","Performance analysis", "injury prevention", "training techniques"],"Science": ["Genetics", "ecology", "microbiology","Quantum mechanics", "astrophysics", "classical mechanics","Organic chemistry", "inorganic chemistry", "physical chemistry"],"Arts": ["Painting", "sculpture", "photography","Theatre", "dance", "music performance","Genres", "authors", "literary analysis"],"Beauty":["Makeup","Skincare","Haircare","Fashion","Nails","Beauty Trends"]}

    sanitized_query=validate_query(query)
    if "user" in session:
        if 'admin' in session['user']:
            prof1=User.query.filter_by(user_id=session['user']).first()
            prof2=None
            campdata=[]
            if sanitized_query.isdigit():
                sanitized_query= int(sanitized_query)
                influ_res = Influencers.query.filter((Influencers.instagram + Influencers.facebook + Influencers.twitter) >= sanitized_query).all()
                campdata = Campaign.query.filter(Campaign.budget >= sanitized_query).all()
            else:
                influ_res=[]
                for cat in categories_dict:
                    # print(value)
                    if sanitized_query.lower() in cat.lower():
                        influ_res = Influencers.query.filter_by(category=cat).all()
                        # print(campdata)
                        break
                    else:
                        for j in categories_dict[cat]:
                            if sanitized_query.lower() in j.lower():
                                influ_res = Influencers.query.filter_by(category=cat).all()
                                # print(campdata)
                                break
                                              
                for cat in categories_dict:
                    value=cat
                    # print(value)
                    if sanitized_query.lower() in cat.lower():
                        campdata = Campaign.query.filter_by(category=value).all()
                        # print(campdata)
                        break
                    else:
                        for j in categories_dict[value]:
                            if sanitized_query.lower() in j.lower():
                                campdata = Campaign.query.filter(Campaign.category.like(f'%{value}%')).all()
                                # print(campdata)
                                break
                

            users = User.query.all()
            print(users)
            return render_template('/search.html',prof1=prof1,prof2=prof2, query=sanitized_query,campdata=campdata,influ_res=influ_res,users=users)
        
        elif 'sp' in session['user']:
            prof1 = User.query.filter_by(user_id=session['user']).first()
            prof2 = Sponsors.query.filter_by(sponsor_id=session['user']).first()
            # print(type(sanitized_query))
            # influ_res=[]
            camp = Campaign.query.filter_by(sponsor_id=session['user']).all()
            # print(camp)
            if sanitized_query.isdigit():
                sanitized_query = int(sanitized_query)
                influ_res = Influencers.query.filter((Influencers.instagram + Influencers.facebook + Influencers.twitter) >= sanitized_query).all()
            else:
                influ_res=[]
                for cat in categories_dict:
                    # print(value)
                    if sanitized_query.lower() in cat.lower():
                        influ_res = Influencers.query.filter_by(category=cat).all()
                        # print(campdata)
                        break
                    else:
                        for j in categories_dict[cat]:
                            if sanitized_query.lower() in j.lower():
                                influ_res = Influencers.query.filter_by(category=cat).all()
                                # print(campdata)
                                break
    


            return render_template('/search.html',prof1=prof1,prof2=prof2,influ_res=influ_res, query=sanitized_query,camp=camp)

        elif 'in' in session['user']:
            prof1 = User.query.filter_by(user_id=session['user']).first()
            prof2 = Influencers.query.filter_by(influencer_id=session['user']).first()
            campdata=[]
            if sanitized_query.isdigit():
                sanitized_query = int(sanitized_query)
                campdata = Campaign.query.filter(Campaign.budget >= sanitized_query).all()
            else:                                      
                for cat in categories_dict:
                    value=cat
                    # print(value)
                    if sanitized_query.lower() in cat.lower():
                        campdata = Campaign.query.filter_by(category=value).all()
                        # print(campdata)
                        break
                    else:
                        for j in categories_dict[value]:
                            if sanitized_query.lower() in j.lower():
                                campdata = Campaign.query.filter(Campaign.category.like(f'%{value}%')).all()
                                # print(campdata)
                                break
                
            addata= AdRequest.query.all()

            return render_template('search.html',prof1=prof1,prof2=prof2,campdata=campdata, query=sanitized_query,addata=addata)

    else:
        prof1=None
        prof2=None

        influ_res = Influencers.query.filter(Influencers.name.like(f"%{sanitized_query}%")).all()


        return render_template('/search.html',prof1=prof1,prof2=prof2,influ_res=influ_res , query=sanitized_query)


@app.route('/contact')
def contact():
    prof1 = None
    prof2 = None

    return render_template('contact.html',prof1=prof1,prof2=prof2)

@app.route('/aboutUs')
def aboutus():
    prof1 = None
    prof2 = None

    return render_template('aboutus.html',prof1=prof1,prof2=prof2)


# ---------------------Some Other Useful function -----------------------------
def validate_query(query):
    if query=="":
        return "Not a Valid Search"
    else:
        return query