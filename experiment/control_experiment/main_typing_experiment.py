#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
PsychoPy Subliminal Audio Priming (TYPING CONTROL)
================================================================================

Dette script implementerer et kontrol-eksperiment med tidskomprimerede ord.
- Objektiv: Teste på hvilket niveau af tidskomprimering deltagere
             ikke længere kan identificere et maskeret ord.
- Design: Deltagere hører en fuld audiosekvens (babble, mask, prime, mask)
          og skal derefter skrive det ord, de hørte.
- Stimuli: 8 niveauer af tidskomprimering (0.1 til 0.8).
- Task: Fri-tekst input, afsluttes med 'Enter'.

File Struktur:
/Experiment_Folder/
|
├── main_typing_experiment.py  (Dette script)
├── sensor-beep.wav
|
├── /audio/                    <-- NY MAPPE
|   ├── /0.1/
|   |   ├── ord1.wav
|   |   └── ...
|   ├── /0.2/
|   ...
|   └── /0.8/
|
├── /masks/
├── /babbling/
|
└── /data_typing/              <-- Ny output mappe
"""

# --- 1. Import Libraries ---
from psychopy import gui, visual, core, data, event, sound, logging
import os
import random
from datetime import datetime
import os.path

# --- 2. Define Constants ---

# Timing (in seconds)
FIXATION_DURATION = 2.0
ITI_DURATION = 2.0     # Inter-trial interval
# Varighed af babble FØR mask/prime sekvensen
BABBLE_DURATION_BEFORE_PRIMES = 1.0


# --- Trial Counts & Stimuli Setup ---
# Mapper som scriptet vil lede efter i /audio/ mappen
COMPRESSION_LEVELS = ['0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8']

# Antal ord der skal vælges fra HVER mappe
N_PRACTICE_WORDS_PER_FOLDER = 1
N_MAIN_WORDS_PER_FOLDER = 1 # vi skal aftale hvor mange

# Totaler (beregnes automatisk)
N_LEVELS = len(COMPRESSION_LEVELS)
N_PRACTICE_TRIALS = N_LEVELS * N_PRACTICE_WORDS_PER_FOLDER # Giver 8
N_MAIN_TRIALS = N_LEVELS * N_MAIN_WORDS_PER_FOLDER     # Giver 80

# Taster
QUIT_KEY = 'escape'
SUBMIT_KEY = 'return'

# Pauser (efter 20, 40, og 60 af de 80 main trials)
MAIN_TRIAL_BREAK_POINTS = []


# --- 3. Setup Functions ---

def get_participant_info():
    """Viser en dialogboks for at få deltagerinfo (ID, session)."""
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
    """Sætter kerne-komponenterne op: vindue, handler, stier."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Gemmer data i en separat mappe for dette eksperiment
    data_dir = os.path.join(base_dir, 'data_typing')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Created data directory: {data_dir}")

    # Filnavn
    file_name = (
        f"{participant_info['Participant ID']}_"
        f"{participant_info['Session']}_"
        f"{participant_info['date']}_typing" # Tilføj suffix
    )
    
    data_file_path = os.path.join(data_dir, file_name)
    
    exp_handler = data.ExperimentHandler(
        name='SubliminalAudio_Typing',
        version='1.0',
        extraInfo=participant_info,
        runtimeInfo=True,
        originPath=__file__,
        savePickle=True,
        saveWideText=True,
        dataFileName=data_file_path
    )
    
    # Vindue
    win = visual.Window(
        size=[1000, 800],
        fullscr=True,
        screen=0,
        winType='pyglet',
        allowGUI=False,
        monitor='testMonitor',
        color=[0, 0, 0],
        units='height'
    )
    
    win.mouseVisible = False
    logging.console.setLevel(logging.WARNING)
    
    return win, exp_handler, base_dir


