"""Use this script to dump usernames : 10010year0xxx00"""
import json


def main():
    """main function"""
    usernames = ['11010' + str(year) + '0' + '{:03d}'.format(xxx) + '00'
                 for year in range(1965, 2018)
                 for xxx in range(1000)]
    with open('usernames.json', mode='w') as fp:
        json.dump(usernames, fp=fp, separators=(',', ':'), indent=4)


if __name__ == '__main__':
    main()
