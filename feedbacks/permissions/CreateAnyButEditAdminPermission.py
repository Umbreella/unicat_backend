from unicat.permissions.DjModelPermForDRF import DjModelPermForDRF


class CreateAnyButEditAdminPermission(DjModelPermForDRF):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True

        return super().has_permission(request, view)
