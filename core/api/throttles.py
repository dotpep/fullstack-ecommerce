from rest_framework import throttling


class AdminRateThrottle(throttling.BaseThrottle):
    scope = 'admin'

    def allow_request(self, request, view):
        if request.user.is_staff:
            return True
        return False
