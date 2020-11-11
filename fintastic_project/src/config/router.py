from rest_framework import routers

from users.api.v1.views import UserListViewSet
from transactions.api.v1.views import TransactionView

router = routers.SimpleRouter()

router.register(r'users', viewset=UserListViewSet)
router.register(r'transactions', viewset=TransactionView)

urlpatterns = []
urlpatterns += router.urls
