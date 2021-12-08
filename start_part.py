import sys
import random
import webbrowser
import pandas as pd
from time import sleep
from rich.console import Console
from playsound import playsound


def load_data(reset=False):
    songs = pd.read_csv("songs.csv")
    participants = pd.read_csv("participants.csv")
    if reset:
        songs["PLAYED"] = False
        participants["SUNG"] = False

    return songs, participants


def save_data(songs, participants):
    songs.to_csv("songs.csv", index=False)
    participants.to_csv("participants.csv", index=False)


def pick_participant(participants):
    eligible_participants = participants[participants["SUNG"] == False].index
    if len(eligible_participants) == 0:
        participants["SUNG"] = False
        eligible_participants = participants[participants["SUNG"] == False].index
    participant_id = random.choice(eligible_participants)
    pick = participants.loc[participant_id]
    participants.at[participant_id, "SUNG"] = True

    return pick


def pick_song(songs, participant_languages):
    unplayed_songs = set(songs[songs["PLAYED"] == False].index)
    if len(unplayed_songs) == 0:
        print("NO MORE SONGS!")
        print("THANK YOU FOR PLAYING!")
        exit(0)
    lang_songs = [
        i
        for i, lang in enumerate(songs["LANGUAGE"])
        if lang.strip() not in participant_languages
    ]
    eligible_songs = list(unplayed_songs.intersection(lang_songs))
    song_id = random.choice(eligible_songs)
    pick = songs.loc[song_id]
    songs.at[song_id, "PLAYED"] = True

    return pick


def print_title(console):
    console.clear()
    console.print(
        ":sparkles:[bold italic green]NEW YEAR'S KARAOKE PARTY:sparkles:[/]:microphone::partying_face:"
    )


def print_welcome(console):
    print_title(console)
    with console.status(
        "Should we get started? :thinking_face:",
        spinner="christmas",
    ) as status:
        input()


def print_picking_singer(console, participant):
    with console.status(
        "Our next singer is... :man_dancing:",
    ) as status:
        playsound("drumroll.mp3")
        console.print(f"  Our next singer is[bold blue] {participant}[/] :man_dancing:")


def print_picking_song(console, song_lang):
    with console.status(
        "... who will be performing a song in... :notes:",
    ) as status:
        playsound("drumroll.mp3")
        console.print(
            f"  ... who will be performing a song in[bold blue] {song_lang} :notes:"
        )


def print_who_next(console):
    input()
    console.clear()
    print_title(console)
    console.print("[bold]  BRAVO! BRAAAAVVO!:clap::clap::clap:")
    console.print("  So who goes[blue bold] next?")
    input()


def print_goodbye(console):
    console.clear()
    console.print("BYE BYE :wave:")


if __name__ == "__main__":
    console = Console()
    try:
        try:
            reset = sys.argv[1].lower() in ["reset", "r"]
        except IndexError:
            reset = False
        print_welcome(console)

        while True:
            print_title(console)
            songs, participants = load_data(reset)
            participant = pick_participant(participants)
            print_picking_singer(console, participant["PARTICIPANT"])
            participant_languages = participant["LANGUAGE"].split(" ")
            song = pick_song(songs, participant_languages)
            print_picking_song(console, song["LANGUAGE"])
            save_data(songs, participants)
            webbrowser.open(song["LINK"])
            print_who_next(console)
    except KeyboardInterrupt:
        print_goodbye(console)
