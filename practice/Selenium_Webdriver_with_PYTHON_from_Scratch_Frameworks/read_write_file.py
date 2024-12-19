# Print line by line
def read_lines(filename):
    my_list = []
    with open(filename) as f:
        for line in f:
            my_list.append(line.strip('\n'))
    return my_list

def write_lines(filename, my_list, direction):
    my_list = my_list if direction == 'forward' else my_list[::-1]
    with open(filename, 'w') as f:
        for line in my_list:
            f.write(line)
            f.write('\n')

def file_manager(filename, mode, direction='forward'):
    if mode == 'r':
        read_list = read_lines(filename)
        print(read_list)
    elif mode == 'w':
        read_list = read_lines(filename)
        write_lines(filename, read_list, direction)



# file = open("test_text.txt")
# #print(file.read())  # Read all the file content
# #print(file.read(2))  # Read just first 2 characters
# #print(file.readline())  # Read a line
# #print(file.readline())  # Read next line
# local_list = read_lines(file)
# single_str = ";".join(local_list)
# print(f"\nMy local list is:  {single_str}")
# file.close()
my_text_file = "test_text.txt"
print(f"----------Reading file : {my_text_file} before modification")
file_manager(my_text_file, 'r')
print(f"----------Writing file : {my_text_file}")
file_manager(my_text_file, 'w', "backward")
print(f"---------Reading file : {my_text_file} after modification")
file_manager(my_text_file, 'r')
