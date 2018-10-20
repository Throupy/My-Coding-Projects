#13/12/2017

import random
import logging

#Logging Configuration
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s:')
file_handler = logging.FileHandler('mathsgame.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

operations = ['+', '-', '*']

class Quiz:
    def __init__(self, rounds=3):
        self.rounds = rounds

    def playGame(self):
        for _round in range(0,self.rounds):
            num1 = random.randint(1,100)
            num2 = random.randint(1,100)
            operation = random.choice(operations)
            if operation == '*':
                num1 = random.randint(1,14)
                num2 = random.randint(1,14)
            answer = eval(str(num1) + operation + str(num2))
            print(f"What is {num1} {operation} {num2}?")
            answerinput = input(">> ")
            try:
                if int(answerinput) == answer:
                    print("Correct!")
                    logger.info(f"User answered {num1} {operation} {num2} Correctly. The answer was {answer}")
                else:
                    print(f"Incorrect! The answer was {answer}")
                    logger.info(f"User answered {num1} {operation} {num2} incorrectly. The answer was {answer}")
            except ValueError:
                print("You must enter an integer!")
                self.playGame()

quiz = Quiz()
quiz.playGame()
