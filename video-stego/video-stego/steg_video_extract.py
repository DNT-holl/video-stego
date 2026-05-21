import cv2
import sys

def bits_to_text(bits):
    chars = [chr(int(bits[i:i+8],2)) for i in range(0, len(bits),8)]
    return ''.join(chars)

def extract_message(frame, msglen):
    bits = ""
    h, w, _ = frame.shape
    idx = 0
    for y in range(h):
        for x in range(w):
            if idx >= msglen*8:
                return bits_to_text(bits)
            pixel = frame[y, x]
            bits += str(pixel[0]&1)
            idx += 1
    return bits_to_text(bits)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python steg_video_extract.py stego.mp4 outmsg.txt msglen frameidx")
        sys.exit(1)
    invis = sys.argv[1]
    outfile = sys.argv[2]
    msglen = int(sys.argv[3])
    frameidx = int(sys.argv[4])

    cap = cv2.VideoCapture(invis)
    idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Frame not found.")
            sys.exit(1)
        if idx == frameidx:
            msg = extract_message(frame, msglen)
            open(outfile,'w').write(msg)
            print("Extracted! Saved to", outfile)
            break
        idx += 1
    cap.release()
