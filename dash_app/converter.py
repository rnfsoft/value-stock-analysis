def number_converter(number):
    conversion = {
        'B': 1000000000,
        'M': 1000000,
        '%': 0.01
    }
    if(any(num.isalnum() for num in number)):
        number = number.replace(',', '')
    else:
        number = number.replace('-', '0') # value includes -

    if number[-1] is ')':
        number = '-' + number[1:-1] # value (0.2) to -0.2

    num_abb = number[-1] # B:Billion M:Million %:Percent 
    if num_abb in [*conversion.keys()]:
        return float(number[:-1]) * conversion[num_abb]
    else:
        return number
