from django.db import models


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    stock = models.IntegerField()

    def __str__(self):
        return self.title

class Member(models.Model):
    full_name = models.CharField(max_length=200)
    date_of_birth = models.DateField(default='1900-01-01')  # Assuming a default birth date
    address = models.CharField(max_length=200, default='', blank=True)
    phone_number = models.CharField(max_length=15, default='')
    email = models.EmailField(unique=True)
    outstanding_debt = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    
    def __str__(self):
        return self.full_name


class Transaction(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    fee = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.book.title} issued to {self.member.name}"
