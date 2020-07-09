from qiskit import *
from qiskit import IBMQ
from qiskit.tools.monitor import *
import random


class Dice:
    def __init__(self, provider, backend='ibmq_qasm_simulator'):
        self.provider = provider
        self.system = provider.get_backend(backend)
        self.monitor = False
        self.max_raw_num = 2**(-1) + 2**(-2) + 2**(-3) + 2 **(-4) + 2**(-5)
        self.p5_circ = self.create_p5()

    def create_p5(self):
        p5 = QuantumCircuit(5)
        for i in range(5):
            p5.h(i)
        p5.measure_all()

        return p5

    def multi_throw(self, dice_dict):
        total_throws = 0
        dice_list = []
        for die in dice_dict:
            try:
                reqs = dice_dict[die]
                if reqs != 0:
                    total_throws += reqs
                    for i in range(reqs):
                        dice_list.append(int(die.strip('d')))
            except Exception as err:
                print('Exception {} has occured'.format(err))

        raw_vals = self.random_int_generator(self.p5_circ, total_throws)
        if len(raw_vals) != len(dice_list):
            raise Exception('Mismatch between request rolls and raw values')

        return [self.convert_rand_to_roll(raw_vals[i], dice_list[i]) for i in range(len(raw_vals))]


    def quant_result_to_int(self, quant_results):
        rolls = []
        for key in quant_results:
            roll = 0
            for i in range(len(key)):
                roll += int(key[i]) * 2 ** (-(i + 1))
            for i in range(int(quant_results[key])):
                rolls.append(roll)
        random.shuffle(rolls)
        return rolls

    def random_int_generator(self, circ, n):
        random_gen_job = execute(circ, backend=self.system, shots=n)
        if self.monitor:
            job_monitor(random_gen_job)
        raw_data = random_gen_job.result().get_counts(circ)
        raw_rand = self.quant_result_to_int(raw_data)
        return raw_rand

    def convert_rand_to_roll(self, rand_val, die):
        normalized_val = rand_val/ self.max_raw_num
        roll = round(normalized_val * (die-1)) + 1
        return roll

    def convert_rands_to_rolls(self, rand_vals, die):
        die_rolls = []
        for vall in rand_vals:
            normalized_vall = vall / self.max_raw_num
            roll = round(normalized_vall * (die-1)) + 1
            die_rolls.append(roll)
        return die_rolls

    def roll_d20(self, n=1):
        rand_vals = self.random_int_generator(self.p5_circ, n)
        d20_rolls = self.convert_rands_to_rolls(rand_vals, 20)
        return d20_rolls

    def roll_d12(self, n=1):
        rand_vals = self.random_int_generator(self.p5_circ, n)
        d12_rolls = self.convert_rands_to_rolls(rand_vals, 12)
        return d12_rolls

    def roll_d10(self, n=1):
        rand_vals = self.random_int_generator(self.p5_circ, n)
        d10_rolls = self.convert_rands_to_rolls(rand_vals, 10)
        return d10_rolls

    def roll_d8(self, n=1):
        rand_vals = self.random_int_generator(self.p5_circ, n)
        d8_rolls = self.convert_rands_to_rolls(rand_vals, 8)
        return d8_rolls

    def roll_d6(self, n=1):
        rand_vals = self.random_int_generator(self.p5_circ, n)
        d6_rolls = self.convert_rands_to_rolls(rand_vals, 6)
        return d6_rolls

    def roll_d4(self, n=1):
        rand_vals = self.random_int_generator(self.p5_circ, n)
        d4_rolls = self.convert_rands_to_rolls(rand_vals, 4)
        return d4_rolls


if __name__ == "__main__":
    provider = IBMQ.load_account()
    quantum_dice = Dice(provider, 'ibmq_qasm_simulator')
    d20_test = quantum_dice.roll_d20(n=100)
    sns.distplot(d20_test, bins=20)
    plt.show()
    roll_dict = {"d20": 1,
                 "d12": 0,
                 "d10": 0,
                 "d8": 1,
                 "d6": 0,
                 "d4": 1}
    rolls = quantum_dice.multi_throw(roll_dict)
    print(rolls)
    # rolls = quantum_dice.throw_dice(roll_dict)
    # print(rolls)
