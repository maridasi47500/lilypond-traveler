from flask import Flask, render_template, request, session, redirect
from bs4 import BeautifulSoup
import subprocess
import os
from yourappdb import query_db, get_db
from flask import g

app = Flask(__name__)
app.secret_key="any string"
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
init_db()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def hello_world():
    user = query_db('select * from contacts')
    the_username = "anonyme"
    one_user = query_db('select * from contacts where first_name = ?',
                [the_username], one=True)
    return render_template("hey.html", users=user, one_user=one_user, the_title="my title")
@app.route("/add_one_user", methods=["GET","POST"])
def add_one_user():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslescountry= query_db("select * from country")

        one_user = query_db("insert into user (username,email,password,phone,country_id) values (:username,:email,:password,:phone,:country_id)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from user')


        last_user = query_db("select * from user where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        session["current_user_id"]=last_user["id"]
        for x in ['username','email','password','phone','country_id']:
            session[x]=hey[x]


        return render_template("userform.html", users=user, one_user=one_user, the_title="add new user", touslescountry=touslescountry)


    touslescountry= query_db("select * from country")

    user = query_db('select * from user')
    one_user = query_db("select * from user limit 1", one=True)
    return render_template("userform.html", users=user, one_user=one_user, the_title="add new user", touslescountry=touslescountry)


@app.route("/user_sign_out", methods=["GET","POST"])
def user_sign_out():
    if request.method == 'POST':
        session["current_user_id"]=""
        for x in ['username','email','password','phone','country_id']:
            session[x]=""
        return redirect("/")


@app.route("/user_log_in", methods=["GET","POST"])
def user_login():
    if request.method == 'POST':
        hey=request.form
        last_user = query_db("select * from user where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        try:
            session["current_user_id"]=last_user["id"]
            for x in ['username','email','password','phone','country_id']:
                session[x]=hey[x]
        except:
            return render_template("userlogin.html")
    return render_template("userlogin.html")
@app.route("/add_one_gem_quest", methods=["GET","POST"])
def add_one_gem_quest():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into gem_quest (place_name,lat,lon) values (:place_name,:lat,:lon)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from gem_quest')


        return render_template("gem_questform.html", gem_quests=user, one_user=one_user, the_title="add new gem_quest")


    user = query_db('select * from gem_quest')
    one_user = query_db("select * from gem_quest limit 1", one=True)
    return render_template("gem_questform.html", gem_quests=user, one_user=one_user, the_title="add new gem_quest")

@app.route("/add_one_seasonal_sport", methods=["GET","POST"])
def add_one_seasonal_sport():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into seasonal_sport (name,season) values (:name,:season)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from seasonal_sport')


        return render_template("seasonal_sportform.html", seasonal_sports=user, one_user=one_user, the_title="add new seasonal_sport")


    user = query_db('select * from seasonal_sport')
    one_user = query_db("select * from seasonal_sport limit 1", one=True)
    return render_template("seasonal_sportform.html", seasonal_sports=user, one_user=one_user, the_title="add new seasonal_sport")

@app.route("/add_one_place_visit", methods=["GET","POST"])
def add_one_place_visit():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslesgem_quest= query_db("select * from gem_quest")

        touslesuser= query_db("select * from user")

        touslesseasonal_sport= query_db("select * from seasonal_sport")

        one_user = query_db("insert into place_visit (gem_quest_id,user_id,seasonal_sport_id) values (:gem_quest_id,:user_id,:seasonal_sport_id)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from place_visit')


        return render_template("place_visitform.html", place_visits=user, one_user=one_user, the_title="add new place_visit", touslesgem_quest=touslesgem_quest, touslesuser=touslesuser, touslesseasonal_sport=touslesseasonal_sport)


    touslesgem_quest= query_db("select * from gem_quest")

    touslesuser= query_db("select * from user")

    touslesseasonal_sport= query_db("select * from seasonal_sport")

    user = query_db('select * from place_visit')
    one_user = query_db("select * from place_visit limit 1", one=True)
    return render_template("place_visitform.html", place_visits=user, one_user=one_user, the_title="add new place_visit", touslesgem_quest=touslesgem_quest, touslesuser=touslesuser, touslesseasonal_sport=touslesseasonal_sport)

@app.route("/add_one_panomaric_view", methods=["GET","POST"])
def add_one_panomaric_view():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslesgem_quest= query_db("select * from gem_quest")

        one_user = query_db("insert into panomaric_view (description,gem_quest_id) values (:description,:gem_quest_id)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from panomaric_view')


        return render_template("panomaric_viewform.html", panomaric_views=user, one_user=one_user, the_title="add new panomaric_view", touslesgem_quest=touslesgem_quest)


    touslesgem_quest= query_db("select * from gem_quest")

    user = query_db('select * from panomaric_view')
    one_user = query_db("select * from panomaric_view limit 1", one=True)
    return render_template("panomaric_viewform.html", panomaric_views=user, one_user=one_user, the_title="add new panomaric_view", touslesgem_quest=touslesgem_quest)

@app.route("/add_one_job_offer", methods=["GET","POST"])
def add_one_job_offer():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslesuser= query_db("select * from user")

        one_user = query_db("insert into job_offer (name,description,user_id) values (:name,:description,:user_id)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from job_offer')


        return render_template("job_offerform.html", job_offers=user, one_user=one_user, the_title="add new job_offer", touslesuser=touslesuser)


    touslesuser= query_db("select * from user")

    user = query_db('select * from job_offer')
    one_user = query_db("select * from job_offer limit 1", one=True)
    return render_template("job_offerform.html", job_offers=user, one_user=one_user, the_title="add new job_offer", touslesuser=touslesuser)

@app.route("/add_one_myscore", methods=["GET","POST"])
def add_one_myscore():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslesuser= query_db("select * from user")

        one_user = query_db("insert into myscore (mymusic,pic,user_id,time_signature,key_signature) values (:mymusic,:pic,:user_id,:time_signature,:key_signature)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from myscore')


        file_pointer = open("./samplescoreexample.ly")
        contents = file_pointer.read()
        contents=contents.replace("KEYSCOREHERE", request.form["key_signature"].replace(" "," \\")).replace("TIMESCOREHERE", request.form["time_signature"]).replace("CONTENTSCOREHERE", request.form["mymusic"])
        file_pointer = open("./scores/myscore_mymusic_sample_"+mylastrowid+".ly", "w")
        file_pointer.write(contents)
        file_pointer.close()
        file_pointer = open("./scores/myscore_mymusic_sample_"+mylastrowid+".html", "w")
        file_pointer.write("<lilypond staffsize=34>"+contents+"</lilypond>")
        file_pointer.close()
        subprocess.run(["lilypond-book", "scores/myscore_mymusic_sample_"+mylastrowid+".html", "-f", "html", "--output", "scores/samplescoremyscore_mymusic"+mylastrowid]) 

        try:
            f= open("scores/samplescoremyscore_mymusic"+mylastrowid+"/myscore_mymusic_sample_"+mylastrowid+".html")
            s = f.read()
            soup = BeautifulSoup(s)

            picvalue={'pic': soup.find_all('img')[0].get("src")}
        except:
            picvalue={'pic': ""}

        hello_there = query_db("update myscore set pic=:pic",picvalue, one=True)

        return render_template("myscoreform.html", myscores=user, one_user=one_user, the_title="add new myscore", touslesuser=touslesuser)


    touslesuser= query_db("select * from user")

    user = query_db('select * from myscore')
    one_user = query_db("select * from myscore limit 1", one=True)
    return render_template("myscoreform.html", myscores=user, one_user=one_user, the_title="add new myscore", touslesuser=touslesuser)

