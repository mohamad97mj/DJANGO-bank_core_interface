import requests
from myapp.models import *
from myapp.serializers import *
from django.http import HttpResponse, HttpResponseRedirect
from myapp.client.exceptions import *

CORE_URL = "http://localhost:8080"


def raise_connection_error():
    CONNECTION_ERROR_MESSAGE = "Server Is Down!"
    raise ConnectionError(CONNECTION_ERROR_MESSAGE)


def raise_http_error(status_code, message=None):
    if status_code == 400:
        raise Http400("Bad Request", message)
    elif status_code == 404:
        raise Http404("Page Not Found", message)
    else:
        raise Http500("Internal Server Error", message)


def get_objects(url, object_class, serializer_class):
    objects = []
    try:
        r = requests.get(url.format(CORE_URL))
        if r.status_code == 200:
            json = r.json()
            for j in json:
                object_serializer = serializer_class(data=j)
                is_valid = object_serializer.is_valid()
                if is_valid:
                    object_instance = object_class(j)
                    objects.append(object_instance)
                else:
                    raise ValueError("Serializer is not valid")
            return objects
        else:
            return raise_http_error(r.status_code, r.text)

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise_connection_error()


def get_object(url, object_class, serializer_class, raise_error=False):
    try:
        r = requests.get(url.format(CORE_URL))
        if r.status_code == 200:
            json = r.json()
            object_serializer = serializer_class(data=json)
            is_valid = object_serializer.is_valid()
            if is_valid:
                object_instance = object_class(json)
                return object_instance
            else:
                raise ValueError("Serializer is not valid")
        else:
            if raise_error:
                raise_http_error(r.status_code, r.text)
            else:
                return None

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise_connection_error()


def get_user(national_code, raise_error=False):
    url = "{}/api/users/{}".format("{}", national_code)
    return get_object(url, UserProfile, UserSerializer, raise_error)


def get_public_owner(bank_account_id, raise_error=False):
    url = "{}/api/publicowners/{}".format("{}", bank_account_id)
    return get_object(url, Owner, OwnerSerializer, raise_error)


def get_operational_owner(owner_type, raise_error=False):
    url = "{}/api/operationalowners/{}".format("{}", owner_type)
    return get_object(url, Owner, OwnerSerializer, raise_error)


def get_judge(national_id, raise_error=False):
    url = "{}/api/judges/{}".format("{}", national_id)
    return get_object(url, JudgeProfile, JudgeSerializer, raise_error)


def get_reporter(reporter_id, raise_error=False):
    url = "{}/api/reporters/{}".format("{}", reporter_id)
    return get_object(url, ReporterProfile, ReporterSerializer, raise_error)


def get_normal_contract(normal_contract_id, raise_error=False):
    url = "{}/api/normalcontracts/{}".format("{}", normal_contract_id)
    return get_object(url, NormalContract, NormalContractSerializer, raise_error)


def get_user_public_owners(user_national_code, raise_error=False):
    url = "{}/api/users/{}/publicowners".format("{}", user_national_code)
    return get_objects(url, Owner, OwnerSerializer)


def get_user_public_owner(user_national_code, owner_bank_account_id, raise_error=False):
    url = "{}/api/users/{}/publicowners/{}".format("{}", user_national_code, owner_bank_account_id)
    return get_object(url, Owner, OwnerSerializer, raise_error)


def get_user_public_owner_in_normal_contracts(user_national_code, owner_bank_account_id):
    url = "{}/api/users/{}/publicowners/{}/innormalcontracts".format("{}",
                                                                     user_national_code,
                                                                     owner_bank_account_id)
    return get_objects(url, NormalContract, NormalContractSerializer)


def get_user_public_owner_out_normal_contracts(user_national_code, owner_bank_account_id):
    url = "{}/api/users/{}/publicowners/{}/outnormalcontracts".format("{}",
                                                                      user_national_code,
                                                                      owner_bank_account_id)
    return get_objects(url, NormalContract, NormalContractSerializer)


