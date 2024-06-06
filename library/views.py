from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Book, Member, Transaction
from .serializers import BookSerializer, MemberSerializer, TransactionSerializer
from django.utils.dateparse import parse_date

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author']

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    
    @action(detail=False, methods=['post'])
    def issue_book(self, request):
        member_id = request.data.get('member_id')
        book_id = request.data.get('book_id')
        member = Member.objects.get(id=member_id)
        book = Book.objects.get(id=book_id)
        
        if book.stock < 1:
            return Response({'error': 'Book stock is not sufficient'}, status=status.HTTP_400_BAD_REQUEST)
        if member.outstanding_debt > 500:
            return Response({'error': 'Member outstanding debt exceeds KES 500'}, status=status.HTTP_400_BAD_REQUEST)
        
        transaction = Transaction.objects.create(book=book, member=member)
        book.stock -= 1
        book.save()
        return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)
    
    
    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        transaction = self.get_object()
        return_date_str = request.data.get('return_date')
        
        
        if not return_date_str:
            return Response({"error": "Return date is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        return_date = parse_date(return_date_str)
        if not return_date:
            return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)
        
        transaction.return_date = return_date
        
        days_issued = (return_date - transaction.issue_date).days
        fee = days_issued * 10  # For example, 10 KES per day
        transaction.fee = fee

        member = transaction.member
        member.outstanding_debt += fee
        if member.outstanding_debt > 500:
            return Response({"error": "Member's outstanding debt exceeds KES 500"}, status=status.HTTP_400_BAD_REQUEST)
        member.save()

        book = transaction.book
        book.stock += 1
        book.save()
        transaction.save()
        return Response(TransactionSerializer(transaction).data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def pay_fee(self, request, pk=None):
        transaction = self.get_object()
        transaction.fee = 0
        transaction.save()
        return Response(TransactionSerializer(transaction).data, status=status.HTTP_200_OK)
    
