from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View

from . forms import ProfileForm
from . models import UserProfile, User

# Create your views here.
def signup_redirect(request):
    return redirect('home_page')


class SampleTemplateView(TemplateView):

    template_name = "login.html"

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name)
    
class WelcomeTemplateView(TemplateView):

    template_name = "welcome.html"
    form = ProfileForm()

    def get(self, request, *args, **kwargs):
        form = ProfileForm()
        template_name="welcome.html"
        profile_added = UserProfile.objects.filter(user=request.user)
        context = {'name': request.user.first_name, 
                    'form': form, 'profile_added': profile_added}
        if profile_added:
            profile = profile_added.first()
            data = {'name': profile.user.first_name,
                'emp_code': profile.emp_code,
                'age': profile.age,
                'phone': profile.phone}
            form = ProfileForm(data)
            template_name="profile.html"
            context = {
                'name': request.user.first_name,
                'user_data': {
                    'name': profile.user.first_name,
                    'emp_code': profile.emp_code,
                    'age': profile.age,
                    'phone': profile.phone,
                    'slug': profile.slug,
                    'salary': profile.salary if profile.salary else None
                    },
                'form': form,
                }
        return render(request, template_name, context=context)
    
    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        form = ProfileForm(data)
        if form.is_valid():
            profile_data = form.cleaned_data
            user = request.user
            profile = UserProfile.objects.filter(user=user)
            if profile:
                profile.update(**profile_data)
                profile = profile.first()
            else:
                profile_data['user'] = user
                profile = UserProfile.objects.create(**profile_data)
        else:
            print(form.errors)
        context = {
            'name': request.user.first_name,
            'user_data': {
                'name': profile.user.first_name,
                'emp_code': profile.emp_code,
                'age': profile.age,
                'phone': profile.phone,
                'slug': profile.slug,
                }
            }
        return render(request, template_name="profile.html", context=context)

class SalaryUpdateView(TemplateView):

    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        profile = UserProfile.objects.get(slug=data.get('slug'))
        profile.salary = float(data.get('salary'))
        profile.save()
        return redirect('/welcome')
    
class EmployeeListView(TemplateView):
    template_name = "employees.html"
    def get(self, request, *args, **kwargs):
        employess = UserProfile.objects.filter(user__is_staff=False, user__is_active=True)
        user_details = [{
            'sl_no': iter+1, 
            "name": '{} {}'.format(item.user.first_name, item.user.last_name),
            "emp_code":item.emp_code,
            "age": item.age,
            "phone": item.phone,
            "salary": item.salary if item.salary else 0.0,
            "slug": item.slug} for iter, item in enumerate(employess)]
        context = {
            'name': request.user.username,
            'user_details': user_details    
            }
        return render(request, self.template_name, context=context)
    
class EmployeeDetailsView(TemplateView):
    template_name = "employee_detail.html"
    def get(self, request, *args, **kwargs):
        employee = UserProfile.objects.filter(slug=kwargs['slug']).first()
        user_details = {
            "name": '{} {}'.format(employee.user.first_name, employee.user.last_name),
            "emp_code":employee.emp_code,
            "age": employee.age,
            "phone": employee.phone,
            "salary": employee.salary if employee.salary else 0.0,
            "slug": employee.slug
        }
        context = {
            'name': request.user.first_name,
            'user_details': user_details    
            }
        return render(request, self.template_name, context=context)
    
class EmployeeDetailsUpdateView(View):
    template_name = "employee_detail.html"
    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        slug = kwargs['slug']
        data.pop('csrfmiddlewaretoken', None)
        updated_data = {
            "emp_code": data.get("emp_code"),
            "age": int(data.get("age")),
            "phone": data.get("phone"),
            "salary": float(data.get("salary")),
        }
        UserProfile.objects.filter(slug=slug).update(**updated_data)
        employee = UserProfile.objects.get(slug=slug)
        user_details = {
            "name": '{} {}'.format(employee.user.first_name, employee.user.last_name),
            "emp_code":employee.emp_code,
            "age": employee.age,
            "phone": employee.phone,
            "salary": employee.salary if employee.salary else 0.0,
            "slug": employee.slug
        }
        context = {
            'name': request.user.first_name,
            'user_details': user_details    
            }
        return render(request, self.template_name, context=context)
    
class EmployeeDeleteView(View):
    def post(self, request, *args, **kwargs):
        slug = kwargs['slug']
        employee = UserProfile.objects.filter(slug=slug).first()
        employee.delete()
        return redirect("/list-employees")