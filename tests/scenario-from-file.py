import datetime
import json
import pathlib

from cltl.brain import LongTermMemory
from utils import transform_capsule


def readCapsuleFromFile (jsonfile):
    f = open(jsonfile, )
    scenario = json.load(f)
    return scenario

if __name__ == "__main__":

    # Create brain connection
    log_path = pathlib.Path.cwd().parent / 'src' / 'cltl' / 'brain' / 'logs'
    scenario_file_name = 'carlani-4.json'
    scenario_json_file = 'capsules/' + scenario_file_name
    brain = LongTermMemory(address="http://localhost:7200/repositories/sandbox",
                           log_dir=str(log_path),
                           clear_all=False)
    scenario = readCapsuleFromFile(scenario_json_file)
    for capsule in scenario['scenario']:
        # Create Utterance object
        #datetime.date(2021, 3, 12)
        capsule['date']= datetime.datetime.strptime(capsule['date'], "%Y:%m:%d")
        print(capsule)
        if capsule['speech-act']=='statement':
            utterance = transform_capsule(capsule)
            x = brain.update(utterance, reason_types=True)

            print(f'\n\n---------------------------------------------------------------\n{utterance.triple}\n')
        else:
            sa = capsule['speech-act']
            print(f'\n\n---------------------------------------------------------------\n{sa}\n')

