from netbox.plugins import PluginMenuButton, PluginMenuItem


appsystem_buttons = [
    PluginMenuButton(
        link='plugins:netbox_app_systems:appsystem_add',
        title='Add',
        icon_class='mdi mdi-plus-thick'
    )
]


menu_items = (
    PluginMenuItem(
        link='plugins:netbox_app_systems:appsystem_list',
        link_text='App Systems',
        buttons=appsystem_buttons
    ),
)
