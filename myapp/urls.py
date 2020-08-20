from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns


from . import views

app_name = 'myapp'

urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
    path('users', views.UserListView.as_view(), name='my_users_list'),
    path('users/<slug:pk>', views.UserDetailView.as_view(), name='my_user_detail'),
    path('users/<slug:pk>/accounts', views.UserOwnersListView.as_view(), name='owners_list'),
    # path('users/<slug:pk>/contracts', views.UserContractsListView.as_view(), name='contracts_list'),
    # path('users/<slug:pk>/transactions', views.UserTransactionsListView.as_view(), name='transactions_list'),

    path('judges', views.JudgeListView.as_view(), name='my_judges_list'),
    path('judges/<int:pk>', views.JudgeDetailView.as_view(), name='my_judge_detail'),

    path('accounts', views.MyOwnerListView.as_view(), name='my_accounts_list'),
    path('accounts/<int:pk>', views.MyOwnerDetailView.as_view(), name='my_owner_detail'),

    path('subcontract', views.MyNewSubcontractView.as_view(), name='my_new_subcontract'),
    path('subcontracts', views.MySubcontractListView.as_view(), name='my_subcontracts_list'),
    path('subcontracts/<int:pk>', views.MySubcontractDetailView.as_view(), name='my_subcontract_detail'),

    path('contract', views.MyNewContractView.as_view(), name='my_new_contract'),
    path('contracts', views.MyContractListView.as_view(), name='my_contracts_list'),
    path('contracts/<int:pk>', views.MyContractDetailView.as_view(), name='my_contract_detail'),

    path('transaction', views.MyNewTransactionView.as_view(), name='my_new_transaction'),
    path('transactions', views.MyTransactionListView.as_view(), name='my_transactions_list'),
    path('transactions/<int:pk>', views.MyTransactionDetailView.as_view(), name='my_transaction_detail'),

    # path('contracts', views.ContractListView.as_view(), name='contracts_list'),
    # path('subcontracts', views.SubcontractListView.as_view(), name='subcontracts_list'),
    # path('transactions', views.TransactionListView.as_view(), name='transactions_list'),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
