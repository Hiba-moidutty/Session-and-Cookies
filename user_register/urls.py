from django.urls import path
from .import views

"""first URLS for LOGIN part"""
"""second URLS for ADMIN part"""

urlpatterns = [
    # path('admin/', admin.site.urls),

    path('',views.login_user,name='login'),
    path('home_user/',views.home_user,name = 'home_user'),
    path('sign_up/',views.signup_user,name='sign_up'),
    path('logout/',views.logout_user,name='logout'),


    path('admin_login/',views.admin_login,name='admin_login'),
    path('admin_home/',views.admin_home,name='admin_home'),
    path('admin_user_delete/<int:id>/',views.admin_user_delete,name='admin_user_delete'),
    path('admin_add_user/',views.admin_add_user,name='admin_add_user'),
    path('update_user/<int:id>/',views.update_user,name='update_user'),
    path('admin_logout/',views.admin_logout,name='admin_logout'),
    path('admin_search/',views.admin_search,name='admin_search')
]
