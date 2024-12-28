from django.contrib.auth import authenticate, login,logout
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
# from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.urls import reverse
from django.views.generic import TemplateView,CreateView,FormView,DetailView,ListView,DeleteView
from django.views.generic.edit import UpdateView
from django.views import View
from AdminApp.models import Property
from AdminApp.forms import PropertyForm
from users.models import Profile,Favorite
from users.forms import UserRegisterForm,UserLoginForm,ProfileForm,InquiryForm
from django.utils.decorators import method_decorator
from users.decorators import login_required
from django.core.mail import send_mail
# Create your views here.

class Home(TemplateView):
    template_name='index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        location = self.request.GET.get('location', '')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        property_type = self.request.GET.get('property_type', '')
        queryset = Property.objects.all()

        if location:
            queryset = queryset.filter(location__icontains=location)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if property_type:
            queryset = queryset.filter(property_type=property_type)

        context["Property"] = queryset
        context["property_type_choices"] = Property.PROPERTY_TYPES
        return context


class UserRegisterView(CreateView):
    template_name="user_register.html"
    form_class=UserRegisterForm
    success_url = reverse_lazy("login")  

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.save()
        # for creating user
        Profile.objects.create(user=user)             
        messages.success(self.request, "Your account has been created successfully! You can now log in.")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request, "There was an error in your submission. Please check the details and try again.")
        return super().form_invalid(form) 


class UserLoginView(FormView):
    template_name="user_login.html"
    form_class=UserLoginForm

    def post(self, request, *args, **kwargs):
        username=request.POST.get("username")
        password=request.POST.get("password")
        user=authenticate(request,username=username,password=password)
        if user :
            login(request,user)
            messages.success(request,'You have logged in successfully!')
            return redirect('home_view')
        else:
            messages.error(request,'Invalid username or password')
            return redirect('login')
        

class LogoutView(View):
    def get(self, request):
        logout(request) 
        messages.success(request, "You have been logged out successfully!") 
        return redirect('login') 


@method_decorator(login_required, name='dispatch')
class ProfileListView(View):
    def get(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=request.user)
            return render(request, 'profile.html', {'profile': profile})
        except Profile.DoesNotExist:
            return render(request, 'profile.html', {'profile': None})


@method_decorator(login_required,name="dispatch")   
class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'profile_edit.html'
    context_object_name = 'profile'

    def get_object(self):
        return Profile.objects.get(user=self.request.user)
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Your profile has been updated successfully.")
        return redirect('profile_view')  
    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)

class PropertiesAllView(ListView):
    model = Property
    template_name = 'all_properties.html'
    context_object_name = 'Property'
    
    def get_queryset(self):
        queryset = Property.objects.all()
        location = self.request.GET.get('location', '')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        property_type = self.request.GET.get('property_type', '')

        if location:
            queryset = queryset.filter(location__icontains=location)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if property_type:
            queryset = queryset.filter(property_type=property_type)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["property_type_choices"] = Property.PROPERTY_TYPES  # Add choices for dropdown
        return context

def properties_buy(request):
    properties = Property.objects.filter(property_for='for sell')
    return render(request, 'buy_properties.html', {'Property': properties})

def properties_rent(request):
    properties = Property.objects.filter(property_for='for rent')
    return render(request, 'rent_properties.html', {'Property': properties})



@method_decorator(login_required,name="dispatch")
class PropertyDetailView(DetailView, FormView):
    model = Property
    template_name = 'property_detail.html'
    context_object_name = 'property'
    form_class = InquiryForm

    def get_initial(self):
        return {
            'name': self.request.user.get_full_name(),
            'email': self.request.user.email,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_favorite'] = Favorite.objects.filter(
            user=self.request.user, property=self.get_object()
        ).exists()
        return context

    def form_valid(self, form):
        property_instance = self.get_object()
        sender_name = form.cleaned_data['name']
        sender_email = form.cleaned_data['email']
        message = form.cleaned_data['message']

        recipient_email = (
            property_instance.owner.email
            if not property_instance.owner.is_staff
            else 'shahulkaniyambetta@gmail.com'  # Replace with your admin email
        )

        full_message = f"Inquiry for {property_instance.title}\n\n" \
                       f"Sender: {sender_name}\n" \
                       f"Email: {sender_email}\n\n" \
                       f"Message:\n{message}"

        send_mail(
            subject=f"Inquiry about {property_instance.title}",
            message=full_message,
            from_email=sender_email,
            recipient_list=[recipient_email],
        )

        messages.success(self.request, "Your inquiry has been sent successfully.")
        return redirect(reverse('property_detail', kwargs={'pk': property_instance.pk}))

    def post(self, request, *args, **kwargs):
        if 'add_to_favorites' in request.POST:
            property_instance = self.get_object()
            favorite, created = Favorite.objects.get_or_create(
                user=request.user, property=property_instance
            )
            if created:
                messages.success(request, "Property added to favorites.")
            else:
                messages.info(request, "Property is already in favorites.")
            return redirect(reverse('property_detail', kwargs={'pk': property_instance.pk}))

        return super().post(request, *args, **kwargs)


@method_decorator(login_required,name="dispatch") 
class FavoritesListView(ListView):
    model = Favorite
    template_name = 'favorites_list.html'  
    context_object_name = 'favorites'

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        if 'remove_from_favorites' in request.POST:
            property_id = request.POST.get('property_id')
            property_instance = Property.objects.get(id=property_id)
            Favorite.objects.filter(user=request.user, property=property_instance).delete()
            messages.success(request, f"{property_instance.title} has been removed from your favorites.")
            return redirect(reverse('favorites_list'))  

        return super().post(request, *args, **kwargs)
    
@method_decorator(login_required,name="dispatch") 
class PropertyListView(ListView):
    model = Property
    template_name = 'property_list.html'
    context_object_name = 'properties'

    def get_queryset(self):
        return Property.objects.filter(owner=self.request.user)
    
class PropertyCreateView(CreateView):
    model = Property
    form_class = PropertyForm
    template_name = 'add_property.html'
    success_url = reverse_lazy('property_list')


    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, "Property added successfully!")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request, "Failed to add property. Please correct the errors below.")
        return super().form_invalid(form)

class PropertyUpdateView(UpdateView):
    model = Property
    form_class = PropertyForm
    template_name = 'update_property.html'
    success_url = reverse_lazy('property_list')
    

    def get_queryset(self):
        return Property.objects.filter(owner=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, "Property updated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Failed to update property. Please correct the errors below.")
        return super().form_invalid(form)


class PropertyDeleteView(SuccessMessageMixin,DeleteView):
    model = Property
    template_name = 'delete_property.html'
    success_url = reverse_lazy('property_list')
    success_message = "Property deleted successfully!"

    def get_queryset(self):
        return Property.objects.filter(owner=self.request.user)
    


    
