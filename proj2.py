
import numpy as np
import cv2


def msgtobinary(msg):
    if type(msg) == str:
        result = ''.join([format(ord(i), "08b") for i in msg])

    elif type(msg) == bytes or type(msg) == np.ndarray:
        result = [format(i, "08b") for i in msg]

    elif type(msg) == int or type(msg) == np.uint8:
        result = format(msg, "08b")

    else:
        raise TypeError("Input type is not supported in this function")

    return result


def encode_img_data(img):
    data = input("\nEnter the data to be Encoded in Image :")
    if (len(data) == 0):
        raise ValueError('Data entered to be encoded is empty')

    nameoffile = input("\nEnter the name of the New Image (Stego Image) after Encoding(with extension):")

    no_of_bytes = (img.shape[0] * img.shape[1] * 3) // 8

    print("\t\nMaximum bytes to encode in Image :", no_of_bytes)

    if (len(data) > no_of_bytes):
        raise ValueError("Insufficient bytes Error, Need Bigger Image or give Less Data !!")

    data += '*^*^*'

    binary_data = msgtobinary(data)
    print("\n")
    print(binary_data)
    length_data = len(binary_data)

    print("\nThe Length of Binary data", length_data)

    index_data = 0

    for i in img:
        for pixel in i:
            r, g, b = msgtobinary(pixel)
            if index_data < length_data:
                pixel[0] = int(r[:-1] + binary_data[index_data], 2)
                index_data += 1
            if index_data < length_data:
                pixel[1] = int(g[:-1] + binary_data[index_data], 2)
                index_data += 1
            if index_data < length_data:
                pixel[2] = int(b[:-1] + binary_data[index_data], 2)
                index_data += 1
            if index_data >= length_data:
                break
    cv2.imwrite(nameoffile, img)
    print("\nEncoded the data successfully in the Image and the image is successfully saved with name ", nameoffile)


def decode_img_data(img):
    data_binary = ""
    for i in img:
        for pixel in i:
            r, g, b = msgtobinary(pixel)
            data_binary += r[-1]
            data_binary += g[-1]
            data_binary += b[-1]
            total_bytes = [data_binary[i: i + 8] for i in range(0, len(data_binary), 8)]
            decoded_data = ""
            for byte in total_bytes:
                decoded_data += chr(int(byte, 2))
                if decoded_data[-5:] == "*^*^*":
                    print("\n\nThe Encoded data which was hidden in the Image was :--  ", decoded_data[:-5])
                    return

                # In[10]:


def img_steg():
    while True:
        print("\n\t\tIMAGE STEGANOGRAPHY OPERATIONS\n")
        print("1. Encode the Text message")
        print("2. Decode the Text message")
        print("3. Exit")
        choice1 = int(input("Enter the Choice: "))
        if choice1 == 1:
            file = input("enter file path: ")
            image = cv2.imread(file)
            encode_img_data(image)
        elif choice1 == 2:
            image1 = cv2.imread(input("Enter the Image you need to Decode to get the Secret message :  "))
            decode_img_data(image1)
        elif choice1 == 3:
            break
        else:
            print("Incorrect Choice")
        print("\n")


def KSA(key):
    key_length = len(key)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]
    return S


def PRGA(S, n):
    i = 0
    j = 0
    key = []
    while n > 0:
        n = n - 1
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        key.append(K)
    return key

def preparing_key_array(s):
    return [ord(c) for c in s]


def encryption(plaintext):
    print("Enter the key : ")
    key = input()
    key = preparing_key_array(key)

    S = KSA(key)

    keystream = np.array(PRGA(S, len(plaintext)))
    plaintext = np.array([ord(i) for i in plaintext])

    cipher = keystream ^ plaintext
    ctext = ''
    for c in cipher:
        ctext = ctext + chr(c)
    return ctext


def decryption(ciphertext):
    print("Enter the key : ")
    key = input()
    key = preparing_key_array(key)

    S = KSA(key)

    keystream = np.array(PRGA(S, len(ciphertext)))
    ciphertext = np.array([ord(i) for i in ciphertext])

    decoded = keystream ^ ciphertext
    dtext = ''
    for c in decoded:
        dtext = dtext + chr(c)
    return dtext

def main():
    print("\t\t      STEGANOGRAPHY")
    while True:
        img_steg()


if __name__ == "__main__":
    main()

# In[ ]:



