import sys
import getopt


def main(argv):
    # Set input and output files
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "h:i:o:l:")
    except getopt.GetoptError:
        print('inversions.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    # exit program if both input and output files not provided
    if not (inputfile and outputfile):
        print('inversions.py -i <inputfile> -o <outputfile>')
        sys.exit(2)

    # get list from input file
    number_list = get_list_from_file(inputfile)
    merged_list, total_inversions = merge_sort(number_list)
    save_number_list(merged_list, outputfile)

    if len(number_list) < 100:
        print(number_list)
        print(merged_list)
    else:
        print("List too long, check output file.")

    print("This list has", total_inversions, "total inversions")


def get_list_from_file(inputfile):
    """
    Read input file and return list
    """
    input_file = open(inputfile)
    file_list = input_file.read().split('\n')
    file_list = [int(num) for num in file_list if not num == '']
    return file_list


def merge(left_list, right_list, inversions=0):
    i, j = 0, 0
    merged_list = []
    while i < len(left_list) and j < len(right_list):
        if left_list[i] < right_list[j]:
            merged_list.append(left_list[i])
            i += 1
        else:
            merged_list.append(right_list[j])
            j += 1
            inversions += len(left_list[i:])
    merged_list += left_list[i:]
    merged_list += right_list[j:]
    return merged_list, inversions


def merge_sort(number_list, inversions=0):
    if len(number_list) is 1:
        return number_list, 0
    middle = int(len(number_list)/2)
    # left_list, right_list = split_list(number_list)
    left_list, l_inversions = merge_sort(number_list[:middle])
    right_list, r_inversions = merge_sort(number_list[middle:])
    inversions = l_inversions + r_inversions
    return merge(left_list, right_list, inversions)


def save_number_list(number_list, filename):
    out_file = open(filename, "wt")
    for num in number_list:
        out_file.write(str(num) + "\n")
    out_file.close()

if __name__ == "__main__":
    main(sys.argv[1:])
