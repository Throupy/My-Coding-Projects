import random
import logging
import math
import configparser

#Nothing mindblowing here. Just testing out configparser and logging modules :)

#Logging Configuration
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s:')
file_handler = logging.FileHandler('mathsgame.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


operations = ['+', '-', '*']
trigValues = {'Sin0':'0', 'Sin30':'0.5', 'Sin45':'r2/2', 'Sin60':'r3/2', 'Sin90':'1',
                 'Cos0':'1', 'Cos30':'r3/2', 'Cos45':'r2/2', 'Cos60':'0.5',
                 'Cos90':'0','Tan0':'0', 'Tan30':'r3/3', 'Tan45':'1', 'Tan60':'r3'}


config = configparser.ConfigParser()

class Quiz:
    def __init__(self):
        config.read('config.ini')
        config.sections()
        self.rounds = int(config['MATH QUIZ']['roundnumber'])

    def trigQuiz(self):
        for _round in range(0,self.rounds):
            question = random.choice(list(trigValues))
            print(f"What is the value of {question}\nUse 'r' for square root.")
            answer = trigValues.get(question)
            answerinput = input(">> ")
            if answerinput == answer:
                print(f"Correct!")
                logger.info(f"User answered What is {question} Correctly. The answer was {answer}")
            else:
                print(f"Incorrect! The answer was {answer}")
                logger.info(f"User answered What is {question} incorrectly. The answer was {answer} and they put {answerinput}")
        print("Play again? (Y/N)");retryinput = input(">> ")
        if retryinput.lower() == 'y':
            self.operationsQuiz()
        else:
            quit()


    def operationsQuiz(self):
        if random.randint(1,2) == 1:
            self.trigQuiz()
        else:
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
                        logger.info(f"User answered {num1} {operation} {num2} incorrectly. The answer was {answer} and they put {answerinput}")
                except ValueError:
                    print("You must enter an integer!")
                    self.operationsQuiz()
        print("Play again? (Y/N)");retryinput = input(">> ")
        if retryinput.lower() == 'y':
            self.operationsQuiz()
        else:
            quit()


                          

quiz = Quiz()
while True:
    print("[1]Play Game\n[2]Edit Config")
    choice = input(">> ")
    if choice == '1':               
        quiz.operationsQuiz()
    elif choice == '2':
        rounds = input("How many rounds: ")
        config['MATH QUIZ'] = {'roundnumber' : str(rounds)}
        with open("config.ini", "w") as configFile:
                  config.write(configFile)
        print("Configuration Saved. Restart game to take effect")






    
