#!/usr/bin/env python3

"""get-def

Usage:
    get-def (WORD)
    get-def -n (WORD)
    get-def -h

Examples:
    get-def hello
    get-def -n hello

Options:
    -n, --no-pager  do not use a pager
    -h, --help      show this help message and exit
"""

import requests
from docopt import docopt
from rich import box
from rich.console import Console
from rich.padding import Padding
from rich.table import Table
from rich.text import Text


def print_def(console: Console, response: requests.Response):
    word = response.json()[0].get("word")

    console.print()
    console.print(" :arrow_forward: ", Text(word, style="bold red", justify="center"))
    console.print()

    phonetics = response.json()[0].get("phonetics")
    phonetics_table = Table(box=box.SQUARE)
    phonetics_table.add_column("Phonetic Text", style="cyan")
    phonetics_table.add_column("Phonetic Audio")
    if len(phonetics) > 0:
        for item in phonetics:
            text = item.get("text") if item.get("text") else "None"
            audio = item.get("audio") if item.get("audio") else "None"
            phonetics_table.add_row(text, audio)
        console.print(phonetics_table)

    console.print(
        "IPA chart: https://www.internationalphoneticassociation.org/IPAcharts/inter_chart_2018/IPA_2018.html"
    )
    console.print()

    meanings = response.json()[0].get("meanings")

    for item in meanings:
        console.print(
            f"[bold]{meanings.index(item) + 1}. [underline]{item['partOfSpeech']}"
        )
        for definition in item["definitions"]:
            console.print(
                Padding(
                    f"[bold blue]Definition:[/bold blue] {definition.get('definition')}",
                    (0, 0, 0, 3),
                )
            )
            if definition.get("example") is not None:
                console.print(
                    Padding(
                        f"[bold magenta]Example:[/bold magenta] {definition.get('example')}",
                        (0, 0, 0, 3),
                    )
                )
            if definition.get("synonyms"):
                console.print(
                    Padding(
                        f"[bold yellow]Synonyms:[/bold yellow] "
                        + ", ".join(definition.get("synonyms")),
                        (0, 0, 0, 3),
                    )
                )
            if definition.get("antonyms"):
                console.print(
                    Padding(
                        f"[bold yellow]Antonyms:[/bold yellow] "
                        + ", ".join(definition.get("antonyms")),
                        (0, 0, 0, 3),
                    )
                )
            console.print()


def main():
    args = docopt(__doc__)

    api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{args['WORD']}"

    try:
        response = requests.get(api_url, timeout=30)
        if response.status_code == 404:
            exit(
                "Sorry, we couldn't find definitions for the word you were looking for."
            )
    except requests.Timeout:
        exit(
            "The connection has timed out. This might indicate an issue with DNS, firewall, or your internet connection."
        )

    console = Console(width=100)

    if not args["--no-pager"]:
        with console.pager(styles=True):
            print_def(console, response)
    else:
        print_def(console, response)


if __name__ == "__main__":
    main()
