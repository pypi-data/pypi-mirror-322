from django.core.checks import Error

from django_tbank_kassa import settings


def check_variable(obj_name: str, correct_type: type, ids: tuple[int, int]):
    obj = getattr(settings, obj_name)
    if obj is None:
        return [
            Error(
                f'{obj_name} {correct_type.__name__} is required.',
                hint=f'Add {obj_name} to settings.py',
                id=f'django_tbank_kassa.E{ids[0]:03}',
            )
        ]
    if not isinstance(obj, correct_type):
        return [
            Error(
                f'Type of {obj_name} is {type(obj).__name__}, '
                f'but must be {correct_type.__name__}.',
                hint=f'Set the value of {obj_name} to {correct_type.__name__} '
                'instance.',
                obj=obj,
                id=f'django_tbank_kassa.E{ids[1]:03}',
            )
        ]
    return []


def settings_variables_check(app_configs, **kwargs):  # noqa: ARG001
    return [
        *check_variable('TBANK_KASSA_TERMINAL_KEY', str, (1, 2)),
        *check_variable('TBANK_KASSA_PASSWORD', str, (3, 4)),
        *check_variable('TBANK_KASSA_TEST', bool, (5, 6)),
    ]
