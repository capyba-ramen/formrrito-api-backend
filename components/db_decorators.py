import functools

from sqlalchemy import inspect


def transaction(func):
    # todo: logging part
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        db = kwargs.get('db')
        if db:
            try:
                return_value = func(*args, **kwargs)
                db.commit()
                print('commit')
                return return_value
            except Exception as error:
                print(f"error in transaction: {error}")
                db.rollback()
                print('rollback')
                raise error
        else:
            return func(*args, **kwargs)

    return wrapper


def instance_to_dict(instance):
    return {c.key: getattr(instance, c.key)
            for c in inspect(instance).mapper.column_attrs}
