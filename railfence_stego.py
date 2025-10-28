from PIL import Image

def rail_fence_encrypt(text, rails):
    fence = [[] for _ in range(rails)]
    rail = 0
    var = 1
    
    for char in text:
        fence[rail].append(char)
        rail += var

        if rail == 0 or rail == rails - 1:
            var = -var

    return ''.join(''.join(row) for row in fence)

def rail_fence_decrypt(cipher, rails):
    pattern = [0] * len(cipher)
    rail = 0
    var = 1
    for i in range(len(cipher)):
        pattern[i] = rail
        rail += var
        if rail == 0 or rail == rails - 1:
            var = -var

    rail_counts = [pattern.count(r) for r in range(rails)]
    pos = 0
    rails_content = []
    for count in rail_counts:
        rails_content.append(list(cipher[pos:pos + count]))
        pos += count

    result = []
    rail_positions = [0] * rails
    rail = 0
    var = 1

    for i in range(len(cipher)):
        result.append(rails_content[rail][rail_positions[rail]])
        rail_positions[rail] += 1
        rail += var
        if rail == 0 or rail == rails - 1:
            var = -var
    
    return ''.join(result)

def embed_in_lsb(image_path, message, output_path):
    image = Image.open(image_path)
    encoded = image.copy()
    width, height = image.size
    message += "<<<END>>>"  # delimiter
    binary_message = ''.join(format(ord(c), '08b') for c in message)

    idx = 0
    for y in range(height):
        for x in range(width):
            if idx >= len(binary_message):
                encoded.save(output_path)
                print("Stego image saved:", output_path)
                return
            r, g, b = image.getpixel((x, y))
            r = (r & ~1) | int(binary_message[idx]); idx += 1
            if idx < len(binary_message):
                g = (g & ~1) | int(binary_message[idx]); idx += 1
            if idx < len(binary_message):
                b = (b & ~1) | int(binary_message[idx]); idx += 1
            encoded.putpixel((x, y), (r, g, b))

def extract_from_lsb(image_path):
    image = Image.open(image_path)
    width, height = image.size
    binary_data = ""
    
    for y in range(height):
        for x in range(width):
            r, g, b = image.getpixel((x, y))
            binary_data += str(r & 1)
            binary_data += str(g & 1)
            binary_data += str(b & 1)
    
    bytes_data = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    decoded = ''.join(chr(int(byte, 2)) for byte in bytes_data)
    return decoded.split("<<<END>>>")[0]

def main():
    while True:
        print("\nMenu:")
        print("1. Encrypt and Embed into Image")
        print("2. Extract and Decrypt from Image")
        print("3. Exit")
        choice = input("Enter choice: ")
        
        if choice == "1":
            text = input("Enter message: ")
            rails = int(input("Enter rails: "))
            image_path = input("Enter image path (e.g. Logo.png): ")
            output_path = "stego.png"
            cipher = rail_fence_encrypt(text, rails)
            print("Ciphertext:", cipher)
            embed_in_lsb(image_path, cipher, output_path)
        
        elif choice == "2":
            image_path = input("Enter stego image path: ")
            rails = int(input("Enter rails: "))
            cipher = extract_from_lsb(image_path)
            text = rail_fence_decrypt(cipher, rails)
            print("Decrypted Message:", text)
        
        else:
            break

if __name__ == "__main__":
    main()
