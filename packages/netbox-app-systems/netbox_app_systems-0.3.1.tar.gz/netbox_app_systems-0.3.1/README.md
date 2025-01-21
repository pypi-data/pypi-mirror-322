# Netbox plugin 'Application systems'

Добавляет:
- в Netbox объект "Application system"
- в карточки объектов virtual machine, device секцию "Application system"

Позволяет проводить группировку активов по сервисам, системам. 

## Установка

1. Установить плагин `pip3 install netbox-app-systems`
2. Добавить плагин в `netbox/netbox/netbox/configuration.py` (обновить или добавить переменную):

```
PLUGINS=['netbox_app_systems']
```

3. Перейти в каталог с файлом `manage.py` и выполнить миграцию БД `python3 manage.py migrate`
4. Перезапустить сервер netbox
5. Проверить, что плагин появился в списке установленных плагинов в административном интерфейсе Django.

