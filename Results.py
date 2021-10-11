import re

name = str(input("Enter the name of the results.txt file to use, excluding the file extension.\n"))
file = open(name + ".txt", "r+")
create_arr = []
write_arr = []
read_arr = []
open_arr = []
modify_arr = []
resize_arr = []
append_arr = []
for lines in file:
    if "Create" in lines:
        create_arr.append(re.findall(r"\d+\.\d+", lines)[0])
    elif "Write" in lines:
        write_arr.append(re.findall(r"\d+\.\d+", lines)[0])
    elif "Open" in lines:
        open_arr.append(re.findall(r"\d+\.\d+", lines)[0])
    elif "Read" in lines:
        read_arr.append(re.findall(r"\d+\.\d+", lines)[0])
    elif "Modify" in lines:
        modify_arr.append(re.findall(r"\d+\.\d+", lines)[0])
    elif "Resize" in lines:
        resize_arr.append(re.findall(r"\d+\.\d+", lines)[0])
    elif "Append" in lines:
        append_arr.append(re.findall(r"\d+\.\d+", lines)[0])


def print_array(arr):
    for i in arr:
        print(i)
    print()


write_arr.insert(0, create_arr[0])
read_arr.insert(0, open_arr[0])
modify_arr.insert(0, open_arr[1])
resize_arr.insert(0, open_arr[2])

print_array(write_arr)
print_array(read_arr)
print_array(modify_arr)
print_array(resize_arr)
print_array(append_arr)
