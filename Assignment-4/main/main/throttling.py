from rest_framework.throttling import UserRateThrottle


class RoleBasedRateThrottle(UserRateThrottle):
    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_staff:
                self.rate = '1000/hour'
            else:
                self.rate = '100/hour'
        else:
            self.rate = '10/hour'
        return super().get_cache_key(request, view)