def get_user_public_owner_in_normal_contract(user_national_code,
                                             owner_bank_account_id,
                                             contract_id,
                                             raise_error=False):
    url = "{}/api/users/{}/publicowners/{}/innormalcontracts/{}".format("{}",
                                                                        user_national_code,
                                                                        owner_bank_account_id,
                                                                        contract_id)
    return get_object(url, NormalContract, NormalContractSerializer, raise_error)


def get_user_public_owner_out_normal_contract(user_national_code,
                                              owner_bank_account_id,
                                              contract_id,
                                              raise_error=False):
    url = "{}/api/users/{}/publicowners/{}/outnormalcontracts/{}".format("{}",
                                                                         user_national_code,
                                                                         owner_bank_account_id,
                                                                         contract_id)
    return get_object(url, NormalContract, NormalContractSerializer, raise_error)


def get_user_public_owner_in_subcontracts(user_national_code, owner_bank_account_id):
    url = "{}/api/users/{}/publicowners/{}/insubcontracts".format("{}",
                                                                  user_national_code,
                                                                  owner_bank_account_id)
    return get_objects(url, Subcontract, SubcontractSerializer)


def get_user_public_owner_in_subcontract(user_national_code,
                                         owner_bank_account_id,
                                         contract_id, raise_error=False):
    url = "{}/api/users/{}/publicowners/{}/insubcontracts/{}".format("{}",
                                                                     user_national_code,
                                                                     owner_bank_account_id,
                                                                     contract_id)
    return get_object(url, Subcontract, SubcontractSerializer, raise_error)


def get_user_public_owner_in_normal_contract_subcontracts(user_national_code,
                                                          owner_bank_account_id,
                                                          normal_contract_id):
    url = "{}/api/users/{}/publicowners/{}/innormalcontracts/{}/subcontracts".format("{}",
                                                                                     user_national_code,
                                                                                     owner_bank_account_id,
                                                                                     normal_contract_id)
    return get_objects(url, Subcontract, SubcontractSerializer)


def get_user_public_owner_in_normal_contract_subcontract(user_national_code,
                                                         owner_bank_account_id,
                                                         normal_contract_id,
                                                         subcontract_id,
                                                         raise_error=False):
    url = "{}/api/users/{}/publicowners/{}/innormalcontracts/{}/subcontracts/{}".format("{}",
                                                                                        user_national_code,
                                                                                        owner_bank_account_id,
                                                                                        normal_contract_id,
                                                                                        subcontract_id)
    return get_object(url, Subcontract, SubcontractSerializer, raise_error)


# post ...............................................................................

def post_object(url, object_instance, serializer_class):
    try:
        object_serializer = serializer_class(data=object_instance.__dict__)
        is_valid = object_serializer.is_valid()
        if is_valid:
            r = requests.post(url.format(CORE_URL), json=object_serializer.data)
            if r.status_code == 200:
                json = r.json()
                return object_instance.__class__(json)
            else:
                raise_http_error(r.status_code, r.text)

        else:
            raise TypeError("serializer error!")
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise_connection_error()


def post_user_public_owner_normal_contract(user_national_code, owner_bank_account_id, normal_contract):
    url = "{}/api/users/{}/publicowners/{}/outnormalcontracts".format("{}", user_national_code, owner_bank_account_id)
    return post_object(url, normal_contract, NormalContractSerializer)


def post_user_public_owner_subcontract(user_national_code, owner_bank_account_id, normal_contract_id, subcontract):
    url = "{}/api/users/{}/publicowners/{}/innormalcontracts/{}/subcontracts".format("{}",
                                                                                     user_national_code,
                                                                                     owner_bank_account_id,
                                                                                     normal_contract_id)
    return post_object(url, subcontract, SubcontractSerializer)


# put ...............................................................................

