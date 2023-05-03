from core.settings import ENVIRONMENT, MAINTENANCEMODE, MAINTENANCETEXT


def get_maintenancemode(request):
    if MAINTENANCEMODE == 'True':
        return {'MAINTENANCEMODE': MAINTENANCEMODE, 'ALERT_TEXT':MAINTENANCETEXT}
    else:
        return {}
