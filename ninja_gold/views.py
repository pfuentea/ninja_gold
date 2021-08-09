from abc import get_cache_token
from django.shortcuts import render, HttpResponse
from random import randint, uniform,random


def index(request):
    request.session['mensajes']=[]
    request.session['gold']=0
    request.session['turnos_pasados']=0
    request.session['turnos_max']=0
    request.session['turnos_restantes']=0
    request.session['gap']=0
    request.session['turno_zero']=1
    return render(request,'ninja.html')

def second(request, name):
    return HttpResponse('Hola ' + name)

def process_money(request,ubi):
    
    if request.method == "POST":
        request.session['turno_zero']=0
        #accion=request.POST['accion']
        accion=ubi
        mensaje=""
        if accion == 'farm':
            ganancia=randint(10,20)
        elif accion == 'cave':
            ganancia=randint(5,10)
        elif accion == 'house':
            ganancia=randint(2,5)
        elif accion == 'casino':
            ganancia=randint(-50,50)
        elif accion == 'reset':
            request.session['gold']=0
            ganancia=0
            request.session['mensajes']=[]
        
        request.session['gold']+=ganancia
        request.session['turnos_pasados']+=1
        restantes=int(request.session['turnos_restantes'])
        restantes-=1
        request.session['turnos_restantes']=restantes
        gap=int(request.session['meta'])-int(request.session['gold'])
        request.session['gap']=gap
        #request.session['gap']=request.session['meta']-request.session['gold']

        mensaje=str(ganancia)+" desde "+accion+"! ()"

        mensaje = f"{'Ganaste' if ganancia >= 0 else 'Perdiste'} {mensaje}"

        jeison={'mensaje':mensaje, 'style':'success' if ganancia >= 0 else 'danger'}
        request.session['mensajes'].append(jeison)
        request.session.save()

    context={
        }

    if gap<=0 and restantes>=0:
        return render(request,'ninja_win.html',context)
    if gap>0 and restantes<=0:
        return render(request,'ninja_loss.html',context)

    print(request.session['mensajes'] )
    return render(request,'ninja.html',context)

def ninja_reset(request):
    request.session['turno_zero']=1
    request.session['mensajes']=[]
    request.session['gold']=0
    request.session['turnos_pasados']=0
    return render(request,'ninja.html')

def configurar(request):
    request.session['turno_zero']=0
    request.session['turnos_max']=request.POST['turnos']
    request.session['turnos_restantes']=request.session['turnos_max']
    request.session['meta']=request.POST['goal']
    request.session['gap']=request.POST['goal']
    

    return render(request,'ninja.html')