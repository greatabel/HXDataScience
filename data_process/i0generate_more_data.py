import argparse
from i0csv_operation import csv_write, csv_reader


def main():
    parser = argparse.ArgumentParser(description="process video/image")
    parser.add_argument(
        "--times",
        type=int,
        default=1,
        help="choose how many times of original file you want to generate",
    )

    # parser.add_argument('--debug', type=bool, default=False,
    #                     help='use debug mode')

    args = parser.parse_args()
    times = args.times
    print('multiple times=', times)

    # global times
    # source_demo.csv 's count is 100
    sourcelist = csv_reader("source_demo.csv")
    # print(len(sourcelist))
    lastrow = sourcelist[-1]
    i = int(lastrow[0])

    csv_write("genreated_demo.csv", sourcelist)
    print("original turn added")
    del sourcelist[0]
    for i_turn in range(0, times - 1):
        print(i_turn, " turn added")

        for idx, val in enumerate(sourcelist):
            # print(idx, val)
            if idx != 0:
                i += 1
                sourcelist[idx][0] = i
        csv_write("genreated_demo.csv", sourcelist, "a")


if __name__ == "__main__":
    main()
