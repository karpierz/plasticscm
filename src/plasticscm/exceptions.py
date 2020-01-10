# Copyright (c) 2019-2020 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/licenses/zlib

import functools

from public import public


@public
class PlasticError(Exception):

    def __init__(self, error_message="", response_code=None, response_body=None):
        if not isinstance(error_message, str):
            try:
                # if we receive str/bytes we try to convert to unicode/str
                # to have consistent message types
                error_message = error_message.decode()
            except Exception:
                pass
        super().__init__(error_message)
        self.__error_message = error_message  # Parsed error message from PlasticSCM
        self.__response_code = response_code  # Http status code
        self.__response_body = response_body  # Full http response

    error_message = property(lambda self: self.__error_message)
    response_code = property(lambda self: self.__response_code)
    response_body = property(lambda self: self.__response_body)

    def __str__(self):
        if self.__response_code is not None:
            return "{}: {}".format(self.__response_code, self.__error_message)
        else:
            return "{}".format(self.__error_message)


def on_http_error(error: Exception):
    """Manage PlasticHttpError exceptions.

    This decorator function can be used to catch PlasticHttpError exceptions
    raise specialized exceptions instead.

    Args:
        error: The exception type to raise -- must inherit from PlasticError
    """

    def wrap(fun):
        @functools.wraps(fun)
        def wrapper(*args, **kwargs):
            try:
                return fun(*args, **kwargs)
            except PlasticHttpError as exc:
                raise error(exc.error_message, exc.response_code, exc.response_body)
        return wrapper

    return wrap


@public
class PlasticHttpError(PlasticError):
    """ """

class GitlabAuthenticationError(PlasticError):
    """ """

class RedirectError(PlasticError):
    """ """

class GitlabParsingError(PlasticError):
    """ """

class GitlabConnectionError(PlasticError):
    """ """

class GitlabOperationError(PlasticError):
    """ """

class GitlabListError(GitlabOperationError):
    """ """

class GitlabGetError(GitlabOperationError):
    """ """

class GitlabCreateError(GitlabOperationError):
    """ """

class GitlabUpdateError(GitlabOperationError):
    """ """

class GitlabDeleteError(GitlabOperationError):
    """ """

class GitlabSetError(GitlabOperationError):
    """ """

class GitlabProtectError(GitlabOperationError):
    """ """

class GitlabTransferProjectError(GitlabOperationError):
    """ """

class GitlabProjectDeployKeyError(GitlabOperationError):
    """ """

class GitlabCancelError(GitlabOperationError):
    """ """

class GitlabPipelineCancelError(GitlabCancelError):
    """ """

class GitlabRetryError(GitlabOperationError):
    """ """

class GitlabBuildCancelError(GitlabCancelError):
    """ """

class GitlabBuildRetryError(GitlabRetryError):
    """ """

class GitlabBuildPlayError(GitlabRetryError):
    """ """

class GitlabBuildEraseError(GitlabRetryError):
    """ """

class GitlabJobCancelError(GitlabCancelError):
    """ """

class GitlabJobRetryError(GitlabRetryError):
    """ """

class GitlabJobPlayError(GitlabRetryError):
    """ """

class GitlabJobEraseError(GitlabRetryError):
    """ """

class GitlabPipelineRetryError(GitlabRetryError):
    """ """

class GitlabBlockError(GitlabOperationError):
    """ """

class GitlabUnblockError(GitlabOperationError):
    """ """

class GitlabDeactivateError(GitlabOperationError):
    """ """

class GitlabActivateError(GitlabOperationError):
    """ """

class GitlabSubscribeError(GitlabOperationError):
    """ """

class GitlabUnsubscribeError(GitlabOperationError):
    """ """

class GitlabMRForbiddenError(GitlabOperationError):
    """ """

class GitlabMRApprovalError(GitlabOperationError):
    """ """

class GitlabMRRebaseError(GitlabOperationError):
    """ """

class GitlabMRClosedError(GitlabOperationError):
    """ """

class GitlabMROnBuildSuccessError(GitlabOperationError):
    """ """

class GitlabTodoError(GitlabOperationError):
    """ """

class GitlabTimeTrackingError(GitlabOperationError):
    """ """

class GitlabUploadError(GitlabOperationError):
    """ """

class GitlabAttachFileError(GitlabOperationError):
    """ """

class GitlabCherryPickError(GitlabOperationError):
    """ """

class GitlabHousekeepingError(GitlabOperationError):
    """ """

class GitlabOwnershipError(GitlabOperationError):
    """ """

class GitlabSearchError(GitlabOperationError):
    """ """

class GitlabStopError(GitlabOperationError):
    """ """

class GitlabMarkdownError(GitlabOperationError):
    """ """

class GitlabVerifyError(GitlabOperationError):
    """ """

class GitlabRenderError(GitlabOperationError):
    """ """

class GitlabRepairError(GitlabOperationError):
    """ """

class GitlabLicenseError(GitlabOperationError):
    """ """
