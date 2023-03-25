from django.shortcuts import render, redirect

# Create your views here.
def signup_redirect(request):
    import pdb; pdb.set_trace()
    print(request.user)
    return render('login.html')