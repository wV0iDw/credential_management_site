from django.shortcuts import render
from .models import*
from .models import CustomUser as Employee
from django.shortcuts import redirect,HttpResponse
from django.contrib import messages
import os
from django.db.models import Q
from django.http import JsonResponse
from context_processors.some_proccesor import*

# Create your views here.
def index(request):
    if 'user_id' not in request.session:
      return redirect('signin')
    else:
     user_count = CustomUser.objects.filter(~Q(status=0)).count()
     role_count = Roles.objects.filter(~Q(status=0)).count()
     context ={     
          'user_count':user_count,
          'role_count':role_count,
     }
     return render(request,'dashboard.html',context)
    

def signin(request):
   messages.success(request, 'Welcome to Credential Management')
   if request.method == 'GET':
            context = ''
            return render(request, 'sign-in.html', {'context': context})

   elif request.method == 'POST':
            email = request.POST.get('email', '')
            password = request.POST.get('password', '')

            if CustomUser.objects.filter(email=email, login_otp=password).exists():
             user_detail = CustomUser.objects.filter(email=email).first()

             #session set
             request.session['user_id'] = user_detail.id
             request.session['role_id'] = user_detail.role_id
             request.session['user_email'] = user_detail.email
             # HISTORY MODEL DATA
             user_id = request.session['user_id']
             user_date = datetime.now().date()
             user_time = datetime.now().time()
             user_ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
             if user_ip_address:
                 ip = user_ip_address.split(',')[0]
             else:
                 ip = request.META.get('REMOTE_ADDR')
             newhistory = histories(user_Id=user_id,login_date=user_date,login_time=user_time,login_ip_address=ip)
             newhistory.save()

            #  messages.info(request, 'Login successfully!')
             return redirect('index')
            elif CustomUser.objects.filter(email=email).exists():
               message="Incorrect password!"
               return render(request, 'sign-in.html',{'msg':message})
            else:
                messages.info(request,'user not register')
                return render(request, 'sign-in.html')

def logout(request):
    try:
        del request.session['user_id']
        messages.success(request, "You're logged out!")
        return redirect('signin')
    except:
        pass
    return HttpResponse("You're logged out.")


def proFile(request):
  if 'user_id' not in request.session:
      return redirect('signin')
  else:
    user_id = request.session['user_id']
    user_detail = CustomUser.objects.filter(id=user_id).first()

    context = {
     'user_detail':user_detail
    }
    

  return render(request, 'profile.html', context)


# def editpage(request,pk):
#   get_data = CustomUser.objects.get(id=pk)
#   return render(request,"edit.html",{'user_id':get_data})


def updateprofile(request):
    if request.method=='POST':
        user_id = request.POST.get('user_id')
        user = CustomUser.objects.get(id = user_id)
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.login_otp =request.POST.get('password')
        user.mobile = int(request.POST.get('phone_number'))
        user.address = request.POST.get('address')
        if 'FILES':
            user.image = request.FILES.get('image')
      # if len(request.FILES)!=0:
      #      os.remove(student.image.path)
        user.save()
        messages.info(request, 'update successfully!')
        return redirect('profile')
    else:
        return render(request,'profile.html')



# def imageupdate(request):
#   if request.method=='POST':
#       user_id = request.POST.get('user_id')
#       user_detail = CustomUser.objects.get(id = user_id)

#       if len(request.FILES)!=0:
#        user_detail.image=request.FILES['image']

#       user_detail.save()  
#   return redirect('profile')




# def get_ip_address(request):
#     user_ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
#     if user_ip_address:
#         ip = user_ip_address.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip

# def show_ip_address(request):
#     user_ip = get_ip_address(request)
#     return render(request, "output.html", {"user_ip":user_ip})

def list(request):
  if request.method=='GET':
   #   roledata=Roles.objects.all()
     roledata=Roles.objects.order_by('-id')

     context = {
        'roledata':roledata
      }
  return render(request,'roles/list.html', context)

def add_role(request):
  if request.method=='POST':
      name=request.POST.get('name')
      status =request.POST.get('status')
      new_role=Roles(name=name,status=status)
      new_role.save()
      messages.success(request, "Role added sucessfully!")
      return redirect('list')
  return render(request, 'roles/add_role.html')


def edit_role(request,role_id=0): 
   role_detail=Roles.objects.get(id=role_id)

   context = {
      'role_detail':role_detail
   }    
   return render(request,'roles/edit_role.html',context)


def update_role(request):
    if request.method=='POST':
      role_id = request.POST.get('role_id')
      new_role = Roles.objects.filter(id = role_id).first()
      new_role.name = request.POST.get('name')
      new_role.save()
      messages.success(request, "Role updated sucessfully!")
      return redirect('list')