def put_object(url, object_instance, serializer_class):
    try:
        object_serializer = serializer_class(data=object_instance.__dict__)
        is_valid = object_serializer.is_valid()
        if is_valid:
            r = requests.put(url.format(CORE_URL), json=object_serializer.data)
            if r.status_code == 200:
                json = r.json()
                return object_instance.__class__(json)
            else:
                raise_http_error(r.status_code, r.text)

        else:
            raise TypeError("serializer error!")
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise_connection_error()


def put_user_public_owner_in_normal_contract(user_national_code, owner_bank_account_id, normal_contract_id,
                                             normal_contract):
    url = "{}/api/users/{}/publicowners/{}/innormalcontracts/{}".format("{}",
                                                                        user_national_code,
                                                                        owner_bank_account_id,
                                                                        normal_contract_id)
    return put_object(url, normal_contract, NormalContractSerializer)


def put_user_public_owner_out_normal_contract(user_national_code, owner_bank_account_id, normal_contract_id,
                                              normal_contract):
    url = "{}/api/users/{}/publicowners/{}/outnormalcontracts/{}".format("{}",
                                                                         user_national_code,
                                                                         owner_bank_account_id,
                                                                         normal_contract_id)
    return put_object(url, normal_contract, NormalContractSerializer)


def put_user_owner_in_subcontract(user_national_code, owner_bank_account_id, subcontract_id, subcontract):
    url = "{}/api/users/{}/publicowners/{}/insubcontracts/{}".format("{}",
                                                                     user_national_code,
                                                                     owner_bank_account_id,
                                                                     subcontract_id)
    return put_object(url, subcontract, SubcontractSerializer)


def put_user_public_owner_in_normal_contract_subcontract(user_national_code, owner_bank_account_id, normal_contract_id,
                                                         subcontract_id, subcontract):
    url = "{}/api/users/{}/publicowners/{}/innormalcontracts/{}/subcontracts/{}".format("{}",
                                                                                        user_national_code,
                                                                                        owner_bank_account_id,
                                                                                        normal_contract_id,
                                                                                        subcontract_id)
    return put_object(url, subcontract, SubcontractSerializer)


def put_json(url, payload, object_class):
    try:
        r = requests.put(url.format(CORE_URL), json=payload)
        if r.status_code == 200:
            return object_class(r.json())
        else:
            raise_http_error(r.status_code, r.text)
    except requests.exceptions.RequestException as e:
        raise_connection_error()


def charge_user_public_owner_out_normal_contract(operator_national_code, owner_bank_account_id, contract_id,
                                                 operator_type):
    url = "{}/api/users/{}/publicowners/{}/outnormalcontracts/{}/charge".format("{}",
                                                                                operator_national_code,
                                                                                owner_bank_account_id,
                                                                                contract_id)
    payload = {
        "operator_type": operator_type,
    }
    return put_json(url, payload, NormalContract)


def claim_user_public_owner_out_normal_contract(operator_national_code,
                                                owner_bank_account_id,
                                                normal_contract_id,
                                                operator_type):
    url = "{}/api/users/{}/publicowners/{}/outnormalcontracts/{}/claim".format("{}",
                                                                               operator_national_code,
                                                                               owner_bank_account_id,
                                                                               normal_contract_id)
    payload = {
        "operator_type": operator_type,
    }
    return put_json(url, payload, NormalContract)


def pay_user_owner_public_in_normal_contract_subcontract(operator_national_code,
                                                         owner_bank_account_id,
                                                         normal_contract_id,
                                                         subcontract_id,
                                                         operator_type):
    url = "{}/api/users/{}/publicowners/{}/innormalcontracts/{}/subcontracts/{}/pay".format("{}",
                                                                                            operator_national_code,
                                                                                            owner_bank_account_id,
                                                                                            normal_contract_id,
                                                                                            subcontract_id)
    payload = {
        "operator_type": operator_type,
    }
    return put_json(url, payload, Subcontract)


