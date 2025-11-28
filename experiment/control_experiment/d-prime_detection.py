"""
================================================================================
PsychoPy Subliminal Audio Priming (SDT / d-prime DETECTION)
================================================================================

Dette script implementerer et Signal Detection Theory (SDT) kontrol-eksperiment.
- Objektiv: Måle d' (sensitivitet) for at detektere et ord
             ved 8 forskellige niveauer af tidskomprimering.
- Design: Deltagere hører en audiosekvens og skal angive,
          om de hørte et ord eller ej (Ja/Nej).
- Trials: 50% Signal-Present (et ord er til stede)
          50% Signal-Absent (stilhed er til stede) 
- Task: Ja/Nej (2-AFC), 'm' for Ja, 'z' for Nej.

File Struktur:
/Experiment_Folder/
|
├── main_detection_experiment.py  (Dette script)
├── sensor-beep.wav
|
├── /audio/
|   ├── /0.1/
|   |   ├── bange_compressed.wav
|   |   └── ...
|   ...
|   └── /0.8/
|
├── /masks/
├── /babbling/
|
└── /data_detection/              <-- Ny output mappe
"""

# --- 1. Import Libraries ---
# from psychopy import prefs 
# prefs.hardware['audioLib'] = ['sounddevice', 'PTB', 'pyo', 'pygame']

from psychopy import gui, visual, core, data, event, sound, logging
import os
import random
from datetime import datetime
import os.path

# --- 2. Define Constants ---

# Timing (in seconds)
FIXATION_DURATION = 1.0
ITI_DURATION = 1.0     # Inter-trial interval
# BABBLE_DURATION_BEFORE_PRIMES er nu tilfældig (defineres i main loop)


# --- Trial Counts & Stimuli Setup ---
COMPRESSION_LEVELS = ['0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7']
N_LEVELS = len(COMPRESSION_LEVELS)

# Antal "Signal-Present" trials per niveau
N_PRACTICE_REPS_PER_LEVEL = 1 # 1 'present' + 1 'absent' per niveau
N_MAIN_REPS_PER_LEVEL = 7  # plejede at være 15, men er for mange for et kontrol forsøg


N_PRACTICE_TRIALS = 2 
# N_MAIN_TRIALS = 8 levels * 10 reps * 2 types (pres/abs) = 160
N_MAIN_TRIALS = N_LEVELS * N_MAIN_REPS_PER_LEVEL * 2

# Taster
QUIT_KEY = 'escape'
YES_KEY = 'm' # 'm' er til højre på et QWERTY-tastatur
NO_KEY = 'z'  # 'z' er til venstre
VALID_KEYS = [YES_KEY, NO_KEY, QUIT_KEY]

