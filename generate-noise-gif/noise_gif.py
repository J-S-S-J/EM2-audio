import numpy as np
from PIL import Image

# --- Configuration ---
WIDTH = 300  # Width of the GIF in pixels
HEIGHT = 200 # Height of the GIF in pixels
NUM_FRAMES = 30  # Total number of frames in the GIF
FRAME_DURATION_MS = 50 # Duration of each frame in milliseconds (e.g., 50ms = 20 Hz)
FILENAME = "dynamic_color_noise_mask.gif"
# --- End Configuration ---

def generate_noise_frame(width, height):
    """
    Creates a single frame of random color "TV static" noise.
    """
    # Create a 3D array (height, width, 3 for RGB) of random bytes (0-255)
    data = np.random.randint(0, 256, size=(height, width, 3), dtype=np.uint8)
    
    # Convert the numpy array to a PIL Image object in 'RGB' mode
    img = Image.fromarray(data, 'RGB')
    return img

def create_noise_gif(filename, width, height, num_frames, duration):
    """
    Generates and saves a dynamic noise GIF.
    """
    print(f"Generating {num_frames} frames for '{filename}'...")
    
    frames = [] # List to hold all the Image objects
    
    for _ in range(num_frames):
        frame = generate_noise_frame(width, height)
        frames.append(frame)
        
    # Save the frames as a GIF
    # frames[0] is the first frame
    # save_all=True tells it to save all subsequent frames
    # append_images=frames[1:] provides the rest of the frames
    # duration is the time per frame in ms
    # loop=0 means the GIF will loop indefinitely
    frames[0].save(
        filename,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0
    )
    
    print(f"Successfully saved '{filename}'!")

# --- Main execution ---
if __name__ == "__main__":
    create_noise_gif(FILENAME, WIDTH, HEIGHT, NUM_FRAMES, FRAME_DURATION_MS)