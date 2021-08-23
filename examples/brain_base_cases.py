"""
THIS SCRIPT FILLS IN THE BRAIN WITH BASIC INFORMATION REGARDING EACH OF THE TEAM'S DEVELOPERS,
FOR EXAMPLE, WHERE THEY ARE FROM, WHAT THEY LIKE, AND WHERE THEY LIVE.
FOR MORE INFORMATION ON WHAT INFORMATION PLEASE REFER TO cltl.brain.utils.base_cases
"""

import pathlib

from cltl.brain.long_term_memory import LongTermMemory
from cltl.brain.utils.base_cases import statements

if __name__ == "__main__":
    # Create brain connection
    log_path = pathlib.Path.cwd().parent / 'src' / 'cltl' / 'brain' / 'logs'
    brain = LongTermMemory(address="http://localhost:7200/repositories/sandbox",
                           log_dir=log_path,
                           clear_all=True)

    for statement in statements:
        # Add information to the brain
        response = brain.update(statement, reason_types=True)
        print(f"\n\n---------------------------------------------------------------\n{statement['triple']}\n")
