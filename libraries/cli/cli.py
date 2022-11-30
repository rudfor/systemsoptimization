import argparse


class Cli():
    @staticmethod
    def cli(verbose=False):
        parser = argparse.ArgumentParser(description='Process Tasks')
        parser.add_argument('--csv', metavar='csv', default=None, help='add CSV')
        parser.add_argument('--seed', metavar='seed', default=999, help='provide random seed')
        parser.add_argument('-p', '--plot', action='store_true', help='activate Plotting')

        args = parser.parse_args()

        if verbose: print(args)

        return args