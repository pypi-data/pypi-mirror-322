'''
things in hidden_things right now:
    - PropositionDefaults
    - ModelConstraints
    - ModelStructure
'''

import sys

from contextlib import redirect_stdout

import time

from functools import reduce

from string import Template

from z3 import (
    And,
    ArrayRef,
    BitVecSort,
    EmptySet,
    IsMember,
    Not,
    BitVecVal,
    SetAdd,
    Solver,
    sat,
    simplify,
)

from .utils import (
    bitvec_to_substates,
    int_to_binary,
    not_implemented_string,
    pretty_set_print,
)

inputs_template = Template(
'''Z3 run time: ${z3_model_runtime} seconds
"""

################
### SETTINGS ###
################

settings = ${settings}


###############
### EXAMPLE ###
###############

# input sentences
premises = ${premises}
conclusions = ${conclusions}


#########################################
### GENERATE Z3 CONSTRAINTS AND PRINT ###
#########################################

### NOTE: run below for individual tests

model_structure = make_model_for(
    settings,
    premises,
    conclusions,
    Semantics,
    Proposition,
    operators,
)
model_structure.print_all()
'''
)

class SemanticDefaults:
    """Includes default attributes and methods to be inherited by a semantics
    including frame constraints, truth and falsity, and logical consequence."""

    def __init__(self, N):

        # Store the name
        self.name = self.__class__.__name__

        # Store the number of states
        self.N = N

        # Define top and bottom states
        max_value = (1 << self.N) - 1 # NOTE: faster than 2**self.N - 1
        self.full_bit = BitVecVal(max_value, self.N)
        self.null_bit = BitVecVal(0, self.N)
        self.all_bits = [BitVecVal(i, self.N) for i in range(1 << self.N)]
        
        # Define the frame constraints
        self.frame_constraints = None

        # Define invalidity conditions
        self.premise_behavior = None
        self.conclusion_behavior = None

    def fusion(self, bit_s, bit_t):
        """Return bitwise OR of bit_s and bit_t (Z3 bit vectors)."""
        return bit_s | bit_t

    def z3_set(self, python_set, N):
        """Convert a Python set to a Z3 set of bit-width N."""
        z3_set = EmptySet(BitVecSort(N))
        for elem in python_set:
            z3_set = SetAdd(z3_set, elem)
        return z3_set

    def z3_set_to_python_set(self, z3_set, domain):
        """Convert a Z3 set to a Python set using domain for membership checks."""
        python_set = set()
        for elem in domain:
            if bool(simplify(IsMember(elem, z3_set))):
                python_set.add(elem)
        return python_set

    def total_fusion(self, set_P):
        """Return the fused result (bitwise OR) of all elements in set_P."""
        if isinstance(set_P, ArrayRef):
            set_P = self.z3_set_to_python_set(set_P, self.all_bits)
        return reduce(self.fusion, list(set_P))

    def is_part_of(self, bit_s, bit_t):
        """the fusion of bit_s and bit_t is identical to bit_t
        returns a Z3 constraint"""
        return self.fusion(bit_s, bit_t) == bit_t

    def is_proper_part_of(self, bit_s, bit_t):
        """the fusion of bit_s and bit_t is identical to bit_t
        returns a Z3 constraint"""
        return And(self.is_part_of(bit_s, bit_t), bit_s != bit_t)

    def non_null_part_of(self, bit_s, bit_t):
        """bit_s verifies atom and is not the null state
        returns a Z3 constraint"""
        return And(Not(bit_s == 0), self.is_part_of(bit_s, bit_t))

    def product(self, set_A, set_B):
        """set of pairwise fusions of elements in set_A and set_B"""
        product_set = set()
        for bit_a in set_A:
            for bit_b in set_B:
                bit_ab = simplify(bit_a | bit_b)
                product_set.add(bit_ab)
        return product_set

    def coproduct(self, set_A, set_B):
        """union closed under pairwise fusion"""
        A_U_B = set_A.union(set_B)
        return A_U_B.union(self.product(set_A, set_B))