def load_reusable_stimuli(win, base_dir):
    """Forud-loader alle stimuli der bruges gentagne gange."""
    stimuli = {}
    
    # 1. Fikseringskryds
    stimuli['fixation'] = visual.TextStim(
        win, text='+',
        height=0.1,
        color='white'
    )
    
    # 2. Prompt-tekst (Hvad hørte du?)
    stimuli['prompt_text'] = visual.TextStim(
        win,
        text="Hvilket ord mener du, du hørte?",
        height=0.06,
        color='white',
        wrapWidth=1.5,
        pos=(0, 0.3) # Placeret i toppen
    )

    # 3. Tekst-display (viser hvad brugeren skriver)
    stimuli['typing_display'] = visual.TextStim(
        win,
        text="", # Vil blive sat på hvert trial
        height=0.1,
        color='white',
        wrapWidth=1.5,
        pos=(0, 0) # Centreret
    )
    
    # 4. Instruktionstekst (generisk)
    stimuli['instructions'] = visual.TextStim(
        win,
        text="", 
        height=0.05,
        color='white',
        wrapWidth=1.5
    )

    # 5. Feedback-tekst (til træning)
    stimuli['feedback'] = visual.TextStim(
        win,
        text="",
        height=0.05,
        color='white',
        wrapWidth=1.5
    )
    
    # 6. Inter-trial tekst
    stimuli['ITI_text'] =  visual.TextStim(
        win,
        text="Et nyt trial begynder om lidt...",
        height=0.05,
        color='white',
        wrapWidth=1.5
    )
    
    # 7. 'Ud' lyd (sensor-beep.wav)
    beep_path = os.path.join(base_dir, 'sensor-beep.wav')
    stimuli['out_sound'] = sound.Sound(beep_path, autoLog=False)
    
    return stimuli


def show_instructions(win, text_stim, message, wait_for_key='space'):
    """Hjælpefunktion til at vise instrukser."""
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
    """Hjælperfunktion til at hente filer fra en mappe."""
    return [f for f in os.listdir(directory) if not f.startswith('.')]

def get_word_from_filename(filename):
    """Hjælperfunktion til at få 'ord' fra 'ord.wav'."""
    return os.path.splitext(filename)[0].split('_')[0]

def generate_trial_lists(base_dir):
    """
    Genererer trial-lister for både træning og hovedeksperiment.
    Sikrer at de samme ord ikke bruges i begge.
    """
    print("Generating trial lists...")
    
    # --- Stier ---
    audio_dir = os.path.join(base_dir, 'audio')
    babbling_dir = os.path.join(base_dir, 'babbling')
    masks_dir = os.path.join(base_dir, 'masks')
    
    # --- Load Lyd-Assets ---
    try:
        babbling_list = get_files_from_dir(babbling_dir)
        mask_list = get_files_from_dir(masks_dir)
    except FileNotFoundError as e:
        print(f"FATAL ERROR: Cannot find masks or babbling directory. {e}")
        core.quit()

    if not babbling_list or not mask_list:
        print("FATAL ERROR: Masks or babbling directory is empty.")
        core.quit()

    practice_list = []
    main_list = []
    
    words_needed_per_folder = N_PRACTICE_WORDS_PER_FOLDER + N_MAIN_WORDS_PER_FOLDER

    # --- Loop gennem hvert komprimeringsniveau ---
    for level in COMPRESSION_LEVELS:
        folder_path = os.path.join(audio_dir, level)
        
        try:
            files_in_folder = get_files_from_dir(folder_path)
        except FileNotFoundError:
            print(f"FATAL ERROR: Kan ikke finde mappen: {folder_path}")
            core.quit()
            
        # Tjek om vi har nok ord
        if len(files_in_folder) < words_needed_per_folder:
            print(f"FATAL ERROR: Ikke nok filer i mappen {folder_path}.")
            print(f"Fandt {len(files_in_folder)}, men skal bruge {words_needed_per_folder} "
                  f"({N_PRACTICE_WORDS_PER_FOLDER} practice + {N_MAIN_WORDS_PER_FOLDER} main).")
            core.quit()
            
        # Bland filerne og vælg
        random.shuffle(files_in_folder)
        
        practice_files = files_in_folder[0:N_PRACTICE_WORDS_PER_FOLDER]
        main_files = files_in_folder[N_PRACTICE_WORDS_PER_FOLDER : words_needed_per_folder]
        
        # Opret practice trials
        for f in practice_files:
            practice_list.append({
                'compression_level': level,
                'prime_file': f,
                'correct_word': get_word_from_filename(f),
                'babbling_file': random.choice(babbling_list),
                'mask1_file': random.choice(mask_list),
                'mask2_file': random.choice(mask_list)
            })
            
        # Opret main trials
        for f in main_files:
            main_list.append({
                'compression_level': level,
                'prime_file': f,
                'correct_word': get_word_from_filename(f),
                'babbling_file': random.choice(babbling_list),
                'mask1_file': random.choice(mask_list),
                'mask2_file': random.choice(mask_list)
            })

    # Bland rækkefølgen af alle trials til sidst
    random.shuffle(practice_list)
    random.shuffle(main_list)
    
    print(f"Successfully generated {len(practice_list)} practice trials.")
    print(f"Successfully generated {len(main_list)} main trials.")
    return practice_list, main_list