def delete_role(request):
   role_id = request.GET.get('role_id')
   roleData = Roles.objects.get(id=role_id)
   roleData.status = 0 
   roleData.save()
   return JsonResponse({'status':'Success', 'msg': 'Role Delete Successfully'})

#########################################Employee

def emp_list(request):
  if request.method=='GET':
     empdata=Employee.objects.filter(~Q(status=0))
   #   role_list = Roles.objects.filter(status=1)
     context = {
        'empdata':empdata,
      #   'role_list':role_list
      }
  return render(request,'employee/emp_list.html', context)



# def emp_add(request):
#   if request.method=='GET':
#      role_list = Roles.objects.filter(status=1)
#      context = {
#         'role_list':role_list
#       }
#   return render(request,'employee/emp_add.html', context)


def emp_add(request):
   if request.method=='POST':
      first_name=request.POST.get('first_name')
      last_name=request.POST.get('last_name')
      mobile=request.POST.get('mobile')
      email=request.POST.get('email')
      if len(request.FILES)!=0:
        image=request.FILES['image']
      role_id=request.POST.get('role_id')
      # rolename = Roles.objects.filter(name=name)
      # # rolid = Roles.objects.get(name=rolename)
      # roolid = rolename.get(id)
      address=request.POST.get('address')
      new_user=Employee(first_name=first_name,last_name=last_name,mobile=mobile,email=email,image=image,role_id=role_id,address=address)
      new_user.save()
      messages.success(request, 'User add successfully!')
      return redirect('emp_list')

   role_list = Roles.objects.filter(status=1)
   context = {
         'role_list':role_list
         }
   return render(request, 'employee/emp_add.html',context)



def emp_edit(request,emp_id=0): 
   user_detail=Employee.objects.get(id=emp_id)
   role_list = Roles.objects.filter(status=1)

   context = {
      'user_detail':user_detail,
      'role_list':role_list
   }    
   return render(request,'employee/emp_edit.html',context)


def update_emp(request):
    if request.method=='POST':
      emp_id = request.POST.get('emp_id')
      new_emp = Employee.objects.filter(id = emp_id).first()
      new_emp.first_name = request.POST.get('first_name')
      new_emp.last_name = request.POST.get('last_name')
      new_emp.email = request.POST.get('email')
      new_emp.mobile = request.POST.get('mobile')
      new_emp.role_id = request.POST.get('role_id')
      new_emp.address = request.POST.get('address')

      # if request.FILES.get('image') is not None:
      #     new_emp.image = request.FILES.get('image')
      if len(request.FILES)!=0:
       new_emp.image=request.FILES['image']
      new_emp.save()
      messages.success(request, 'Employee update successfully!')
      return redirect('emp_list')


def emp_view(request,emp_id): 
   user_detail=Employee.objects.get(id=emp_id)

   context = {
      'user_detail':user_detail
   }    
   return render(request,'employee/emp_view.html',context)


def delete_emp(request):
   emp_id = request.GET.get('emp_id')
   empData = Employee.objects.get(id=emp_id)
   empData.status = 0 
   empData.save()
   return JsonResponse({'status':'Success', 'msg': 'Employee Delete Successfully'})
   # if emp_id:
   #    try:
   #       user_to_be_removed = Employee.objects.get(id=emp_id)
   #       user_to_be_removed.delete()
   #       messages.success(request, 'Employee Deleted successfully!')
   #       return redirect('emp_list')
   #    except:
   #     return HttpResponse('failed')



########################################

def list_cred_web(request):
  if request.method=='GET':
   cred_web_data = None
   if request.session['user_id'] == 1:
     cred_web_data = website_credentials.objects.filter(~Q(status=0)).order_by('-id').raw("Select management_website_credentials.id, management_CustomUser.first_name, management_CustomUser.last_name,management_website_credentials.added_by,management_website_credentials.website_name,management_website_credentials.website_host,management_website_credentials.website_ip,management_website_credentials.website_username,management_website_credentials.website_password,management_website_credentials.created_at,management_website_credentials.updated_at,management_website_credentials.user_ids from management_website_credentials left join management_CustomUser on management_CustomUser.id = management_website_credentials.added_by") 
   else:
      user_id = request.session['user_id']
      cred_web_data = website_credentials.objects.filter(user_ids = user_id)
   context = {
         'cred_web_data':cred_web_data,
      }
   return render(request,'credentials/list_cred.html', context)


