import csv

# We need to extract the English utterance from the speaker's column.
def identify_speaker(row, speaker):
    if speaker == "ARI":
        en_utt = row['ARI_EN']
    elif speaker == "LC":
        en_utt = row['PersonLeft_C_EN']
    elif speaker == "LP":
        en_utt = row['PersonLeft_P_EN']
    elif speaker == "RC":
        en_utt = row['PersonRight_C_EN']
    elif speaker == "RP":
        en_utt = row['PersonRight_P_EN']
    else: print("Big problem, unidentified speaker")
    return en_utt

# Parse the turn's dialogue act if it exists.
def extract_dst(row):
    if row['Dialogue_Act'] != '':
        return row['Dialogue_Act']
    else:
        return ""

# Parse the turn's goal if it exists.
def extract_goal(row):
    if row['Goal'] != '':
        return row['Goal']
    else:
        return ""

# Given a conversation in the original csv format from ELAN, we need to map it for our preprocessing.
def transform_converstion(convo, fid):
    # We want to try direct DST, direct goal tracking, and goal tracking given dialogue acts. These lists will collect data as needed for each task.
    dst_only = []
    goals_only = []
    dst_and_goals = []

    # run through all turns in the convo and parse into the three task lists
    for row in convo:
        speaker = row['Speaker']
        en_utt = identify_speaker(row, speaker)
        dst = extract_dst(row)
        goal = extract_goal(row)
        if en_utt != '':
            if dst != '':
                dsto = speaker + ": " + en_utt + " # " + dst
            else:
                dsto = speaker + ": " + en_utt
            if goal != '':
                go = speaker + ": " + en_utt + " @ " + goal
                both = dsto + " @ " + goal
            else:
                go = speaker + ": " + en_utt
                both = dsto
            dst_only.append(dsto)
            goals_only.append(go)
            dst_and_goals.append(both)

    # write three files for the three tasks
    with open('./Preprocessing/data/dialogues/dst-only/convo' + str(fid) + '.txt', 'w') as dstof:
        for turn in dst_only:
            dstof.write(f"{turn}\n")
    with open('./Preprocessing/data/dialogues/goals-only/convo' + str(fid) + '.txt', 'w') as gof:
        for turn in goals_only:
            gof.write(f"{turn}\n")
    with open('./Preprocessing/data/dialogues/dst-and-goals/convo' + str(fid) + '.txt', 'w') as bothf:
        for turn in dst_and_goals:
            bothf.write(f"{turn}\n")

# Hardcoded path here, need to switch - but read the csv into a dictionary
with open('./trash/29files.csv', newline='') as csvf:
    reader = csv.DictReader(csvf)
    # We need to set some initial variables to an impossible value for processing.
    filepath = "impossible"
    convo = "impossible"
    fid = 1
    # We ned to process each conversation separately, but they are all in the same file.
    # We therefore store turns until the 'File' column changes value.
    for row in reader:
        # If the 'File' value changes, we transform the stored conversation into our required format.
        if row['File'] != filepath:
            # The very first row is technically a change, so we don't have a convo to parse yet. Otherwise, we process the stored convo.
            if convo != "impossible":
                transform_converstion(convo, fid)
                fid = fid + 1
            # We then update the check variables to start the next convo.
            filepath = row['File']
            convo = [row]
        else:
            # If the convo is simply continuing, we simply append it.
            convo.append(row)
    # Finally, we process the stored convo at the end of the csv.
    transform_converstion(convo, fid)