# --- 5. Core Logic: Trial Execution ---

def run_trial(win, base_dir, trial_info, trial_handler, stimuli, rt_clock, babble_before_prime):
    """
    Kører et enkelt trial.
    """
    
    # --- 1. Fiksering ---
    stimuli['fixation'].draw()
    win.flip()
    core.wait(FIXATION_DURATION)
    
    # --- 2. Audio Sekvens ---
    
    # Load lyde
    babble_path = os.path.join(base_dir, 'babbling', trial_info['babbling_file'])
    mask1_path = os.path.join(base_dir, 'masks', trial_info['mask1_file'])
    mask2_path = os.path.join(base_dir, 'masks', trial_info['mask2_file'])
    
    # NY prime path
    prime_path = os.path.join(
        base_dir,
        'audio',
        trial_info['compression_level'],
        trial_info['prime_file']
    )
    
    try:
        babble_sound = sound.Sound(babble_path, autoLog=False)
        mask1_sound = sound.Sound(mask1_path, autoLog=False)
        mask2_sound = sound.Sound(mask2_path, autoLog=False)
        prime_sound = sound.Sound(prime_path, autoLog=False)
    except Exception as e:
        print(f"FEJL ved indlæsning af lyd: {e}")
        return 'QUIT' # Afbryd hvis en lydfil er korrupt

    # Udfør tidslinje
    babble_sound.play()  
    core.wait(babble_before_prime) # Babble i 1s

    # --- Synkrone lyde (spil og vent) ---
    mask1_sound.play()
    core.wait(mask1_sound.getDuration()) 

    prime_sound.play()
    core.wait(prime_sound.getDuration())
    
    mask2_sound.play()
    core.wait(mask2_sound.getDuration())
    
    babble_sound.stop()
    
    # --- 3. Tekst-input (NYT) ---
    
    typed_string = ""
    stimuli['typing_display'].setText(typed_string)
    
    # Nulstil RT-ur. Vi fanger RT til det *første* tryk.
    rt_clock.reset()
    rt_first_press = None
    
    event.clearEvents(eventType='keyboard')

    # Typing-loop
    while True:
        # Tegn prompt og det indtastede
        stimuli['prompt_text'].draw()
        stimuli['typing_display'].draw()
        win.flip()
        
        # Vent på et tastetryk
        key_list = event.waitKeys(keyList=None, timeStamped=rt_clock)
        key, timestamp = key_list[0]
        
        # Gem kun RT for det allerførste tastetryk
        if rt_first_press is None:
            rt_first_press = timestamp

        # Håndter taster
        if key == QUIT_KEY:
            return 'QUIT'
        elif key == SUBMIT_KEY:
            break # Bryd løkken og aflever svar
        elif key == 'backspace':
            typed_string = typed_string[:-1]
        elif key == 'space':
            typed_string += ' ' # Tillad mellemrum
        elif len(key) == 1: # Tjek om det er en enkelt karakter (a, b, 1, 2 etc.)
            typed_string += key
        
        # Opdater teksten
        stimuli['typing_display'].setText(typed_string)

    
    # --- 4. Gem Data ---
    # Normaliser både svar og korrekt ord for at undgå fejl
    submitted_word = typed_string.strip().lower()
    correct_word = trial_info['correct_word'].strip().lower()
    
    accuracy = 0
    if submitted_word == correct_word:
        accuracy = 1
        
    trial_handler.addData('response_word', submitted_word)
    trial_handler.addData('rt_first_press', rt_first_press)
    trial_handler.addData('accuracy', accuracy)
    # Gem også de data, der er i trial_info
    trial_handler.addData('compression_level', trial_info['compression_level'])
    trial_handler.addData('correct_word', trial_info['correct_word']) # Gemmer det rene ord
    trial_handler.addData('prime_file', trial_info['prime_file'])

    
    # --- 5. ITI (Inter-Trial Interval) ---
    stimuli['ITI_text'].draw()
    win.flip()
    core.wait(ITI_DURATION)
    stimuli['out_sound'].play() 
    
    return None


