#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
PsychoPy Subliminal Audio Priming Experiment
================================================================================

This script implements a subliminal audio priming experiment using PsychoPy.
It is designed to be run as a single procedural (function-based) script.

Experiment Overview:
- Objective: Test if subliminal audio prime valence (positive, negative, neutral,
             no-prime) and its congruency with face valence (positive, negative,
             neutral) affects valence ratings (1-7) and reaction times.
- Design: Within-subjects, 10 practice trials + 200 main trials.
- Trial Generation: Face-prime pairings are randomly generated for each
                   participant at the start of the script.

File Structure (ASSUMED):
/Experiment_Folder/
|
├── main.py                (This script)
├── face_mask.gif          (A static mask image)
├── sensor-beep.wav        (End-of-trial sound)
|
├── /faces/                (Contains p1.JPG, p2.JPG, ... p210.JPG)
├── /primes/
|   ├── /positive/         (e.g., happy.wav)
|   ├── /negative/         (e.g., sad.wav)
|   └── /neutrale/         (e.g., table.wav)
|
├── /masks/                (Contains word1_rev.wav, ...)
├── /babbling/             (Contains bab1.wav, ...)
|
└── /data/                 (Output directory for CSV/log files)

"""

# --- 1. Import Libraries ---
from psychopy import prefs 
prefs.hardware['audioLib'] = ['sounddevice', 'PTB', 'pyo', 'pygame']  
from psychopy import gui, visual, core, data, event, sound, logging
import os
import random
from datetime import datetime



# --- 2. Define Constants test ---

# # Timing (in seconds)
FIXATION_DURATION = 2.0
FACE_DURATION = 1.0  # 500ms
MASK_DURATION = 0.5  # 250ms
ITI_DURATION = 2.0     # Inter-trial interval


# Trial Counts
N_PRACTICE_TRIALS = 2    # Was 10
N_MAIN_TRIALS = 8        # Was 200
N_TOTAL_TRIALS = N_PRACTICE_TRIALS + N_MAIN_TRIALS # This now equals 10

# Prime list counts - MUST ALSO SUM TO 10
N_POS_PRIMES = 3         # Was 70
N_NEG_PRIMES = 3         # Was 70
N_NEU_PRIMES = 2         # Was 35
N_NO_PRIMES = 2          # Was 35
# (Total: 3 + 3 + 2 + 2 = 10. This matches N_TOTAL_TRIALS)

# Rating keys
RATING_KEYS = ['1', '2', '3', '4', '5', '6', '7']
QUIT_KEY = 'escape'
VALID_KEYS = RATING_KEYS + [QUIT_KEY]

# Block breaks (trial numbers *within the main block*)
# The old values [49, 99, 149] are outside our 8-trial limit.
# Set it to [] for no breaks, or [3] for a break after the 4th trial.
MAIN_TRIAL_BREAK_POINTS = [3]


# --- 3. Setup Functions ---

def get_participant_info():
    """
    Displays a dialog box to get participant info (ID, session).
    
    Returns:
        dict or None: A dictionary with 'Participant ID' and 'Session'.
                      Returns None if the user cancels.
    """
    exp_info = {
        'Participant ID': '',
        'Session': '001',
    }
    dlg = gui.DlgFromDict(dictionary=exp_info, title='Experiment Setup')
    
    if not dlg.OK:
        print("User cancelled the experiment.")
        core.quit()
    
    # Create a timestamp
    exp_info['date'] = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    return exp_info


def setup_experiment(participant_info):
    """
    Sets up the core PsychoPy components: window, experiment handler, and paths.
    
    Args:
        participant_info (dict): The dictionary from get_participant_info().
    
    Returns:
        tuple: (win, exp_handler, base_dir)
            - win (visual.Window): The main experiment window.
            - exp_handler (data.ExperimentHandler): Handler for saving data.
            - base_dir (str): The absolute path to the script's directory.
    """
    # --- Setup File/Folder Paths ---
    # Assumes the script is in the root 'Experiment_Folder'
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    data_dir = os.path.join(base_dir, 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Created data directory: {data_dir}")

    # --- Setup Filename and Experiment Handler ---
    file_name = (
        f"{participant_info['Participant ID']}_"
        f"{participant_info['Session']}_"
        f"{participant_info['date']}"
    )
    
    # Full path for the output CSV file
    data_file_path = os.path.join(data_dir, file_name)
    
    # This handler will automatically save all data from TrialHandlers
    exp_handler = data.ExperimentHandler(
        name='SubliminalAudioPriming',
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
        fullscr=True,  # Set to True for actual experiment
        screen=0,
        winType='pyglet',
        allowGUI=False,
        allowStencil=False,
        monitor='testMonitor',
        color=[0, 0, 0],  # Black background
        colorSpace='rgb',
        blendMode='avg',
        useFBO=True,
        units='height'
    )
    
    # Hide the mouse cursor
    win.mouseVisible = False
    
    # Set logging level to warning to avoid spamming the console
    logging.console.setLevel(logging.WARNING)
    
    return win, exp_handler, base_dir


def load_reusable_stimuli(win, base_dir):
    """
    Pre-loads all stimuli that are used repeatedly (fixation, text, etc.).
    
    Args:
        win (visual.Window): The main experiment window.
        base_dir (str): The absolute path to the script's directory.
        
    Returns:
        dict: A dictionary containing all pre-loaded stimuli.
    """
    stimuli = {}
    
    # 1. Fixation Cross
    stimuli['fixation'] = visual.TextStim(
        win, text='+',
        height=0.1,
        color='white'
    )
    
    # 2. Face Stimulus (Image will be set on each trial)
    stimuli['face'] = visual.ImageStim(
        win,
        image=None,  # Will be set later
        size=(0.7, 0.7),  # Adjust as needed
        units='height'
    )
    
    # 3. Face Mask (from face_mask.gif)
    mask_path = os.path.join(base_dir, 'face_mask.gif')
    stimuli['mask_gif'] = visual.ImageStim(
        win,
        image=mask_path,
        size=(0.7, 0.7), # Match face size
        units='height'
    )
    
    # 4. Rating Scale Text
    stimuli['rating_text'] = visual.TextStim(
        win,
        text="How positive or negative is the face?\n\n"
             "1 (Very Negative) - 4 (Neutral) - 7 (Very Positive)",
        height=0.05,
        color='white',
        wrapWidth=1.5
    )
    
    # 5. Instruction Text (generic, will be updated)
    stimuli['instructions'] = visual.TextStim(
        win,
        text="", # Will be set as needed
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

    # 7. Inter trial text
    stimuli['ITI-text'] =  visual.TextStim(
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
    """
    Helper function to display instructions and wait for a keypress.
    
    Args:
        win (visual.Window): The main experiment window.
        text_stim (visual.TextStim): The pre-loaded instruction text object.
        message (str): The text to display.
        wait_for_key (str): The key to wait for to continue.
    """
    text_stim.setText(message)
    text_stim.draw()
    win.flip()
    
    # Wait for the specified key
    event.waitKeys(keyList=[wait_for_key, 'escape'])
    
    # Check for escape
    if 'escape' in event.getKeys():
        print("Experiment aborted by user during instructions.")
        win.close()
        core.quit()


# --- 4. Core Logic: Trial Generation ---

def get_files_from_dir(directory):
    """Helper function to get a list of non-hidden files from a directory."""
    return [f for f in os.listdir(directory) if not f.startswith('.')]


def generate_trial_list(base_dir):
    """
    This is the core function for generating the 210-trial list.
    It loads all assets, creates the 210 prime conditions, pairs them
    randomly with the 210 faces, and shuffles the final list.
    
    Args:
        base_dir (str): The absolute path to the script's directory.
        
    Returns:
        list: A list of 210 trial dictionaries, randomly shuffled.
    """
    print("Generating trial list...")
    
    # --- Define Paths ---
    faces_dir = os.path.join(base_dir, 'faces')
    primes_dir = os.path.join(base_dir, 'primes')
    babbling_dir = os.path.join(base_dir, 'babbling')
    masks_dir = os.path.join(base_dir, 'masks')
    
    # --- 1. Load Assets ---
    
    # Load 210 faces from faces.csv
    # Load face files by scanning the /faces/ directory
    try:
        # Use the existing helper function to get all face filenames
        face_list = get_files_from_dir(faces_dir)
    except FileNotFoundError:
        print(f"FATAL ERROR: Cannot find faces directory at {faces_dir}")
        core.quit()
        
    # Check if we have *at least* enough faces for the experiment
    if len(face_list) < N_TOTAL_TRIALS:
        print(f"FATAL ERROR: Not enough faces in {faces_dir}.")
        print(f"Found {len(face_list)}, but experiment requires {N_TOTAL_TRIALS}.")
        core.quit()

    # Scan /primes/ subfolders
    prime_pos_files = get_files_from_dir(os.path.join(primes_dir, 'positive'))
    prime_neg_files = get_files_from_dir(os.path.join(primes_dir, 'negative'))
    prime_neu_files = get_files_from_dir(os.path.join(primes_dir, 'neutrale')) # Note folder spelling
    
    # Load babbling and mask sounds
    babbling_list = get_files_from_dir(babbling_dir)
    mask_list = get_files_from_dir(masks_dir)
    
    # Check if any sound lists are empty
    if not all([prime_pos_files, prime_neg_files, prime_neu_files, babbling_list, mask_list]):
        print("FATAL ERROR: One or more sound asset directories are empty.")
        print(f"Positive primes: {len(prime_pos_files)}")
        print(f"Negative primes: {len(prime_neg_files)}")
        print(f"Neutral primes: {len(prime_neu_files)}")
        print(f"Babbling files: {len(babbling_list)}")
        print(f"Mask files: {len(mask_list)}")
        core.quit()

    # --- 2. Define Prime List (210 total) ---
    prime_list = []
    
    # 70 'positive' (sampling with replacement)
    pos_choices = random.choices(prime_pos_files, k=N_POS_PRIMES)
    for f in pos_choices:
        prime_list.append({'file': f, 'valence': 'positive'})
        
    # 70 'negative'
    neg_choices = random.choices(prime_neg_files, k=N_NEG_PRIMES)
    for f in neg_choices:
        prime_list.append({'file': f, 'valence': 'negative'})
        
    # 35 'neutral' (note: valence is 'neutral', folder is 'neutrale')
    neu_choices = random.choices(prime_neu_files, k=N_NEU_PRIMES)
    for f in neu_choices:
        prime_list.append({'file': f, 'valence': 'neutral'})
        
    # 35 'no-prime'
    for _ in range(N_NO_PRIMES):
        prime_list.append({'file': 'SILENCE', 'valence': 'no-prime'})
        
    # --- 3. Shuffle & Pair ---
    
    # Shuffle the 210-item face_list
    random.shuffle(face_list)
    # Shuffle the 210-item prime_list
    random.shuffle(prime_list)
    
    # --- 4. Build Final Trial List ---
    generated_trials = []
    for i in range(N_TOTAL_TRIALS):
        
        # Ensure mask1 and mask2 are not the same file
        mask1 = random.choice(mask_list)
        mask2 = random.choice(mask_list)
        while mask1 == mask2:
            mask2 = random.choice(mask_list)
            
        # Create the trial dictionary by pairing the shuffled lists
        # Create the trial dictionary by pairing the shuffled lists
        trial_data = {
            'trial_i': i + 1,  # 1-indexed trial number

            # Paired Face & Prime
            'face_file': face_list[i], # <-- This is correct
            # 'face_valence' key is already removed
            'prime_file': prime_list[i]['file'],
            'prime_valence': prime_list[i]['valence'],

            # Randomly chosen sounds
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

def run_trial(win, base_dir, trial_info, trial_handler, stimuli, rt_clock,bable_duration_before_prime):
    """
    Executes a single trial based on the trial_info dictionary.
    
    Args:
        win (visual.Window): The main experiment window.
        base_dir (str): The absolute path to the script's directory.
        trial_info (dict): The dictionary for this specific trial.
        trial_handler (data.TrialHandler): The handler (practice or main).
        stimuli (dict): Dictionary of pre-loaded stimuli.
        rt_clock (core.Clock): The clock for timing responses.
        
    Returns:
        str or None: 'QUIT' if user pressed escape, else None.
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
    
    # Load prime sound (or set to None if 'SILENCE')
    prime_sound = None
    if trial_info['prime_file'] != 'SILENCE':
        
        # Map logical valence 'neutral' to folder name 'neutrale'
        prime_valence_folder = trial_info['prime_valence']
        if prime_valence_folder == 'neutral':
            prime_valence_folder = 'neutrale'
            
        prime_path = os.path.join(
            base_dir,
            'primes',
            prime_valence_folder,
            trial_info['prime_file']
        )
        prime_sound = sound.Sound(prime_path, autoLog=False)

    # Execute Timeline
    babble_sound.play()  
    core.wait(bable_duration_before_prime)

    # --- Synchronous sounds (play and wait) ---
    mask1_sound.play()
    core.wait(mask1_sound.getDuration()) # Manually pause script

    if prime_sound:
        prime_sound.play()
        core.wait(prime_sound.getDuration()) # Manually pause script
    

    mask2_sound.play()
    core.wait(mask2_sound.getDuration()) # Manually pause script
    
    babble_sound.stop()            # Stop the babbling# Stop the babbling
    
    # --- 3. Face ---
    face_path = os.path.join(base_dir, 'faces', trial_info['face_file'])
    stimuli['face'].setImage(face_path)
    stimuli['face'].draw()
    win.flip()
    core.wait(FACE_DURATION)
    
    # --- 4. Face Mask ---
    stimuli['mask_gif'].draw()
    win.flip()
    core.wait(MASK_DURATION)
    
    # --- 5. Rating ---
    stimuli['rating_text'].draw()
    win.flip()
    
    # Clear keyboard buffer and reset RT clock
    event.clearEvents(eventType='keyboard')
    rt_clock.reset()
    
    # Wait for a valid keypress
    response = event.waitKeys(
        maxWait=float('inf'),
        keyList=VALID_KEYS,
        timeStamped=rt_clock
    )
    
    key, rt = None, None
    if response:
        key = response[0][0]
        rt = response[0][1]
        
    # Add response data to the handler
    # All other trial_info (face_file, prime_valence, etc.) is saved automatically
    trial_handler.addData('response_key', key)
    trial_handler.addData('rt', rt)
    
    # --- 6. ITI (Blank Screen) ---
    stimuli['ITI-text'].draw()
    win.flip()
    core.wait(ITI_DURATION)
    stimuli['out_sound'].play() 
    
    # --- 8. Check for Quit ---
    if key == QUIT_KEY:
        return 'QUIT'
    
    return None


