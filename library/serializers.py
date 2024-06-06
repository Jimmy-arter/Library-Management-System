from rest_framework import serializers
from .models import Book, Member, Transaction

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
    
    
    def validate_phone_number(self, value):
        if not value.startswith('+254'):
            raise serializers.ValidationError('Phone number must start with +254')
        return value
    
    def create(self, validated_data):
        book = validated_data.get('book')
        if book.stock < 1:
            raise serializers.ValidationError('Book stock is not sufficient')
        book.stock -= 1
        book.save()
        return super().create(validated_data)
    
    
    def update(self, instance, validated_data):
        if 'return_date' in validated_data:
            days_issued = (validated_data['return_date'] - instance.issue_data).days
            fee = days_issued * 10   # For example, 10/= per day
            validated_data['fee'] = fee
            
            member = instance.member
            member.outstanding_debt += fee
            if member.outstanding_debt > 500:
                raise serializers.ValidationError("Member's outstanding debt exceeds KES 500")
            member.save()
            
            book = instance.book
            book.stock += 1
            book.save()
            
        return super().update(instance, validated_data)
