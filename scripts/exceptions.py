
class Exceptions(Exception):

    def __init__(self, msg=None, error=None, type='GENERAL'):
        self.message = msg if msg else 'A general Exception has occurred'
        self.error = error
        self.type = type
        super(Exception).__init__()


class FileNotFound(Exceptions, FileNotFoundError):

    def __init__(self, path, error):
        super(Exceptions, self).__init__(msg='A file was not found at {}'.format(path), error=error)


class AggregateException(Exceptions):

    def __init__(self, error):
        super(Exceptions, self).__init__(msg='A general Aggregate Exception has occurred', error=error, type='REPORT')


class PipelineExceptions(Exceptions):

    def __init__(self, error):
        super(Exceptions, self).__init__(msg='A error occurred in the pipeline', error=error, type='REPORT')
