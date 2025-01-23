from .util import (
    progress_update,
    download,
    complete,
    _error,
    progress,
    progress2,
    getDefaultTitle,
)
from pytubefix import YouTube, Stream, Caption
from pytubefix.exceptions import PytubeFixError as PytubeError
from urllib.error import URLError
from pathlib import Path
import questionary
from typing import Iterable

global _ATTEMPTS
_ATTEMPTS = 1


def initialize(url: str) -> tuple[Stream, Iterable[Caption], str]:
    global _ATTEMPTS
    try:
        yt = YouTube(
            url=url,
            client="WEB",
            on_complete_callback=complete,
            on_progress_callback=progress_update,
        )
        stream = yt.streams.filter(progressive=True).get_highest_resolution()
        defaultTitle = getDefaultTitle(stream.title)

        captions = []
        if len(yt.captions) == 0:
            print("No caption available")
        elif len(yt.captions) > 1:
            caption_choices = questionary.checkbox(
                message="Select captions to download",
                choices=[
                    f"{code} ---- {yt.captions[code].name}"
                    for code in yt.captions.lang_code_index.keys()
                ],
            ).ask()
            for choice in caption_choices:
                code = choice.split("----", 1)[0].strip()
                captions.append(yt.captions.get(code))
        else:
            captions = yt.captions
        return stream, captions, defaultTitle + ".mp4"
    except URLError:
        if _ATTEMPTS < 4:
            print("\nConnection Error !!! Trying again ... ")
            _ATTEMPTS += 1
            return initialize(url)
        else:
            _error(Exception("Cannot connect to Youtube !!!"))
    except PytubeError as err:
        _error(err)


def get_srt_name(fname: str, code: str) -> str:
    filename = Path(fname).stem
    return f"{filename} ({code}).srt"


def get_video_srt(url: str, save_dir: Path):
    stream, captions, defaultTitle = initialize(url)
    with progress:
        progress.custom_add_task(
            title=stream.title, description=defaultTitle, total=stream.filesize
        )
        # print(f"Downloading {defaultTitle} - {stream.resolution}")
        download(stream, save_dir, defaultTitle)

    with progress2:
        id = progress2.add_task(
            "Downloading captions ... ", total=len(captions)
        )
        for cap in captions:
            # print(f"Downloading subtitle {cap.name} ")
            with open(
                save_dir.joinpath(get_srt_name(defaultTitle, cap.code)), "w"
            ) as file_handle:
                file_handle.write(cap.generate_srt_captions())
            progress2.update(id, advance=1)
            print(f"Successfully downloaded {cap.name} caption")


if __name__ == "__main__":
    pass
