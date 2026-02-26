class InvalidGoogleTokenError(Exception):
    pass

class CorporateEmailRequiredError(Exception):
    pass

class InactiveUserError(Exception):
    pass

class InvalidRefreshTokenError(Exception):
    pass

class InvalidAccessTokenError(Exception):
    pass

class AccessTokenExpiredError(Exception):
    pass

class InvalidTokenPayloadError(Exception):
    pass

class UserNotFoundError(Exception):
    pass

class ForbiddenError(Exception):
    pass
