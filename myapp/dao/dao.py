def load_owner(pk):
    try:
        return Owner.objects.get(pk=pk)
    except Owner.DoesNotExist:
        raise Http404


def load_user(pk):
    try:
        return UserProfile.objects.get(pk=pk)
    except UserProfile.DoesNotExist:
        raise Http404


def load_judge(pk):
    try:
        return JudgeProfile.objects.get(pk=pk)
    except JudgeProfile.DoesNotExist:
        raise Http404


def load_contract(pk):
    try:
        return NormalContract.objects.get(pk=pk)
    except NormalContract.DoesNotExist:
        raise Http404


def load_subcontract(pk):
    try:
        return Subcontract.objects.get(pk=pk)
    except Subcontract.DoesNotExist:
        raise Http404


def load_transaction(pk):
    try:
        return Transaction.objects.get(pk=pk)
    except Transaction.DoesNotExist:
        raise Http404
