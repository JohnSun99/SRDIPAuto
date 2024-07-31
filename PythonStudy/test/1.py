import random
while True:
    low_random = 100; high_random = 999
    random_number = int(random.uniform(low_random, high_random))
    s_random_number = str(random_number)
    print ('Do you want to overwrite the port configuration and continue?')
    input_message = " type '" + s_random_number + "' for yes, or type 'no' to exiting:"
    your_input = input(input_message)
    print (your_input)
    if your_input == s_random_number:
        print('yes')
        break
    elif your_input == 'no':
        print('no')
        exit()
