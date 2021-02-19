from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns


from . import views

app_name = 'myapp'

urlpatterns = [

    path('login', views.LoginView.as_view(), name='login'),
    path('special-login', views.SpecialLoginView.as_view(), name='special-login'),

    path('users/<slug:pk>', views.UserDetailView.as_view(), name='user_detail'),
    path('judges/<slug:pk>', views.JudgeDetailView.as_view(), name='judge_detail'),
    path('reporters/<slug:pk>', views.ReporterDetailView.as_view(), name='reporter_detail'),

    path('owners', views.OwnerListView.as_view(), name='owners_list'),
    path('owners/<int:pk>', views.OwnerDetailView.as_view(), name='owner_detail'),

    path('subcontract', views.NewSubcontractView.as_view(), name='new_subcontract'),
    path('subcontracts/<int:pk>', views.SubcontractDetailView.as_view(), name='subcontract_detail'),

    path('contract', views.NewContractView.as_view(), name='new_contract'),
    path('contracts', views.ContractListView.as_view(), name='contracts_list'),
    path('contracts/<int:pk>', views.ContractDetailView.as_view(), name='contract_detail'),


    path('report', views.ReportView.as_view(), name='report'),
    path('ajax/get_judge_name', views.get_judge_name, name='get_judge_name'),

]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
