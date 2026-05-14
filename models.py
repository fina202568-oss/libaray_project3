from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    cover = models.ImageField(upload_to='book_images/', blank=True, null=True)  # ✅ Image field

    def __str__(self):
        return self.title

from django.db import models

class Borrow(models.Model):
    STATUS_CHOICES = (
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
    )

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)


    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='borrowed'   # 🔴 very important
    )

    damage_or_loss_agreement = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.customer_name} - {self.book.title}"
    

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

