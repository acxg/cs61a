"""Typing test implementation"""

from utils import *
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1
    cnt = -1
    for par in paragraphs:
        if select(par):
            cnt = cnt + 1  
            if cnt == k:
                return par
    if cnt < k:
       return ''
    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    def check(string):
        lst = split(lower(remove_punctuation(string)))
        for par in lst:
            for che in topic:
                if che == par:
                    return True
        return False 
    return check 
    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    den = len(typed_words)
    if den == 0:
        return 0.0
    num = 0
    comp = min(len(typed_words),len(reference_words))
    for cnt in range(comp):
        if typed_words[cnt] == reference_words[cnt]:
            num = num + 1
    return 100.0*(num/den)
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    den = len(typed)/5.0
    if den == 0:
        return 0.0
    return den*(60/elapsed) 
    # END PROBLEM 4


def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.
    """
    # BEGIN PROBLEM 5
    if user_word in valid_words:
        return user_word
    min_word = min(valid_words, key = lambda x: diff_function(user_word, x, limit))
    if diff_function(user_word, min_word, limit) <= limit:
        return min_word
    else:
        return user_word       
    # END PROBLEM 5


def swap_diff(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6
    def helper(start, goal, limit, cnt):
        if cnt > limit:
            return cnt
        if start == '' or goal == '':
            return cnt + abs(len(start)-len(goal))
        if start[0] == goal[0]:
            return helper(start[1:], goal[1:], limit, cnt)
        else:
            return helper(start[1:], goal[1:], limit, cnt+1)
    return helper(start, goal, limit, 0)
    # END PROBLEM 6

def edit_diff(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL."""
    def dif(start, goal, cnt):
        """function that calculates the distance between two words"""
        if start == '' or goal == '': 
            return cnt + abs(len(start) - len(goal))
        elif start[0] == goal[0]:
            return dif(start[1:], goal[1:], cnt)
        else:
            return dif(start[1:], goal[1:], cnt+1)

    def helper(start, goal, limit, cnt):
        if cnt > limit or start == goal: 
            return cnt
        min_change = min(rm, ad, rep, key = lambda f: f(start, goal)[1])
        if start == '' or goal == '' or start[0] != goal[0]:
            start = min_change(start, goal)[0]
            return helper(start, goal, limit, cnt+1)
        else:
            return helper(start[1:], goal[1:], limit, cnt)
            
    def rm(start, goal):
        if start != '':
            start = start[1:]
            return start, dif(start, goal, 0)
        else: 
            return start, 2**32-1
    def ad(start, goal):
        if goal != '':
            start = goal[0]+start
            return start, dif(start, goal, 0)
        else:
            return start, 2**23-1

    def rep(start, goal):
        if goal != '':
            start = goal[0] + start[1:]
            return start, dif(start, goal, 0)
        else: 
            return start, 2**23-1

    return helper(start, goal, limit, 0)


def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'




###########
# Phase 3 #
###########


def report_progress(typed, prompt, id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    def send(dic):
        print('ID:', dic['id'],'Progress:',dic['progress'])
    cnt = 0
    min_len = min(len(typed),len(prompt))
    for i in range(min_len):
        if typed[i] == prompt[i]:
            cnt += 1
        else:
            break
    progress = 1.0*(cnt/len(prompt))
    dic = {}
    dic['id'] = id
    dic['progress'] = progress
    send(dic)
    return progress
    # END PROBLEM 8


def fastest_words_report(word_times):
    """Return a text description of the fastest words typed by each player."""
    fastest = fastest_words(word_times)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def fastest_words(word_times, margin=1e-5):
    """A list of which words each player typed fastest."""
    n_players = len(word_times)
    n_words = len(word_times[0]) - 1
    assert all(len(times) == n_words + 1 for times in word_times)
    assert margin > 0
    # BEGIN PROBLEM 9
    res = []
    for j in range(n_players):
        res.append([])
    for i in range(1,n_words+1):
        cur_word = word(word_times[0][i])
        fast_time = elapsed_time(word_times[0][i])-elapsed_time(word_times[0][i-1])
        for j in range(1,n_players):
            cur_time = elapsed_time(word_times[j][i])-elapsed_time(word_times[j][i-1])
            if fast_time > cur_time:
                fast_time = cur_time
        t_w = fast_time + margin
        for j in range(n_players):
            dur = elapsed_time(word_times[j][i]) - elapsed_time(word_times[j][i-1])
            if dur < t_w:
                res[j].append(cur_word)
    return res
    # END PROBLEM 9


def word_time(word, elapsed_time):
    """A data abstrction for the elapsed time that a player finished a word."""
    return [word, elapsed_time]
    

def word(word_time):
    """An accessor function for the word of a word_time."""
    return word_time[0]


def elapsed_time(word_time):
    """An accessor function for the elapsed time of a word_time."""
    return word_time[1]


enable_multiplayer = True  # Change to True when you


##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)
