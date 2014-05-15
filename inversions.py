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
    list_length = len(number_list)
    a_list, b_list = split_list(number_list)
    a_list, a_inversions = sort_numbered_list(a_list)
    b_list, b_inversions = sort_numbered_list(b_list)
    merged_list, m_inversions = merge_lists(a_list, b_list, list_length)
    total_inversions = sum([a_inversions, b_inversions, m_inversions])
    print(merged_list)
    print("This list has", total_inversions, "total inversions")
    merged_list, total_inversions = merge_sort(number_list)
    save_number_list(merged_list, outputfile)

    print(a_list)
    print(b_list)
    print(merged_list)
    print("This list has", total_inversions, "total inversions")


def get_list_from_file(inputfile):
    """
    Read input file and return list
    """
    input_file = open(inputfile)
    file_list = input_file.read().split('\n')
    file_list = [int(num) for num in file_list if not num == '']
    return file_list


def split_list(input_list):
    half = int(len(input_list)/2)
    return input_list[:half], input_list[half:]


def sort_numbered_list(number_list, sorted_list=None, inversions=0, keep_sorting=True):
    if sorted_list is None:
        sorted_list = []

    # import pdb; pdb.set_trace()
    def sort_function(number_list, sorted_list, inversions):
        # loop through list and append to sorted list
        num = number_list[0]
        try:
            next_num = number_list[1]
            keep_sorting = True
        except IndexError:
            sorted_list.append(num)
            keep_sorting = False
            return sorted_list, number_list, inversions, keep_sorting

        if num < next_num:
            new_num = number_list.pop(0)
        else:
            new_num = number_list.pop(1)
            inversions += 1
        sorted_list.append(new_num)

        return sorted_list, number_list, inversions, keep_sorting

    if keep_sorting is True:
        sorted_list, number_list, inversions, keep_sorting = sort_function(
            number_list, sorted_list, inversions)
        return sort_numbered_list(number_list, sorted_list, inversions, keep_sorting)
    else:
        return sorted_list, inversions


def merge_lists(a_list, b_list, list_length):
    merged_list = []
    inversions = 0
    a_length = len(a_list)
    b_length = len(b_list)
    a = 0
    b = 0

    for k in range(0, list_length):
        if b == b_length:
            new_num = a_list[a]
            a += 1
        elif a == a_length:
            new_num = b_list[b]
            b += 1
            inversions += 1
        elif a_list[a] < b_list[b]:
            new_num = a_list[a]
            a += 1
        else:
            new_num = b_list[b]
            b += 1
            inversions += 1
        merged_list.append(new_num)

        if (a + b) == (list_length):
            return merged_list, inversions


def merge(left_list, right_list):
    i, j, inversions = 0, 0, 0
    merged_list = []
    import pdb; pdb.set_trace()
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


def merge_sort(number_list):
    if len(number_list) is 1:
        return number_list, 0
    middle = int(len(number_list)/2)
    # left_list, right_list = split_list(number_list)
    left_list = merge_sort(number_list[:middle])[0]
    right_list = merge_sort(number_list[middle:])[0]
    return merge(left_list, right_list)


def save_number_list(number_list, filename):
    out_file = open(filename, "wt")
    for num in number_list:
        out_file.write(str(num) + "\n")
    out_file.close()

if __name__ == "__main__":
    main(sys.argv[1:])
