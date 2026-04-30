from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Advertisement, Comment, BookMark
from django.http import HttpRequest
from .forms import CategoryForm, AdvertisementForm, CommentForm
from django.contrib.auth.decorators import login_required

def home(request: HttpRequest):
    categories = Category.objects.all()

    if request.GET.get('adversisment'):
        if not request.user.is_authenticated:
            return redirect('home')
        advertisements = []
        bookmarks = BookMark.objects.filter(user=request.user)
        for bookmark in bookmarks:
            advertisment = bookmark.advertisement
            advertisment.like = True
            advertisements.append(advertisment)
    else:
        advertisements = Advertisement.objects.all()
        if request.user.is_authenticated:
            for advertisment in advertisements:
                res = advertisment.bookmark_set.filter(user=request.user).exists()
                if res:
                    advertisment.like = True
        else:
            advertisment = Advertisement.objects.all()
    
    context = {
        'advertisements': advertisements,
        'categories': categories
    }

    return render(request, 'olxapp/home.html', context)

def ad_by_category(request: HttpRequest, category_id):
    category = Category.objects.get(id=category_id)
    ad = Advertisement.objects.filter(category=category)

    context = {
        'category': category,
        'ad': ad
    }

    return render(request, 'olxapp/advens_by_category.html', context)

def ad(request: HttpRequest, ad_id):
    categories = Category.objects.all()
    ad = get_object_or_404(Advertisement, id=ad_id)
    comments = Comment.objects.filter(advertisment=ad).order_by('-created')
    context = {
        'ad': ad,
        'categories': categories,
        'title': ad.title,
        'form': CommentForm(),
        'comments': comments
    }

    return render(request, 'olxapp/advens.html', context)



def add_advens(request: HttpRequest):
    if request.user.is_staff:
        if request.method == 'POST':
            form = AdvertisementForm(data=request.POST, files=request.FILES)
            if form.is_valid():
                advens = form.save()
                return redirect('advens', ad_id=advens.id)
        else:
            form = AdvertisementForm()
        context = {
            'form': form
        }

        return render(request, 'olxapp/add_advens.html', context)
    return redirect('home')

def add_category(request: HttpRequest):
    if request.user.is_staff:
        if request.method == 'POST':
            form = CategoryForm(data=request.POST, files=request.FILES)
            if form.is_valid():
                category = form.save()
                return redirect('advens_by_category', category_id=category.id)
        else:
            form = CategoryForm()
        context = {
            'form': form
        }
        return render(request, 'olxapp/add_category.html', context)
    return redirect('home')

def update_category(request: HttpRequest, category_id: int):
    if request.user.is_staff:
        category = get_object_or_404(Category, id=category_id)
        if request.method == "POST":
            form = CategoryForm(data=request.POST, files=request.FILES, instance=category)
            if form.is_valid():
                form.save()
                return redirect('advens_by_category', category_id=category.id)
        else:
            form = CategoryForm(instance=category)

        context = {
            'form': form
        }
        return render(request, 'olxapp/update_category.html', context)
    return redirect('home')

def update_advens(request: HttpRequest, ad_id: int):
    if request.user.is_staff:
        advens = get_object_or_404(Advertisement, id=ad_id)
        if request.method == 'POST':
            form = AdvertisementForm(data=request.POST, files=request.FILES, instance=advens)
            if form.is_valid():
                form.save()
                return redirect('advens', ad_id=advens.id)
        else:
            form = AdvertisementForm(instance=advens)

        context = {
            'form': form
        }
        return render(request, 'olxapp/update_advens.html', context)
    return redirect('home')

def delete_advens(request: HttpRequest, advens_id: int):
    if request.user.is_staff:
        advens = get_object_or_404(Advertisement, id=advens_id)
        if request.method == "POST":
            advens.delete()
            return redirect('home')
        
        context = {
            'advens': advens
        }
        return render(request, 'olxapp/confirm_advens.html', context)
    return redirect('home')

def delete_category(request: HttpRequest, category_id: int):
    if request.user.is_staff:
        category = get_object_or_404(Category, id=category_id)
        if request.method == "POST":
            category.delete()
            return redirect('home')
        context = {
            'category': category
        }

        return render(request, 'olxapp/confirm_category.html', context)
    return redirect('home')


#---/comment start\-----

def create_comment(request: HttpRequest, adversiment_id: int):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = CommentForm(data=request.POST)
            if form.is_valid():
                advertisment = get_object_or_404(Advertisement, id=adversiment_id)
                comment = form.save(commit=False)
                comment.advertisment = advertisment
                comment.user = request.user
                comment.save()
        return redirect('advens', ad_id=adversiment_id)
    else:
        return redirect('home')
    
@login_required(login_url='home')
def update_comment(request: HttpRequest, comment_id: int):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user == request.user:
        if request.method == 'POST':
            form = CommentForm(data=request.POST, instance=comment)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.edited = True
                comment.save()
                return redirect('advens', ad_id=comment.advertisment.id)
        else:
            form = CommentForm(instance=comment)
        context = {
            'form': form
        }
        return render(request, 'olxapp/update_comment.html', context)
    else:
        return redirect('advens', ad_id=comment.advertisment.id)

@login_required(login_url='home')
def delete_comment(request: HttpRequest, comment_id: int, advens_id: int):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user == request.user or request.user.is_superuser:
        comment.delete()
    return redirect('advens', ad_id=advens_id)

#---/comment edn\-----

#---/bookmark start\-----

@login_required(login_url='home')
def add_bookmark(request: HttpRequest, advertisment_id: int):
    advertisement = get_object_or_404(Advertisement, id=advertisment_id)
    bookmark, created = BookMark.objects.get_or_create(advertisement=advertisement, user=request.user)
    if not created:
        bookmark.delete()
    current_page = request.META.get('HTTP_REFERER', 'home')
    return redirect(current_page)

#---/bookmark end\-----