from pydub import AudioSegment
from pydub.silence import detect_nonsilent

def remove_silence(input_file, output_file, silence_threshold=-40.0, min_silence_len=1000, buffer_duration=500):
    """
    Removes silence from an audio file and saves the processed audio.
    
    Args:
        input_file (str): Path to the input audio file.
        output_file (str): Path to save the output audio file.
        silence_threshold (float): Threshold in dBFS for detecting silence.
        min_silence_len (int): Minimum duration (ms) for a silence to be considered.
        buffer_duration (int): Duration (ms) of silence to add between nonsilent chunks.
    """
    # Load the audio file
    audio = AudioSegment.from_file(input_file)
    
    # Detect nonsilent chunks [(start_time, end_time), ...]
    nonsilent_chunks = detect_nonsilent(audio, min_silence_len=min_silence_len, silence_thresh=silence_threshold)
    
    # Define a buffer (silent audio segment)
    buffer = AudioSegment.silent(duration=buffer_duration)
    
    # Combine nonsilent chunks
    output_audio = AudioSegment.empty()
    for start, end in nonsilent_chunks:
        output_audio += audio[start:end] + buffer
    
    # Export the processed audio
    output_audio.export(output_file, format="wav")
    print(f"Processed audio saved as {output_file}")
