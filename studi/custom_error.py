from studi import log

class BaseError(Exception):
    def __init__(self, code=400, status='', message='', params=[], error_message=''):
        Exception.__init__(self)
        self.code = code
        self.status = status
        self.message = message
        self.params = params
        self.error_message = error_message

    def __str__(self):
        return self.message

    def to_dict(self):
        params = ''
        if self.params:
            params = ''.join(f'{key}: {value}' for key, value in self.params.items())

        log.logger.error('Exception, code : {0}, status : {1}, message : {2}, parms : {3}, error_message : {4}'.format(self.code, self.status, self.message, params, self.error_message))

        response = {'code' : self.code, 'status' : self.status, 'message' : self.message}
        return response


class AttributeError(BaseError):
    def __init__(self, error_message):
        BaseError.__init__(self)
        self.code = 500
        self.status = 'AttributeError'
        self.message = '인스턴스의 속성 이름이나 모듈의 이름이 잘못되었습니다. 해당 인스턴스에 속성이 있는지 확인해주세요'
        self.error_message = error_message


class UnExpectedError(BaseError):
    def __init__(self):
        BaseError.__init__(self)
        self.code = 500
        self.status = "UnExpectedError"
        self.message = '예기치 못한 서버 오류가 발생했습니다. 관리자에게 문의해주세요'


class BadRequestError(BaseError):
    def __init__(self):
        BaseError.__init__(self)
        self.code = 400
        self.status = 'Bad Request'
        self.message = '요청에 필요한 파라미터 값이 존재하지 않거나 올바르지 않은 파라미터 값이 포함되었습니다'
        # self.params = params
        # self.error_message = error_message


class HTTPRequestError(BaseError):
    def __init__(self, error_message):
        BaseError.__init__(self)
        self.code = 400
        self.status = "HTTPException"
        self.message = '잘못된 요청이 들어와 요청을 처리하지 못하였습니다.'
        self.error_message = error_message


class SQLAlchemyNotInsertError(BaseError):
    def __init__(self, error_message):
        BaseError.__init__(self)
        self.code = 500
        self.status = 'NotInserted'
        self.message = 'SQLAlchemy에서 원인을 알 수 없는 이유로 DB에 데이터가 저장되지 않았습니다.'


class SQLAlchemyError(BaseError):
    def __init__(self, error_message):
        BaseError.__init__(self)
        self.code = 500
        self.status = 'SQLALchemyError'
        self.message = 'DB 요청을 처리하는데 문제가 발생하였습니다.'
        self.error_message = error_message


class CSVError(BaseError):
    def __init__(self, error_message):
        BaseError.__init__(self)
        self.code = 400
        self.status = 'CSVError'
        self.message = 'csv 파일을 처리하는데 문제가 발생하였습니다. csv 파일이 비어있거나 파일 내부 형식이 잘못되었습니다.'
        self.error_message = error_message


class NotCSVFileError(BaseError):
    def __init__(self, filename):
        BaseError.__init__(self)
        self.code = 400
        self.status = 'NotCSVFileError'
        self.message = '요청하신 {0} 파일은 csv 형태가 아닙니다. 파일 형식을 다시 확인하여 주세요'.format(filename)
