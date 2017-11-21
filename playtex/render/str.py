from playtex.render.common import latex_escapes

def render(obj):
    return str(obj).translate(latex_escapes)
