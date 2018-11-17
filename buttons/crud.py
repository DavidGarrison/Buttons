from buttons import get_model, oauth2, storage
from flask import Blueprint, current_app, redirect, render_template, request, \
    session, url_for

crud = Blueprint('crud', __name__)

@crud.route("/<sessionId>/<comparisonId>/<buttonId>")
def cont(sessionId, comparisonId, buttonId):
    get_model().buttonPress(int(sessionId), int(comparisonId), int(buttonId))

    buttons = get_model().list(int(comparisonId) + 1)

    print('completed comparison {0}'.format(comparisonId))
    
    if comparisonId == '36':
        #end session
        return render_template(
            "end.html")
    
    return render_template(
        "list.html",
        buttons=buttons,
        sessionId=sessionId)
    
@crud.route("/")
def list():
    sessionId = get_model().createSession()
    
    print('starting session {0}'.format(sessionId))
    
    buttons = get_model().list()
    
    return render_template(
        "list.html",
        buttons=buttons,
        sessionId=sessionId)
