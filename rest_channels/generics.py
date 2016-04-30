# from rest_framework import exceptions
#
# http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']
# authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
# throttle_classes = api_settings.DEFAULT_THROTTLE_CLASSES
# permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES
# content_negotiation_class = api_settings.DEFAULT_CONTENT_NEGOTIATION_CLASS
# metadata_class = api_settings.DEFAULT_METADATA_CLASS
# versioning_class = api_settings.DEFAULT_VERSIONING_CLASS
#
#
# def get_authenticators(self):
#     """
#     Instantiates and returns the list of authenticators that this view can use.
#     """
#     return [auth() for auth in self.authentication_classes]
#
#
# def get_permissions(self):
#     """
#     Instantiates and returns the list of permissions that this view requires.
#     """
#     return [permission() for permission in self.permission_classes]
#
#
# def get_throttles(self):
#     """
#     Instantiates and returns the list of throttles that this view uses.
#     """
#     return [throttle() for throttle in self.throttle_classes]
#
#
# def perform_authentication(self, request):
#     """
#     Perform authentication on the incoming request.
#
#     Note that if you override this and simply 'pass', then authentication
#     will instead be performed lazily, the first time either
#     `request.user` or `request.auth` is accessed.
#     """
#     request.user
#
#
# def check_permissions(self, request):
#     """
#     Check if the request should be permitted.
#     Raises an appropriate exception if the request is not permitted.
#     """
#     for permission in self.get_permissions():
#         if not permission.has_permission(request, self):
#             self.permission_denied(
#                 request, message=getattr(permission, 'message', None)
#             )
#
#
# def check_object_permissions(self, request, obj):
#     """
#     Check if the request should be permitted for a given object.
#     Raises an appropriate exception if the request is not permitted.
#     """
#     for permission in self.get_permissions():
#         if not permission.has_object_permission(request, self, obj):
#             self.permission_denied(
#                 request, message=getattr(permission, 'message', None)
#             )
#
#
# def check_throttles(self, request):
#     """
#     Check if request should be throttled.
#     Raises an appropriate exception if the request is throttled.
#     """
#     for throttle in self.get_throttles():
#         if not throttle.allow_request(request, self):
#             self.throttled(request, throttle.wait())
#
#
# def determine_version(self, request, *args, **kwargs):
#     """
#     If versioning is being used, then determine any API version for the
#     incoming request. Returns a two-tuple of (version, versioning_scheme)
#     """
#     if self.versioning_class is None:
#         return None, None
#     scheme = self.versioning_class()
#     return (scheme.determine_version(request, *args, **kwargs), scheme)
#
#
# def throttled(self, request, wait):
#     """
#     If request is throttled, determine what kind of exception to raise.
#     """
#     raise exceptions.Throttled(wait)
#
#
# def get_authenticate_header(self, request):
#     """
#     If a request is unauthenticated, determine the WWW-Authenticate
#     header to use for 401 responses, if any.
#     """
#     authenticators = self.get_authenticators()
#     if authenticators:
#         return authenticators[0].authenticate_header(request)
#
#
# def permission_denied(self, message, message=None):
#     """
#     If message is not permitted, determine what kind of exception to raise.
#     """
#     if not message.successful_authenticator:
#         raise exceptions.NotAuthenticated()
#     raise exceptions.PermissionDenied(detail=message)