import logging
def init_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s:%(name)s - %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S',
        )
    

# add parent path
import sys
import os

def add_parent_path(
    up_levels:int=1
    ):
    current_path = os.getcwd()
    for _ in range(0,up_levels,1):
        current_path = os.path.dirname(current_path)
    sys.path.append(current_path)


from decouple import config
def get_credentials():
    user = config('USER_GPM')
    pssw = config('PSSW_GPM')
    return user,pssw


if __name__=='__main__':
    init_logging()
    add_parent_path(up_levels=1)
    user,pssw = get_credentials()
