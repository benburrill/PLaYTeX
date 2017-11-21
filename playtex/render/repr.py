from playtex.render.common import latex_escapes

def render(obj):
    return repr(obj).translate(latex_escapes)
