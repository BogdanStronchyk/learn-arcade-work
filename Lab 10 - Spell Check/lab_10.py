import re
import time

# This function takes in a line of text and returns
# a list of words in the line.


def split_line(line):
    return re.findall('[A-Za-z]+(?:\'[A-Za-z]+)?', line)


def main():
    dictionary_list = []
    with open('dictionary.txt') as my_file0:
        for line in my_file0:
            dictionary_list.append(line.strip())

    print('--- Linear search ---')
    t1 = time.time()
    with open('AliceInWonderLand200.txt') as my_file1:
        iters = 0
        line_n = 0
        for line in my_file1:
            line_n += 1
            word_list = split_line(line)
            for word in word_list:
                i = 0
                while i < len(dictionary_list) and dictionary_list[i] != word.upper():
                    i += 1

                if i >= len(dictionary_list):
                    print(f'Line {line_n}: possible typo in word "{word}"')
                iters += i

    t2 = time.time()
# ----------------------

# ----------------------
    print('--- Binary search ---')
    t3 = time.time()
    with open('AliceInWonderLand200.txt') as my_file1:
        iters1 = 0
        line_n = 0
        for line in my_file1:
            line_n += 1
            word_list = split_line(line)
            for word in word_list:
                lower_boundary = 0
                upper_boundary = len(dictionary_list) - 1
                found = False

                while lower_boundary <= upper_boundary and not found:
                    mid_pos = (lower_boundary + upper_boundary) // 2
                    if dictionary_list[mid_pos] < word.upper():
                        lower_boundary = mid_pos + 1
                    elif dictionary_list[mid_pos] > word.upper():
                        upper_boundary = mid_pos - 1
                    else:
                        found = True
                    iters1 += 1

                if not found:
                    print(f'Line {line_n}: possible typo in word "{word}"')
    t4 = time.time()

    print(f'\nLinear search has been running for {t2 - t1:.2f} seconds. Trials made: {iters}.')
    print(f'Binary search has been running for {t4 - t3:.5f} seconds. Trials made: {iters1}.')
    print(f'Binary made {iters/iters1:.2f} times less trials and was {(t2 - t1)/(t4 - t3):.2f} times more quick.')


if __name__ == '__main__':
    main()

