import cv2
import numpy as np
import sys

def text_to_bits(text):
    return ''.join([bin(ord(c))[2:].zfill(8) for c in text])

def embed_message(frame, message):
    bits = text_to_bits(message)
    h, w, _ = frame.shape
    idx = 0
    for y in range(h):
        for x in range(w):
            if idx >= len(bits):
                return frame
            pixel = list(frame[y, x])
            # Ghi vào LSB của kênh Blue
            pixel[0] = (pixel[0] & ~1) | int(bits[idx])
            frame[y, x] = tuple(pixel)
            idx += 1
    return frame

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python steg_video_embed.py input.mp4 message.txt output.mp4 frameidx")
        sys.exit(1)
    invid = sys.argv[1]
    msgfile = sys.argv[2]
    outvid = sys.argv[3]
    frameidx = int(sys.argv[4])

    msg = open(msgfile).read()
    bits_needed = len(msg)*8
    cap = cv2.VideoCapture(invid)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps    = cap.get(cv2.CAP_PROP_FPS)
    out = cv2.VideoWriter(outvid, fourcc, fps, (width, height))

    idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if idx == frameidx:
            frame = embed_message(frame, msg)
        out.write(frame)
        idx += 1
    cap.release()
    out.release()
    print("Done embed.")
