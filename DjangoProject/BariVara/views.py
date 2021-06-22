from django.shortcuts import render,redirect,get_object_or_404
from .forms import *
from .models import advertisements,images,Comment
from django.forms import modelformset_factory
from django.contrib import messages
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Function for homepage after login
def HomePage(request):

    advertisement = advertisements.objects.all().order_by('-id')
    paginator = Paginator(advertisement, 6)
    page = request.GET.get('page')
    try:
        advertisement = paginator.page(page)
    except PageNotAnInteger:
        advertisement = paginator.page(1)
    except EmptyPage:
        advertisement = paginator.page(paginator.num_pages)
    context = {
        'advertisement' : advertisement,
    }
    return render(request, 'BariVara/HomePage.html', context)

# Function for creating new advertisement
def create_advertisements(request):
    ImageFormset= modelformset_factory(images,fields=('image',),extra=3)
    if request.method=='POST':
        form=advertisementForm(request.POST)
        formset=ImageFormset(request.POST or None, request.FILES or None)
        if form.is_valid() and formset.is_valid():
            advertisement=form.save(commit=False)
            advertisement.owner=request.user
            advertisement.save()
            for f in formset:
                try:
                    photo=images(advertisement=advertisement,image=f.cleaned_data['image'])
                    photo.save()                   
                except Exception as e:
                    break
            return redirect('HomePage')
            
    else:
        form=advertisementForm()
        formset= ImageFormset(queryset=images.objects.none())
    
    context={
        'form':form,
        'formset':formset,
    }
    return render (request,'BariVara/create_advertisements.html',context)

# Function for editing advertisement
def advertisement_edit(request, id):
    advertisement = get_object_or_404(advertisements, id=id)
    ImageFormset= modelformset_factory(images,fields=('image',),extra=3, max_num=3)
    if advertisement.owner != request.user:
        raise Http404()
    if request.method == "POST":
        form = advertisementEditForm(request.POST or None, instance=advertisement)
        formset=ImageFormset(request.POST or None, request.FILES or None)
        if form.is_valid() and formset.is_valid():
            form.save()
            print(formset.cleaned_data)
            data = images.objects.filter(advertisement=advertisement)
            for index, f in enumerate(formset):
                if f.cleaned_data:
                    if f.cleaned_data['id'] is None:
                        photo=images(advertisement=advertisement,image=f.cleaned_data['image'])
                        photo.save()
                    elif f.cleaned_data['image'] is False:
                        photo = images.objects.get(id=request.POST.get('form-'+str(index)+'-id'))
                        photo.delete()
                    else:
                        photo=images(advertisement=advertisement,image=f.cleaned_data['image'])
                        d = images.objects.get(id=data[index].id)
                        d.image = photo.image
                        d.save()

            return HttpResponseRedirect(advertisement.get_absolute_url())
    else:
        form = advertisementEditForm(instance=advertisement)
        formset = ImageFormset(queryset=images.objects.filter(advertisement=advertisement))
        context = {
            'form': form,
            'advertisement': advertisement,
            'formset':formset,
        }
    return render(request, 'Barivara/advertisement_edit.html', context)

# Function for deleting advertisement
def advertisement_delete(request, id):
    advertisement = get_object_or_404(advertisements, id=id)
    if advertisement.owner != request.user:
        raise Http404()
    advertisement.delete()
    return redirect('HomePage')

# Function for showing user's own advertisements        
def your_advertisements(request):
    advertisement={
        'advertisements': advertisements.objects.all()
    }
    return render (request, 'BariVara/your_advertisements.html',advertisement)

# Function for showing details of any particular advertisement
def advertisement_details(request,id):
    advertisement = get_object_or_404(advertisements, id=id)

    Comments=Comment.objects.filter(advertisement=advertisements.objects.get(id=id) , reply = None)
    if request.method=='POST':
        form=commentForm(request.POST or None)
        if form.is_valid():

            content=request.POST.get('content')
            print(content)
            reply_id = request.POST.get('comment_id')
            print(reply_id)
            comment_qs = None
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)
            comment=Comment.objects.create(advertisement=advertisements.objects.get(id=id),user=request.user,content=content , reply = comment_qs)
            print(content)

            comment.save()
            return HttpResponseRedirect(advertisement.get_absolute_url())
            #form.save()
            #return redirect('HomePage')
    else:
        form=commentForm()
    context={
        'advertisement':advertisements.objects.get(id=id),
        'comments':Comments,
        'form':form,        
        }
    
    return render(request,'BariVara/advertisement_details.html',context)

# Function for filtering advertisements by budget
def Filter(request):

    query = request.GET['query']
    if query=="0":
        posts = advertisements.objects.filter(rent__gte=0)
        params = {'advertisements':posts}
        return render(request, 'BariVara/filter.html', params)
    elif query=="1":
        posts = advertisements.objects.filter(rent__lt=15000)
        params = {'advertisements':posts}
        return render(request, 'BariVara/filter.html', params)
    elif query=="2":
        posts = advertisements.objects.filter(rent__range=(15000,20000))
        params = {'advertisements':posts}
        return render(request, 'BariVara/filter.html', params)
    elif query=="3":
        posts = advertisements.objects.filter(rent__range=(20001,25000))
        params = {'advertisements':posts}
        return render(request, 'BariVara/filter.html', params)
    elif query=="4":
        posts = advertisements.objects.filter(rent__range=(25001,30000))
        params = {'advertisements':posts}
        return render(request, 'BariVara/filter.html', params)
    elif query=="5":
        posts = advertisements.objects.filter(rent__gt=30000)
        params = {'advertisements':posts}
        return render(request, 'BariVara/filter.html', params)    
        
    
# Function for searching advertisements by area
def Search(request):

    query = request.GET['query']
    posts = advertisements.objects.filter(place__icontains=query)
    params = {'advertisements':posts}
    return render(request, 'BariVara/search.html', params)


