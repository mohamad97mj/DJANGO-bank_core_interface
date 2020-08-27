import requests
from myapp.models import *
from myapp.serializers import *

CORE_URL = "http://localhost:8080"
CONNECTION_ERROR_MESSAGE = "ارتباط با سرور قطع است لطفا بعدا امتحان کنید!"


def raise_connection_error():
    raise ConnectionError(CONNECTION_ERROR_MESSAGE)


def send_get_request(url):
    try:
        r = requests.get(url)
        return r.json()
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise_connection_error()


def get_objects(url, path_var, object_class, serializer_class):
    objects = []
    try:
        r = requests.get(url.format(CORE_URL, path_var))
        if r.json():
            for j in r.json():
                object_serializer = serializer_class(data=j)
                is_valid = object_serializer.is_valid()
                if is_valid:
                    object_instance = object_class(j)
                    objects.append(object_instance)
        return objects

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise ConnectionError("ارتباط با سرور قطع است لطفا بعدا امتحان کنید!")


def get_object(url, path_var, object_class, serializer_class):
    object_instance = None
    try:
        r = requests.get(url.format(CORE_URL, path_var))
        json = r.json()
        if json:
            object_serializer = serializer_class(data=json)
            is_valid = object_serializer.is_valid()
            if is_valid:
                object_instance = object_class(json)
        return object_instance

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise ConnectionError("ارتباط با سرور قطع است لطفا بعدا امتحان کنید!")


def get_user_owners(user_national_code):
    url = "{}/api/users/{}/owners"
    return get_objects(url, user_national_code, Owner, OwnerSerializer)


def get_owner_normal_contracts(owner_bank_account_id):
    url = "{}/api/owners/{}/contracts"
    return get_objects(url, owner_bank_account_id, NormalContract, NormalContractSerializer)


def get_owner_subcontracts(owner_bank_account_id):
    url = "{}/api/owners/{}/contracts"
    return get_objects(url, owner_bank_account_id, Subcontract, SubcontractSerializer)


def get_owner_transactions(owner_bank_account_id):
    url = "{}/api/owners/{}/transactions"
    return get_objects(url, owner_bank_account_id, Transaction, TransactionSerializer)


def get_owner(bank_account_id):
    url = "{}/api/owners/{}"
    return get_object(url, bank_account_id, Owner, OwnerSerializer)


def get_user(national_code):
    url = "{}/api/users/{}"
    return get_object(url, national_code, UserProfile, UserSerializer)


def get_normal_contract(contract_id):
    url = "{}/api/normalcontracts/{}"
    return get_object(url, contract_id, NormalContract, NormalContractSerializer)


def get_subcontract(contract_id):
    url = "{}/api/subcontracts/{}"
    return get_object(url, contract_id, Subcontract, SubcontractSerializer)


def get_judge(national_id):
    url = "{}/api/judges/{}"
    return get_object(url, national_id, JudgeProfile, JudgeSerializer)
