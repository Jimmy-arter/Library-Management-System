from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, MemberViewSet, TransactionViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'members', MemberViewSet)
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('transactions/issue_book', TransactionViewSet.as_view({'post': 'issue_book'}), name='issue-book'),
    path('transactions/<int:pk>/return_book/', TransactionViewSet.as_view({'post': 'return_book'}), name='return-book'),
]