class PropositionDefaults:
    """Defaults inherited by every proposition."""

    def __init__(self, sentence, model_structure):

        # Raise error if instantiated directly instead of as a bare class
        if self.__class__ == PropositionDefaults:
            raise NotImplementedError(not_implemented_string(self.__class__.__name__))

        # Store values from sentence
        self.name = sentence.name
        self.operator = sentence.operator
        self.arguments = sentence.arguments
        self.sentence_letter = sentence.sentence_letter

        # Store values from model_structure argument
        self.model_structure = model_structure
        self.N = self.model_structure.N
        self.model_constraints = self.model_structure.model_constraints

        # Store values from model_constraints
        self.semantics = self.model_constraints.semantics
        self.sentence_letters = self.model_constraints.sentence_letters
        self.settings = self.model_constraints.settings

        # Set defaults for verifiers and falsifiers (important they are lists)
        self.verifiers, self.falsifiers = [], []

    # NOTE: is responsive to unilateral/bilateral props, so long as
    # falsifiers, if there are any, are _sets_; the default is a list,
    # so if it is a list, it is because the defaults are unchanged, meaning
    # the proposition is unilateral (a prop with no falsifiers but within
    # a bilateral system would have an empty set as falsifiers, not the
    # default empty list)
    def __repr__(self):
        N = self.model_structure.model_constraints.semantics.N
        possible = self.model_structure.model_constraints.semantics.possible
        z3_model = self.model_structure.z3_model
        ver_states = {
            bitvec_to_substates(bit, N)
            for bit in self.verifiers
            if z3_model.evaluate(possible(bit)) or self.settings['print_impossible']
        }
        if isinstance(self.falsifiers, set): # because default is an empty list
            fal_states = {
                bitvec_to_substates(bit, N)
                for bit in self.falsifiers
                if z3_model.evaluate(possible(bit)) or self.settings['print_impossible']
            }
            return f"< {pretty_set_print(ver_states)}, {pretty_set_print(fal_states)} >"
        return pretty_set_print(ver_states)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, PropositionDefaults):
            return self.name == other.name
        return False

    def set_colors(self, name, indent_num, truth_value, world_state, use_colors):
        if not use_colors:
            VOID = ""
            return VOID, VOID, VOID
        RED, GREEN, RESET = "\033[31m", "\033[32m", "\033[0m" 
        FULL, PART = "\033[37m", "\033[33m"
        if indent_num == 1:
            FULL, PART = (GREEN, GREEN) if truth_value else (RED, RED)
            if truth_value is None:
                # world_state = bitvec_to_substates(eval_world, N)
                print(
                    f"\n{RED}WARNING:{RESET}"
                    f"{name} is neither true nor false at {world_state}.\n"
                )
        return RESET, FULL, PART

