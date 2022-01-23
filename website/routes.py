from flask import render_template, request, redirect
from models.nursing import Nursing
from website import app
from datetime import datetime
from bll.nursing_processor import NursingProcessor

nursing_processor = NursingProcessor()


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return render_template('time_elapsed.html', timestamps={
        "last_nursing_time": nursing_processor.get_last_nursing_time().astimezone().strftime("%Y-%m-%dT%H:%M:%S%z"),
        "last_nursing_time_display": nursing_processor.get_last_nursing_time().astimezone().strftime("%H:%M:%S"),
        "last_bath_time": nursing_processor.get_last_bath_time().astimezone().strftime("%Y-%m-%d"),
        "last_poo_time": nursing_processor.get_last_poo_time().astimezone().strftime("%Y-%m-%d")})


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
    nursing_processor.add_poo(datetime.utcnow(), request.form.get('is_sick') == 'on')
    return redirect('/')


@app.route('/statistic', methods=['GET'])
def statistic():
    all_nursing = nursing_processor.get_all_nursing()
    for nursing in all_nursing:
        nursing.feeding_time = nursing.feeding_time.astimezone()
    all_poo = nursing_processor.get_all_poo()
    return render_template('statistic.html', statistic_result={"nursing_history": all_nursing, "poo_history": all_poo})


@app.route('/update', methods=['GET'])
def update():
    nursing_id = request.args['id']
    nursing = nursing_processor.get_nursing_by_id(nursing_id)
    return render_template('update.html', 
                           nursing = 
                               {"id": nursing_id, 
                               "date": nursing.feeding_time, 
                               "milk_feeding_ml": nursing.milk_feeding_ml})


@app.route('/update', methods=['POST'])
def update_nursing():
    print(request.form)
    nursing = Nursing()
    nursing.id = int(request.form['id'])
    nursing.feeding_time = datetime.fromisoformat(request.form['date'])
    nursing.milk_feeding_ml = request.form['milk_feeding_ml']
    nursing_processor.update_nursing(nursing)
    return redirect("/")


@app.route('/delete', methods=['POST'])
def delete():
    nursing_processor.delete_nursing(int(request.form['id']))
    return redirect("/")


@app.route('/new_bath', methods=['POST'])
def new_bath():
    nursing_processor.add_bath(datetime.utcnow())
    return redirect("/")

