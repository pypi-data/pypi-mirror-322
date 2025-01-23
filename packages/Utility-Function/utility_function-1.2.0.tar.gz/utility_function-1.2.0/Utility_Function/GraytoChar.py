from PIL import Image
import subprocess

def GraytoChar(gray, chars):
    rate = gray / 256
    return chars[int(len(chars) * rate)]

def UseGraytoChar(path, chars):
    try:
        img = Image.open(path).resize((60, 60)).convert('L')
    except Exception:
        return

    text = "\n".join("".join(GraytoChar(img.getpixel((i, j)), chars) for j in range(60)) for i in range(60))
    print(text)
    try:
        with open("output.txt", "w") as result:
            result.write(text)
        subprocess.Popen(['notepad.exe', 'output.txt'])
    except Exception:
        pass
