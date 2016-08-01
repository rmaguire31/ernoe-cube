"""Python Rubik's Cube package.

Package layout:
    ernoe/
        __init__.py
        cube/
            internals/
                __init__.py
                cube3d.py
                cubie3d.py
                ...
            __init__.py
            cube_instances.py
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
