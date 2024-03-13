import argparse
import json
import os
import sys


def get_args():
    parser = argparse.ArgumentParser(description="""
      This script is used to process raw json dataset of GigaSpeech,
      where the long wav is splitinto segments and
      data of kaldi format is generated.
      """)
    parser.add_argument('input_json', help="""Input json file of Gigaspeech""")
    parser.add_argument('output_txt', help="""Output txt file for prepared data""")

    args = parser.parse_args()
    return args


def opus_split_to_wav(opus_path, sub_wav_path, start_time, end_time, target_sr=16000):
    if os.path.isfile(sub_wav_path):
        return
    cmd = f'ffmpeg -y -i {opus_path} -ss {start_time} -to {end_time} -ar {target_sr} {sub_wav_path}'
    try:
        os.system(cmd)
    except:
        sys.exit(f'Failed to run the cmd: {cmd}')


def prepare_data(input_json, output_txt):
    try:
        with open(input_json, 'r') as injson:
            json_data = json.load(injson)
    except:
        sys.exit(f'Failed to load input json file: {input_json}')
    else:
        if json_data is not None:
            with open(output_txt, 'w') as out_file:
                for item in json_data:
                    try:
                        sid = item["sid"]
                        path = item["path"]
                        text_tn = item["text_tn"]
                        begin_time = item["begin_time"]
                        end_time = item["end_time"]
                    except:
                        print(f'Warning: {item} something is wrong, skipped')
                        continue
                    else:
                        audio_dir = os.path.dirname(path)
                        sub_wav_path = f"{audio_dir}/{sid}.wav"
                        opus_split_to_wav(path, sub_wav_path, begin_time, end_time)
                        out_file.write(f"{sub_wav_path} {text_tn}\n")


def main():
    args = get_args()

    prepare_data(args.input_json, args.output_txt)


if __name__ == '__main__':
    main()
