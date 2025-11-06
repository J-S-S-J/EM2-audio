"""
main.py: PsychoPy script for a subliminal audio priming experiment.

This script runs a within-subjects experiment investigating the effect of
subliminal emotional audio primes on valence ratings of faces.

It assumes the following directory structure:
/Subliminal_Experiment/
|
├── main.py
├── conditions.csv
├── /faces/ (p1.jpg, p2.jpg, ...)
├── /primes/ (happy_1.mp3, sad_1.mp3, silence_100ms.mp3, ...)
├── /masks/ (rev_1.mp3, rev_2.mp3, ...)
├── /other_sounds/ (out_sound.mp3)
├── /face_mask/ (mask.gif)
└── /data/ (output directory)
"""

# Import necessary libraries
import os
import random
from datetime import datetime
from psychopy import core, visual, event, gui, data, sound, logging

# --- Experiment Constants ---
# Timing (in seconds)
FIXATION_DURATION = 2.0
FACE_DURATION = 0.5
FACE_MASK_DURATION = 0.25
ITI_DURATION = 1.0

# Trial numbers
N_PRACTICE_TRIALS = 10
N_TRIALS_PER_BLOCK = 70
N_BLOCKS = 3

# Rating keys
RATING_KEYS = ['1', '2', '3', '4', '5', '6', '7']
ESCAPE_KEY = 'escape'


