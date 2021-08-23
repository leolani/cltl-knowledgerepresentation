import datetime
import json
import pathlib

from cltl.brain import LongTermMemory


def readCapsuleFromFile(jsonfile):
    f = open(jsonfile, )
    scenario = json.load(f)
    return scenario


if __name__ == "__main__":

    # Create brain connection
    log_path = pathlib.Path.cwd().parent / 'src' / 'cltl' / 'brain' / 'logs'
    brain = LongTermMemory(address="http://localhost:7200/repositories/sandbox",
                           log_dir=log_path,
                           clear_all=False)

    # Read scenario from file
    scenario_file_name = 'carlani-4.json'
    scenario_json_file = 'capsules/' + scenario_file_name
    scenario = readCapsuleFromFile(scenario_json_file)

    for capsule in scenario['scenario']:
        capsule['date'] = datetime.datetime.strptime(capsule['date'], "%Y:%m:%d")

        if capsule['speech-act'] == 'statement':
            x = brain.update(capsule, reason_types=True)

            print(f'\n\n---------------------------------------------------------------\n{capsule["triple"]}\n')
        else:
            sa = capsule['speech-act']
            print(f'\n\n---------------------------------------------------------------\n{sa}\n')

        print(capsule)
