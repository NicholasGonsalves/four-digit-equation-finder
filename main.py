# Generate equations for all 4 digit numbers
import re
from typing import Dict, Optional, List
import logging
from itertools import product
from progressbar import progressbar, streams
from math import factorial, sqrt  # imports are required although they appear 'unused', as they are called within eval()


class EquationGenerator:
    def __init__(self, num_digits: int):
        self.num_digits = num_digits
        self.allowed_operators = [
            '+', '-', '*', '/', '%',
            '!+', '!-', '!*', '!/', '!%',
            '**(1/2)+', '**(1/2)-', '**(1/2)*', '**(1/2)/', '**(1/2)%'
        ]
        self.operator_permutations = list(product(self.allowed_operators, repeat=num_digits - 1))
        self.solutions: Dict[int, str] = {}

        if self.num_digits != 4:
            raise NotImplemented("Woops, it's almost there, but currently we only support 4 digit numbers!")

    def __str__(self):
        """Display possible found solutions"""
        if len(self.solutions) == 0:
            raise LookupError(
                "No solutions could be found. You need to call .calculate_for_all_numbers() to generate them!"
            )

        start_number = 10 ** (self.num_digits - 1)
        end_number = (10 ** self.num_digits)
        solutions_found = len([sol for sol in self.solutions.values() if sol is not None])
        return (
            f"Generator run for all {self.num_digits} digit numbers: "
            f"{solutions_found} solutions found of a possible {end_number - start_number}"
        )

    def calculate_for_all_numbers(self) -> None:
        """Call equation generation function for all self.num_digits length numbers. Add each solution to solutions."""
        for number in progressbar(range(10 ** (self.num_digits - 1), (10 ** self.num_digits)), redirect_stdout=True):
            # Generate a valid solution if one exists, and save it in self.solutions
            solution = self._generate_valid_equation(number)
            self.solutions[number] = solution

    def _generate_valid_equation(self, number: int) -> Optional[str]:
        """Generate list of all possible equations for number, and then validate, returning the first valid equation."""
        possible_equations = self._generate_possible_equations(number)
        valid_equation = self._validate_equations(possible_equations)

        if valid_equation is None:
            logging.info(f"Solution for {number} was not found. Sad times.")

        return valid_equation

    def _generate_possible_equations(self, number: int) -> List[str]:
        """For all permutations of operators (that I could think of), generate equations for 'number'. Messy."""
        first, second, third, fourth = list(str(number))
        equals = '=='

        possible_equations = []
        for operators in self.operator_permutations:
            op1, op2, op3 = operators

            # Original 3, which I then got too lazy to modify with brackets correctly,
            # and now we're left with the mess below...
            # possible_equations.append(f"{first}{equals}{second}{op2}{third}{op3}{fourth}")
            # possible_equations.append(f"{first}{op1}{second}{equals}{third}{op3}{fourth}")
            # possible_equations.append(f"{first}{op1}{second}{op2}{third}{equals}{fourth}")

            # e.g. a=b+c+d
            possible_equations.append(f"{first}{equals}{second}{op2}{third}{op3}{fourth}")
            possible_equations.append(f"{first}{equals}({second}{op2}{third}){op3}{fourth}")
            possible_equations.append(f"{first}{equals}{second}{op2}({third}{op3}{fourth})")

            possible_equations.append(f"sqrt({first}){equals}{second}{op2}{third}{op3}{fourth}")
            possible_equations.append(f"{first}{equals}sqrt({second}{op2}{third}){op3}{fourth}")
            possible_equations.append(f"{first}{equals}{second}{op2}sqrt({third}{op3}{fourth})")
            possible_equations.append(f"{first}{equals}sqrt({second}{op2}{third}{op3}{fourth})")

            # e.g. a+b=c+d
            possible_equations.append(f"{first}{op1}{second}{equals}{third}{op3}{fourth}")

            # e.g. a+b+c=d
            possible_equations.append(f"{first}{op1}{second}{op2}{third}{equals}{fourth}")
            possible_equations.append(f"({first}{op1}{second}){op2}{third}{equals}{fourth}")
            possible_equations.append(f"{first}{op1}({second}{op2}{third}){equals}{fourth}")

            possible_equations.append(f"{first}{op1}{second}{op2}{third}{equals}sqrt({fourth})")
            possible_equations.append(f"sqrt({first}{op1}{second}){op2}{third}{equals}{fourth}")
            possible_equations.append(f"{first}{op1}sqrt({second}{op2}{third}){equals}{fourth}")
            possible_equations.append(f"sqrt({first}{op1}{second}{op2}{third}){equals}{fourth}")

        return possible_equations

    @staticmethod
    def _validate_equations(equations: List[str]) -> Optional[str]:
        for equation in equations:

            equation = re.sub(r"(\d)!", r"factorial(\1)", equation)  # should be somewhere else!

            try:
                if eval(equation):
                    return equation
            except ZeroDivisionError:  # pff probably just remove this, let Exception handle it amirite.
                continue
            except Exception as e:
                logging.info(f"{equation} is ILLEGAL. Big oof. {e}")
                continue

        return None


if __name__ == '__main__':
    streams.wrap_stderr()  # This is required so logging plays nicely with progressbar

    # logging.basicConfig(level=logging.INFO)
    # logging.basicConfig(level=logging.WARNING)
    logging.basicConfig(level=logging.CRITICAL)

    # Init generator and run for all 'num_digit' numbers
    generator = EquationGenerator(num_digits=4)
    generator.calculate_for_all_numbers()

    # Log output
    logging.critical(generator)
