EMPTY_USERNAME = "Никнейм пользователя не может быть пустым."
EMPTY_CONTACT = "Необходимо указать хотя бы один контактный номер."

TOO_LONG_USERNAME = lambda length: (  # noqa
    f"Никнейм пользователя не может " f"быть длиннее {length} символов."
)

WRONG_USERNAME_FORMAT = (
    "Никнейм пользователя должен начинаться с буквы и содержать "
    "только латинские буквы, цифры, и знак подчеркивания."
)

WRONG_PHONE_NUMBER_FORMAT = "Телефонный номер должен быть указан в строковом значении."
WRONG_EMAIL_FORMAT = "Почта должна быть указана в строковом значении."
