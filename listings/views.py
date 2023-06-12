from django.shortcuts import render, get_object_or_404
from .models import Listing
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from .choices import price_choices, bedroom_choices, state_choices
# Create your views here.

def index (request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)
    paginator = Paginator(listings, 3)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)
    context={'listings':paged_listings,
             'price_choices':price_choices,
             'bedroom_choices':bedroom_choices,
             'state_choices':state_choices}
    return render(request, 'listings/listings.html', context=context)
    
def listing (request,id):
    listing = get_object_or_404(Listing, pk=id)
    context = {'listing':listing}
    return render(request, 'listings/listing.html', context)
    
def search (request):
    
    queryset_list = Listing.objects.order_by('-list_date')
    
    #keyword
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = Listing.objects.filter(descriptionity__icontains = keywords)
            
    #city
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = Listing.objects.filter(city__iexact = city)
            
    #state
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_list = Listing.objects.filter(state__iexact = state)
            
    #Bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            queryset_list = Listing.objects.filter(bedroom__lte = bedrooms)
            
    #Price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = Listing.objects.filter(price__lte = price)
    context={
        'listings':queryset_list,
        'price_choices':price_choices,
        'bedroom_choices':bedroom_choices,
        'state_choices':state_choices,
        'values':request.GET
    }
    return render(request, 'listings/search.html', context)