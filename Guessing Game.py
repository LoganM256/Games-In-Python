import random

def guess(x):
    random_number = random.randint(1,x)
    count = 0
    guess = 0 
    while guess != random_number:
        guess = int(input(f"Please enter a number between 1 and {x}: "))
        if guess < random_number:
            print("You get a feeling it might be higher...")
            count = count + 1 
        elif guess > random_number:
            print("You get the feeling it might be lower...")
            count = count + 1 
    count = count + 1
    print(f"Your guess of {guess} was correct! Congrats! Guesses to get to correct value: {count}")

def computerguess(x):
    low = 1 
    high = x
    feedback = ""
    while feedback != "c":
        if low != high:
            guess = random.randint(low,high)
        else:
            guess = low
        feedback = input(f"Is {guess} too high (H) or too low (L), or correct (C)?? ").lower()
        if feedback == "h":
            high = guess - 1 
        elif feedback == "l":
            low = guess + 1
    print(f"The computer has guessed your number, {guess}, correctly!")

computerguess(1000)