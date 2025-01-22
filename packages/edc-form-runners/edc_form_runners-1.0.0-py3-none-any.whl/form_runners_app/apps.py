from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = "form_runners_app"
    verbose_name = "form_runners test app"
