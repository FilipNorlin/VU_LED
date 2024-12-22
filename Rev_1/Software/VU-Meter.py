import pygame
import pyaudio
import numpy as np
import math
import time

# Initialize Pygame
pygame.init()

# Set up screen
screen = pygame.display.set_mode((800, 200))
pygame.display.set_caption("VU Meter")

# Updated LED thresholds (dB)
db_thresholds = [0, -2, -6, -12, -18, -30]

# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LED_COLOR = (0, 255, 0)

# Set up audio parameters
rate = 22050  # Reduced sample rate
chunk = 512  # Reduced chunk size
device_index = (
    2  # MacBook Air Microphone (replace with the correct device index if needed)
)

# Initialize PyAudio
p = pyaudio.PyAudio()

# Check available devices
print("Available audio devices:")
for i in range(p.get_device_count()):
    dev_info = p.get_device_info_by_index(i)
    print(
        f"Device {i}: {dev_info['name']}, Input: {dev_info['maxInputChannels']} channels"
    )

# Open audio stream
stream = p.open(
    format=pyaudio.paInt16,
    channels=1,  # Mono audio input
    rate=rate,
    input=True,
    input_device_index=device_index,
    frames_per_buffer=chunk,
    stream_callback=None,
)  # Set to None for non-blocking mode


# Function to calculate dB from audio data
def get_dB(audio_data):
    # Calculate RMS (Root Mean Square) value
    rms = np.sqrt(np.mean(np.square(audio_data)))
    # Calculate dB (20 * log10(RMS))
    if rms > 0:
        db = 20 * math.log10(rms)
    else:
        db = -100  # To handle cases with no sound
    return db


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    try:
        # Read audio data
        audio_data = np.frombuffer(
            stream.read(chunk, exception_on_overflow=False), dtype=np.int16
        )
        db_level = get_dB(audio_data)
    except IOError:  # Handle input overflow
        print("Audio buffer overflow. Skipping frame.")
        time.sleep(0.1)  # Avoid tight looping and give buffer time to clear
        continue  # Skip this iteration if there was an overflow

    # Debugging: print dB level
    print(f"DB Level: {db_level}")

    # Visual feedback for debugging (Red screen for debugging)
    screen.fill((255, 0, 0))  # Red background to show the program is running
    pygame.display.flip()

    # Draw LEDs based on dB level
    for i, threshold in enumerate(db_thresholds):
        if db_level >= threshold:
            pygame.draw.circle(
                screen, LED_COLOR, (100 + i * 120, 100), 20
            )  # Draw LED circles
        else:
            pygame.draw.circle(screen, BLACK, (100 + i * 120, 100), 20)  # Turn off LED

    # Update the display
    pygame.display.flip()

# Close the stream and PyAudio
stream.stop_stream()
stream.close()
p.terminate()

# Quit Pygame
pygame.quit()
