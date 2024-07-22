import subprocess
import string
# Desired value
desired_input1 = [-42148619422891531582255418903, -42148619422891531582255418927, -42148619422891531582255418851, -42148619422891531582255418907, -42148619422891531582255418831, -42148619422891531582255418859, -42148619422891531582255418855, -42148619422891531582255419111, -42148619422891531582255419103, -42148619422891531582255418687, -42148619422891531582255418859, -42148619422891531582255419119, -42148619422891531582255418843, -42148619422891531582255418687, -42148619422891531582255419103, -42148619422891531582255418907, -42148619422891531582255419107, -42148619422891531582255418915, -42148619422891531582255419119, -42148619422891531582255418935, -42148619422891531582255418823]


# Function to run the ./rust binary with input prompts
def run_rust(input1, input2):
    process = subprocess.Popen(['./rust'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    inputs = f"{input1}\n{input2}\n".encode()
    stdout, stderr = process.communicate(input=inputs)
    output = stdout.decode().strip()
    return output


def get_output_after_value(output, value):
    i = output.index(value)
    return output[i+len(value):]

"""
If we examine the rust::encrypt function, we could see that each value is independent.
So by figuring out key that gets us the first value, we can use the same key for the rest.
Since we know that the flag starts with `i`, and the encrypt is a simple math equation that
the output correspond to the key value, we can do a quick bruteforce to get the key.
"""

input1 = "ictf{"
index = len(input1)
desired_value = desired_input1[0]
i = 10**28
input2 = 10 ** 28
while True:
    output = get_output_after_value(run_rust(input1, str(input2)), 'Encrypted: ')
    print(output)
    print(input2)
    values = eval(output.split('\n')[0])
    diff = desired_value - values[0]
    if diff == 0:
        print("Desired input2 obtained:", input2)
        break
    elif abs(diff) < 1000:
        input2 += 1
        continue
    elif diff > 0:
        input2 -= i
        i //= 10
    input2 += i

"""
Now we have the key, let's run through the rust by looping through printable and try to match the next given output.
"""
while len(input1) < len(desired_input1):
    desired_value = str(desired_input1[:len(input1)+1]).rstrip(']')
    for i in string.printable:
        output = run_rust(input1 + i, str(input2))
        if desired_value in output:
            input1 += i
            print("Desired output obtained:", input1)
            break