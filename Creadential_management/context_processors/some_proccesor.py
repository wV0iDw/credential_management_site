from management.models import*
from django.shortcuts import redirect  
from management.views import*


def base_logo(request):
    if 'user_id' not in request.session:
        return ""
    else:
        user_id = request.session['user_id']
        user_deta = CustomUser.objects.filter(id=user_id).first()
        role_list = Roles.objects.filter(status=1)
        uroledata= user_deta.role_id
        # urole_list = Roles.objects.filter(id=uroledata)
        perm__id = permissions.objects.filter(role_id=uroledata).first()
        permdict = perm__id.permission.split()
        cred_list = CustomUser.objects.filter(status=1)
        # creduser_list = website_credentials.objects.filter(role_id=uroledata).first()
        # creduser_id =  creduser_list.user_ids.split()
        dete = { 'roles_per' : user_deta.role_id,
                 'roles_img' : user_deta.image,
                 'user_name' : user_deta,
                 'role_list' : role_list,
                #  'urole_list': urole_list,
                 'permdict' : permdict,
                 'cred_list' : cred_list,
                #  'creduser_id' : creduser_id
                 }
   #   = Orgao.objects.filter(name='somename') # or whatever object you need
        return dete

# def gfrole(request):
#     if 'user_id' not in request.session:
#         return ""
#     else:
#         role_list = Roles.objects.filter(status=1)
#         rolecontext = {
#          'role_list':role_list
#          }
#         return rolecontext