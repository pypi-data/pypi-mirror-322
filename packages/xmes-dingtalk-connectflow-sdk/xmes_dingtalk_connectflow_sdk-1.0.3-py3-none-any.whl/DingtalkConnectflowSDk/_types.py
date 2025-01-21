from dataclasses import fields


class FilteredDataclass(type):
    """过滤kwargs中多余的键"""

    def __call__(cls, *args, **kwargs):
        valid_fields = {f.name for f in fields(cls)}
        kwargs = {k: v for k, v in kwargs.items() if k in valid_fields}
        return super().__call__(*args, **kwargs)
