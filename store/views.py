from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ReviewRating, ProductGallery
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from .forms import ReviewForm
from django.contrib import messages
from orders.models import OrderProduct
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import nltk
import os
# Create your views here.
def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True).order_by('id')
        paginator = Paginator(products, 5)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 5)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context =  {
        'products' : paged_products,
        'product_count': product_count,
    }

    return render(request, 'store/store.html', context)



def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e

    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None


    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)

    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'orderproduct': orderproduct,
        'reviews': reviews,
        'product_gallery': product_gallery,
    }

    return render(request, 'store/product_detail.html', context)



def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter( Q(description__icontains = keyword) | Q(product_name__icontains = keyword))
            product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
    }

    return render(request, 'store/store.html', context)


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Muchas gracias!, tu comentario ha sido actualizado')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id

                # Analizar el sentimiento del comentario
                #nltk.data.path.append('SentiLex-lem-PT02.txt')
                lexicon_path = 'ecommerce/static/SentiLex-lem-PT02.txt'

                lexicon = {}
                with open(lexicon_path, 'r', encoding='utf-8') as file:
                    for line in file:
                        word, _, sentiment = line.strip().split('\t')
                        lexicon[word] = float(sentiment)

                sia = SentimentIntensityAnalyzer(lexicon)


                nltk.download('vader_lexicon')
                sia = SentimentIntensityAnalyzer()
                sentiment_scores = sia.polarity_scores(data.review, lang='es')

                data.sentiment_score = sentiment_scores['compound']
                print(data.sentiment_score)
                #review_text = form.cleaned_data['review']
                #blob = TextBlob(review_text)
                #sentiment_score = blob.sentiment.polarity

                # Guardar el puntaje de sentimiento en la base de datos
                # data.sentiment_score = sentiment_score

                data.save()

                messages.success(request, 'Muchas gracias, tu comentario fue enviado con exito!')
                return redirect(url)
