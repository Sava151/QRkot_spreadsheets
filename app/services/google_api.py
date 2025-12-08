import copy
from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings

FORMAT = "%Y/%m/%d %H:%M:%S"
DEFAULT_ROW_COUNT = 100
DEFAULT_COLUMN_COUNT = 11

SPREADSHEET_BODY_TEMPLATE = {
    'properties': {
        'title': 'Отчёт от {date}',
        'locale': 'ru_RU'
    },
    'sheets': [{
        'properties': {
            'sheetType': 'GRID',
            'sheetId': 0,
            'title': 'Лист1',
            'gridProperties': {
                'rowCount': DEFAULT_ROW_COUNT,
                'columnCount': DEFAULT_COLUMN_COUNT
            }
        }
    }]
}

PERMISSIONS_BODY_TEMPLATE = {
    'type': 'user',
    'role': 'writer',
    'emailAddress': settings.email
}


async def create_spreadsheets(
        wrapper_services: Aiogoogle,
        spreadsheet_body_template: dict = SPREADSHEET_BODY_TEMPLATE
) -> str:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = copy.deepcopy(spreadsheet_body_template)
    spreadsheet_body['property']['title'] = spreadsheet_body[
        'properties'
    ]['title'].format(date=now_date_time)
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheetid = response['spreadsheetId']
    return spreadsheetid


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=PERMISSIONS_BODY_TEMPLATE,
            fields="id"
        ))


async def update_spreadsheets_value(
        spreadsheetid: str,
        charity: list,
        wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        ['Отчёт от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Названиее проекта', 'Время сбора', 'Описание']
    ]
    for res in charity:
        new_row = [str(res['name']), str(res['time']), str(res['description'])]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
