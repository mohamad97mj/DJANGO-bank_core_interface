from django.urls import path

from . import views

app_name = 'myapp'

urlpatterns = [
    # path('', views.index, name='index'),
    path('login', views.LoginView.as_view(), name='login'),
    path('users', views.UserListView.as_view(), name='users_list'),
    path('users/<slug:pk>', views.UserDetailView.as_view(), name='user_detail'),
    path('users/<slug:pk>/accounts', views.UserOwnersListView.as_view(), name='user-owners_list'),
    path('users/<slug:pk>/accounts/<slug:pk2>', views.UserOwnerDetailView.as_view(), name='user-owner_detail'),
    path('users/<slug:pk>/contracts', views.UserContractsListView.as_view(), name='user-contracts_list'),
    path('users/<slug:pk>/transactions', views.UserTransactionsListView.as_view(), name='user-transactions_list'),
    path('judges', views.JudgeListView.as_view(), name='judges_list'),
    path('judges/<slug:pk>', views.JudgeDetailView.as_view(), name='judge_detail'),
    path('contract', views.NewContractView.as_view(), name='new_contract'),
    path('contracts', views.ContractListView.as_view(), name='contracts_list'),
    path('contracts/<int:pk>', views.ContractDetailView.as_view(), name='contract_detail'),
    path('subcontract', views.NewSubcontractView.as_view(), name='new_subcontract'),
    path('subcontracts', views.SubcontractListView.as_view(), name='subcontracts_list'),
    path('subcontracts/<int:pk>', views.SubcontractDetailView.as_view(), name='subcontract_detail'),
    path('transaction', views.NewTransactionView.as_view(), name='new_transaction'),
    path('transactions', views.TransactionListView.as_view(), name='transactions_list'),
    path('transactions/<int:pk>', views.TransactionDetailView.as_view(), name='transaction_detail'),
]
