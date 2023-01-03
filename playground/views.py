from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product, OrderItem, Order, Customer, Collection
from django.db.models import Q, F, Value, Func, ExpressionWrapper, DecimalField
from django.db.models.aggregates import Count, Max, Min, Avg
from django.db.models.functions import Concat
from django.contrib.contenttypes.models import ContentType
from tags.models import TaggedItem
from django.db import transaction, connection


# @transaction.atomic()
# def a_transaaction():
#     pass

# Create your views here.
def say_hello(request):
    try:
        #query_set  = Product.objects.filter(unit_price__gt=20)
        query_set  = Product.objects.filter(unit_price__range=(20,30))
        temp = Product.objects.filter(collection__id__range=(1,2,3))
        query_set  = Product.objects.filter(title__icontains='coffee')
        query_set  = Product.objects.filter(unit_price__lt = 20, inventory__lt = 10)
        query_set  = Product.objects.filter(unit_price__lt = 20).filter(inventory__lt=10)
        query_set  = Product.objects.filter(Q(inventory__lt=10)|~Q(unit_price__lt = 20))
        query_set  = Product.objects.filter(inventory=F('unit_price'))
        query_set  = Product.objects.order_by('-title','unit_price')
        #product = Product.objects.earliest('unit_price') #return a product
        query_set  = Product.objects.all()[:5]
        query_set  = Product.objects.values('id','title','collection__title').distinct()
        query_set  = Product.objects.values_list('id','title','collection__title')
        query_set  = Product.objects.only('id','title') #Product.objects.defer also
        query_set  = Product.objects.select_related('collection').all() #JOIN
        query_set  = Product.objects.prefetch_related('promotions').all() #JOIN for manytomany
        query_set = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]
        #result = Product.objects.aggregate(Count('id'),Min('unit_price'))
        query_set = Customer.objects.annotate(is_new = Value(True))
        query_set = Customer.objects.annotate(new_id=F('id')+2)
        query_set = Customer.objects.annotate(
            full_name=Func(F('first_name'),Value(' '),F('last_name'), function='CONCAT')
        )
        query_set = Customer.objects.annotate(
            full_name=Concat('first_name',Value(' '),'last_name')
        )
        query_set = Customer.objects.annotate(
            orders_count = Count('order')
        )
        discounted_price = ExpressionWrapper(F('unit_price')*0.8, output_field=DecimalField())
        query_set = Product.objects.annotate(
            discounted_price = discounted_price
        )

        content_type = ContentType.objects.get_for_model(Product)
        query_set = TaggedItem.objects.select_related('tag').filter(
            content_type = content_type,
            object_id = 1
        )



        # collection = Collection()
        # collection.title = 'Video Games'
        # collection.featured_product = Product(pk=1)
        #collection.featured_product_id = 1
        #colection2 = Collection(title = 'New games') Don't use this approach
        # collection.save()

        # c = Collection.objects.create(name='a', featured_product_id = 3) same problem

        #Update
        # collection = Collection.objects.get(pk=11)
        # collection.featured_product = None
        # collection.save()

        #Collection.objects.filter(pk=11).update(featured_product=None)
        # collection.delete()

        #Collection.objects.filter(id__gt=5).delete()

        #transaction
        # with transaction.atomic():
        #     order = Order()
        #     order.customer_id = 1
        #     order.save()

        #     item = OrderItem()
        #     item.order = order
        #     item.product_id = 1
        #     item.quantity = 1
        #     item.unit_price = 10
        #     item.save()
        
        #Raw SQL queries
        query_set = Product.objects.raw('SELECT * FROM store_product')

        # cursor = connection.cursor()
        # cursor.execute('')
        # cursor.close()

        # with connection.cursor() as cursor:
        #     cursor.execute('')



    except ObjectDoesNotExist as e:
        pass
    for product in query_set:
        print(product)
    return render(request, 'hello.html', {'name':'Mosh','products':list(query_set)})