class ModelConstraints:
    """Takes semantics and proposition_class as arguments to build generate
    and storing all Z3 constraints. This class is passed to ModelStructure."""

    def __init__(
        self,
        settings,
        syntax,
        semantics,
        proposition_class,
    ):

        # Store inputs
        self.syntax = syntax
        self.semantics = semantics
        self.proposition_class = proposition_class
        self.settings = settings

        # Store syntax values
        self.premises = self.syntax.premises
        self.conclusions = self.syntax.conclusions
        self.sentence_letters = self.syntax.sentence_letters

        # Store operator dictionary
        self.operators = self.copy_dictionary(self.syntax.operator_collection)

        # use semantics to recursively update all derived_objects
        self.instantiate(self.premises + self.conclusions)

        # Use semantics to generate and store Z3 constraints
        self.frame_constraints = self.semantics.frame_constraints
        self.model_constraints = [
            constraint
            for sentence_letter in self.sentence_letters
            for constraint in self.proposition_class.proposition_constraints(
                self,
                sentence_letter.sentence_letter,
            )
        ]
        self.premise_constraints = [
            self.semantics.premise_behavior(
                premise,
                self.semantics.main_world,
            )
            for premise in self.premises
        ]
        self.conclusion_constraints = [
            self.semantics.conclusion_behavior(
                conclusion,
                self.semantics.main_world,
            )
            for conclusion in self.conclusions
        ]
        self.all_constraints = (
            self.frame_constraints
            + self.model_constraints
            + self.premise_constraints
            + self.conclusion_constraints
        )

    def __str__(self):
        """useful for using model-checker in a python file"""
        premises = list(self.syntax.premises)
        conclusions = list(self.syntax.conclusions)
        return f"ModelConstraints for premises {premises} and conclusions {conclusions}"

    def copy_dictionary(self, operator_collection):
        """Copies the operator_dictionary from operator_collection."""
        return {
            op_name : op_class(self.semantics)
            for (op_name, op_class) in operator_collection.items()
        }

    # # NOTE: UPDATE OP STRATEGY
    # def apply_semantics(self, operator_collection):
    #     """Passes semantics into each operator in collection."""
    #     operator_collection.update_operators(self.semantics)
    #     return operator_collection

    def instantiate(self, sentences):
        """Updates each instance of Sentence in sentences by adding the
        prefix_sent to that instance, returning the input sentences."""
        for sent_obj in sentences:
            if sent_obj.arguments:
                self.instantiate(sent_obj.arguments)
            sent_obj.update_objects(self)

    def print_enumerate(self, output=sys.__stdout__):
        """prints the premises and conclusions with numbers"""
        premises = self.syntax.premises
        conclusions = self.syntax.conclusions
        start_con_num = len(premises) + 1
        if conclusions:
            if len(premises) < 2:
                print("Premise:", file=output)
            else:
                print("Premises:", file=output)
            for index, sent in enumerate(premises, start=1):
                print(f"{index}. {sent}", file=output)
        if conclusions:
            if len(conclusions) < 2:
                print("\nConclusion:", file=output)
            else:
                print("\nConclusions:", file=output)
            for index, sent in enumerate(conclusions, start=start_con_num):
                print(f"{index}. {sent}", file=output)

