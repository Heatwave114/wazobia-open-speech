# Core
import csv
import copy
import os
import re
import sys
from pathlib import Path

# External
from num2words import num2words

# Internal
from resource import resources

new_resources = resources.copy()
r = new_resources[0]


def tokenize_text(resource=r, r_id=None):
    rsrc = []
    resource = copy.deepcopy(r)
    if r_id is not None:
        rsrc = list(filter(lambda x: x.uid == r_id, new_resources))
    if len(rsrc) == 1:
        resource = copy.deepcopy(rsrc[0])
    count = 0
    while True:
        first_match = re.search(r' +|\s+', resource.text)
        if first_match is not None:
            p, q = first_match.span()
            resource.text = resource.text[:p] + \
                '__!i{}__'.format(count) + resource.text[q:]
        else:
            break
        count += 1
    print('tokinized: ' + resource.uid)
    return resource.text, count


def tokenize_texts(resources=new_resources):
    tokinized = []
    for r in resources:
        t = tokenize_text(r)
        tokinized.append(t)
    print('tokinized: ' + str(len(tokinized)))
    return tokinized


def get_token_file_length(directory='test', resource=r, r_id=None):
    rsrc = []
    uid = resource.uid
    if r_id is not None:
        rsrc = list(filter(lambda x: x.uid == r_id, new_resources))
        uid = r_id
    if len(rsrc) == 1:  # this if statement is kinda redundant but i dont care xD
        resource = rsrc[0]

    for root, dirs, files in os.walk(directory):
        for f in files:
            match = re.search(rf'{uid}_(\d+)_.txt', f)
            if match is not None:
                return int(match.group(1))


re.search


def get_chunk_text(p=0, q=9999, resource=r, r_id=None):
    rsrc = []
    if r_id is not None:
        rsrc = list(filter(lambda x: x.uid == r_id, new_resources))
    if len(rsrc) == 1:
        resource = rsrc[0]

    tokens, length = tokenize_text(resource=resource, r_id=r_id)
    # length = get_token_file_length(directory=...)

    if p < 0 or p > length - 2:
        raise Exception(f'first index(p) is not within range. p: {p}')
    if q <= 0:
        raise Exception(f'second index(q) is not within range. q: {q}')
    if p >= q:
        raise Exception(
            f'second index(q) must me greater than first index(p). p: {p}, q: {q}')

    if p == 0:
        # if q >= length - 1:
        #     pattern = rf'.+'
        # else:
        pattern = rf'.+__!i{q}__'
    elif q >= length - 1:
        pattern = rf'__!i{p}__.+'
    else:
        pattern = rf'__!i{p}__.+__!i{q}__'

    match_object = re.search(pattern, tokens, flags=re.DOTALL)
    match = match_object.group(0)

    text = re.sub(r'__!i\d+__', ' ', match).strip()

    return text


def make_chunk_token_files(directory='test'):
    for root, dirs, files in os.walk(directory):
        for f in files:
            titles = f.split('-')
            if f.find('__chunk__') != -1 and f.find('.flac') != -1 and len(titles) == 5:
                p_, q_ = titles[2], titles[3]
                p = int(p_)
                q = int(q_)

                file_name = f.replace('.flac', '.txt')
                file_path = os.path.join(root, file_name)

                with open(file_path, 'w') as output_file:
                    token = get_chunk_text(p, q, r_id=f[0:5].strip())
                    output_file.write(token)
                    output_file.close()
                    print('Written: ', os.path.basename(file_path))


def make_token_files(directory='test'):
    for root, dirs, files in os.walk(directory):
        match_object = re.search(r'T-\d{3}', root)
        if match_object is None:
            continue
        uid = match_object.group(0)
        if root.endswith(uid):
            token, count = tokenize_text(r_id=uid)
            file_path = os.path.join(root, uid + f'_{count}_.txt')
            with open(file_path, 'w') as output_file:
                output_file.write(token)
                output_file.close()
                print('Written: ', os.path.basename(file_path))


def delete_all_token_file(directory='test'):
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.endswith('.txt'):
                file_path = os.path.join(root, f)
                os.remove(file_path)
                print('Deleted: ', file_path)


def get_file_size(file):
    filesize = Path(file).stat().st_size
    # print(type(filesize))
    return filesize


def prepare_csv(directory='test'):
    with open('speech_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['wav_filename', 'wav_filesize', 'transcript'])
        for root, dirs, files in os.walk(directory):
            for f in files:
                if f.endswith('.wav'):
                    titles = f.split('-')
                    if f.find('__chunk__') != -1 and len(titles) == 5:
                        p_, q_ = titles[2], titles[3]
                        p = int(p_)
                        q = int(q_)
                        r_id = re.search('T-\d{3}', f).group(0)
                        chunk_text = get_chunk_text(p, q, r_id=r_id)
                        

                        while True:
                            first_match = re.search(r'\d+', chunk_text)
                            if first_match is not None:
                                p, q = first_match.span()
                                number = chunk_text[p : q]
                                replacement = num2words(number)
                                chunk_text = chunk_text.replace(number, replacement)
                            else:
                                break

                        writer.writerow(
                            [os.path.join(os.path.join(os.getcwd(), root), f), get_file_size(os.path.join(root, f)), re.sub(' +', ' ', re.sub(r"[^a-z\s']", ' ', chunk_text.lower()))])


# tokenize_text(r)

# tokenize_texts(new_resources)

# f = get_chunk_text(94, 109, r_id='T-001')
# with open('flush.txt', 'w') as flush:
#     flush.write(f)
#     flush.close()

# make_chunk_token_files()

# make_token_files()

# delete_all_token_file()

# get_chunk_text(r_id='T-001')

# print(get_token_file_length(r_id='T-002'))

# get_file_size('prepare_tokens.py')

# prepare_csv(directory='wazobia')

if __name__ == '__main__':
    prepare_csv(directory='wazobia')
    # print('hello')
    