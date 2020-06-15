def write_errors(exception, text):
    with open('errors.log', 'a+') as log_archive:
        log_archive.write(str(exception))
        log_archive.write(text)