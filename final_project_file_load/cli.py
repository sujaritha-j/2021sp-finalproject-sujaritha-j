from argparse import ArgumentParser

from dotenv import load_dotenv
from luigi import WrapperTask, Parameter
from luigi import build

from .tasks import DataDownloadTask


class MainTask(WrapperTask):
    """
    Wrapper Task to trigger individual analysis task
    """
    s3_data_path = Parameter()
    s3_output_path = Parameter()

    def requires(self):
        return{
            'data_download': DataDownloadTask(self.s3_data_path, self.s3_output_path)
        }


def main():
    """
    Read command line arguments --full -> to select entire dataset
    --canvas_submit  -> to submit the assignment
    :return: None
    """
    parser = ArgumentParser()
    parser.add_argument('--full', action='store_false')
    args = parser.parse_args()
    subset = args.full
    load_dotenv()
    s3_data_path = 's3://finalproject-spring-2021/data/*.csv'
    s3_output_path = 's3://finalproject-spring-2021/output/'
    build([
        MainTask(s3_data_path=s3_data_path, s3_output_path=s3_output_path)
    ], local_scheduler=True)
    print('-----File load complete------')