class SubliminalExperiment:
    """
    Encapsulates the entire subliminal audio priming experiment.

    This class handles:
    - Participant setup
    - Window and stimuli initialization
    - Loading conditions
    - Running practice and main trial loops
    - Executing the precise trial sequence
    - Secure data handling and saving
    """

    def __init__(self):
        """
        Initializes the experiment, sets up paths, gets participant info,
        and pre-loads all necessary components.
        """
        self.win = None
        self.exp_handler = None
        self.all_conditions = None
        self.mask_files = []
        self.exp_info = {}

        try:
            # --- 1. Define Paths ---
            # Use os.path.abspath and os.path.dirname to get the script's dir
            self.base_dir = os.path.dirname(os.path.abspath(__file__))
            self.data_dir = os.path.join(self.base_dir, 'data')
            self.face_dir = os.path.join(self.base_dir, 'faces')
            self.prime_dir = os.path.join(self.base_dir, 'primes')
            self.mask_dir = os.path.join(self.base_dir, 'masks')
            self.other_sound_dir = os.path.join(self.base_dir, 'other_sounds')
            self.face_mask_dir = os.path.join(self.base_dir, 'face_mask')
            self.conditions_file = os.path.join(self.base_dir, 'conditions.csv')

            # Ensure data directory exists
            if not os.path.exists(self.data_dir):
                os.makedirs(self.data_dir)

            # --- 2. Get Participant Info ---
            self.get_participant_info()

            # --- 3. Set up Data Handling ---
            self.setup_experiment_handler()

            # --- 4. Set up Window ---
            self.setup_window()

            # --- 5. Pre-load All Stimuli ---
            self.load_stimuli()

            # --- 6. Initialize Clocks ---
            self.trial_clock = core.Clock()  # For timing entire trials (if needed)
            self.rt_clock = core.Clock()     # For timing the valence rating

        except Exception as e:
            print(f"Error during initialization: {e}")
            core.quit()

    def get_participant_info(self):
        """
        Displays a dialog box to collect participant and session info.
        If 'Cancel' is hit, the script exits.
        """
        info_dict = {'participant': '', 'session': '01'}
        dlg = gui.DlgFromDict(dictionary=info_dict,
                                title="Experiment Setup",
                                fixed=['session'])
        if not dlg.OK:
            print("User cancelled the experiment.")
            core.quit()

        # Add current date to exp_info
        info_dict['date'] = datetime.now().strftime('%Y-%m-%d_%H-%M')
        self.exp_info = info_dict

    def setup_experiment_handler(self):
        """
        Initializes the PsychoPy ExperimentHandler for data saving.
        """
        filename = (
            f"{self.exp_info['participant']}_"
            f"{self.exp_info['session']}_"
            f"{self.exp_info['date']}.csv"
        )
        data_filepath = os.path.join(self.data_dir, filename)

        self.exp_handler = data.ExperimentHandler(
            name='SubliminalAudioPriming',
            version='1.0',
            extraInfo=self.exp_info,
            runtimeInfo=True,
            originPath=__file__,
            savePickle=True,
            saveWideText=True,
            dataFileName=data_filepath
        )
        
        # Set up a log file for more detailed, non-data-frame info
        log_filepath = data_filepath.replace('.csv', '.log')
        logging.LogFile(log_filepath, level=logging.EXP, filemode='w')

    def setup_window(self):
        """
        Initializes the main PsychoPy window.
        """
        self.win = visual.Window(
            size=[1920, 1080],  # Or your specific monitor resolution
            fullscr=True,
            screen=0,
            winType='pyglet',
            allowGUI=False,
            allowStencil=False,
            monitor='testMonitor',
            color=[0, 0, 0],  # Black background
            colorSpace='rgb',
            units='height'
        )
        self.exp_info['frameRate'] = self.win.getActualFrameRate()
        if self.exp_info['frameRate'] is None:
            logging.warning("Could not get frame rate. Using 60Hz as default.")
            self.exp_info['frameRate'] = 60

    def load_stimuli(self):
        """
        Pre-defines all reusable visual and audio stimuli.
        """
        print("Loading stimuli...")
        # --- Visual Stimuli ---
        self.fixation_cross = visual.TextStim(
            self.win, text='+', height=0.1, color='white'
        )
        self.rating_scale_text = visual.TextStim(
            self.win,
            text="How positive or negative is the face?\n\n(1=Very Negative, 7=Very Positive)",
            height=0.05,
            wrapWidth=1.5
        )
        self.feedback_text = visual.TextStim(
            self.win, text='', height=0.05, color='white'
        )
        # Face stim is an empty container; its image will be set on each trial
        self.face_stim = visual.ImageStim(self.win, size=(0.5, 0.5))

        # Face mask stim (GIF)
        mask_gif_path = os.path.join(self.face_mask_dir, 'mask.gif')
        self.face_mask_stim = visual.ImageStim(
            self.win, image=mask_gif_path, size=(0.5, 0.5)
        )

        # --- Audio Stimuli ---
        # Initialize sound backend (pygame is often reliable)
        try:
            sound.Sound.init(backend='pygame')
            print("Using 'pygame' sound backend.")
        except:
            print("pygame backend failed, trying default.")
            pass # Use default

        # Pre-load the non-trial-specific "out" sound
        out_sound_path = os.path.join(self.other_sound_dir, 'out_sound.mp3')
        self.out_sound = sound.Sound(out_sound_path)

        # Load the *list* of available mask files
        self.mask_files = [
            f for f in os.listdir(self.mask_dir)
            if f.endswith('.mp3')
        ]
        if len(self.mask_files) < 2:
            raise RuntimeError("Not enough audio masks found in /masks/ folder. Need at least 2.")
        
        print(f"Found {len(self.mask_files)} mask files.")
        print("Stimuli loaded.")

    def load_conditions(self):
        """
        Loads trial conditions from the conditions.csv file.
        """
        try:
            self.all_conditions = data.importConditions(self.conditions_file)
            print(f"Loaded {len(self.all_conditions)} conditions from CSV.")
        except Exception as e:
            print(f"Failed to load {self.conditions_file}")
            print(e)
            self.close()

    def show_instructions(self, text, keys=None):
        """
        Displays instruction text and waits for a keypress.
        
        Args:
            text (str): The text to display.
            keys (list, optional): List of keys to wait for. 
                                  Defaults to any key.
        """
        instr_stim = visual.TextStim(
            self.win, text=text, height=0.05, wrapWidth=1.5
        )
        instr_stim.draw()
        self.win.flip()

        # Wait for a response
        keys = event.waitKeys(keyList=keys)
        
        # Check for escape
        if ESCAPE_KEY in keys:
            self.close()

    def run_trial(self, trial_data, is_practice=False, trial_n=0, block_n=0):
        """
        Executes the precise 10-step sequence for a single trial.
        
        Args:
            trial_data (dict): A dictionary from the TrialHandler.
            is_practice (bool): Flag for practice trials (adds feedback).
            trial_n (int): The trial number (for data logging).
            block_n (int): The block number (for data logging).
        """
        
        # --- 1. Fixation (2000ms) ---
        self.fixation_cross.draw()
        self.win.flip()
        core.wait(FIXATION_DURATION)

        # --- 2. Mask 1 ---
        # Randomly select a mask file
        mask1_file = random.choice(self.mask_files)
        mask1_path = os.path.join(self.mask_dir, mask1_file)
        mask1_sound = sound.Sound(mask1_path)
        
        # Play the sound and wait for it to finish
        mask1_sound.play(sync=True)

        # --- 3. Prime ---
        prime_file = trial_data['prime_sound_file']
        prime_path = os.path.join(self.prime_dir, prime_file)
        prime_sound = sound.Sound(prime_path)

        # Play the prime and wait for it to finish
        prime_sound.play(sync=True)
        
        # --- 4. Mask 2 ---
        # Select a *different* mask file
        mask2_file = random.choice(
            [f for f in self.mask_files if f != mask1_file]
        )
        mask2_path = os.path.join(self.mask_dir, mask2_file)
        mask2_sound = sound.Sound(mask2_path)
        
        # Play the sound and wait for it to finish
        mask2_sound.play(sync=True)

        # --- 5. Face (500ms) ---
        face_file = trial_data['face_image_file']
        face_path = os.path.join(self.face_dir, face_file)
        self.face_stim.setImage(face_path)
        
        self.face_stim.draw()
        self.win.flip()
        core.wait(FACE_DURATION)

        # --- 6. Face Mask (250ms) ---
        self.face_mask_stim.draw()
        self.win.flip()
        core.wait(FACE_MASK_DURATION)

        # --- 7. Valence Rating ---
        self.rating_scale_text.draw()
        self.win.flip()
        
        # Clear buffer and start RT clock
        event.clearEvents()
        self.rt_clock.reset()

        # Wait for a valid response key
        keys = event.waitKeys(
            keyList=RATING_KEYS + [ESCAPE_KEY],
            maxWait=float('inf'),
            timeStamped=self.rt_clock
        )
        
        # --- 8. Record Response ---
        response, rt = None, None
        
        if keys:
            key_name, key_rt = keys[0] # (key, rt)
            if key_name == ESCAPE_KEY:
                self.close()
            
            response = key_name
            rt = key_rt # This is the RT from the clock reset

        # --- 9. Black Screen (ITI - 1000ms) ---
        self.win.flip()  # Clear the rating scale
        core.wait(ITI_DURATION)

        # --- 10. Out Sound ---
        # Plays *during* the subsequent fixation cross (which is fine)
        self.out_sound.play(sync=False)

        # --- Data Saving ---
        # Add trial-specific data to the ExperimentHandler
        # The TrialHandler automatically adds data from the conditions file
        self.exp_handler.addData('is_practice', is_practice)
        self.exp_handler.addData('block_n', block_n)
        self.exp_handler.addData('trial_n_in_block', trial_n)
        self.exp_handler.addData('mask1_file', mask1_file)
        self.exp_handler.addData('mask2_file', mask2_file)
        self.exp_handler.addData('valence_rating', response)
        self.exp_handler.addData('rating_rt', rt)

        # --- Feedback (Practice Only) ---
        if is_practice:
            feedback_msg = f"You responded: {response}"
            self.feedback_text.setText(feedback_msg)
            self.feedback_text.draw()
            self.win.flip()
            core.wait(1.0) # Show feedback for 1 second

    def run(self):
        """
        The main experiment flow:
        1. Loads conditions
        2. Runs practice block
        3. Runs main experiment blocks
        4. Cleans up
        """
        # --- 1. Load Conditions ---
        self.load_conditions()

        # --- 2. Practice Block ---
        self.show_instructions(
            "Welcome to the experiment.\n\n"
            "You will hear a brief sequence of sounds, followed by a face.\n"
            "Your task is to rate how positive or negative the face feels to you "
            "using the number keys 1 (Very Negative) to 7 (Very Positive).\n\n"
            "We will start with a few practice trials.\n\n"
            "Press any key to begin practice."
        )

        # Randomly sample 10 trials for practice
        practice_conditions = random.sample(self.all_conditions, N_PRACTICE_TRIALS)
        practice_trials = data.TrialHandler(
            trialList=practice_conditions,
            nReps=1,
            method='random',
            name='practice_trials'
        )
        self.exp_handler.addLoop(practice_trials)

        for i, trial in enumerate(practice_trials):
            self.run_trial(trial, is_practice=True, trial_n=i+1, block_n=0)
            self.exp_handler.nextEntry() # Save data after each practice trial

        # --- 3. Main Experiment ---
        self.show_instructions(
            "Practice complete.\n\n"
            "The main experiment will now begin. It is divided into 3 blocks.\n"
            "Remember to rate the face (1-7) as quickly and accurately as possible.\n\n"
            "Press any key to start the first block."
        )

        # Create the main TrialHandler for all 210 trials
        main_trials = data.TrialHandler(
            trialList=self.all_conditions,
            nReps=1,  # nReps=1 because we manually manage the 3 blocks
            method='random',
            name='main_trials'
        )

        # --- Requirement 3.1: Save randomization backup ---
        # This saves the *order* of trials before they are run
        backup_filename = os.path.join(
            self.data_dir,
            f"{self.exp_info['participant']}_{self.exp_info['session']}_randomization_order.txt"
        )
        main_trials.saveAsText(backup_filename, delim=',', fileCollisionMethod='overwrite')
        logging.info(f"Saved trial randomization order to {backup_filename}")
        # ---

        self.exp_handler.addLoop(main_trials)

        # Manually iterate through the 210 trials, adding breaks
        total_trials = N_TRIALS_PER_BLOCK * N_BLOCKS
        for i, trial in enumerate(main_trials):
            # Check for block breaks *before* running the trial
            # i will be 0, 1, ..., 209
            # Break after trial 70 (i=69) and 140 (i=139)
            # Correction: Prompt says 'if i in [70, 140]', which means *at the start*
            # of trial 70 and 140. This is cleaner.
            if i in [N_TRIALS_PER_BLOCK, N_TRIALS_PER_BLOCK * 2]:
                block_completed = i // N_TRIALS_PER_BLOCK
                self.show_instructions(
                    f"You have completed block {block_completed} of {N_BLOCKS}.\n\n"
                    "Take a short break.\n\n"
                    "Press any key to continue."
                )

            # Calculate block and trial numbers
            current_block = (i // N_TRIALS_PER_BLOCK) + 1
            trial_in_block = (i % N_TRIALS_PER_BLOCK) + 1
            
            # Log the start of the trial
            logging.info(f"Running Block: {current_block}, Trial: {trial_in_block}")

            # Run the actual trial
            self.run_trial(
                trial_data=trial,
                is_practice=False,
                trial_n=trial_in_block,
                block_n=current_block
            )
            
            # Save the data for this trial
            self.exp_handler.nextEntry()
            
            # Check for escape *between* trials, just in case
            if event.getKeys([ESCAPE_KEY]):
                self.close()

        # --- 4. Experiment End ---
        self.show_instructions(
            "Experiment complete.\n\n"
            "Thank you for your participation!\n\n"
            "Press any key to exit."
        )
        
        # --- 5. Clean up ---
        self.close()

    def close(self):
        """
        Cleans up all resources and quits the script.
        This is called on 'escape' or at the end of the experiment.
        """
        print("Cleaning up and exiting.")
        if self.win:
            self.win.close()
        
        # ExperimentHandler file saving is typically finalized here or on quit
        if self.exp_handler:
            # You might save extra experiment-wide data here
            # self.exp_handler.addData(...) 
            pass

        core.quit()


# --- Main Execution ---
if __name__ == "__main__":
    """
    Main entry point of the script.
    
    Uses a try...finally block to ensure that PsychoPy
    quits properly even if an error occurs during the experiment.
    """
    exp = None
    try:
        # 1. Create and initialize the experiment object
        exp = SubliminalExperiment()
        
        # 2. Run the experiment
        exp.run()

    except Exception as e:
        print(f"An unhandled error occurred: {e}")
        logging.critical(f"Unhandled error: {e}")
    
    finally:
        # 3. Ensure cleanup, even if an error occurred
        if exp:
            # exp.close() will call core.quit()
            exp.close() 
        else:
            # If exp failed to initialize, just quit
            core.quit()