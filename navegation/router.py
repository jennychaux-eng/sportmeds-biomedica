from inventario.view import render as inventario_view


def render_module(modulo):

    if "Inventario" in modulo:
        inventario_view()
