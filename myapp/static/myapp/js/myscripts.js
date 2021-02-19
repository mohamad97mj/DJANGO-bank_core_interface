const thousands_separator = (id) => {
    let value = $('#' + id).val()
    let without_commas = value.replaceAll(',', "")
    let with_comas = without_commas.replace(/\D/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, ",")
    $('#' + id).val(with_comas)
}


const translate_currency = (eng_currency) => {

    const currencies = {
        'DOLLAR': 'دلار',
        'EURO': 'یورو',
        'RIAL': 'ریال',
        'RUBLE': 'روبل',
    }

    return currencies[eng_currency]
}

