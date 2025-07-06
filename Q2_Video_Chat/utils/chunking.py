def chunk_transcript(transcript, max_words=150):
    segments = transcript['segments']
    chunks = []
    chunk, start, end = [], None, None

    for seg in segments:
        words = seg['text'].split()
        if len(chunk) + len(words) > max_words:
            chunks.append({'text': ' '.join(chunk), 'start': start, 'end': end})
            chunk = []
        if not chunk:
            start = seg['start']
        chunk.extend(words)
        end = seg['end']
    if chunk:
        chunks.append({'text': ' '.join(chunk), 'start': start, 'end': end})
    return chunks
