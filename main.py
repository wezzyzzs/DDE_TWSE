import sys
sys.path.append('./libs')

from libs.base import Executor


def main():
    runner = Executor('')
    runner.execute()



    
if __name__ =='__main__':
    main()