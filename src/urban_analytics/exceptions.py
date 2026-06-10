class UrbanAnalyticsError(Exception):
    """Базовое исключение для библиотеки urban_analytics.

    От него будут наследоваться все остальные наши ошибки.
    """

    pass


class EmptyDataError(UrbanAnalyticsError):
    """Вызывается, когда входные GeoDataFrame пусты."""

    pass


class CRSMismatchError(UrbanAnalyticsError):
    """Вызывается, когда системы координат (CRS) входных слоев не совпадают."""

    pass
