"""Python Rubik's Cube package.

Package layout:
    ernoe/
        __init__.py
        cube/
            internals/
                __init__.py
                cubemxx3.py
                cubiemxxn.py
                ...
            __init__.py
            cube2xx3.py
            cube3xx3.py
            cube4xx3.py
            cube5xx3.py
            cube6xx3.py
            cube7xx3.py
            ...
        display/
            backend/
                __init__.py
                ...
            __init__.py
            cli.py
            ...
        solve/
            __init__.py
            ...
"""


__all__ = ["cube", "display", "solve"]
