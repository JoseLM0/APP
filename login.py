from flask import Flask, render_template, request, session, redirect, url_for 
from run import app    

def abrir_sesion(user):
    session['id'] = user.id
    session['Usuario'] = user.Usuario
    session['Puesto'] = user.Puesto


def estalogueado():
    if "id" in session:
        return True
    else:
        return False

def es_admin():
    return session.get("Puesto", 1)        

@app.context_processor
def logear():
    if "id" in session:
        return {'estalogueado':True}
    else: 
        return {'estalogueado':False}

@app.context_processor
def admin():
    return {'es_admin':session.get("Puesto", 1)}     