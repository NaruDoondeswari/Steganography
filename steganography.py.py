from PIL import Image
import requests
from io import BytesIO

def genData(data):
    """Convert encoding data into 8-bit binary form using ASCII value of characters."""
    return [format(ord(i), '08b') for i in data]

def modPix(pix, data):
    """Modify pixels according to the 8-bit binary data and return them."""
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)
    
    for i in range(lendata):
        # Extracting 3 pixels at a time
        pixels = [value for value in next(imdata)[:3] + next(imdata)[:3] + next(imdata)[:3]]
        
        # Pixel value should be made odd for 1 and even for 0
        for j in range(8):
            if (datalist[i][j] == '0' and pixels[j] % 2 != 0):
                pixels[j] -= 1
            elif (datalist[i][j] == '1' and pixels[j] % 2 == 0):
                pixels[j] = pixels[j] - 1 if pixels[j] != 0 else pixels[j] + 1

        # Eighth pixel of every set tells whether to stop or read further
        if i == lendata - 1:
            if pixels[-1] % 2 == 0:
                pixels[-1] -= 1
        else:
            if pixels[-1] % 2 != 0:
                pixels[-1] -= 1

        yield tuple(pixels[:3])
        yield tuple(pixels[3:6])
        yield tuple(pixels[6:9])

def encode_enc(newimg, data):
    """Encode data into image."""
    w, h = newimg.size
    (x, y) = (0, 0)
    
    for pixel in modPix(newimg.getdata(), data):
        newimg.putpixel((x, y), pixel)
        if x == w - 1:
            x = 0
            y += 1
        else:
            x += 1

def encode(image, data):
    """Encode data into the image and return the encoded image."""
    print(f"Encoding data into image from URL...")
    
    if not data:
        raise ValueError('Data is empty')
    
    newimg = image.copy()
    encode_enc(newimg, data)
    return newimg

def decode(image):
    """Decode the data in the image."""
    print("Decoding data from image...")
    
    data = ''
    imgdata = iter(image.getdata())
    
    while True:
        pixels = [value for value in next(imgdata)[:3] + next(imgdata)[:3] + next(imgdata)[:3]]
        binstr = ''.join(['0' if i % 2 == 0 else '1' for i in pixels[:8]])
        
        decoded_char = chr(int(binstr, 2))
        print(f"Decoded binary string: {binstr} -> {decoded_char}")  # Debugging output
        
        data += decoded_char
        if pixels[-1] % 2 != 0:
            return data

def main():
    """Main function."""
    img_url = "https://res.cloudinary.com/dgltnm7jo/image/upload/v1721884721/image_cwdxgb.jpg"  # Image URL
    response = requests.get(img_url)
    image = Image.open(BytesIO(response.content))

    choice = int(input(":: Welcome to Steganography ::\n1. Encode\n2. Decode\n"))
    
    if choice == 1:
        data = "You've just uncovered a new clue. Check the attic for the next piece of the puzzle."
        encoded_image = encode(image, data)
        print("Data encoded into the image (not saved).")
        decoded_message = decode(encoded_image)
        print("Decoded Message: " + decoded_message)
    elif choice == 2:
        decoded_message = decode(image)
        print("Decoded Message: " + decoded_message)
    else:
        raise Exception("Enter correct input")

if __name__ == '_main_':
    main()