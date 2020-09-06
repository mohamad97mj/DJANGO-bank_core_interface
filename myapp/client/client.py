import requests
from myapp.models import *
from myapp.serializers import *
from django.http import HttpResponse, HttpResponseRedirect, Http404

CORE_URL = "http://localhost:8080"
CONNECTION_ERROR_MESSAGE = "ارتباط با سرور قطع است لطفا بعدا امتحان کنید!"


def raise_connection_error():
    raise ConnectionError(CONNECTION_ERROR_MESSAGE)


def get_objects(url, object_class, serializer_class):
    objects = []
    try:
        r = requests.get(url.format(CORE_URL))
        json = r.json()
        if json:
            for j in json:
                object_serializer = serializer_class(data=j)
                is_valid = object_serializer.is_valid()
                if is_valid:
                    object_instance = object_class(j)
                    objects.append(object_instance)
        return objects

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise ConnectionError("ارتباط با سرور قطع است لطفا بعدا امتحان کنید!")


def get_object(url, object_class, serializer_class, raise_error=False):
    try:
        r = requests.get(url.format(CORE_URL))
        json = r.json()
        if r.status_code != 404 and json:
            object_serializer = serializer_class(data=json)
            is_valid = object_serializer.is_valid()
            if is_valid:
                object_instance = object_class(json)
                return object_instance
            else:
                raise ValueError("Serializer is not valid")
        else:
            if raise_error:
                raise Http404
            else:
                return None

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise_connection_error()


def get_user(national_code, raise_error=False):
    url = "{}/api/users/{}".format("{}", national_code)
    return get_object(url, UserProfile, UserSerializer, raise_error)


def get_owner(bank_account_id, raise_error=False):
    url = "{}/api/owners/{}".format("{}", bank_account_id)
    return get_object(url, Owner, OwnerSerializer, raise_error)


def get_judge(national_id, raise_error=False):
    url = "{}/api/judges/{}".format("{}", national_id)
    return get_object(url, JudgeProfile, JudgeSerializer, raise_error)


def get_user_owners(user_national_code, raise_error=False):
    url = "{}/api/users/{}/owners".format("{}", user_national_code)
    return get_objects(url, Owner, OwnerSerializer)


def get_user_owner(user_national_code, owner_bank_account_id, raise_error=False):
    url = "{}/api/users/{}/owners/{}".format("{}", user_national_code, owner_bank_account_id)
    return get_object(url, Owner, OwnerSerializer, raise_error)


def get_user_owner_in_normal_contracts(user_national_code, owner_bank_account_id, raise_error=False):
    url = "{}/api/users/{}/owners/{}/innormalcontracts".format("{}", user_national_code, owner_bank_account_id)
    return get_objects(url, NormalContract, NormalContractSerializer)


def get_user_owner_out_normal_contracts(user_national_code, owner_bank_account_id, raise_error=False):
    url = "{}/api/users/{}/owners/{}/outnormalcontracts".format("{}", user_national_code, owner_bank_account_id)
    return get_objects(url, NormalContract, NormalContractSerializer)


def get_user_owner_in_normal_contract(user_national_code, owner_bank_account_id, contract_id, raise_error=False):
    url = "{}/api/users/{}/owners/{}/innormalcontracts/{}".format("{}", user_national_code, owner_bank_account_id,
                                                                  contract_id)
    return get_object(url, NormalContract, NormalContractSerializer, raise_error)


def get_user_owner_out_normal_contract(user_national_code, owner_bank_account_id, contract_id, raise_error=False):
    url = "{}/api/users/{}/owners/{}/outnormalcontracts/{}".format("{}", user_national_code, owner_bank_account_id,
                                                                   contract_id)
    return get_object(url, NormalContract, NormalContractSerializer, raise_error)


def get_user_owner_in_subcontracts(user_national_code, owner_bank_account_id):
    url = "{}/api/users/{}/owners/{}/insubcontracts".format("{}", user_national_code, owner_bank_account_id)
    return get_objects(url, Subcontract, SubcontractSerializer)


def get_user_owner_in_subcontract(user_national_code, owner_bank_account_id, contract_id, raise_error=False):
    url = "{}/api/users/{}/owners/{}/insubcontracts/{}".format("{}", user_national_code, owner_bank_account_id,
                                                               contract_id)
    return get_object(url, Subcontract, SubcontractSerializer)