class ModelStructure:
    """Solves and stores the Z3 model for an instance of ModelSetup."""

    def __init__(self, model_constraints, max_time=1):
        self.constraint_dict = {} # hopefully temporary, for unsat_core

        # Store arguments
        self.model_constraints = model_constraints
        self.max_time = max_time

        # Store from model_constraint.syntax
        self.syntax = self.model_constraints.syntax
        self.start_time = self.syntax.start_time
        self.premises = self.syntax.premises
        self.conclusions = self.syntax.conclusions
        self.sentence_letters = self.syntax.sentence_letters

        # Store from model_constraint.semantics
        self.semantics = self.model_constraints.semantics
        self.main_world = self.semantics.main_world
        self.all_bits = self.semantics.all_bits
        self.N = self.semantics.N

        # Store from model_constraint
        self.proposition_class = self.model_constraints.proposition_class
        self.settings = self.model_constraints.settings

        # Solve Z3 constraints and store values
        timeout, z3_model, z3_model_status, z3_model_runtime = self.solve(
            self.model_constraints,
            self.max_time,
        )
        self.timeout = timeout
        self.z3_model = z3_model if z3_model_status else None
        self.unsat_core = z3_model if not z3_model_status else None
        self.z3_model_status = z3_model_status
        self.z3_model_runtime = z3_model_runtime

        # Store possible_bits, world_bits, and main_world from the Z3 model
        if not self.z3_model_status:
            self.poss_bits, self.world_bits, self.main_world = None, None, None
            return
        self.poss_bits = [
            bit
            for bit in self.all_bits
            if bool(self.z3_model.evaluate(self.semantics.possible(bit)))
            # LINTER: cannot access attribute "evaluate" for class "AstVector"
        ]
        self.world_bits = [
            bit
            for bit in self.poss_bits
            if bool(self.z3_model.evaluate(self.semantics.is_world(bit)))
            # LINTER: cannot access attribute "evaluate" for class "AstVector"
        ]
        if not self.z3_model is None:
            self.main_world = self.z3_model[self.main_world]

        # Define ANSI color codes
        self.COLORS = {
            "default": "\033[37m",  # WHITE
            "world": "\033[34m",    # BLUE
            "possible": "\033[36m", # CYAN
            "impossible": "\033[35m", # MAGENTA
            "initial": "\033[33m",  # YELLOW
        }
        self.RESET = "\033[0m"
        self.WHITE = self.COLORS["default"]

        # Recursively update propositions
        self.interpret(self.premises + self.conclusions)

    def solve(self, model_constraints, max_time):
        solver = Solver()
        # Track each constraint with a unique name
        fc, mc, pc, cc = (
            model_constraints.frame_constraints,
            model_constraints.model_constraints,
            model_constraints.premise_constraints,
            model_constraints.conclusion_constraints
        )
        for c_group, c_group_name in [
            (fc, "frame"),
            (mc, "model"),
            (pc, "premises"),
            (cc, "conclusions")
        ]:
            for ix, c in enumerate(c_group):
                c_id = f"{c_group_name}{ix+1}"
                solver.assert_and_track(c, c_id)
                self.constraint_dict[c_id] = c

        solver.set("timeout", int(max_time * 1000))  # time in seconds
        try:
            model_start = time.time()  # start benchmark timer
            result = solver.check()
            model_end = time.time()  # end benchmark timer
            model_runtime = round(model_end - model_start, 4)
            if result == sat:
                return False, solver.model(), True, model_runtime
            if solver.reason_unknown() == "timeout":
                return True, None, False, model_runtime
            return False, solver.unsat_core(), False, model_runtime
        except RuntimeError as e:  # Handle unexpected exceptions
            print(f"An error occurred while running `solve_constraints()`: {e}")
            return True, None, False, None

    def interpret(self, sentences):
        """Updates each instance of Sentence in sentences by adding the
        prefix_sent to that instance, returning the input sentences."""

        for sent_obj in sentences:
            if sent_obj.proposition is not None:
                continue
            if sent_obj.arguments:
                self.interpret(sent_obj.arguments)
            sent_obj.update_proposition(self)

    def print_evaluation(self, output=sys.__stdout__):
        """print the evaluation world and all sentences letters that true/false
        in that world"""
        BLUE = ""
        RESET = ""
        main_world = self.main_world
        if output is sys.__stdout__:
            BLUE = "\033[34m"
            RESET = "\033[0m"
        print(
            f"\nThe evaluation world is: {BLUE}{bitvec_to_substates(main_world, self.N)}{RESET}\n",
            file=output,
        )

    def print_grouped_constraints(self, output=sys.__stdout__):
        """Prints constraints organized by their groups (frame, model, premises, conclusions)"""
        groups = {
            "FRAME": [],
            "MODEL": [],
            "PREMISES": [],
            "CONCLUSIONS": []
        }
        
        # Get the relevant constraints based on model status
        if self.z3_model:
            print("\nSATISFIABLE CONSTRAINTS:", file=output)
            constraints = self.model_constraints.all_constraints
        elif self.unsat_core is not None:
            print("\nUNSATISFIABLE CORE CONSTRAINTS:", file=output)
            constraints = [self.constraint_dict[str(c)] for c in self.unsat_core]
        else:
            print("\nNO CONSTRAINTS AVAILABLE", file=output)
            constraints = []
            
        # Print summary of constraint groups
        frame_count = sum(1 for c in constraints if c in self.model_constraints.frame_constraints)
        model_count = sum(1 for c in constraints if c in self.model_constraints.model_constraints) 
        premise_count = sum(1 for c in constraints if c in self.model_constraints.premise_constraints)
        conclusion_count = sum(1 for c in constraints if c in self.model_constraints.conclusion_constraints)
        
        print(f"- Frame constraints: {frame_count}", file=output)
        print(f"- Model constraints: {model_count}", file=output)
        print(f"- Premise constraints: {premise_count}", file=output)
        print(f"- Conclusion constraints: {conclusion_count}\n", file=output)
        
        # Organize constraints into groups
        for constraint in constraints:
            constraint_str = str(constraint)
            if constraint in self.model_constraints.frame_constraints:
                groups["FRAME"].append(constraint)
            elif constraint in self.model_constraints.model_constraints:
                groups["MODEL"].append(constraint)
            elif constraint in self.model_constraints.premise_constraints:
                groups["PREMISES"].append(constraint)
            elif constraint in self.model_constraints.conclusion_constraints:
                groups["CONCLUSIONS"].append(constraint)
        
        # Print each group
        for group_name, group_constraints in groups.items():
            if group_constraints:  # Only print groups that have constraints
                print(f"{group_name} CONSTRAINTS:", file=output)
                for index, con in enumerate(group_constraints, start=1):
                    print(f"{index}. {con}\n", file=output)

    def print_constraints(self, constraints, name, output=sys.__stdout__):
        """prints constraints in an numbered list"""
        if self.z3_model_status:
            print(f"Satisfiable {name} constraints:\n", file=output)
        else:
            print("Unsatisfiable core constraints:\n", file=output)
        for index, con in enumerate(constraints, start=1):
            print(f"{index}. {con}\n", file=output)

    def print_to(self, default_settings, example_name, theory_name, print_constraints=None, output=sys.__stdout__):
        """append all elements of the model to the file provided
        
        Args:
            print_constraints: Whether to print constraints. Defaults to value in settings.
            output: Output stream to print to. Defaults to sys.stdout.
        """
        if print_constraints is None:
            print_constraints = self.settings["print_constraints"]
        if self.timeout:
            print(f"TIMEOUT: {self.timeout}")
            print(f"No model for example {example_name} found before timeout.", file=output)
            print(f"Try increasing max_time > {self.max_time}.\n", file=output)
            return
        self.print_all(default_settings, example_name, theory_name, output)
        if print_constraints and self.unsat_core is not None:
            self.print_grouped_constraints(output)

    def build_test_file(self, output):
        """generates a test file from input to be saved"""

        inputs_data = {
            "settings": self.model_constraints.settings,
            "premises": self.premises,
            "conclusions": self.conclusions,
            "z3_model_runtime": self.z3_model_runtime,
        }
        inputs_content = inputs_template.substitute(inputs_data)
        print(inputs_content, file=output)


    def save_to(self, example_name, theory_name, include_constraints, output):
        """append all elements of the model to the file provided"""
        constraints = self.model_constraints.all_constraints
        self.print_all(example_name, theory_name, output)
        self.build_test_file(output)
        if include_constraints:
            print("# Satisfiable constraints", file=output)
            print(f"all_constraints = {constraints}", file=output)

    def print_states(self, output=sys.__stdout__):
        """Print all fusions of atomic states in the model."""

        def binary_bitvector(bit):
            return (
                bit.sexpr()
                if self.N % 4 != 0
                else int_to_binary(int(bit.sexpr()[2:], 16), self.N)
            )
        
        def format_state(bin_rep, state, color, label=""):
            """Helper function to format and print a state."""
            label_str = f" ({label})" if label else ""
            use_colors = output is sys.__stdout__
            if use_colors:
                print(f"  {self.WHITE}{bin_rep} = {color}{state}{label_str}{self.RESET}", file=output)
            else:
                print(f"  {bin_rep} = {state}{label_str}", file=output)
        
        # Print formatted state space
        print("State Space:", file=output)
        for bit in self.all_bits:
            state = bitvec_to_substates(bit, self.N)
            bin_rep = binary_bitvector(bit)
            if bit == 0:
                format_state(bin_rep, state, self.COLORS["initial"])
            elif bit in self.world_bits:
                format_state(bin_rep, state, self.COLORS["world"], "world")
            elif bit in self.poss_bits:
                format_state(bin_rep, state, self.COLORS["possible"])
            elif self.settings['print_impossible']:
                format_state(bin_rep, state, self.COLORS["impossible"], "impossible")

    def recursive_print(self, sentence, eval_world, indent_num, use_colors):
        if indent_num == 2:  # NOTE: otherwise second lines don't indent
            indent_num += 1
        if sentence.sentence_letter is not None:  # Print sentence letter
            # print(f"OUTPUT REC PRINT: {output is sys.__stdout__}")
            sentence.proposition.print_proposition(eval_world, indent_num, use_colors)
            return
        operator = sentence.original_operator
        operator.print_method(sentence, eval_world, indent_num, use_colors)  # Print complex sentence

    def print_input_sentences(self, output):
        """Prints the interpreted premises and conclusions, leveraging recursive_print."""
        
        def print_sentences(title_singular, title_plural, sentences, start_index, destination):
            """Helper function to print a list of sentences with a title."""
            if sentences:
                title = title_singular if len(sentences) < 2 else title_plural
                print(title, file=output)
                for index, sentence in enumerate(sentences, start=start_index):
                    print(f"{index}.", end="", file=output)
                    with redirect_stdout(destination):
                        # print(f"OUTPUT PRINT_SENT {destination} is STD: {output is sys.__stdout__}")
                        use_colors = output is sys.__stdout__
                        self.recursive_print(sentence, self.main_world, 1, use_colors)
                        print(file=output)
        
        start_index = 1
        print_sentences(
            "INTERPRETED PREMISE:\n",
            "INTERPRETED PREMISES:\n",
            self.premises,
            start_index,
            output
        )
        continue_index = len(self.premises) + 1
        print_sentences(
            "INTERPRETED CONCLUSION:\n",
            "INTERPRETED CONCLUSIONS:\n",
            self.conclusions,
            continue_index,
            output
        )

    def print_model(self, output):
        if self.settings["print_z3"]:
            if self.z3_model_status:
                print(self.z3_model, file=output)
            else:
                print(self.unsat_core, file=output)

    def print_info(self, model_status, default_settings, example_name, theory_name, output):
        """Print model information including example details, settings, and runtime.
        
        Args:
            model_status (bool): Whether a countermodel was found
            default_settings (dict): Default settings to compare against
            example_name (str): Name of the example being checked
            theory_name (str): Name of the semantic theory being used
            output (file): Output stream to write to
        """
        
        # Determine result header
        header = "there is a countermodel." if model_status else "there is no countermodel."
        
        # Print example information
        self._print_section_header(example_name, header, output)
        self._print_model_details(theory_name, output)
        self._print_modified_settings(default_settings, output)
        
        # Print constraints and runtime
        self.model_constraints.print_enumerate(output)
        self._print_runtime_footer(output)

    def _print_section_header(self, example_name, header, output):
        """Print the section header with example name and result."""
        print(f"{'='*40}", file=output)
        print(f"\nEXAMPLE {example_name}: {header}\n", file=output)

    def _print_model_details(self, theory_name, output):
        """Print model details including atomic states and semantic theory."""
        print(f"Atomic States: {self.N}\n", file=output)
        print(f"Semantic Theory: {theory_name}\n", file=output)

    def _print_modified_settings(self, default_settings, output):
        """Print any settings that differ from defaults."""
        modified_settings = {
            key: self.settings[key]
            for key, default_value in default_settings.items() 
            if default_value != self.settings[key]
        }
        
        if modified_settings:
            print("Non-Default Settings:", file=output)
            for key, value in modified_settings.items():
                print(f"  {key} = {value}", file=output)
            print()

    def _print_runtime_footer(self, output):
        """Print Z3 runtime and separator footer."""
        print(f"\nZ3 Run Time: {self.z3_model_runtime} seconds", file=output)
        print(f"\n{'='*40}\n", file=output)

    def print_all(self, default_settings, example_name, theory_name, output=sys.__stdout__):
        """prints states, sentence letters evaluated at the designated world and
        recursively prints each sentence and its parts"""
        model_status = self.z3_model_status
        self.print_info(model_status, default_settings, example_name, theory_name, output)
        if model_status:
            self.print_states(output)
            self.print_evaluation(output)
            self.print_input_sentences(output)
            self.print_model(output)
            if output is sys.__stdout__:
                total_time = round(time.time() - self.start_time, 4) 
                print(f"Total Run Time: {total_time} seconds\n", file=output)
                print(f"{'='*40}", file=output)
            return
