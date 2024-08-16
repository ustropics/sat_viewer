# create_output.py

from imports import *
from process_data import get_hashed_filenames

import config

img_dir = config.img_dir
media_dir = config.media_dir
current_time = pd.Timestamp.now().strftime("%Y%m%d%H%M%S")


def create_widgets(ds):
    # Create the Play widget and the slider

    # Access the hashed filenames using the function
    hashed_filenames = get_hashed_filenames()

    play = widgets.Play(
        value=0,
        min=0,
        max=ds.sizes['t'] - 1,
        step=1,
        interval=500,
        description="Press play",
        disabled=False
    )
    slider = widgets.IntSlider(min=0, max=ds.sizes['t'] - 1)
    widgets.jslink((play, 'value'), (slider, 'value'))

    # Create buttons to increase and decrease the interval
    interval_increase_button = widgets.Button(description="Decrease Speed")
    interval_decrease_button = widgets.Button(description="Increase Speed")

    # Create a button to save images as an animated GIF or mp4
    save_gif_button = widgets.Button(description="Save as GIF")
    save_mp4_button = widgets.Button(description="Save as MP4")

    # Create an output widget to display images
    output = widgets.Output()

    # Define a function to update the image based on the slider value
    def update_image(change):
        with output:
            output.clear_output(wait=True)

            # Ensure `change['new']` is a valid index
            index = change['new']
            if 0 <= index < len(hashed_filenames):
                filename = hashed_filenames[index]
                file_path = os.path.join(img_dir, f"{filename}.png")

                # Check if file exists before trying to display it
                if os.path.isfile(file_path):
                    display(Image(filename=file_path))
                else:
                    print("File does not exist:", file_path)
            else:
                print("Index out of range:", index)
                
    # Attach the update function to the slider's value change event
    slider.observe(update_image, names='value')

    # Define callback functions for the interval buttons
    def increase_interval(b):
        play.interval += 100  # Adjust the increment as needed
        return play.interval

    def decrease_interval(b):
        # Adjust the decrement as needed
        play.interval = max(100, play.interval - 100)
        return play.interval

    # Define callback function to save images as an animated GIF
    def save_as_gif(b):
        frames = []

        # Ensure the output directory exists
        if not os.path.exists(media_dir):
            os.makedirs(media_dir)

        # Load images into frames
        for i in range(ds.sizes['t']):
            file_path = os.path.join(img_dir, hashed_filenames[i] + ".png")
            if os.path.exists(file_path):
                try:
                    img = PILImage.open(file_path)
                    frames.append(img)
                    print(f"Loaded image: {file_path}")
                except Exception as e:
                    print(f"Error loading image {file_path}: {e}")
            else:
                print(f"Image not found: {file_path}")

        # Check if we have frames to save
        if frames:
            gif_path = os.path.join(
                media_dir, f"{config.widget_values['selected_rgb']}_{current_time}.gif")
            try:
                frames[0].save(gif_path, format='GIF', append_images=frames[1:], save_all=True, duration=play.interval,
                               loop=0, optimize=False, dither=PILImage.NONE, quality=95)
                print(f"GIF saved as: {gif_path}")
            except Exception as e:
                print(f"Error saving GIF: {e}")
        else:
            print("No frames to save.")

    # Define callback function to save images as an MP4 video
    def save_as_mp4(b):
        frames = []

        # Ensure the output directory exists
        if not os.path.exists(media_dir):
            os.makedirs(media_dir)

        # Load images into frames
        for i in range(ds.sizes['t']):
            file_path = os.path.join(img_dir, hashed_filenames[i] + ".png")

            if os.path.exists(file_path):
                try:
                    img = PILImage.open(file_path).convert(
                        'RGB')  # Convert the image to RGB format
                    # Convert PIL image to numpy array
                    frames.append(np.array(img))
                    print(f"Loaded image: {file_path}")
                except Exception as e:
                    print(f"Error loading image {file_path}: {e}")
            else:
                print(f"Image not found: {file_path}")

        # Check if we have frames to save
        if frames:
            video_path = os.path.join(
                media_dir, f"{config.widget_values['selected_rgb']}_{current_time}.mp4")
            try:
                video_clip = ImageSequenceClip(
                    frames, fps=12)  # Use numpy arrays directly
                video_clip.write_videofile(video_path, codec='libx264', fps=12)
                print(f"MP4 saved as: {video_path}")
            except Exception as e:
                print(f"Error saving MP4: {e}")
        else:
            print("No frames to save.")

    # Link buttons to callback functions
    interval_increase_button.on_click(increase_interval)
    interval_decrease_button.on_click(decrease_interval)
    save_gif_button.on_click(save_as_gif)
    save_mp4_button.on_click(save_as_mp4)

    # Display the play widget, slider, and image output
    display(widgets.VBox([widgets.HBox([play, slider]),
                          widgets.HBox(
                              [interval_increase_button, interval_decrease_button, save_gif_button, save_mp4_button]),
                          output]))

    # Initialize the first image
    update_image({'new': 0})
