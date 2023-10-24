import re

result = ""
with open('model_data.txt','r') as model:
    for line in model:
        line = line.replace("stddev","ts_std_dev")
        if line.find("A") != 0:
            result = result[:-1]
        result += line[0] + line[1:].lower()
print(result)

with open('model_data.txt','w') as model:
    model.write(result)


# Path to your text file
file_path = 'model_data.txt'

# Read the content of the file
with open(file_path, 'r') as file:
    file_content = file.read()

# # Use regular expression to replace 'adv' followed by digits with 'ts_mean(volume, x)'
# updated_content = re.sub(r'adv(?!20)\d+', lambda x: 'ts_mean(volume, ' + x.group()[3:] + ')', file_content)


# Regular expression to match float numbers after comma and space
# pattern = r',\s*([\d.]+)'

# # Function to convert float to nearest integer as string
# def convert_to_nearest_integer(match):
#     return ', ' + str(round(float(match.group(1))))

# # Use regular expression to replace float numbers after comma with nearest integers
# updated_content = re.sub(pattern, convert_to_nearest_integer, file_content)


# Use regular expression to replace 'adv' followed by digits with 'ts_mean(volume, x)'
updated_content = re.sub(r'Alpha#\d+:', '', file_content)

# Write the updated content back to the file
with open(file_path, 'w') as file:
    file.write(updated_content)

print("Replacement complete.")


