from buttons import get_model
from flask import Blueprint, current_app, redirect, render_template, request, \
    session, url_for

crud = Blueprint('crud', __name__)

@crud.route("/start", methods=['GET'])
def start():
    return render_template("start.html")

@crud.route("", methods=['POST'])
def cont():
    sessionId = request.form['sessionId']
    comparisonId = request.form['comparisonId']
    buttonId = request.form['buttonId']
    
    get_model().buttonPress(int(sessionId), int(comparisonId), int(buttonId))

    buttons = get_model().list(sessionId)

    print('completed comparison {0}'.format(comparisonId))
    print('chose button {0}'.format(buttonId))
    
    if comparisonId == '36':
        #end session
        return render_template("end.html")
    
    return render_template(
        "list.html",
        buttons=buttons,
        sessionId=sessionId)
    
@crud.route("/", methods=['GET'])
def list():
    sessionId = get_model().createSession()
    
    print('starting session {0}'.format(sessionId))
    
    buttons = get_model().list(sessionId)
    
    return render_template(
        "list.html",
        buttons=buttons,
        sessionId=sessionId)
