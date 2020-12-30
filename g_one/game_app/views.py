from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Place, Way

@method_decorator(csrf_exempt, name='dispatch')
class GameAppView(View):
    def get(self, request):
        pid = Place.objects.all().order_by('description')[0].id
        if "current_place" not in request.session:
            request.session["current_place"] = pid
        place = request.session.get("current_place")
        ow =  Place.objects.get(id=place)
        desc = ow.description
        dsc = Way.objects.all().values_list("description")
        ways = ow.outgoiing_ways.all().values_list('short_description')
        way_list = []
        for way in dsc:
            way_list.append(way[0])

        context = {'place': desc, 'ways': ways, 'way_list': way_list}
        return render(request, 'index.html', context)

#class SetCookieCurrentPlace(View):



# Create your views here.
