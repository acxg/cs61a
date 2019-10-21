def mario_number(level):
    if level == '-' or level == '--':
        return 1
    elif level[-3:] == 'P--':
        return mario_number(level[:-1])
    elif level[-3:] == '---':
        return mario_number(level[:-1]) + mario_number(level[:-2])
    elif level[-3:] == '-P-':
        return mario_number(level[:-2])
    else:
        return 0

print(mario_number('-P-P-'))
print(mario_number('-P-P--'))
print(mario_number('--P-P-'))
print(mario_number('---P-P-'))
print(mario_number('-P-PP-'))
print(mario_number('----'))
print(mario_number('----P----'))
print(mario_number('---P----P-P---P--P-P----P-----P-'))
