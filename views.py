from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Book,Borrow,Category,ContactMessage
from .forms import BookForm, BorrowForm
from datetime import date
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models import Exists, OuterRef
from .models import ContactMessage

# --------------------
# Home page
# --------------------
def home(request):
    borrowed_books = Borrow.objects.filter(
        book=OuterRef('pk'),
        return_date__isnull=True
    )

    books = Book.objects.annotate(
        is_borrowed=Exists(borrowed_books)
    )

    return render(request, 'books/home.html', {
        'books': books
    })
# --------------------
# Book create page
# --------------------
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BookForm()
    return render(request, 'books/book_form.html', {'form': form})


# --------------------
# Static pages
# --------------------
def about(request):
    return render(request, 'books/about.html')

def services(request):
    return render(request, 'books/services.html')

def contact(request):
    return render(request, 'books/contact.html')


# --------------------
# Search + Borrow page
# --------------------
def search_borrow(request):
    query = request.GET.get('q', '')

    borrowed_books = Borrow.objects.filter(
        book=OuterRef('pk'),
        return_date__isnull=True
    )

    books = Book.objects.annotate(
        is_borrowed=Exists(borrowed_books)
    )

    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()

    return render(request, 'books/search_borrow.html', {
        'books': books,
        'query': query
    })


def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    today = date.today()

    if request.method == 'POST':
        form = BorrowForm(request.POST)
        if form.is_valid():
            borrow = form.save(commit=False)
            borrow.book = book
            borrow.borrow_date = today

            # ✅ SAFE lines (NEW)
            borrow.status = 'borrowed'
            borrow.return_date = None

            borrow.save()

            messages.success(
                request,
                f'✅ "{book.title}" borrowed successfully!'
            )

            return redirect('search_borrow')
    else:
        form = BorrowForm()

    return render(request, 'books/borrow_form.html', {
        'form': form,
        'book': book,
        'today': today,
        'year': today.year
    })


# --------------------
# Admin & Security pages
# --------------------
@login_required
def admin_dashboard(request):
    total_books = Book.objects.count()
    total_users = User.objects.count()
    total_borrowed = Borrow.objects.filter(status='borrowed').count()
    pending_returns = Borrow.objects.filter(status='borrowed').count()
    recent_borrowings = Borrow.objects.order_by('-borrow_date')[:5]
    recent_messages = ContactMessage.objects.order_by('-created_at')[:5]

    context = {
        'total_books': total_books,
        'total_users': total_users,
        'total_borrowed': total_borrowed,
        'pending_returns': pending_returns,
        'recent_borrowings': recent_borrowings,
        'recent_messages': recent_messages,
    }

    return render(request, 'books/admin_dashboard.html', context)

@login_required
def secure_reliable(request):
    return render(request, 'books/secure_reliable.html')

def my_books(request):
    category_id = request.GET.get('category')

    categories = Category.objects.all()

    borrowed_books = Borrow.objects.filter(
        book=OuterRef('pk'),
        return_date__isnull=True
    )

    books = Book.objects.annotate(
        is_borrowed=Exists(borrowed_books)
    )

    if category_id:
        books = books.filter(category_id=category_id)

    context = {
        'books': books,
        'categories': categories
    }
    return render(request, 'books/my_books.html', context)

def category_books(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    books = Book.objects.filter(category=category)

    return render(request, 'books/category_books.html', {
        'category': category,
        'books': books
    })


# --------------------
# Return book (FIXED)
# --------------------
def return_book(request, borrow_id):
    borrow = get_object_or_404(Borrow, id=borrow_id)

    if borrow.status != 'returned':
        borrow.status = 'returned'
        borrow.return_date = date.today()
        borrow.save()

        messages.success(request, '📗 Book returned successfully!')

    return redirect('admin_dashboard')

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        messages.success(request, "Your message has been sent successfully!")
        return redirect("contact")

    return render(request, "books/contact.html")


def digital_books(request):
    return render(request, 'books/digital_books.html')

def online_membership(request):
    return render(request, 'books/online_membership.html')
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
        else:
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            messages.success(request, "Registration Successful!")
            return redirect('register')   # same page ma farkine

    return render(request, 'books/register.html')

def dashboard(request):
    # तपाईंको dashboard को logic यहाँ राख्नुहोस्
    return render(request, 'books/dashboard.html')