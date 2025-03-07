# from common.const import response_exceptions as resp_exc
# from common.enums.role import RoleEnum
#
# GET_USER_INFO_TEST_DATA = (
#     "user_id, test_result",
#     (
#         ("beb247ae-58cc-4e75-b6fc-61e57e10a606", True),
#         # не существующий пользователь
#         ("922f323e-abda-4192-b9f8-c9091fd2654d", resp_exc.USER_NOT_FOUND),
#         ("922f323e-abda-4192-b9f8-c9091fd2686d", True),
#     ),
# )
#
#
# CREATE_USERS_PROFILE_TEST_DATA = (
#     "test_data",
#     (
#         {
#             "role": RoleEnum.CUSTOMER,
#             "email": "TestCustomer@gmail.com",
#             "phone_number": "+79999999999",
#             "password_hash": "1234567890",
#             "last_name": "Борунов",
#             "first_name": "Айдар",
#             "second_name": "Владимирович",
#             "is_man": True,
#             "birthday": "1994-04-26",
#             "test_result": resp_exc.EMAIL_CONFLICT,
#         },
#         {
#             "role": RoleEnum.CUSTOMER,
#             "email": "Guest10@gmail.com",
#             "phone_number": "+79839199999",
#             "password_hash": "guest_2134_leonov",
#             "last_name": "Горбунов",
#             "first_name": "Инсаф",
#             "second_name": "Олегович",
#             "is_man": True,
#             "birthday": "1987-05-12 18:45:00",
#             "test_result": True,
#         },
#         {
#             "role": RoleEnum.CUSTOMER,
#             "email": "Driver10@gmail.com",
#             "phone_number": "+7(924)596-30-99",
#             "password_hash": "driver_2134_leonov",
#             "last_name": "Горбунов",
#             "first_name": "Инсаф",
#             "second_name": "Олегович",
#             "is_man": True,
#             "birthday": "1987-05-12 18:45:00",
#             "test_result": resp_exc.PHONE_NUMBER_CONFLICT,
#         },
#     ),
# )
