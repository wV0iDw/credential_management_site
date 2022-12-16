from django.urls import path,include
from .import views
# from ip_address import show_ip_address

urlpatterns = [
    path("", views.signin, name="signin"),
    path("index", views.index, name="index"),
    path("profile", views.proFile, name="profile"),
    path("updateprofile", views.updateprofile, name="updateprofile"),
    path("login", views.signin, name="signin"),
    path("logout", views.logout, name="logout"),
    # path("imageupdate",views.imageupdate, name="imageupdate"),
    # path('user_ip/',views.show_ip_address,"user_ip"),
    path("list", views.list, name="list"),
    path("add_role", views.add_role, name="add_role"),
    path("update", views.update_role, name="update"),
    path("edit_role/<int:role_id>", views.edit_role, name="edit_role"),
    path("delete_role", views.delete_role, name="delete_role"),
    path("emp_list", views.emp_list, name="emp_list"),
    path("emp_add", views.emp_add, name="emp_add"),
    path("emp_edit/<int:emp_id>", views.emp_edit, name="emp_edit"),
    path("update_emp", views.update_emp, name="update_emp"),
    path("emp_view/<emp_id>", views.emp_view, name="emp_view"),
    path("delete_emp", views.delete_emp, name="delete_emp"),
    path("list_cred", views.list_cred_web, name="list_cred"),
    path("add_cred", views.add_cred_web, name="add_cred"),
    path("edit_cred/<int:cred_id>", views.edit_cred_web, name="edit_cred"),
    path("update_cred", views.update_cred_web, name="update_cred"),
    path("view_cred/<cred_id>", views.view_cred_web, name="view_cred"),
    path("delete_cred", views.delete_cred_web, name="delete_cred"),
    path("list_history",views.list_history,name="list_history"),
    path("delete_history/<int:his_id>", views.delete_history, name="delete_history"),
    path("permission",views.perk,name="permission"),
    
    
]