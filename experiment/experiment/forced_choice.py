#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
PsychoPy Subliminal Audio Priming (FORCED-CHOICE CONTROL)
================================================================================

This script implements a 2-Alternative Forced Choice (2AFC) control experiment.
- Objective: Test if participants can consciously identify the prime word
             when presented with the same audio masking.
- Design: Participants hear the full audio sequence (babble, mask, prime, mask)
          and must then choose the prime word they heard from two
          on-screen options (the correct word and a random distractor).
- Task: 2AFC, using 'left' and 'right' arrow keys.

"""

# --- 1. Import Libraries ---
from psychopy import gui, visual, core, data, event, sound, logging
import os
import random
from datetime import datetime
import os.path

# --- 2. Define Constants (Test) ---

# Timing (in seconds)
FIXATION_DURATION = 2.0
ITI_DURATION = 2.0     # Inter-trial interval


# Trial Counts
N_PRACTICE_TRIALS = 2    # Was 10
N_MAIN_TRIALS = 8        # Was 200
N_TOTAL_TRIALS = N_PRACTICE_TRIALS + N_MAIN_TRIALS # This now equals 10

# Prime list counts - MUST SUM TO 10
# NOTE: N_NO_PRIMES is removed, as it doesn't work for a 2AFC task.
N_POS_PRIMES = 4         # Was 3
N_NEG_PRIMES = 3         # Was 3
N_NEU_PRIMES = 3         # Was 2
# (Total: 4 + 3 + 3 = 10. This matches N_TOTAL_TRIALS)

# Rating keys
QUIT_KEY = 'escape'
CHOICE_KEYS = ['left', 'right']
VALID_KEYS = CHOICE_KEYS + [QUIT_KEY]

# Block breaks
MAIN_TRIAL_BREAK_POINTS = []


# --- 3. Setup Functions ---

def get_participant_info():
    """Displays a dialog box to get participant info (ID, session)."""
    exp_info = {
        'Participant ID': '',
        'Session': '001',
    }
    dlg = gui.DlgFromDict(dictionary=exp_info, title='Experiment Setup')
    
    if not dlg.OK:
        print("User cancelled the experiment.")
        core.quit()
    
    exp_info['date'] = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    return exp_info


def setup_experiment(participant_info):
    """Sets up the core PsychoPy components: window, experiment handler, and paths."""
    # --- Setup File/Folder Paths ---
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    data_dir = os.path.join(base_dir, 'data_control') # Separate data folder
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Created data directory: {data_dir}")

    # --- Setup Filename and Experiment Handler ---
    file_name = (
        f"{participant_info['Participant ID']}_"
        f"{participant_info['Session']}_"
        f"{participant_info['date']}_control" # Add suffix
    )
    
    data_file_path = os.path.join(data_dir, file_name)
    
    exp_handler = data.ExperimentHandler(
        name='SubliminalAudio_Control',
        version='1.0',
        extraInfo=participant_info,
        runtimeInfo=True,
        originPath=__file__,
        savePickle=True,
        saveWideText=True,
        dataFileName=data_file_path
    )
    
    # --- Setup Window ---
    win = visual.Window(
        size=[1000, 800],
        fullscr=True,
        screen=0,
        winType='pyglet',
        allowGUI=False,
        allowStencil=False,
        monitor='testMonitor',
        color=[0, 0, 0],
        colorSpace='rgb',
        blendMode='avg',
        useFBO=True,
        units='height'
    )
    
    win.mouseVisible = False
    logging.console.setLevel(logging.WARNING)
    
    return win, exp_handler, base_dir


def load_reusable_stimuli(win, base_dir):
    """Pre-loads all stimuli that are used repeatedly."""
    stimuli = {}
    
    # 1. Fixation Cross
    stimuli['fixation'] = visual.TextStim(
        win, text='+',
        height=0.1,
        color='white'
    )
    
    # 2. Main Prompt Text
    stimuli['prompt_text'] = visual.TextStim(
        win,
        text="Which word do you think you heard?",
        height=0.06,
        color='white',
        wrapWidth=1.5,
        pos=(0, 0.3) # Positioned at the top
    )

    # 3. Left Word Option
    stimuli['word_left'] = visual.TextStim(
        win,
        text="", # Will be set on each trial
        height=0.08,
        color='white',
        wrapWidth=1.5,
        pos=(-0.4, 0) # Positioned on the left
    )

    # 4. Right Word Option
    stimuli['word_right'] = visual.TextStim(
        win,
        text="", # Will be set on each trial
        height=0.08,
        color='white',
        wrapWidth=1.5,
        pos=(0.4, 0) # Positioned on the right
    )
    
    # 5. Instruction Text (generic, will be updated)
    stimuli['instructions'] = visual.TextStim(
        win,
        text="", 
        height=0.05,
        color='white',
        wrapWidth=1.5
    )

    # 6. Feedback Text (for practice)
    stimuli['feedback'] = visual.TextStim(
        win,
        text="",
        height=0.05,
        color='white'
    )
    
    # 7. Inter-trial text
    stimuli['ITI_text'] =  visual.TextStim(
        win,
        text="A new trial will begin",
        height=0.05,
        color='white',
        wrapWidth=1.5
    )
    
    # 8. Out Sound (sensor-beep.wav)
    beep_path = os.path.join(base_dir, 'sensor-beep.wav')
    stimuli['out_sound'] = sound.Sound(beep_path, autoLog=False)
    
    return stimuli


def show_instructions(win, text_stim, message, wait_for_key='space'):
    """Helper function to display instructions and wait for a keypress."""
    text_stim.setText(message)
    text_stim.draw()
    win.flip()
    
    keys = event.waitKeys(keyList=[wait_for_key, 'escape'])
    
    if 'escape' in keys:
        print("Experiment aborted by user during instructions.")
        win.close()
        core.quit()


# --- 4. Core Logic: Trial Generation ---

def get_files_from_dir(directory):
    """Helper function to get a list of non-hidden files from a directory."""
    return [f for f in os.listdir(directory) if not f.startswith('.')]

def get_word_from_filename(filename):
    """Helper to extract 'happy' from 'happy_compresssed.wav'."""
    full_word = os.path.splitext(filename)[0]
    return full_word.split('_')[0]

def generate_trial_list(base_dir):
    """
    Generates the trial list for the forced-choice task.
    - Loads all prime words.
    - Creates a trial list.
    - For each trial, adds a 'correct_word' and a random 'distractor_word'.
    """
    print("Generating trial list for control experiment...")
    
    # --- Define Paths ---
    primes_dir = os.path.join(base_dir, 'primes')
    babbling_dir = os.path.join(base_dir, 'babbling')
    masks_dir = os.path.join(base_dir, 'masks')
    
    # --- 1. Load Sound Assets ---
    
    # Scan /primes/ subfolders
    try:
        prime_pos_files = get_files_from_dir(os.path.join(primes_dir, 'positive'))
        prime_neg_files = get_files_from_dir(os.path.join(primes_dir, 'negative'))
        prime_neu_files = get_files_from_dir(os.path.join(primes_dir, 'neutrale'))
        
        babbling_list = get_files_from_dir(babbling_dir)
        mask_list = get_files_from_dir(masks_dir)
    except FileNotFoundError as e:
        print(f"FATAL ERROR: Cannot find asset directory. {e}")
        core.quit()
    
    if not all([prime_pos_files, prime_neg_files, prime_neu_files, babbling_list, mask_list]):
        print("FATAL ERROR: One or more sound asset directories are empty.")
        core.quit()

    # --- 2. Create Master Word List (for distractors) ---
    all_prime_files = prime_pos_files + prime_neg_files + prime_neu_files
    # Get unique words, e.g., ["happy", "sad", "table", ...]
    all_prime_words = list(set([get_word_from_filename(f) for f in all_prime_files]))
    
    if len(all_prime_words) < 2:
        print("FATAL ERROR: Need at least 2 unique prime words to create distractors.")
        core.quit()

    # --- 3. Define Prime List (N_TOTAL_TRIALS total) ---
    prime_list = []
    
    # Positive
    pos_choices = random.choices(prime_pos_files, k=N_POS_PRIMES)
    for f in pos_choices:
        prime_list.append({'file': f, 'valence': 'positive', 'word': get_word_from_filename(f)})
        
    # Negative
    neg_choices = random.choices(prime_neg_files, k=N_NEG_PRIMES)
    for f in neg_choices:
        prime_list.append({'file': f, 'valence': 'negative', 'word': get_word_from_filename(f)})
        
    # Neutral
    neu_choices = random.choices(prime_neu_files, k=N_NEU_PRIMES)
    for f in neu_choices:
        prime_list.append({'file': f, 'valence': 'neutral', 'word': get_word_from_filename(f)})
        
    # Shuffle the list of primes
    random.shuffle(prime_list)
    
    # --- 4. Build Final Trial List ---
    generated_trials = []
    for i in range(N_TOTAL_TRIALS):
        
        # Ensure mask1 and mask2 are not the same file
        mask1 = random.choice(mask_list)
        mask2 = random.choice(mask_list)
        while mask1 == mask2:
            mask2 = random.choice(mask_list)
        
        # Get the correct word for this trial
        correct_word = prime_list[i]['word']
        
        # Get a random distractor word
        distractor_word = random.choice(all_prime_words)
        # Make sure distractor is not the same as the correct word
        while distractor_word == correct_word:
            distractor_word = random.choice(all_prime_words)
            
        # Create the trial dictionary
        trial_data = {
            'trial_i': i + 1,
            'prime_file': prime_list[i]['file'],
            'prime_valence': prime_list[i]['valence'],
            'correct_word': correct_word,
            'distractor_word': distractor_word,
            'babbling_file': random.choice(babbling_list),
            'mask1_file': mask1,
            'mask2_file': mask2
        }
        generated_trials.append(trial_data)

    # --- 5. Final Shuffle ---
    # This shuffles the *order* of the paired trials
    random.shuffle(generated_trials)
    
    print(f"Successfully generated {len(generated_trials)} trials.")
    return generated_trials


# --- 5. Core Logic: Trial Execution ---

def run_trial(win, base_dir, trial_info, trial_handler, stimuli, rt_clock, babling_before_prime):
    """
    Executes a single trial based on the trial_info dictionary.
    """
    
    # --- 1. Fixation ---
    stimuli['fixation'].draw()
    win.flip()
    core.wait(FIXATION_DURATION)
    
    # --- 2. Audio Sequence ---
    
    # Load all sounds for this trial
    babble_path = os.path.join(base_dir, 'babbling', trial_info['babbling_file'])
    mask1_path = os.path.join(base_dir, 'masks', trial_info['mask1_file'])
    mask2_path = os.path.join(base_dir, 'masks', trial_info['mask2_file'])
    
    babble_sound = sound.Sound(babble_path, autoLog=False)
    mask1_sound = sound.Sound(mask1_path, autoLog=False)
    mask2_sound = sound.Sound(mask2_path, autoLog=False)
    
    # Load prime sound
    prime_sound = None
    if trial_info['prime_file'] != 'SILENCE': # Should not happen, but good check
        prime_valence_folder = trial_info['prime_valence']
        if prime_valence_folder == 'neutral':
            prime_valence_folder = 'neutrale'
            
        prime_path = os.path.join(
            base_dir, 'primes', prime_valence_folder, trial_info['prime_file']
        )
        prime_sound = sound.Sound(prime_path, autoLog=False)

    # Execute Timeline
    babble_sound.play()  
    core.wait(babling_before_prime) # Babble for 1s

    # --- Synchronous sounds (play and wait) ---
    mask1_sound.play()
    core.wait(mask1_sound.getDuration()) 

    if prime_sound:
        prime_sound.play()
        core.wait(prime_sound.getDuration())
    
    mask2_sound.play()
    core.wait(mask2_sound.getDuration())
    
    babble_sound.stop() # Stop the babbling
    
    
    # Randomly assign words to left/right
    if random.random() > 0.5:
        left_word = trial_info['correct_word']
        right_word = trial_info['distractor_word']
        correct_key = 'left'
    else:
        left_word = trial_info['distractor_word']
        right_word = trial_info['correct_word']
        correct_key = 'right'
        
    # Set text for the stimuli
    stimuli['prompt_text'].draw()
    stimuli['word_left'].setText(left_word)
    stimuli['word_left'].draw()
    stimuli['word_right'].setText(right_word)
    stimuli['word_right'].draw()
    
    win.flip()
    
    # Clear keyboard buffer and reset RT clock
    event.clearEvents(eventType='keyboard')
    rt_clock.reset()
    
    # Wait for a valid keypress ('left', 'right', or 'escape')
    response = event.waitKeys(
        maxWait=float('inf'),
        keyList=VALID_KEYS,
        timeStamped=rt_clock
    )
    
    key, rt = None, None
    accuracy = 0
    if response:
        key = response[0][0]
        rt = response[0][1]
        if key == correct_key:
            accuracy = 1
        
    # Add response data to the handler
    trial_handler.addData('response_key', key)
    trial_handler.addData('rt', rt)
    trial_handler.addData('correct_key', correct_key)
    trial_handler.addData('accuracy', accuracy)
    trial_handler.addData('left_word', left_word)
    trial_handler.addData('right_word', right_word)
    
    # --- 6. ITI (Inter-Trial Interval) ---
    stimuli['ITI_text'].draw()
    win.flip()
    core.wait(ITI_DURATION)
    stimuli['out_sound'].play() 
    
    # --- 7. Check for Quit ---
    if key == QUIT_KEY:
        return 'QUIT'
    
    return None


# --- 6. Main Experiment Flow ---

def main():
    """
    The main function that runs the entire experiment.
    """
    result = None # Initialize result
    try:
        # --- 1. Setup ---
        participant_info = get_participant_info()
        win, exp_handler, base_dir = setup_experiment(participant_info)
        stimuli = load_reusable_stimuli(win, base_dir)
        rt_clock = core.Clock() 
        
        # --- 2. Generate Trial List ---
        full_trial_list = generate_trial_list(base_dir)
        
        # --- 3. Create Trial Handlers ---
        practice_list = full_trial_list[0:N_PRACTICE_TRIALS]
        main_list = full_trial_list[N_PRACTICE_TRIALS:N_TOTAL_TRIALS]
        
        practice_trials = data.TrialHandler(
            trialList=practice_list, nReps=1, method='sequential', name='practice'
        )
        main_trials = data.TrialHandler(
            trialList=main_list, nReps=1, method='sequential', name='main'
        )
        
        exp_handler.addLoop(practice_trials)
        exp_handler.addLoop(main_trials)
        
        # --- 4. Run Practice ---
        practice_instructions = (
            "Welcome to the practice round.\n\n"
            "You will hear a series of sounds. Your task is to identify \n"
            "the word that was hidden in the sounds.\n\n"
            "After the sounds, you will see two words on the screen.\n"
            "Use the LEFT and RIGHT arrow keys to choose the word you heard.\n\n"
            "Press the 'space' bar to begin."
        )
        show_instructions(win, stimuli['instructions'], practice_instructions)
        
        for trial in practice_trials:
            
            val = random.uniform(0.5,1.5)
            
            result = run_trial(
                win, base_dir, trial, practice_trials, stimuli, rt_clock, val
            )
            
            if result == 'QUIT':
                break
            
            exp_handler.nextEntry() 

        if result == 'QUIT':
            raise KeyboardInterrupt("Experiment aborted by user.")

        # --- 5. Run Main Experiment ---
        main_instructions = (
            "Practice complete. Now the main experiment will begin.\n\n"
            "The task is the same.\n"
            "Use the LEFT and RIGHT arrow keys to choose the word you heard.\n\n"
            "Press the 'space' bar to start."
        )
        show_instructions(win, stimuli['instructions'], main_instructions)
        
        quit_experiment = False
        for trial in main_trials:
            current_trial_n = main_trials.thisN 


            val = random.uniform(0.5,1.5)
            
            result = run_trial(
                win, base_dir, trial, main_trials, stimuli, rt_clock, val
            )

            if result == 'QUIT':
                quit_experiment = True
                break
                
            exp_handler.nextEntry()
            
            if current_trial_n in MAIN_TRIAL_BREAK_POINTS:
                break_message = (
                    f"You have completed {current_trial_n + 1} of {N_MAIN_TRIALS} trials.\n\n"
                    "Time for a short break.\n\n"
                    "Press the 'space' bar to continue when you are ready."
                )
                show_instructions(win, stimuli['instructions'], break_message)
        
        # --- 6. End Experiment ---
        if quit_experiment:
            end_message = "Data has been saved.\n\nThank you for your time."
        else:
            end_message = "Experiment complete!\n\nThank you for your participation."
            
        show_instructions(win, stimuli['instructions'], end_message, wait_for_key='space')

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        logging.error(e)
    
    finally:
        # --- 7. Cleanup ---
        if 'exp_handler' in locals():
            exp_handler.close()
        
        if 'win' in locals() and win:
            win.close()
            
        core.quit()


# --- 7. Script Execution ---
if __name__ == "__main__":
    main()