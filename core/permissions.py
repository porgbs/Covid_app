class BaseGlobalMixin(object):
    base_global_allowed = True

    @classmethod
    def has_read_permission(cls, request):
        return cls.base_global_allowed

    @classmethod
    def has_write_permission(cls, request):
        return cls.base_global_allowed


class BaseObjectMixin(object):
    base_object_allowed = True

    def has_object_read_permission(self, request):
        return self.base_object_allowed

    def has_object_write_permission(self, request):
        return self.base_object_allowed


class SpecificGlobalMixin(object):
    specific_global_allowed = True

    @classmethod
    def has_list_permission(cls, request):
        return cls.specific_global_allowed

    @classmethod
    def has_create_permission(cls, request):
        return cls.specific_global_allowed

    @classmethod
    def has_destroy_permission(cls, request):
        return cls.specific_global_allowed

    @classmethod
    def has_retrieve_permission(cls, request):
        return cls.specific_global_allowed

    @classmethod
    def has_update_permission(cls, request):
        return cls.specific_global_allowed


class SpecificObjectMixin(object):
    specific_object_allowed = True

    def has_object_list_permission(self, request):
        return self.specific_object_allowed

    def has_object_create_permission(self, request):
        return self.specific_object_allowed

    def has_object_destroy_permission(self, request):
        return self.specific_object_allowed

    def has_object_retrieve_permission(self, request):
        return self.specific_object_allowed

    def has_object_update_permission(self, request):
        return self.specific_object_allowed