def get_judged_normal_contracts(judge_national_id):
    url = "{}/api/judges/{}/judgednormalcontracts".format("{}", judge_national_id)
    return get_objects(url, NormalContract, NormalContractSerializer)


def get_not_judged_normal_contracts(judge_national_id):
    url = "{}/api/judges/{}/notjudgednormalcontracts".format("{}", judge_national_id)
    return get_objects(url, NormalContract, NormalContractSerializer)


def get_judged_normal_contract(judge_national_id, normal_contract_id, raise_error=False):
    url = "{}/api/judges/{}/judgednormalcontracts/{}".format("{}", judge_national_id, normal_contract_id)
    return get_object(url, NormalContract, NormalContractSerializer, raise_error)


def get_not_judged_normal_contract(judge_national_id, normal_contract_id, raise_error=False):
    url = "{}/api/judges/{}/notjudgednormalcontracts/{}".format("{}", judge_national_id, normal_contract_id)
    return get_object(url, NormalContract, NormalContractSerializer, raise_error)


def get_judged_normal_contract_subcontracts(judge_national_id, normal_contract_id):
    url = "{}/api/judges/{}/judgednormalcontracts/{}/subcontracts".format("{}", judge_national_id, normal_contract_id)
    return get_objects(url, Subcontract, SubcontractSerializer)


def get_not_judged_normal_contracts_judged_subcontracts(judge_national_id, normal_contract_id):
    url = "{}/api/judges/{}/notjudgednormalcontracts/{}/judgedsubcontracts".format("{}",
                                                                                   judge_national_id,
                                                                                   normal_contract_id)
    return get_objects(url, Subcontract, SubcontractSerializer)


def get_not_judged_normal_contracts_not_judged_subcontracts(judge_national_id, normal_contract_id):
    url = "{}/api/judges/{}/notjudgednormalcontracts/{}/notjudgedsubcontracts".format("{}",
                                                                                      judge_national_id,
                                                                                      normal_contract_id)
    return get_objects(url, Subcontract, SubcontractSerializer)


def get_judge_normal_contract_subcontract(judge_national_id, normal_contract_id, subcontract_id, raise_error=False):
    url = "{}/api/judges/{}/normalcontracts/{}/subcontracts/{}".format("{}",
                                                                       judge_national_id,
                                                                       normal_contract_id,
                                                                       subcontract_id)
    return get_object(url, Subcontract, SubcontractSerializer, raise_error)


def judge_subcontract(judge_national_id, normal_contract_id, subcontract_id, operator_type, judge_vote):
    url = "{}/api/judges/{}/normalcontracts/{}/subcontracts/{}/judge".format("{}", judge_national_id,
                                                                             normal_contract_id,
                                                                             subcontract_id)
    payload = {
        "operator_type": operator_type,
        "judge_vote": judge_vote,
    }
    return put_json(url, payload, Subcontract)


def get_operational_owner_in_external_transactions(owner_type):
    url = '{}/api/operationalowners/{}/inexternaltransactions'.format("{}", owner_type)
    return get_objects(url, Transaction, TransactionSerializer)


def get_operational_owner_out_external_transactions(owner_type):
    url = '{}/api/operationalowners/{}/outexternaltransactions'.format("{}", owner_type)
    return get_objects(url, Transaction, TransactionSerializer)


def get_operational_owner_in_external_transactions_time_interval(owner_type, from_date, to_date):
    url = '{}/api/operationalowners/{}/inexternaltransactions/timeinterval?from={}&to={}'.format("{}",
                                                                                                 owner_type,
                                                                                                 from_date,
                                                                                                 to_date)
    return get_objects(url, Transaction, TransactionSerializer)


def get_operational_owner_out_external_transactions_time_interval(owner_type, from_date, to_date):
    url = '{}/api/operationalowners/{}/outexternaltransactions/timeinterval?from={}&to={}'.format("{}",
                                                                                                  owner_type,
                                                                                                  from_date,
                                                                                                  to_date)
    return get_objects(url, Transaction, TransactionSerializer)
