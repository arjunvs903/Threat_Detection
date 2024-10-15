from moviepy.editor import VideoFileClip

# Load the video clip
input_video_path = r"D:\projects\MainProject\Threat Detection\ThreatDetection\Processed\output.mp4"
video_clip = VideoFileClip(input_video_path)

# Reduce frame rate to simplify the video
new_frame_rate = 20  # Set your desired frame rate
video_clip = video_clip.set_fps(new_frame_rate)


# Write the compressed video to a new file
output_video_path = "output.mp4"
video_clip.write_videofile(output_video_path, codec="libx264")