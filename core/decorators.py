import time


def timing_decorator(func):
    ''' Decorator for timing functions '''
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"[ - ] Function '{func.__name__}' executed in {end_time - start_time:.2f} seconds")  # noqa
        return result
    return wrapper
