from datetime import datetime


def print_func_name(func):
    def wrapper(*args, **kwargs):
        print(f"now running {func.__name__}")
        func(*args, **kwargs)

    return wrapper


def timer(func):
    def timer_wrapper(*args, **kwargs):
        start_time = datetime.now()
        print(args)
        print(kwargs)
        func(*args, **kwargs)
        end_time = datetime.now()
        time_diff = round((end_time - start_time).total_seconds(), 2)
        print(f"Spent {time_diff} seconds calling {func.__name__} from {start_time} to {end_time}")

    return timer_wrapper
