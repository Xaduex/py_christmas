from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Place, Way

@method_decorator(csrf_exempt, name='dispatch')
class GameAppView(View):
    def get(self, request):
        if "current_place" not in request.session:
            place = Place.objects.all().order_by('description')[0].id
            request.session["current_place"] = place
            request.session["money"] = 0
        else:
            place = request.session.get("current_place")
        ow =  Place.objects.get(id=place)
        desc = ow.description
        dsc = Way.objects.all()
        ways = ow.outgoiing_ways.all().values_list('description')
        way_all_list = []
        cash = request.session.get("money")
        for way in dsc:
            way_list = []
            way_list.append(way.description)
            way_list.append(way.id)
            if cash < way.cost:
                way_list.append(0)
            else:
                way_list.append("")
            way_list.append(way.cost)
            way_list.append(way.gain)
            way_all_list.append(way_list)
        context = {'place': desc, 'ways': ways, 'way_list': dsc, 'cash': cash, 'wal': way_all_list }
        return render(request, 'index.html', context)

@method_decorator(csrf_exempt, name='dispatch')
class GameAppViewGo(View):
    def post(self, request, way_id):
        wid = request.POST.get('way_id')
        pid = request.session.get("current_place")
        p = Place.objects.get(id=pid)
        pw = p.outgoiing_ways.all()
        for way in pw:
            if way_id == way.id:
                if request.session.get("money") >= way.cost:
                    request.session["current_place"] = way.destination.id
                    request.session["money"] -= way.cost
                    request.session["money"] += way.gain
                else:
                    redirect('/')
                print('nowe miejsce', request.session.get("current_place"))
        return redirect('/')




# Create your views here.
