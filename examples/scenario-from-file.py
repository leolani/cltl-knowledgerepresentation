import argparse
import datetime
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from tqdm import tqdm

from cltl.brain import LongTermMemory


def readCapsuleFromFile(jsonfile):
    f = open(jsonfile, )
    scenario = json.load(f)
    return scenario


def main(log_path):
    # Create brain connection
    brain = LongTermMemory(address="http://localhost:7200/repositories/sandbox",
                           log_dir=log_path,
                           clear_all=False)
    # Read scenario from file
    scenario_file_name = 'carlani-4.json'
    scenario_json_file = 'capsules/' + scenario_file_name
    scenario = readCapsuleFromFile(scenario_json_file)

    for capsule in tqdm(scenario['scenario']):
        print(f"\n\n---------------------------------------------------------------\n")

        capsule['date'] = datetime.datetime.strptime(capsule['date'], "%Y:%m:%d")

        if capsule['speech-act'] == 'statement':
            x = brain.update(capsule, reason_types=True, create_label=True)

            print(f'\n{capsule["triple"]}\n')
        else:
            sa = capsule['speech-act']
            print(f'\n{sa}\n')

        print(capsule)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Carl-Leolani scenario')
    parser.add_argument('--logs', type=str,
                        help="Directory to store the brain log files. Must be specified to persist the log files.")
    args, _ = parser.parse_known_args()

    if args.logs:
        main(Path(args.logs))
    else:
        with TemporaryDirectory(prefix="brain-log") as log_path:
            main(Path(log_path))
