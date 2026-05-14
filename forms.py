from django import forms
from .models import Book, Borrow
from .models import ContactMessage


# --------------------
# Book Form
# --------------------
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Book Title'
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Author Name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Short description',
                'rows': 3
            }),
        }


# --------------------
# Borrow Form
# --------------------
class BorrowForm(forms.ModelForm):
    
    damage_or_loss_agreement = forms.BooleanField(
        required=True,
        label="I agree to the following conditions before borrowing this book:",
        help_text="""
Users can borrow a book only if they agree to pay a fine in case the book is lost or damaged.
If the book is returned, the system can check the book’s condition.
Based on the condition of the book (e.g., missing pages, torn cover, or any damage), the user must pay a fine.
The agreement checkbox in the Borrow form ensures users acknowledge this responsibility before borrowing.
""",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    class Meta:
        model = Borrow
        fields = ['customer_name', 'phone', 'email', 'address', 'return_date']  # address add
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address'
            }),
            'address': forms.TextInput(attrs={       # new field
                'class': 'form-control',
                'placeholder': 'Your Address / Room'
            }),
            'return_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        }
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        