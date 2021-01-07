from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Place, Way

@method_decorator(csrf_exempt, name='dispatch')
class GameAppView(View):
    def get(self, request):
        print('poczatek', request.session)
        if "current_place" not in request.session:
            place = Place.objects.all().order_by('description')[0].id
            request.session["current_place"] = place
            print('default place', request.session.get("current_place"))
        else:
            place = request.session.get("current_place")
            print('new place session', request.session.get("current_place"))
            print('new place', place)
        ow =  Place.objects.get(id=place)
        desc = ow.description
        dsc = Way.objects.all()
        ways = ow.outgoiing_ways.all().values_list('description')
        print('ways out', ways)
        way_list = []
        way_id_list = []
        for way in dsc:
            way_list.append(way.description)
            way_id_list.append(way.id)
        context = {'place': desc, 'ways': ways, 'way_list': dsc}
        return render(request, 'index.html', context)

@method_decorator(csrf_exempt, name='dispatch')
class GameAppViewGo(View):
    def post(self, request, way_id):
        wid = request.POST.get('way_id')
        print('id_drogi', way_id)
        pid = request.session.get("current_place")
        print('aktualne miejsce', pid)
        p = Place.objects.get(id=pid)
        print('aktualne miejsce z bazy', p)
        pw = p.outgoiing_ways.all()
        for way in pw:
            if way_id == way.id:
                print(way.id)
                request.session["current_place"] = way.destination.id
                print('nowe miejsce', request.session.get("current_place"))
        return redirect('/')

#class SetCookieCurrentPlace(View):



# Create your views here.
