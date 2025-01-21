from netbox.plugins import PluginTemplateExtension
from core.models import ObjectType
from .models import AppSystemAssignment
# from netbox.models.


class AppSystemVMPanel(PluginTemplateExtension):
    model = 'virtualization.virtualmachine'
    # model = 'dcim.device'

    def left_page(self):
        vm = self.context['object']
        object_type_id = ObjectType.objects.get_for_model(model=vm).id
        app_systems = AppSystemAssignment.objects.filter(
            object_id=vm.id, object_type=object_type_id)
        # print(vars(AppSystem_ass))
        # print(AppSystem_ass)
        AppSystems = []
        for s in app_systems:
            AppSystems.append({
                'id': s.id,
                'app_system': s.app_system})
            # print(s.__dict__)

        # print(AppSystems)
        return self.render('netbox_app_systems/app_system_panel.html', extra_context={
            'app_systems': AppSystems
        })


class AppSystemDevicePanel(PluginTemplateExtension):
    model = 'dcim.device'

    def left_page(self):
        vm = self.context['object']
        object_type_id = ObjectType.objects.get_for_model(model=vm).id
        app_systems = AppSystemAssignment.objects.filter(
            object_id=vm.id, object_type=object_type_id)
        AppSystems = []
        for s in app_systems:
            AppSystems.append({
                'id': s.id,
                'app_system': s.app_system})
            # print(s.__dict__)

        return self.render('netbox_app_systems/app_system_panel.html', extra_context={
            'app_systems': AppSystems
        })


template_extensions = [AppSystemVMPanel, AppSystemDevicePanel]
