from django.conf.urls import url
from .views import *

urlpatterns=[
		url(r'^$',login,name="login"),
		url(r'^categoria/$',categoria,name="categoria"),
		url(r'^listado/(\d+)/$',listado,name="listado"),
		url(r'^viewCart/$',viewCart,name="viewCart"),
		url(r'^invoice/$',invoice,name="invoice"),
	]