# Pauser (efter 40, 80, og 120 af de 160 main trials)
MAIN_TRIAL_BREAK_POINTS = [29, 59, 89, 119, 149]  # [39, 79, 119]


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
    data_dir = os.path.join(base_dir, 'data_detection')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Created data directory: {data_dir}")

    # Filnavn
    file_name = (
        f"{participant_info['Participant ID']}_"
        f"{participant_info['Session']}_"
        f"{participant_info['date']}_detection" # Tilføj suffix
    )
    
    data_file_path = os.path.join(data_dir, file_name)
    
    exp_handler = data.ExperimentHandler(
        name='SubliminalAudio_Detection',
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
    
    # 2. Prompt-tekst (Ja/Nej)
    stimuli['prompt_text'] = visual.TextStim(
        win,
        text="Hørte du et ord?",
        height=0.08,
        color='white',
        wrapWidth=1.5,
        pos=(0, 0.1) # Lidt over midten
    )

    # 3. Taste-prompt (Viser tasterne)
    stimuli['key_prompt'] = visual.TextStim(
        win,
        text=f"NEJ = '{NO_KEY}'   /   JA = '{YES_KEY}'",
        height=0.05,
        color='white',
        wrapWidth=1.5,
        pos=(0, -0.2) # Lidt under midten
    )
    
    # 4. Instruktionstekst (generisk)
    stimuli['instructions'] = visual.TextStim(
        win,
        text="", 
        height=0.05,
        color='white',
        wrapWidth=1.5
    )

    # 5. Feedback-tekst (Beholdt for struktur, men bruges ikke)
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
    """
    Hjælpefunktion til at få 'bange' fra 'bange_compressed.wav'.
    """
    # f.eks. 'bange_compressed.wav' -> 'bange_compressed'
    filename_without_ext = os.path.splitext(filename)[0]
    # f.eks. 'bange_compressed' -> ['bange', 'compressed'] -> 'bange'
    return filename_without_ext.split('_')[0]

def generate_trial_lists(base_dir):
    """
    Genererer trial-lister med 50% Signal-Present og 50% Signal-Absent
    for både træning og hovedeksperiment.
    """
    print("Generating SDT trial lists...")
    
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
    
    # Antal *ord-filer* vi skal bruge fra hver mappe
    files_needed_per_folder = N_PRACTICE_REPS_PER_LEVEL + N_MAIN_REPS_PER_LEVEL

    # --- Loop gennem hvert komprimeringsniveau ---
    for level in COMPRESSION_LEVELS:
        folder_path = os.path.join(audio_dir, level)
        
        try:
            files_in_folder = get_files_from_dir(folder_path)
        except FileNotFoundError:
            print(f"FATAL ERROR: Kan ikke finde mappen: {folder_path}")
            core.quit()
            
        # Tjek om vi har nok ord
        if len(files_in_folder) < files_needed_per_folder:
            print(f"FATAL ERROR: Ikke nok filer i mappen {folder_path}.")
            print(f"Fandt {len(files_in_folder)}, men skal bruge {files_needed_per_folder} "
                  f"({N_PRACTICE_REPS_PER_LEVEL} practice + {N_MAIN_REPS_PER_LEVEL} main).")
            core.quit()
            
        # Bland filerne og vælg
        random.shuffle(files_in_folder)
        
        practice_files = files_in_folder[0:N_PRACTICE_REPS_PER_LEVEL]
        main_files = files_in_folder[N_PRACTICE_REPS_PER_LEVEL : files_needed_per_folder]
        
        # --- Opret Practice Trials (Present + Absent) ---
        for f in practice_files:
            # Signal-Present trial
            practice_list.append({
                'signal_type': 'present',
                'compression_level': level,
                'prime_file': f,
                'correct_word': get_word_from_filename(f),
                'babbling_file': random.choice(babbling_list),
                'mask1_file': random.choice(mask_list),
                'mask2_file': random.choice(mask_list)
            })
            # Signal-Absent trial
            practice_list.append({
                'signal_type': 'absent',
                'compression_level': level, # Stadig relevant for d'-analyse
                'prime_file': 'SILENCE',
                'correct_word': 'NA',
                'babbling_file': random.choice(babbling_list),
                'mask1_file': random.choice(mask_list),
                'mask2_file': random.choice(mask_list)
            })
            
        # --- Opret Main Trials (Present + Absent) ---
        for f in main_files:
            # Signal-Present trial
            main_list.append({
                'signal_type': 'present',
                'compression_level': level,
                'prime_file': f,
                'correct_word': get_word_from_filename(f),
                'babbling_file': random.choice(babbling_list),
                'mask1_file': random.choice(mask_list),
                'mask2_file': random.choice(mask_list)
            })
            # Signal-Absent trial
            main_list.append({
                'signal_type': 'absent',
                'compression_level': level,
                'prime_file': 'SILENCE',
                'correct_word': 'NA',
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
    
    prime_sound = None # Vigtigt: Start som None
    
    try:
        babble_sound = sound.Sound(babble_path, autoLog=False)
        mask1_sound = sound.Sound(mask1_path, autoLog=False)
        mask2_sound = sound.Sound(mask2_path, autoLog=False)
        
        # Load kun prime-lyd hvis det er et 'present' trial
        if trial_info['signal_type'] == 'present':
            prime_path = os.path.join(
                base_dir,
                'audio',
                trial_info['compression_level'],
                trial_info['prime_file']
            )
            prime_sound = sound.Sound(prime_path, autoLog=False)
            
    except Exception as e:
        print(f"FEJL ved indlæsning af lyd: {e}")
        return 'QUIT' # Afbryd hvis en lydfil er korrupt

    # Udfør tidslinje
    babble_sound.play()  
    core.wait(babble_before_prime) # Tilfældig varighed

    # --- Synkrone lyde (spil og vent) ---
    mask1_sound.play()
    core.wait(mask1_sound.getDuration()) 

    # Spil kun prime-lyden HVIS den er loadet (dvs. 'present' trial)
    if prime_sound:
        prime_sound.play()
        core.wait(prime_sound.getDuration())
    
    mask2_sound.play()
    core.wait(mask2_sound.getDuration())
    
    babble_sound.stop()
    
    # --- 3. Ja/Nej Respons ---
    
    stimuli['prompt_text'].draw()
    stimuli['key_prompt'].draw()
    win.flip()
    
    # Nulstil RT-ur og vent på respons
    rt_clock.reset()
    event.clearEvents(eventType='keyboard')
    
    response = event.waitKeys(
        maxWait=float('inf'),
        keyList=VALID_KEYS,
        timeStamped=rt_clock
    )
    
    key, rt = None, None
    if response:
        key = response[0][0]
        rt = response[0][1]

    # --- 4. Gem Data ---
    
    # Find trial outcome (Hit, Miss, FA, CR)
    signal = trial_info['signal_type']
    outcome = "NA"
    
    if signal == 'present' and key == YES_KEY:
        outcome = 'Hit'
    elif signal == 'present' and key == NO_KEY:
        outcome = 'Miss'
    elif signal == 'absent' and key == YES_KEY:
        outcome = 'False Alarm'
    elif signal == 'absent' and key == NO_KEY:
        outcome = 'Correct Rejection'
        
    trial_handler.addData('response_key', key)
    trial_handler.addData('rt', rt)
    trial_handler.addData('trial_outcome', outcome)
    
    # Gem også de data, der er i trial_info
    trial_handler.addData('signal_type', trial_info['signal_type'])
    trial_handler.addData('compression_level', trial_info['compression_level'])
    trial_handler.addData('correct_word', trial_info['correct_word'])
    trial_handler.addData('prime_file', trial_info['prime_file'])
    trial_handler.addData('babble_duration', babble_before_prime) # Gem tilfældig varighed

    
    # --- 5. ITI (Inter-Trial Interval) ---
    stimuli['ITI_text'].draw()
    win.flip()
    core.wait(ITI_DURATION)
    stimuli['out_sound'].play() 
    
    # --- 6. Tjek for Quit ---
    if key == QUIT_KEY:
        return 'QUIT'
    
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
            "Du vil høre en række lyde. Nogle gange er et ord gemt i lydene,\n"
            "andre gange er der kun støj.\n\n"
            "De gemte ord vil være danske ord med to-tre stavelser.\n\n"
            "Din opgave er at trykke 'Nej' eller 'Ja' for, \n"
            "om du mener, du hørte et ord.\n\n"
            f"Tryk '{NO_KEY}' for NEJ.\n"
            f"Tryk '{YES_KEY}' for JA.\n\n"
            "Tryk 'mellerum' for at begynde."
        )
        show_instructions(win, stimuli['instructions'], practice_instructions)
        
        for trial in practice_trials:
            # Sæt tilfældig babble-varighed
            val = random.uniform(0.5, 1.5)
            result = run_trial(
                win, base_dir, trial, practice_trials, stimuli, rt_clock, val
            )
            
            if result == 'QUIT':
                break
            
            # Ingen feedback i træning, som aftalt
            exp_handler.nextEntry() 

        if result == 'QUIT':
            raise KeyboardInterrupt("Experiment aborted by user.")

        # --- 5. Kør Hovedeksperiment ---
        main_instructions = (
            "Træning er slut. Nu begynder hovedeksperimentet.\n\n"
            "Opgaven er den samme.\n"
            f"Tryk '{NO_KEY}' for NEJ, og '{YES_KEY}' for JA.\n\n"
            "Der vil være korte pauser undervejs.\n\n"
            "Tryk 'mellemrum' for at begynde."
        )
        show_instructions(win, stimuli['instructions'], main_instructions)
        
        quit_experiment = False
        for trial in main_trials:
            current_trial_n = main_trials.thisN 
            
            # Sæt tilfældig babble-varighed
            val = random.uniform(0.5, 1.5)
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
                    f"Du har gennemført nu {current_trial_n + 1} ud af {N_MAIN_TRIALS} runder.\n\n"
                    "Tid til en kort pause.\n\n"
                    "Tryk 'mellemrum' for at fortsætte, når du er klar."
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
