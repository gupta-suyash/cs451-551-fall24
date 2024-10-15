import time
import functools

def timer(func):
    @functools.wraps(func)  # Preserves the original function's metadata
    def wrapper(*args, **kwargs):
        # Prepare argument representations
        args_repr = []
        for a in args:
            if isinstance(a, type):  # Check if the argument is a class
                args_repr.append(a.__name__)  # Use class name only
            elif isinstance(a, int):
                args_repr.append(f"{a:_}")  # Format integer with underscores
            else:
                args_repr.append(repr(a))  # Default representation

        kwargs_repr = [f"{k}={v:_r}" if isinstance(v, int) else f"{k}={v!r}" for k, v in kwargs.items()]
        
        all_args = ", ".join(args_repr + kwargs_repr)  # Combine all
        
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        duration = end_time - start_time
        print(f"{func.__name__}({all_args}) executed in {duration:.4f} seconds")
        return result
    
    return wrapper