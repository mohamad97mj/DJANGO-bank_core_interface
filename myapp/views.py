from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import renderers
from . import models
from . import forms
from . import serializers
from django.db.models import Q


# Create your views here.

class LoginView(APIView):

    def get(self, request):
        login_form = forms.LoginForm()
        context = {'login_form': login_form}
        return render(request, 'myapp/login.html', context)

    def post(self, request):
        print("post request received")

        login_form = forms.LoginForm(request.data)
        if login_form.is_valid():
            if request.data['role'] == 'user':
                print(request.data)
                return redirect('myapp:user_detail', pk=request.data['username'])
            else:
                return redirect('myapp:judge_detail', pk=request.data['username'])

        context = {'login_form': login_form}
        return render(request, 'myapp/login.html', context)


class UserDetailView(APIView):
    renderer_classes = [renderers.TemplateHTMLRenderer]

    def get_object(self, pk):
        try:
            return models.UserProfile.objects.get(pk=pk)
        except models.UserProfile.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user_profile = self.get_object(pk)
        user_profile_form = forms.UserProfileForm(instance=user_profile)
        context = {'pk': pk, 'user_profile_form': user_profile_form}
        return Response(context, template_name='myapp/user-profile.html')


class UserListView(generics.ListAPIView):
    queryset = models.UserProfile.objects.all()
    serializer_class = serializers.UserSerializer
    pass


class JudgeDetailView(APIView):
    renderer_classes = [renderers.TemplateHTMLRenderer]

    def get_object(self, pk):
        try:
            return models.JudgeProfile.objects.get(pk=pk)
        except models.JudgeProfile.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        judge_profile = self.get_object(pk)
        judge_profile_form = forms.JudgeProfileForm(instance=judge_profile)
        context = {'judge_profile_form': judge_profile_form}
        return Response(context, template_name='myapp/judge-profile.html')


class JudgeListView(generics.ListAPIView):
    queryset = models.JudgeProfile.objects.all()
    serializer_class = serializers.JudgeSerializer
    pass


# owner views ......................................................................................

# class OwnerDetailView(APIView):
#     renderer_classes = [renderers.TemplateHTMLRenderer]
#
#     def get_object(self, pk):
#         try:
#             return models.Owner.objects.get(pk=pk)
#         except models.Owner.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         owner = self.get_object(pk)
#         owner_detail_form = forms.OwnerDetailForm(instance=owner)
#         context = {'owner_detail_form': owner_detail_form}
#         return Response(context, template_name='myapp/owner-detail.html')


class OwnerListView(generics.ListAPIView):
    queryset = models.Owner.objects.all()
    serializer_class = serializers.OwnerSerializer
    pass


class UserOwnersListView(APIView):
    renderer_classes = [renderers.TemplateHTMLRenderer]
    template_name = 'myapp/user-accounts-list.html'

    def get_object(self, pk):
        try:
            return models.UserProfile.objects.get(pk=pk)
        except models.UserProfile.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user_profile = self.get_object(pk)
        accounts = user_profile.owners.all()
        return Response({"pk": pk, "accounts": accounts})


class UserOwnerDetailView(APIView):
    renderer_classes = [renderers.TemplateHTMLRenderer]
    template_name = 'myapp/user-account-detail.html'

    def get_object(self, pk):
        try:
            return models.UserProfile.objects.get(pk=pk)
        except models.UserProfile.DoesNotExist:
            raise Http404

    def get_owner(self, pk):
        try:
            return models.Owner.objects.get(pk=pk)
        except models.Owner.DoesNotExist:
            raise Http404

    def get_contracts_list(self, instance):
        queryset = models.Contract.objects.filter(
            Q(src_owner=instance.bank_account_id) | Q(dst_owner=instance.bank_account_id))

        return queryset

    def get_transactions_list(self, instance):
        queryset = models.Transaction.objects.filter(
            Q(owner=instance.bank_account_id) | Q(otherside_owner=instance.bank_account_id))

        return queryset

    def get(self, request, pk, pk2, format=None):
        # user_profile = self.get_object(pk)
        owner = self.get_owner(pk2)
        print(owner)
        contracts = self.get_contracts_list(owner)
        transactions = self.get_transactions_list(owner)
        return Response({"pk": pk, 'pk2': pk2, "contracts": contracts, 'transactions': transactions})


# Contract views ......................................................................................

