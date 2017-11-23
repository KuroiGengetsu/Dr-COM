"""dump passwords from 000000 to 999999"""
import json

def main():
    """main function"""
    passwords = [
        '{:06d}'.format(password)
        for password in range(1000000)
    ]
    with open('passwords.json', mode='w') as fp:
        json.dump(passwords, fp, indent=4)

if __name__ == '__main__':
    main()
