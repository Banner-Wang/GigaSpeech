# Copyright 2021  Xiaomi Corporation (Author: Yongqing Wang)
#                 Xia GaoGao (Author: Banner Wang)

import sys
import os
import argparse
import json


def get_args():
    parser = argparse.ArgumentParser(description="""
      This script is used to process raw json dataset of GigaSpeech,
      where the long wav is splitinto segments and
      data of wenet format is generated.
      """)
    parser.add_argument('input_json', help="""Input json file of Gigaspeech""")
    parser.add_argument('output_dir', help="""Output dir for prepared data""")

    args = parser.parse_args()
    return args


def meta_analysis(input_json, output_dir):
    input_dir = os.path.dirname(input_json)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        with open(input_json, 'r') as injson:
            json_data = json.load(injson)
    except:
        sys.exit(f'Failed to load input json file: {input_json}')
    else:
        if json_data['audios'] is not None:
            with open(f'{output_dir}/test2subsets.json', 'w') as test2json, \
                    open(f'{output_dir}/dev2subsets.json', 'w') as dev2json:
                test_json_data = []
                dev_json_data = []
                for long_audio in json_data['audios']:
                    try:
                        long_audio_path = os.path.realpath(os.path.join(input_dir, long_audio['path']))
                        aid = long_audio['aid']
                        segments_lists = long_audio['segments']
                        assert (os.path.exists(long_audio_path))
                        assert ('opus' == long_audio['format'])
                        assert (16000 == long_audio['sample_rate'])
                    except AssertionError:
                        print(f'Warning: {aid} something is wrong, maybe AssertionError, skipped')
                        continue
                    except:
                        print(f'Warning: {aid} something is wrong, maybe the error path: {long_audio_path}, skipped')
                        continue
                    else:
                        for segment_file in segments_lists:
                            try:
                                test_dict_data = {}
                                dev_dict_data = {}
                                sid = segment_file['sid']
                                start_time = segment_file['begin_time']
                                end_time = segment_file['end_time']
                                text = segment_file['text_tn']
                                segment_subsets = segment_file["subsets"]
                            except:
                                print(f'Warning: {segment_file} something is wrong, skipped')
                                continue
                            else:
                                segment_sub_names = " ".join(segment_subsets)
                                if "TEST" in segment_sub_names:
                                    test_dict_data["sid"] = sid
                                    test_dict_data["path"] = long_audio_path
                                    test_dict_data["text_tn"] = text
                                    test_dict_data["begin_time"] = start_time
                                    test_dict_data["end_time"] = end_time
                                    test_json_data.append(test_dict_data)
                                elif "DEV" in segment_sub_names:
                                    dev_dict_data["sid"] = sid
                                    dev_dict_data["path"] = long_audio_path
                                    dev_dict_data["text_tn"] = text
                                    dev_dict_data["begin_time"] = start_time
                                    dev_dict_data["end_time"] = end_time
                                    dev_json_data.append(dev_dict_data)
                test2json.write(json.dumps(test_json_data))
                dev2json.write(json.dumps(dev_json_data))


def main():
    args = get_args()

    meta_analysis(args.input_json, args.output_dir)


if __name__ == '__main__':
    main()
