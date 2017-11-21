""" Tools that are useful in creating renderers """

latex_escapes = {
    # https://en.wikibooks.org/wiki/LaTeX/Basics#Reserved_Characters
    ord("#"): r"\#",
    ord("$"): r"\$",
    ord("%"): r"\%",
    ord("&"): r"\&",
    ord("^"): r"\^{}",
    ord("_"): r"\_",
    ord("{"): r"\{",
    ord("}"): r"\}",
    ord("~"): r"\~{}",
    ord("\\"): r"\textbackslash{}",

    # Ensure correct printing regardless of font encoding
    ord("<"): r"\textless{}",
    ord(">"): r"\textgreater{}",
    ord("|"): r"\textbar{}"

    # TODO: -
}
