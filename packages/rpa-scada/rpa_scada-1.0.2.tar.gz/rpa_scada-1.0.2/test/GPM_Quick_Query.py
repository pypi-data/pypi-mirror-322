from utils import get_credentials


USER,PSSW = get_credentials()

# Ahora puedes importar el módulo QuickQuery directamente
from rpa_scada.GPM.QuickQuery import GpmQuickQuery
gpm = GpmQuickQuery(
    user=USER,
    pssw=PSSW,
    timezone='-04:00',
    ID_PMGD_GPM=8724
    )
response = gpm.get_element_by_subtype(subtype_config={
            "type": 4,
            "subtype": 451,
            "iddl": "44126,44128",
            "idtj": "219148,219158",
            "deviceType": 1,
            "name": "Inverter - (INVERTER)"
        })
# from rpa_scada.GPM.reports import GpmReports
# gpm = GpmReports(
#     user=USER,
#     pssw=PSSW,
#     timezone='-04:00'
#     )

# print(gpm.login_status)
# from datetime import datetime

# response = gpm.get_report(
#     start_date=datetime(2024,4,1),
#     end_date=datetime(2024,4,1),
#     id_planta=9590,
#     id_report=277552,
#     report_name='Reporte'
# )
if response != None:
    from rpa_scada.GPM.utils import GpmUtils
    directory = rf"C:\Users\DanielTaiba\Documents\MODULES\rpa_scada\data\QuickQuery\\"
    
    GpmUtils().write_json_to_file(
        data = response,
        path = directory,
        name_file='get_element_by_subtype_451.json'
    )