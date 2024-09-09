from common.const.response_exceptions import USER_NOT_FOUND
from common.enums.role import RoleEnum

GET_LIST_USERS_ADMIN_TEST_DATA = (
    "test_data",
    (
        {
            "page_number": 0,
            "page_size": 10,
            "search_string": None,
            "date_begin": None,
            "date_end": None,
            "role_uuid": None,
            "count": 5,
        },
        {
            "page_number": 0,
            "page_size": 10,
            "search_string": "Динаров Алмаз Антонович",  # покупатель
            "date_begin": None,
            "date_end": None,
            "role_uuid": None,
            "count": 1,
        },
        {
            "page_number": 0,
            "page_size": 10,
            "search_string": "Леонов",  # курьер
            "date_begin": None,
            "date_end": None,
            "role_uuid": None,
            "count": 1,
        },
        {
            "page_number": 1,
            "page_size": 10,
            "search_string": None,
            "date_begin": None,
            "date_end": None,
            "role_uuid": None,
            "count": 5,
        },
        {
            "page_number": 1,
            "page_size": 3,
            "search_string": None,
            "date_begin": None,
            "date_end": None,
            "role_uuid": None,
            "count": 3,
        },
        {
            "page_number": 2,
            "page_size": 3,
            "search_string": None,
            "date_begin": None,
            "date_end": None,
            "role_uuid": None,
            "count": 2,
        },
        {
            "page_number": 0,
            "page_size": 10,
            "search_string": "Айназ",  # такого пользователя не существует
            "date_begin": None,
            "date_end": None,
            "role_uuid": None,
            "count": 0,
        },
        {
            "page_number": 0,
            "page_size": 10,
            "search_string": "Анатольевна",  # поставщик
            "date_begin": None,
            "date_end": None,
            "role_uuid": None,
            "count": 1,
        },
        {
            "page_number": 0,
            "page_size": 10,
            "search_string": "Динар Олегович",  # менеджер
            "date_begin": None,
            "date_end": None,
            "role_uuid": None,
            "count": 1,
        },
        {
            "page_number": 0,
            "page_size": 10,
            "search_string": "Долотов Давид",  # администратор
            "date_begin": None,
            "date_end": None,
            "role_uuid": None,
            "count": 1,
        },
        {
            "page_number": 0,
            "page_size": 10,
            "search_string": "TestAdmin@gmail.com",  # администратор
            "date_begin": None,
            "date_end": None,
            "role_uuid": None,
            "count": 1,
        },
    ),
)

UPDATE_USER_ADMIN_TEST_DATA = (
    "test_data",
    (
        {
            "id": "beb247ae-58cc-4e75-b6fc-61e57e10a606",
            "last_name": "Динаров",
            "first_name": "Алмаз",
            "second_name": "Антонович",
            "birthday": "1986-02-25",
            "phone_number": "+7(925)555-35-35",
            "role": RoleEnum.MANAGER,
            "test_result": True
        },
        {
            "id": "beb247ae-58cc-4e75-b6fc-61e57e12b666",
            "last_name": "Динаров",
            "first_name": "Алмаз",
            "second_name": "Антонович",
            "birthday": "1986-02-25",
            "phone_number": "+7(925)555-35-35",
            "role": RoleEnum.CUSTOMER,
            "test_result": USER_NOT_FOUND
        },
    ),
)
