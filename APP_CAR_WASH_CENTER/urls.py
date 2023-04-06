from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views


urlpatterns = [
                path('',views.home,name="home"),
                path('base/',views.base,name="base"),
                path('Add_Timings/',views.Add_Timings,name='Add_Timings'),
                path('test1/',views.test1,name='test1'),
                path('test2/',views.test2,name='test2'),
                path('Manage_Booths/',views.Manage_Booths,name='Manage_Booths'),
                path('Simulation_dashboard/',views.Simulation_dashboard,name="Simulation_dashboard"),
                path('Add_Booths/',views.Add_Booths,name="Add_Booths"),
                path('Update_Booth/',views.Update_Booth,name='Update_Booth'),
                path('performance_booth/',views.performance_booth,name='performance_booth'),
                



]




urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)