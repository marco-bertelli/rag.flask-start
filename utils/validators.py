def validateSourceType(type):
    return type in ['qa', 'csv', 'pdf']

def validateBodyFields(body, type):
    if type == 'qa':
        return 'question' in body and 'answer' in body
    elif type == 'csv':
        return 'path' in body
    elif type == 'pdf':
        return 'path' in body
    else:
        return False