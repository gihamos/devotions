from utils.fonction import download_youtube_audio,transcript_with_timestamps
text =transcript_with_timestamps( download_youtube_audio("https://www.youtube.com/watch?v=LM7rtFJcnG8"))

print(text)