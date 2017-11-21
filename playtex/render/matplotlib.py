import io
from matplotlib import rc_context

MPL_RC = {
    "pgf.rcfonts": False
}

def render(plot):
    with rc_context(rc=MPL_RC):
        buf = io.BytesIO()
        plot.savefig(buf, format="pgf")
        buf.seek(0)
        return buf.read().decode()
