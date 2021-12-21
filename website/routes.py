from flask import render_template, request, redirect
from website import app
from datetime import datetime
from bll.nursing_processor import NursingProcessor

nursing_processor = NursingProcessor()


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return render_template('time_elapsed.html', timestamps={
        "last_nursing_time": nursing_processor.get_last_nursing_time().strftime("%Y-%m-%dT%H:%M:%S"),
        "last_nursing_time_display": nursing_processor.get_last_nursing_time().strftime("%H:%M:%S")})


@app.route('/new_nursing', methods=['GET'])
def new_nursing_get():
    return render_template('new_nursing.html')


@app.route('/new_nursing', methods=['POST'])
def new_nursing():
    nursing_processor.add_nursing(breast_feeding_ml=0,
                                  milk_feeding_ml=int(request.form['feed_ml']),
                                  feed_time=datetime.utcnow())
    return redirect('/')


@app.route('/new_poo', methods=['GET'])
def new_poo_get():
    return render_template('new_poo.html')


@app.route('/new_poo', methods=['POST'])
def new_poo():
    nursing_processor.add_poo(datetime.utcnow())
    return redirect('/')


@app.route('/statistic', methods=['GET'])
def statistic():
    all_nursing = nursing_processor.get_all_nursing()
    return render_template('statistic.html', statistic_result={"nursing_history": all_nursing})
