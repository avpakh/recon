from django.shortcuts import render

# Create your views here.
def map_page(request):



    return render(request,'gmap.html',{})