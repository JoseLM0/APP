from flask import Flask, render_template, request, session, redirect, url_for 
from run import app    

def abrir_sesion(Usuarios):
    session["id"]=Usuarios.id
    session["Usuario"]=Usuarios.Usuario
    session["Puesto"]=Usuarios.Puesto

def cerrar_sesion (Usuarios):
    session.pop("id", None)    
    session.pop("username", None) 
    session.pop("Puesto", None) 

def estalogueado():
    if "id" in session:
        return True
    else:
        return False

def es_admin():
    return session.get("1", False)        

@app.context_processor
def logear():
    if "id" in session:
        return {'estalogueado':True}
    else: 
        return {'estalogueado':False}

@app.context_processor
def admin():
    return {'es_admin':session.get("1", False)}     