# --- 6. Main Experiment Flow ---

def main():
    """
    Hovedfunktionen der kører hele eksperimentet.
    """
    result = None
    try:
        # --- 1. Setup ---
        participant_info = get_participant_info()
        win, exp_handler, base_dir = setup_experiment(participant_info)
        stimuli = load_reusable_stimuli(win, base_dir)
        rt_clock = core.Clock() 
        
        # --- 2. Generer Trial Lister ---
        practice_list, main_list = generate_trial_lists(base_dir)
        
        # --- 3. Opret Trial Handlers ---
        practice_trials = data.TrialHandler(
            trialList=practice_list, nReps=1, method='sequential', name='practice'
        )
        main_trials = data.TrialHandler(
            trialList=main_list, nReps=1, method='sequential', name='main'
        )
        
        exp_handler.addLoop(practice_trials)
        exp_handler.addLoop(main_trials)
        
        # --- 4. Kør Træning ---
        practice_instructions = (
            "Velkommen til træningsrunden.\n\n"
            "Du vil høre en række lyde. Din opgave er at identificere \n"
            "det ord, der var gemt i lydene.\n\n"
            "Efter lydene skal du skrive det ord, du hørte, \n"
            "og trykke 'Enter' for at afgive dit svar.\n\n"
            "Tryk 'space' for at begynde."
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

        # --- 5. Kør Hovedeksperiment ---
        main_instructions = (
            "Træning er slut. Nu begynder hovedeksperimentet.\n\n"
            "Opgaven er den samme.\n"
            "Skriv det ord, du hører, og tryk 'Enter'.\n\n"
            "Der vil være korte pauser undervejs.\n\n"
            "Tryk 'space' for at starte."
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
            
            # Tjek for pauser
            if current_trial_n in MAIN_TRIAL_BREAK_POINTS:
                break_message = (
                    f"Du har gennemført {current_trial_n + 1} ud af {N_MAIN_TRIALS} trials.\n\n"
                    "Tid til en kort pause.\n\n"
                    "Tryk 'space' for at fortsætte, når du er klar."
                )
                show_instructions(win, stimuli['instructions'], break_message)
        
        # --- 6. Afslut Eksperiment ---
        if quit_experiment:
            end_message = "Data er blevet gemt.\n\nTak for din tid."
        else:
            end_message = "Eksperimentet er slut!\n\nTak for din deltagelse."
            
        show_instructions(win, stimuli['instructions'], end_message, wait_for_key='space')

    except Exception as e:
        print(f"En uventet fejl opstod: {e}")
        logging.error(e)
    
    finally:
        # --- 7. Oprydning ---
        if 'exp_handler' in locals():
            exp_handler.close()
        
        if 'win' in locals() and win:
            win.close()
            
        core.quit()


# --- 7. Script Execution ---
if __name__ == "__main__":
    main()