def get_user_owner_in_normal_contract_subcontracts(user_national_code, owner_bank_account_id, normal_contract_id, ):
    url = "{}/api/users/{}/owners/{}/innormalcontracts/{}/subcontracts".format("{}", user_national_code,
                                                                               owner_bank_account_id,
                                                                               normal_contract_id)
    return get_objects(url, Subcontract, SubcontractSerializer)


def get_user_owner_in_normal_contract_subcontract(user_national_code, owner_bank_account_id, normal_contract_id,
                                                  subcontract_id,
                                                  raise_error=False):
    url = "{}/api/users/{}/owners/{}/innormalcontracts/{}/subcontracts/{}".format("{}", user_national_code,
                                                                                  owner_bank_account_id,
                                                                                  normal_contract_id, subcontract_id)
    return get_object(url, Subcontract, SubcontractSerializer, raise_error)


# post ...............................................................................

def post_object(url, object_instance, serializer_class):
    try:
        object_serializer = serializer_class(data=object_instance.__dict__)
        is_valid = object_serializer.is_valid()
        if is_valid:
            r = requests.post(url.format(CORE_URL), json=object_serializer.data)
            json = r.json()
            return object_instance.__class__(json)
        raise TypeError("serializer error!")
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise_connection_error()


def post_normal_contract(normal_contract):
    url = "{}/api/normalcontracts"
    return post_object(url, normal_contract, NormalContractSerializer)


# put ...............................................................................

def put_object(url, object_instance, serializer_class):
    try:
        object_serializer = serializer_class(data=object_instance.__dict__)
        is_valid = object_serializer.is_valid()
        if is_valid:
            r = requests.put(url.format(CORE_URL), json=object_serializer.data)
            json = r.json()
            return object_instance.__class__(json)
        raise TypeError("serializer error!")
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise_connection_error()


def put_user_owner_in_normal_contract(user_national_code, owner_bank_account_id, normal_contract_id, normal_contract):
    url = "{}/api/users/{}/owners/{}/innormalcontracts/{}".format("{}", user_national_code, owner_bank_account_id,
                                                                  normal_contract_id)
    return put_object(url, normal_contract, NormalContractSerializer)


def put_user_owner_out_normal_contract(user_national_code, owner_bank_account_id, normal_contract_id, normal_contract):
    url = "{}/api/users/{}/owners/{}/outnormalcontracts/{}".format("{}", user_national_code, owner_bank_account_id,
                                                                   normal_contract_id)
    return put_object(url, normal_contract, NormalContractSerializer)


def put_user_owner_in_subcontract(user_national_code, owner_bank_account_id, subcontract_id, subcontract):
    url = "{}/api/users/{}/owners/{}/insubcontracts/{}".format("{}", user_national_code, owner_bank_account_id,
                                                               subcontract_id)
    return put_object(url, subcontract, SubcontractSerializer)


def put_user_owner_in_normal_contract_subcontract(user_national_code, owner_bank_account_id, normal_contract_id,
                                                  subcontract_id, subcontract):
    url = "{}/api/users/{}/owners/{}/innormalcontracts/{}/subcontracts/{}".format("{}", user_national_code,
                                                                                  owner_bank_account_id,
                                                                                  normal_contract_id,
                                                                                  subcontract_id)
    return put_object(url, subcontract, SubcontractSerializer)


def put_json(url, payload, object_class, raise_error=False):
    try:
        r = requests.put(url.format(CORE_URL), json=payload)
        json = r.json()
        if r.status_code != 404 and json:
            return object_class(json)
        else:
            if raise_error:
                raise Http404
            else:
                return None
    except requests.exceptions.RequestException as e:
        raise_connection_error()


def charge_user_owner_out_normal_contract(contract_id, operator_national_code, owner_bank_account_id, operator_type):
    url = "{}/api/users/{}/owners/{}/outnormalcontracts/{}/charge".format("{}", operator_national_code,
                                                                          owner_bank_account_id, contract_id)
    payload = {
        "operator_type": operator_type,
    }
    return put_json(url, payload, NormalContract)


def pay_user_owner_normal_contract(contract_id, operator_national_code, owner_bank_account_id, operator_type):
    url = "{}/api/users/{}/owners/{}/innormalcontracts/{}/pay".format("{}", contract_id, operator_national_code,
                                                                      owner_bank_account_id)
    payload = {
        "operator_type": operator_type,
    }
    return put_json(url, payload, NormalContract)
