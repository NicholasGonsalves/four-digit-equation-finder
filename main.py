# Generate equations for all 4 digit numbers
import re
from typing import Dict, Optional, List
import logging
from itertools import product
from math import factorial, sqrt


class EquationGenerator:
    def __init__(self, num_digits: int):
        self.num_digits = num_digits
        self.allowed_operators = [
            '+', '-', '*', '/', '%', '!+', '!-', '!*', '!/', '**(1/2)+', '**(1/2)-', '**(1/2)*', '**(1/2)/'
        ]
        self.operator_permutations = list(product(self.allowed_operators, repeat=num_digits - 1))
        self.solutions: Dict[int, str] = dict()

        if self.num_digits != 4:
            raise NotImplemented("Woops, it's almost there, but currently we only support 4 digit numbers!")

    def __str__(self):
        start_number = 10 ** (self.num_digits - 1)
        end_number = (10 ** self.num_digits)
        return (
            f"Generator run for all {self.num_digits} digit numbers: "
            f"{len(self.solutions)} solutions found of a possible {end_number - start_number}"
        )

    def calculate_for_all_numbers(self) -> None:
        """Call equation generation function for all self.num_digits length numbers. Add each solution to solutions."""

        for number in range(10 ** (self.num_digits - 1), (10 ** self.num_digits)):
            # Generate a valid solution if one exists, and save it in self.solutions
            if number % 100 == 0:
                logging.warning(f"Checking {number}")
            solution = self.generate_valid_equation(number)
            self.solutions[number] = solution

    def generate_valid_equation(self, number: int) -> Optional[str]:
        """Generate list of all possible equations for number, and then validate, returning the first valid equation."""
        possible_equations = self.generate_possible_equations(number)
        valid_equation = self.validate_equations(possible_equations)

        if valid_equation is None:
            logging.info(f"Solution for {number} was not found. Sad times.")

        return valid_equation

    def generate_possible_equations(self, number: int) -> List[str]:
        first, second, third, fourth = list(str(number))
        equals = '=='

        possible_equations = []
        for operators in self.operator_permutations:
            op1, op2, op3 = operators

            # for each op, replace with '==' once, could do this way more neatly
            # possible_equations.append(f"{first}{equals}{second}{op2}{third}{op3}{fourth}")
            # possible_equations.append(f"{first}{op1}{second}{equals}{third}{op3}{fourth}")
            # possible_equations.append(f"{first}{op1}{second}{op2}{third}{equals}{fourth}")

            # similarly for brackets this isn't neat........................................

            ###
            possible_equations.append(f"{first}{equals}{second}{op2}{third}{op3}{fourth}")
            possible_equations.append(f"{first}{equals}({second}{op2}{third}){op3}{fourth}")
            possible_equations.append(f"{first}{equals}{second}{op2}({third}{op3}{fourth})")

            possible_equations.append(f"sqrt({first}){equals}{second}{op2}{third}{op3}{fourth}")
            possible_equations.append(f"{first}{equals}sqrt({second}{op2}{third}){op3}{fourth}")
            possible_equations.append(f"{first}{equals}{second}{op2}sqrt({third}{op3}{fourth})")

            # possible_equations.append(f"factorial({first}){equals}{second}{op2}{third}{op3}{fourth}")
            # possible_equations.append(f"{first}{equals}factorial({second}{op2}{third}){op3}{fourth}")
            # possible_equations.append(f"{first}{equals}{second}{op2}factorial({third}{op3}{fourth})")

            ###
            possible_equations.append(f"{first}{op1}{second}{equals}{third}{op3}{fourth}")

            ###
            possible_equations.append(f"{first}{op1}{second}{op2}{third}{equals}{fourth}")
            possible_equations.append(f"({first}{op1}{second}){op2}{third}{equals}{fourth}")
            possible_equations.append(f"{first}{op1}({second}{op2}{third}){equals}{fourth}")

            possible_equations.append(f"{first}{op1}{second}{op2}{third}{equals}sqrt({fourth})")
            possible_equations.append(f"sqrt({first}{op1}{second}){op2}{third}{equals}{fourth}")
            possible_equations.append(f"{first}{op1}sqrt({second}{op2}{third}){equals}{fourth}")

            # possible_equations.append(f"{first}{op1}{second}{op2}{third}{equals}factorial({fourth})")
            # possible_equations.append(f"factorial({first}{op1}{second}){op2}{third}{equals}{fourth}")
            # possible_equations.append(f"{first}{op1}factorial({second}{op2}{third}){equals}{fourth}")

            # ah we need to apply the 'modifiers' sqrt and factorial on either side too, to anything in a bracket also..
            # very manual and messy above

        # possible_equations = [
        #     f"{first}{ops[0]}{second}{ops[1]}{third}{ops[2]}{fourth}{ops[3]}"
        #     for ops in self.operator_permutations
        # ]

        return possible_equations

    @staticmethod
    def validate_equations(equations: List[str]) -> Optional[str]:
        illegal_operators = ['/0', '%0', '(0+0)!', '(0-0)!', '*0)!']
        for equation in equations:
            if any(op in equation for op in illegal_operators):
                continue
            if '!' in equation:
                equation = re.sub(r"(\d)!", r"factorial(\1)", equation)

            try:
                valid = eval(equation)
            except ZeroDivisionError:
                continue
            except Exception as e:
                logging.info(f"{equation} is ILLEGAL. Big oof. {e}")
                continue

            if valid:
                return equation

        return None


if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO)
    logging.basicConfig(level=logging.WARNING)

    generator = EquationGenerator(num_digits=4)
    generator.calculate_for_all_numbers()
    print(len([sol for k, sol in generator.solutions.items() if sol is not None]))
