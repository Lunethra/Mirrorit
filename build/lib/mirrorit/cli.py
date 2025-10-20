import typer
from rich.console import Console
from pathlib import Path
import re

console = Console()
app = typer.Typer(add_completion=False, rich_markup_mode="rich")


# ---------- Mirror modes ----------
def mirror_word_by_word(text: str) -> str:
    """Reverse each word separately, keeping punctuation in place."""
    words = text.split(" ")
    mirrored = []
    for word in words:
        letters = [c for c in word if c.isalnum()]
        reversed_letters = letters[::-1]
        ri = 0
        result = ""
        for ch in word:
            if ch.isalnum():
                result += reversed_letters[ri]
                ri += 1
            else:
                result += ch
        mirrored.append(result)
    return " ".join(mirrored)


def mirror_text_mode(text: str, mode: str) -> str:
    """Apply the selected mirror mode."""
    if mode == "w":
        return text[::-1]
    elif mode == "t":
        return mirror_word_by_word(text)
    elif mode == "k":
        # reverse letters in words, move symbols to front
        return "".join([s[::-1] if s.isalpha() else s for s in re.split(r"(\W+)", text)])
    return text


# ---------- CLI ----------
@app.command(context_settings={"help_option_names": ["-h", "--help"]})
def mirror(
    source: str = typer.Argument(..., help="Text or file path to mirror"),
    mode: str = typer.Option(
        "w",
        "-m",
        "--mode",
        help=(
            "Mirror mode (default=w):\n"
            "  w → reverse the whole text as one string\n"
            "  t → reverse each word separately, keep symbols in place\n"
            "  k → reverse each word and move symbols to the front"
        ),
    ),
    save: bool = typer.Option(False, "-s", help="Overwrite the original file"),
    new_file: bool = typer.Option(False, "-n", help="Create a new mirrored file"),
    just_show: bool = typer.Option(False, "-j", help="Just show output, don’t modify files"),
):
    """
    Mirrorit — mirror text or file content.

    Examples:
      mirrorit hello world! -m t
      mirrorit file.txt -m k -j
      mirrorit file.txt -m w -s
      mirrorit file.txt -m t -n
    """
    path = Path(source)
    if path.exists():
        text = path.read_text(encoding="utf-8")
        mirrored = mirror_text_mode(text, mode)

        if just_show:
            console.print(mirrored)
        elif save:
            path.write_text(mirrored, encoding="utf-8")
            console.print(f"[green]File updated:[/] {path}")
        elif new_file:
            new_path = path.parent / f"mirrored_{path.name}"
            new_path.write_text(mirrored, encoding="utf-8")
            console.print(f"[cyan]New file created:[/] {new_path}")
        else:
            console.print("[red]You must use one of -s, -n, or -j![/]")
    else:
        # input is text, not file
        mirrored = mirror_text_mode(source, mode)
        console.print(mirrored)


if __name__ == "__main__":
    app()
