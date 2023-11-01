from django.shortcuts import render
from offers.models import ProductOffer



# Create your views here.
def offers(request):
    main_slid = ProductOffer.objects.all()

    context = {'main_slid':main_slid,}
    return render (request, "offers/offer_page.html", context)