# --- 6. Main Experiment Flow ---

def main():
    """
    The main function that runs the entire experiment.
    """
    try:
        # --- 1. Setup ---
        participant_info = get_participant_info()
        win, exp_handler, base_dir = setup_experiment(participant_info)
        stimuli = load_reusable_stimuli(win, base_dir)
        rt_clock = core.Clock() # One clock for all response times
        
        # --- 2. Generate Trial List ---
        full_trial_list = generate_trial_list(base_dir)
        
        # --- 3. Create Trial Handlers ---
        # Split the full list into practice and main
        practice_list = full_trial_list[0:N_PRACTICE_TRIALS]
        main_list = full_trial_list[N_PRACTICE_TRIALS:N_TOTAL_TRIALS]
        
        # Create TrialHandler for practice
        practice_trials = data.TrialHandler(
            trialList=practice_list,
            nReps=1,
            method='sequential', # We already shuffled the list
            name='practice'
        )
        
        # Create TrialHandler for main experiment
        main_trials = data.TrialHandler(
            trialList=main_list,
            nReps=1,
            method='sequential', # We already shuffled the list
            name='main'
        )
        
        # Add handlers to the ExperimentHandler (so it saves their data)
        exp_handler.addLoop(practice_trials)
        exp_handler.addLoop(main_trials)
        
        # --- 4. Run Practice ---
        practice_instructions = (
            "Welcome to the practice round.\n\n"
            "You will hear a series of sounds and then see a face.\n"
            "Please rate how positive or negative the face is "
            "using the 1-7 keys.\n\n"
            "1 = Very Negative, 4 = Neutral, 7 = Very Positive\n\n"
            "Press the 'space' bar to begin."
        )
        show_instructions(win, stimuli['instructions'], practice_instructions)
        
        for trial in practice_trials:
            # Run the trial
            result = run_trial(
                win, base_dir, trial, practice_trials, stimuli, rt_clock, 1
            )
            
            # Check for quit signal
            if result == 'QUIT':
                break
                
            # # Show practice feedback
            # response = practice_trials.data['response_key'][-1]
            # if response:
            #     feedback_msg = f"You pressed: {response}"
            # else:
            #     feedback_msg = "You did not respond in time."
                
            # stimuli['feedback'].setText(feedback_msg)
            # stimuli['feedback'].draw()
            # win.flip()
            # core.wait(1.5)
            
            # This is necessary *after* adding data
            exp_handler.nextEntry() 

        # Check if user quit during practice
        if result == 'QUIT':
            raise KeyboardInterrupt("Experiment aborted by user.")

        # --- 5. Run Main Experiment ---
        main_instructions = (
            "Practice complete. Now the main experiment will begin.\n\n"
            "The task is the same. Please rate each face from 1-7.\n\n"
            "There will be short breaks during the experiment.\n\n"
            "Press the 'space' bar to start."
        )
        show_instructions(win, stimuli['instructions'], main_instructions)
        
        quit_experiment = False
        for trial in main_trials:
            # main_trials.thisN is the 0-indexed number of the *current loop*
            current_trial_n = main_trials.thisN 
            val = random.uniform(0.5,1.5)
            
            # Run the trial
            result = run_trial(
                win, base_dir, trial, main_trials, stimuli, rt_clock, val
            )

            # Check for quit signal
            if result == 'QUIT':
                quit_experiment = True
                break
                
            # Save data for this trial
            exp_handler.nextEntry()
            
            # Check for block breaks
            if current_trial_n in MAIN_TRIAL_BREAK_POINTS:
                break_message = (
                    f"You have completed {current_trial_n + 1} of {N_MAIN_TRIALS} trials.\n\n"
                    "Time for a short break.\n\n"
                    "Press the 'space' bar to continue when you are ready."
                )
                show_instructions(win, stimuli['instructions'], break_message)
        
        # --- 6. End Experiment ---
        if quit_experiment:
            print("Experiment aborted by user during main task.")
            end_message = "Data has been saved.\n\nThank you for your time."
        else:
            end_message = "Experiment complete!\n\nThank you for your participation."
            
        show_instructions(win, stimuli['instructions'], end_message, wait_for_key='space')

    except Exception as e:
        # Handle any other errors
        print(f"An unexpected error occurred: {e}")
        # Log the error
        logging.error(e)
    
    finally:
        # --- 7. Cleanup ---
        # This will save any remaining data
        # (ExperimentHandler automatically saves on quit)
        if 'exp_handler' in locals():
            exp_handler.close()
        
        # Close the window
        if 'win' in locals() and win:
            win.close()
            
        # Quit PsychoPy
        core.quit()


# --- 7. Script Execution ---
if __name__ == "__main__":
    main()