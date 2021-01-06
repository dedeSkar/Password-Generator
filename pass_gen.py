import random, string, os, requests

def clr_scr():
    os.system('cls' if os.name=='nt' else 'clear')

#this function makes user's config
def user_pass_gen_config():
    user_config = {} 
    clr_scr()
    user_config['include_sym'] = user_config['include_numbers'] = 'n'
    user_config['gen_method']= input("""_____--------Simple_Password_Generator--------_____
_______________________________________________________________________
Choose between 3 methods of generating passwords
--1. Method _MNEMONICS_
----1.1 Example:
        user choisen word: Lopas
        L - Lithuania
        O - Ocean
        P - Parrot
        A - Ascend
        S - Survive
        Scambles it in meaningful intervals and adds a date
        liThuAn1iAoce9AnpaRrota9ScendSs8uRvive
_______________________________________________________________________
--2. Method _String-Distortion_
----2.1 Example:
        user choisen word: Lopas
        output: l8P@s
_______________________________________________________________________
--3. Method _Randomly-Generated_

type 1,2 or 3 to choose method: """)
    if user_config['gen_method'] == '2' or user_config['gen_method'] == '3':
        if user_config['gen_method'] == '3':
            user_config['lenght'] = input('How long does your password need to be? type a number: ')
            user_config['exclude_s_letters'] = input('Does your password need similar letters excluded y/n?: ') 
        user_config['include_numbers'] = input('Does your password need numbers? y/n: ')
        user_config['include_sym'] = input('Does your password need symbols y/n?: ')
    if user_config['gen_method'] == '2' or user_config['gen_method'] == '1':
        user_config['user_string'] = input('Enter a word that you want to use for password: ')
        if user_config['gen_method'] == '1': user_config['user_date'] = input('Enter a date of 4 digits that you want to use for password: ')
    user_config['include_upper'] = input('Does your password need uppercase letters y/n: ')
    return user_config

def string_distortion(user_string, user_config):
    gen_password = list(user_string)
    for i in range(0, len(gen_password)):
        if random.randint(0,100) > 60:
            random_number = random.randint(0,100)
            if random_number <= 33:
                gen_password[i] = random.choice(string.ascii_letters)
            elif random_number >= 34 and random_number < 67 and user_config['include_numbers'] == 'y':
                gen_password[i] = random.choice(string.digits)
            elif random_number >= 67 and user_config['include_sym'] == 'y':
                gen_password[i] = random.choice(string.punctuation)
    gen_password = "".join(gen_password)
    return gen_password

def mnemonics_generator(user_config):
    main_string = ''
    for i in range(0, len(user_config['user_string'])):
        while True:
            #todo find a faster and better API and use a better method for finding words
            r = requests.get(f'https://random-word-api.herokuapp.com/word?number=1')
            word_data = r.json()
            word = word_data[0] 
            u_string = user_config['user_string'].lower()
            if word[0] == u_string[i]:
                main_string += word
                break
    main_string = string_distortion(main_string, user_config)        
    main_string = list(main_string)
    date = user_config['user_date']
    for i in range(0, len(user_config['user_date'])):
        random_number = random.randint(0, len(main_string))
        main_string.insert(random_number, date[i])
    main_string = "".join(main_string)
    return main_string

def random_generation(user_config):
    gen_password = ''
    similar_letters_list = ['i', 'I', 'L', 'l', 'O', 'o']
    for i in range(0, int(user_config['lenght'])):
        gen_password += random.choice(string.ascii_letters)
        while True:
            if user_config['exclude_s_letters'] == 'y' and gen_password[i] in similar_letters_list:
                gen_password = gen_password[:-1]
                gen_password += random.choice(string.ascii_letters)
            else:
                break
        if random.randint(0,100) > 70 and user_config['include_numbers'] == 'y':
            gen_pass_list= list(gen_password)
            gen_pass_list[i] = str(random.choice(string.digits))
            gen_password = "".join(gen_pass_list)
        if random.randint(0,100) > 80 and user_config['include_sym'] == 'y':
            gen_pass_list= list(gen_password)
            gen_pass_list[i] = str(random.choice(string.punctuation))
            gen_password = "".join(gen_pass_list)   
    return gen_password

def check_if_all_included(gen_password, user_config):
    upper_list = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numbers = sym = upper = 'n'
    for i in range(0, len(gen_password)): 
        if gen_password[i] in string.digits: numbers = 'y'
        if gen_password[i] in string.punctuation: sym ='y'
        if gen_password[i] in upper_list: upper ='y'
    if numbers == user_config['include_numbers'] and sym == user_config['include_sym'] and upper == user_config['include_upper']:
        return True
    else:
        return False


def main_user_pass_gen(user_config):
    user_string = user_config['user_string']
    if user_config['gen_method'] == '1': gen_password = mnemonics_generator(user_config)
    else:
        while True:
            if user_config['gen_method'] == '2': gen_password = string_distortion(user_string, user_config)
            elif user_config['gen_method'] == '3': gen_password = random_generation(user_config)
            if check_if_all_included(gen_password, user_config) == True:
                break
    if user_config['include_upper'] =='n': gen_password = gen_password.lower()
    return gen_password

print('Password:', main_user_pass_gen(user_pass_gen_config()))
