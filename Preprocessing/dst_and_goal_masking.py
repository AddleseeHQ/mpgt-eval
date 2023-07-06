import os
import random
import json
import argparse
import numpy as np
from time import time
from os.path import join, exists
from nltk import word_tokenize, sent_tokenize
from datetime import timedelta

# tokenize a turn
def tokenize(sent):
    return ' '.join(word_tokenize(sent))

# return the number of the tokens in a long dialogue
def token_num(data):
    cnt = 0
    for i in range(len(data)):
        cnt += len(data[i].split())
    return cnt

# find the last possible position of the starting point of the noised window
def last_position(data, window_size):
   n = len(data)
   cnt = 0
   for i in range(n - 1, -1, -1):
        cnt += len(data[i].split())
        if cnt > window_size:
            return i

def find_str(s, s_target):
    for i in range(len(s)):
        if s[i] == s_target:
            return i

def dst_mask(data):
    new_data = []
    for i in range(len(data)):
        s = data[i].split()
        cur = []
        if '#' not in str(s):
            for j in range(len(s)):
                cur.append(s[j])
            new_data.append(' '.join(cur))
        else:
            idx = find_str(s, '#')
            if '@' not in str(s):
                for j in range(0, idx):
                    cur.append(s[j])
                cur.append('[MASK]')
                new_data.append(' '.join(cur))
            else:
                idx_g = find_str(s, '@')
                for j in range(0, idx):
                    cur.append(s[j])
                cur.append('[MASK]')
                for k in range(idx_g, len(s)):
                    cur.append(s[k])
                new_data.append(' '.join(cur))
    return new_data

def goal_mask(data):
    new_data = []
    for i in range(len(data)):
        s = data[i].split()
        cur = []
        if '@' not in str(s):
            for j in range(len(s)):
                cur.append(s[j])
            new_data.append(' '.join(cur))
        else:
            idx = find_str(s, '@')
            for j in range(0, idx):
                cur.append(s[j])
            cur.append('[MASK]')
            new_data.append(' '.join(cur))
    return new_data

# [start]: the start point of the noised window
# [end]: the end point of the noised window
def add_special_token(data):
    data[0] = '[start] ' + data[0]
    data[len(data) - 1] = data[len(data) - 1] + ' [end]'
    return data

def add_noise(data, window_size):
    st_idx = 0
    ed_idx = last_position(data, window_size)
    # the start point of the window
    window_st = random.randint(st_idx, ed_idx)
    # the end point of the window
    window_ed = window_st
    # the number of words in the window
    window_cnt = 0
    window_data = []
    for i in range(window_st, len(data)):
        if window_cnt + len(data[i].split()) > window_size:
            break
        window_cnt += len(data[i].split())
        window_data.append(data[i])
        window_ed = i
    # can not find a suitable window in this dialogue
    if len(window_data) == 0:
        return -1, -1
    
    noise_data = window_data
    
    if '#' in str(noise_data) and args.dst_mask_switch:
        noise_data = dst_mask(noise_data)
    # then goal mask if goals in window and needed
    if '@' in str(noise_data) and args.goal_mask_switch:
        noise_data = goal_mask(noise_data)
    noise_data = add_special_token(noise_data)
    source = []
    have_window = 0
    for i in range(len(data)):
        if i >= window_st and i <= window_ed:
            if have_window == 0:
                for j in range(len(noise_data)):
                    source.append(noise_data[j])
                have_window = 1
        else:
            source.append(data[i])
    return source, window_data

def to_json(src, tgt):
    cur = {}
    cur['src'] = ' '.join(src)
    cur['tgt'] = ' '.join(tgt)
    return cur

def write_jsonl(data, path):
    processed_path = join(join(path, '..'), 'processed_dialogues')
    if not exists(processed_path):
        os.makedirs(processed_path)
    dialogue_path = join(processed_path, 'dialogue_with_noised_window.jsonl')
    print(dialogue_path)
    assert not exists(dialogue_path)
    with open(dialogue_path, 'w') as f:
        for i in range(len(data)):
            print(json.dumps(data[i], ensure_ascii=False), file=f)

def main(args):
    
    dialogues = os.listdir(args.data_path)
    n = len(dialogues)
    print('Total of {} dialogues to be processed'.format(n))

    start = time()
    all_dialogues = []
    for i in range(n):
        dialogue = dialogues[i]
        data = []
        with open(join(args.data_path, dialogue)) as f:
            for line in f:
                data.append(tokenize(line.strip()))
        cnt = token_num(data)
        src, tgt = add_noise(data, min(args.max_window_words, 
                                       int(cnt * args.window_ratio)))
        if src == -1 and tgt == -1:
            continue
        all_dialogues.append(to_json(src, tgt))
        print('{}/{} ({:.2f}%) processed in {} seconds\r'.format(
               i, n, i/n*100, timedelta(seconds=int(time()-start))), end='')

    print('\nFinished data processing and start writing data !!!')
    write_jsonl(all_dialogues, args.data_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Randomly select a window in a long dialogue \
                     and execute dst and goal masking'
    )

    parser.add_argument('--data_path', default='data/dialogues',
        help='Path to the long dialogue data', type=str)
    parser.add_argument('--window_ratio', default=0.7,
        help='Ratio of the original dialogue as a noised window', type=float)
    parser.add_argument('--max_window_words', default=500,
        help='Maximum number of words in the window', type=int)
    parser.add_argument('--dst_mask_switch', default=False,
        help='Whether dialogue states in the window will be masked', type=bool)
    parser.add_argument('--goal_mask_switch', default=False,
        help='Whether goals in the window will be masked', type=bool)

    args = parser.parse_args()

    main(args)