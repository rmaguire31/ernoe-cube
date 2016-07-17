"""Python Rubik's Cube package.

Package layout:
    ernoe/
        __init__.py
        cube/
            internals/
                eval/
                    __init__.py
                    cube3d.py
                    void3d.py
                    ...
                __init__.py
                cube3d.py
                cubie3d.py
                ...
            __init__.py
            cube2x2.py
            cube3x3.py
            cube4x4.py
            cube5x5.py
            void3x3.py
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