def add_cred_web(request):
   if request.method=='POST':
      user_ids = request.POST.get('UserIDS')
      website_name=request.POST.get('website_name')
      website_host=request.POST.get('website_host')
      website_ip=request.POST.get('website_ip')
      # if len(request.FILES)!=0:
      #   image=request.FILES['image']
      website_username=request.POST.get('website_username')
      website_password=request.POST.get('website_password')
      add_by = request.session['user_id']
      
      # added_by=request.POST.get('added_by')
      new_credentials=website_credentials(user_ids=user_ids,website_name=website_name,website_host=website_host,website_ip=website_ip,website_username=website_username,website_password=website_password,added_by=add_by)
      new_credentials.save()
      messages.success(request, "Credential added sucessfully!")
      return redirect('list_cred')
   return render(request, 'credentials/add_cred.html')



def edit_cred_web(request, cred_id=0): 
   cred_detail=website_credentials.objects.filter(id=cred_id).first()

   context = {
      'cred_detail':cred_detail,
   }    
   return render(request,'credentials/edit_cred.html',context)



def update_cred_web(request):
   if request.method=='POST':
      cred_id = request.POST.get('cred_id')
      new_cred = website_credentials.objects.filter(id = cred_id).first()
      new_cred.user_ids = request.POST.get('UserID')
      new_cred.website_name = request.POST.get('website_name')
      new_cred.website_host = request.POST.get('website_host')
      new_cred.website_ip = request.POST.get('website_ip')
      new_cred.website_username = request.POST.get('website_username')
      new_cred.website_password = request.POST.get('website_password')
      # new_cred.added_by = request.POST.get('added_by')
      # new_cred.updated_by = request.POST.get['update_by']
      # new_cred.created_at = request.POST.get('created_at')
      # new_cred.updated_at = request.POST.get('updated_at')
      # if 'FILES':
      #     new_emp.image = request.FILES.get('image')
      new_cred.save()
      messages.success(request, "Credential updated sucessfully!")
      return redirect('list_cred')
   

   
def view_cred_web(request,cred_id): 
   #cred_detail = website_credentials.objects.filter(id=cred_id).raw('Select 1 id, management_CustomUser.first_name, management_CustomUser.last_name,management_website_credentials.added_by,management_website_credentials.website_name,management_website_credentials.website_host,management_website_credentials.website_ip,management_website_credentials.website_username,management_website_credentials.website_password,management_website_credentials.created_at,management_website_credentials.updated_at from management_website_credentials left join management_CustomUser on management_CustomUser.id = management_website_credentials.added_by')
   cred_detail = website_credentials.objects.filter(id = cred_id).first()
  
   context = {
      'cred_detail':cred_detail
   }    
   return render(request,'credentials/view_cred.html',context)


def delete_cred_web(request):
   cred_id = request.GET.get('cred_id')
   credential = website_credentials.objects.get(id=cred_id)
   credential.delete()
   messages.success(request, "Credential deleted sucessfully!")
   return JsonResponse({'status':'Success', 'msg': 'Data Delete Successfully'})



def list_history(request):
    user_id = request.session['user_id']
    user_detail = CustomUser.objects.filter(id=user_id).first()
    historylisting = histories.objects.filter().order_by('-id').raw('Select management_histories.id, management_CustomUser.first_name, management_CustomUser.last_name, management_histories.user_Id, management_histories.login_date, management_histories.login_time from management_histories left join management_CustomUser on management_CustomUser.id = management_histories.user_Id') 
   
    # historylisting=histories.objects.all()
    context = {
            'user_detail':user_detail,
            'historylisting':historylisting,
              }
    return render(request,"history/history_listing.html", context)


def delete_history(request, his_id=0):
   if his_id:
      try:
         cred_user_to_be_removed = histories.objects.get(id=his_id)
         cred_user_to_be_removed.delete()
         messages.success(request, "History deleted sucessfully!")
         return redirect('history_listing')
      except:
       return HttpResponse('failed')


###################### PERMISSION ##########################

def perk(request):
   if request.method == "POST":
      if request.POST.get('role_id'):
          new_perm = permissions() 
          new_perm.role_id=request.POST.get('role_id')
          rr = new_perm.role_id
          permdata={}
          if permissions.objects.filter(role_id = rr).first():
            per = permissions.objects.filter(role_id = rr).first()
            permd = per.permission.split()
            permdata={
               "permd" : permd,
            }
            if request.POST.get('permission'):
               new_perm.permission = request.POST.get('permission')
               per.delete()
               new_perm.save()
            else:
               return render(request,"permission/permission.html",permdata)

          else:
            new_perm.permission = request.POST.get('permission')
            new_perm.save()
          return render(request,"permission/permission.html",permdata)
   else:
      return render(request,"permission/permission.html")
