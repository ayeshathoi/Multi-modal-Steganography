import numpy as np
import cv2
import matplotlib.pyplot as plt


#####################################################
# Function to convert the message to binary
def msgtobinary(msg):
    if type(msg) == str:
        binary_data= ''.join([ format(ord(i), "08b") for i in msg ])
    elif type(msg) == int or type(msg) == np.uint8:
        binary_data=format(msg, "08b")
    elif type(msg) == bytes or type(msg) == np.ndarray:
        binary_data= [ format(i, "08b") for i in msg ]
    else:
        raise TypeError("Input type is not supported in this function")
    
    return binary_data

#####################################################

# Image Steganography
def image_steg_encode(img_path):
    img = cv2.imread(img_path)
    data=input("\nEnter the message to be hide in Image :")    
    if (len(data) == 0): 
        raise ValueError('Message entered to be encoded is empty')
  
    stego_file = input("\nEnter the name of the New Image (Stego Image) after Encoding(with extension):")
    
    no_of_bytes=(img.shape[0] * img.shape[1] * 3) // 8 # convert bits to bytes
    
    if(len(data)>no_of_bytes):
        raise ValueError("Insufficient bytes Error, Need Bigger Image or Less Data !!")
    
    data +='$t3g0'   
    
    binary_data=msgtobinary(data)
    length_data=len(binary_data)

    index_data = 0
    # LSB 
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
    cv2.imwrite(stego_file, img)

def image_steg_decode(img_path):
    img = cv2.imread(img_path)
    data_binary = ""
    for i in img:
        for pixel in i:
            r, g, b = msgtobinary(pixel) 
            data_binary += r[-1]  
            data_binary += g[-1]  
            data_binary += b[-1]  
            total_bytes = [ data_binary[i: i+8] for i in range(0, len(data_binary), 8) ]
            decoded_data = ""
            for byte in total_bytes:
                decoded_data += chr(int(byte, 2))
                if decoded_data[-5:] == "$t3g0": 
                    print("\nThe Encoded data which was hidden in the Image was :  ",decoded_data[:-5])
                    return 


#####################################################

# Main Function
print("Multi-modal Steganography")
print("1. Image Steganography")
print("2. Audio Steganography")
print("3. Text Steganography")
print("4. Video Steganography")
print("5. Exit")

steg_choice = int(input("Enter your choice: "))
if steg_choice == 1:
    print("Image Steganography")
    print("1. Encode")
    print("2. Decode")
    print("3. Exit")

    img_choice = int(input("Enter your choice: "))
    if img_choice == 1:
        print("Encode")
        img_path = input("Enter the image path: ")
        image_steg_encode(img_path)
    elif img_choice == 2:
        print("Decode")
        img_path = input("Enter the image path: ")
        image_steg_decode(img_path)
    elif img_choice == 3:
        print("Exit")
    else:
        print("Invalid choice")
