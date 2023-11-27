import re

file_to_read = open("XDATCAR_NEW", "r")
new_XDATCAR = file_to_read.read()
file_to_read.close()

replace_phrase = r'(Direct configuration=\s+)(\d+)'
replacement_counter = 1

# Define a function for replacement
def repl_func(match):
    global replacement_counter
    old_number = match.group(2)
    new_number = str(replacement_counter)
    replacement_counter += 1
    return match.group(1) + new_number

replacement_counter = 1

new_XDATCAR = re.sub(replace_phrase, repl_func, new_XDATCAR)

new_file = open("XDATCAR_COMBINED", "w")
new_file.write(new_XDATCAR)
new_file.close()

print("Done!")
