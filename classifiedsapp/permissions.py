from django.contrib.auth.mixins import PermissionRequiredMixin


# Меняем работу миксина, чтобы он проверял автора объявления
class ChangedPRM(PermissionRequiredMixin):
    def has_permission(self):
        perms = self.get_permission_required()
        if self.request.user != self.get_object().author:
            return False
        return self.request.user.has_perms(perms)
