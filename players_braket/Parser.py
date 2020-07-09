class Parser:
    def __init__(self, user_input):
        self.valid_roll_requests = {'d20': 0,
                                   'd12': 0,
                                   'd10': 0,
                                   'd8': 0,
                                   'd6': 0,
                                   'd4': 0}
        self.raw_input = user_input
        self.dice_requests = self.convert_raw_input_to_request(self.raw_input)
        self.generate_roll_requests(self.dice_requests)

    def convert_raw_input_to_request(self, raw_input):
        raw_input.replace('++', '+',)
        if raw_input[0] == '+':
            valid_input = raw_input[1:-1]
        elif raw_input[-1] == '+':
            valid_input = raw_input[0:-1]
        else:
            valid_input = raw_input
        dice_requests = valid_input.split('+')
        return dice_requests


    def generate_roll_requests(self, dice_requests):
        for req in dice_requests:
            self.parse_single_request(req)

    def parse_single_request(self, req):
        die = ''
        d_indice = req.find('d')

        quant_str = ''
        for i in range(d_indice):
            quant_str += req[i]

        try:
            die_quant = int(quant_str)
        except ValueError as err:
            print("{} not a valid quantity".format(quant_str))
            die_quant = 0

        for i in range(d_indice, len(req)):
            die += req[i]

        try:
            self.valid_roll_requests[die]
            self.valid_roll_requests[die] = die_quant
        except KeyError as err:
            print("{} not a recognized die".format(die))


if __name__=="__main__":
    user_input = '1d20+1d10+1d4'
    parsed_input = Parser(user_input)
    print(parsed_input.valid_roll_requests)
