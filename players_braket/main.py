from Dice import *
from Parser import *
from extras import *


def save_ibmq_account():
    try:
        print('IBMQ Token: ')
        token = input()
        IBMQ.save_account()
    except Exception as err:
        print('The following exception was raised{}'.format(err))


def user_dice_request(quantum_dice):
    print('The Oracle Gygax is ready for your request . . .')
    print("Please enter as form: 1d20+1d10")

    user_input = str(input())
    parsed_input = Parser(user_input)

    stalling_message()

    roll_req = parsed_input.valid_roll_requests
    rolls = quantum_dice.multi_throw(roll_req)

    roll_to_ascii(rolls)


connecting = True
while connecting:
    try:
        provider = IBMQ.load_account()
        print('Please enter preferred backend (default to ibmq_qasm_simulator):')
        backend = str(input())
        if backend == '':
            backend = 'ibmq_qasm_simulator'
        print('Attempting to contact the Oracle Gygax . . .')
        quantum_dice = Dice(provider, backend)
        connecting = False

    except Exception as err:
        print('The following exception was raised{}'.format(err))
        if err == 'IBMQAccountCredentialsInvalidFormat':
            print('default provider stored on disk could not be parsed. Please reenter IBMQ token')
            save_ibmq_account()
        elif err == 'IBMQAccountCredentialsNotFound':
            print('no IBM Quantum Experience credentials can be found. Please enter IBMQ token')
            save_ibmq_account()
        elif err == 'IBMQAccountMultipleCredentialsFound':
            print('Multiple IBM Quantum Experience credentials are found')
        elif err == 'IBMQAccountCredentialsInvalidUrl':
            print('Invalid IBM Quantum Experience credentials found. Please reenter IBMQ token')
            save_ibmq_account()
        elif err == 'IBMQProviderError':
            print('Default provider stored on disk could not be found.  Please reenter IBMQ token')
            save_ibmq_account()

while True:
    user_dice_request(quantum_dice)
