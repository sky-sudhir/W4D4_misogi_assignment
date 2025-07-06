def chunk_transcript(segments, max_chars=500, overlap=50):
    full_text = ""
    for seg in segments:
        full_text += f"[{seg['start']:.2f} - {seg['end']:.2f}] {seg['text']}\n"

    chunks = []
    start = 0
    while start < len(full_text):
        end = min(start + max_chars, len(full_text))
        chunk_text = full_text[start:end]

        lines = chunk_text.splitlines()
        start_time, end_time = 0.0, 0.0
        for line in lines:
            if line.startswith("[") and "-" in line:
                try:
                    time_part = line.split("]")[0][1:]
                    s, e = map(float, time_part.split(" - "))
                    start_time = s if start_time == 0.0 else start_time
                    end_time = e
                except:
                    continue

        chunks.append({
            "text": chunk_text,
            "start": start_time,
            "end": end_time
        })
        start += max_chars - overlap

    return chunks