import pathlib
import whisper
from datetime import timedelta
from time import sleep
from tqdm import tqdm
import googletrans
from config import *


def make_subtitle(segments):
    translator = googletrans.Translator()
    subtitle = ""
    srt_zh_cn = ""
    srt_zh_tw = ""
    combined_en_tw = ""
    for segment in segments:
        text = segment['text']
        try:
            text_cn = translator.translate(text, src='en', dest='zh-cn').text
            # text_tw = translator.translate(text, src='en', dest='zh-tw').text
        except:
            text_cn = ''
        try:
            # text_cn = translator.translate(text, src='en', dest='zh-cn').text
            text_tw = translator.translate(text, src='en', dest='zh-tw').text
        except:
            text_tw = ''
        subtitle += str(segment['id'] + 1)
        subtitle += '\n'
        subtitle += str(timedelta(seconds=round(segment['start']))) + ',000'
        subtitle += ' --> '
        subtitle += str(timedelta(seconds=round(segment['end']))) + ',000'
        subtitle += '\n'
        subtitle += text
        subtitle += '\n\n'

        srt_zh_cn += str(segment['id'] + 1)
        srt_zh_cn += '\n'
        srt_zh_cn += str(timedelta(seconds=round(segment['start']))) + ',000'
        srt_zh_cn += ' --> '
        srt_zh_cn += str(timedelta(seconds=round(segment['end']))) + ',000'
        srt_zh_cn += '\n'
        srt_zh_cn += text_cn
        srt_zh_cn += '\n\n'

        srt_zh_tw += str(segment['id'] + 1)
        srt_zh_tw += '\n'
        srt_zh_tw += str(timedelta(seconds=round(segment['start']))) + ',000'
        srt_zh_tw += ' --> '
        srt_zh_tw += str(timedelta(seconds=round(segment['end']))) + ',000'
        srt_zh_tw += '\n'
        srt_zh_tw += text_tw
        srt_zh_tw += '\n\n'

        combined_en_tw += str(segment['id'] + 1)
        combined_en_tw += '\n'
        combined_en_tw += str(timedelta(seconds=round(segment['start']))) + ',000'
        combined_en_tw += ' --> '
        combined_en_tw += str(timedelta(seconds=round(segment['end']))) + ',000'
        combined_en_tw += '\n'
        combined_en_tw += text + "\n" + text_tw
        combined_en_tw += '\n\n'
        sleep(2)
    return subtitle, srt_zh_cn, srt_zh_tw, combined_en_tw


if __name__ == '__main__':

    root_folder = pathlib.Path(video_location)
    file_list = list(root_folder.glob('*.mp4'))

    model = whisper.load_model("medium", download_root=model_location, device=device_model)

    for file_name in tqdm(file_list):
        result = model.transcribe(str(file_name))
        srt, srt_zh_cn, srt_zh_tw, srt_en_tw = make_subtitle(result['segments'])

        with open(str(file_name).replace(".mp4", ".srt"), "w") as fl:
            fl.write(srt)

        with open(str(file_name).replace(".mp4", "_zh_cn.srt"), "w", encoding="utf-8") as fl:
            fl.write(srt_zh_cn)

        with open(str(file_name).replace(".mp4", "_zh_tw.srt"), "w", encoding="utf-8") as fl:
            fl.write(srt_zh_tw)

        with open(str(file_name).replace(".mp4", "_en_tw.srt"), "w", encoding="utf-8") as fl:
            fl.write(srt_en_tw)

        with open(str(file_name).replace(".mp4", ".txt"), "w") as fl:
            fl.write(result['text'])

        sleep(10)