class ContractDetailView(APIView):
    renderer_classes = [renderers.TemplateHTMLRenderer]

    def get_object(self, pk):
        try:
            return models.Contract.objects.get(pk=pk)
        except models.Contract.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        contract = self.get_object(pk)
        contract_detail_form = forms.ContractDetailForm(instance=contract)
        context = {'contract_detail_form': contract_detail_form}
        return Response(context, template_name='myapp/contract-detail.html')


class ContractListView(generics.ListAPIView):
    queryset = models.Contract.objects.all()
    serializer_class = serializers.ContractSerializer
    pass


class NewContractView(APIView):
    renderer_classes = [renderers.TemplateHTMLRenderer]

    def get(self, request, format=None):
        new_contract_form = forms.NewContractForm()
        context = {'new_contract_form': new_contract_form}
        return Response(context, template_name='myapp/new-contract.html')

    # TODO define post method


class UserContractsListView(APIView):
    renderer_classes = [renderers.TemplateHTMLRenderer]
    template_name = 'myapp/user-contracts-list.html'

    def get_object(self, pk):
        try:
            return models.UserProfile.objects.get(pk=pk)
        except models.UserProfile.DoesNotExist:
            raise Http404

    def get_list(self, instance):
        queryset = models.Contract.objects.none()
        for owner in instance.owners.all():
            queryset = queryset | models.Contract.objects.filter(
                Q(dst_owner=owner.bank_account_id) | Q(src_owner=owner.bank_account_id))

        return queryset

    def get(self, request, pk, format=None):
        user_profile = self.get_object(pk)
        contracts = self.get_list(instance=user_profile)
        return Response({"pk": pk, "contracts": contracts})

    # Subcontract views ......................................................................................


class SubcontractDetailView(APIView):
    renderer_classes = [renderers.TemplateHTMLRenderer]

    def get_object(self, pk):
        try:
            return models.Subcontract.objects.get(pk=pk)
        except models.Subcontract.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        subcontract = self.get_object(pk)
        subcontract_detail_form = forms.SubcontractDetailForm(instance=subcontract)
        context = {'subcontract_detail_form': subcontract_detail_form}
        return Response(context, template_name='myapp/subcontract-detail.html')


class SubcontractListView(generics.ListAPIView):
    queryset = models.Subcontract.objects.all()
    serializer_class = serializers.SubcontractSerializer
    pass


class NewSubcontractView(APIView):
    renderer_classes = [renderers.TemplateHTMLRenderer]

    def get(self, request, format=None):
        new_subcontract_form = forms.NewSubcontractForm()
        context = {'new_subcontract_form': new_subcontract_form}
        return Response(context, template_name='myapp/new-subcontract.html')

    # TODO define post method


# transaction views ......................................................................................

class TransactionDetailView(APIView):
    renderer_classes = [renderers.TemplateHTMLRenderer]

    def get_object(self, pk):
        try:
            return models.Transaction.objects.get(pk=pk)
        except models.Transaction.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        transaction = self.get_object(pk)
        transaction_detail_form = forms.TransactionDetailForm(instance=transaction)
        context = {'transaction_detail_form': transaction_detail_form}
        return Response(context, template_name='myapp/transaction-detail.html')


class UserTransactionsListView(APIView):
    renderer_classes = [renderers.TemplateHTMLRenderer]
    template_name = 'myapp/user-transactions-list.html'

    def get_object(self, pk):
        try:
            return models.UserProfile.objects.get(pk=pk)
        except models.UserProfile.DoesNotExist:
            raise Http404

    def get_list(self, instance):
        queryset = models.Transaction.objects.none()
        for owner in instance.owners.all():
            queryset = queryset | models.Transaction.objects.filter(
                Q(owner=owner.bank_account_id) | Q(otherside_owner=owner.bank_account_id))

        return queryset

    def get(self, request, pk, format=None):
        user_profile = self.get_object(pk)
        transactions = self.get_list(instance=user_profile)
        return Response({'pk': pk, 'transactions': transactions})


class TransactionListView(generics.ListAPIView):
    queryset = models.Transaction.objects.all()
    serializer_class = serializers.TransactionSerializer
    pass


class NewTransactionView(APIView):
    renderer_classes = [renderers.TemplateHTMLRenderer]

    def get(self, request, format=None):
        new_transaction_form = forms.NewTransactionForm()
        context = {'new_transaction_form': new_transaction_form}
        return Response(context, template_name='myapp/new-transaction.html')

    # TODO define post method
