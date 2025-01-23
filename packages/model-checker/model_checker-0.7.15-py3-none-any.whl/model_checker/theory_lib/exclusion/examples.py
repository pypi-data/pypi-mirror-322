"""
This module tests the unilateral exclusion semantics, providing a evaluate the
logical relationships in a language with an exclusion operator and comparing the
result to the bilateral semantics.

Module Structure:
----------------
1. Imports:
   - Local semantic and operator definitions
   - Core model checker primitives
   - System utilities

2. Semantic Theories:
   - exclusion_theory: Implements exclusion logic with unilateral operators
   - default_theory: Classical logic implementation for comparison

3. Settings:
   - general_settings: Global configuration for output and debugging
   - example_settings: Default parameters for model checking

4. Example Categories:
   - Countermodels (EX_CM_*): Examples demonstrating invalid inferences
   - Logical Consequences (EX_TH_*): Examples of valid logical relationships

Configuration:
-------------
- semantic_theories: Dict of semantic theories to test against
- example_range: Dict of example cases to evaluate

Usage:
------
From the project directory, run:
    model-checker examples.py

Each example consists of:
1. Premises (list of logical formulas)
2. Conclusions (list of logical formulas)
3. Settings (dictionary of model checking parameters)

Help:
-----
More information can be found in the README.md for the exclusion theory.
"""

##########################
### DEFINE THE IMPORTS ###
##########################

import sys
import os
sys.path.append(os.path.dirname(__file__))  # Add the current directory to sys.path
from semantic import (
    ExclusionSemantics,
    UnilateralProposition,
)
from operators import (
    UniAndOperator, UniOrOperator, ExclusionOperator, # extensional
    UniIdentityOperator, # constitutive
)
from model_checker.primitive import (
    AndOperator,
    IdentityOperator,
    NegationOperator,
    OrOperator,
)
from model_checker.semantic import Proposition, Semantics
from model_checker import syntactic

####################################
### DEFINE THE SEMANTIC THEORIES ###
####################################

exclusion_operators = syntactic.OperatorCollection(
    UniAndOperator, UniOrOperator, ExclusionOperator, # extensional
    UniIdentityOperator, # constitutive
)

default_operators = syntactic.OperatorCollection(
    NegationOperator, AndOperator, OrOperator, # extensional
    IdentityOperator, # constitutive
)

exclusion_theory = {
    "semantics": ExclusionSemantics,
    "proposition": UnilateralProposition,
    "operators": exclusion_operators,
}

default_dictionary = {
    "\\exclude" : "\\neg",
    "\\uniwedge" : "\\wedge",
    "\\univee" : "\\vee",
    "\\uniequiv" : "\\equiv",
}

default_theory = {
    "semantics": Semantics,
    "proposition": Proposition,
    "operators": default_operators,
    "dictionary": default_dictionary,
}

#######################
### DEFINE SETTINGS ###
#######################

general_settings = {
    "print_constraints": False,
    "print_impossible": False,
    "print_z3": False,
    "save_output": False,
    "compare_theories": False,
}

example_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'disjoint' : False,
    'non_empty' : False,
    'non_null' : False,
    'fusion_closure' : False,
    'max_time' : 1,
}

# premises = ['\\exclude (A \\univee B)']
# conclusions = ['(\\exclude A \\uniwedge \\exclude B)']

# premises = ['\\exclude (A \\uniwedge B)']
# conclusions = ['(\\exclude A \\univee \\exclude B)']

# premises = ['(A \\uniequiv B)']

# premises = []
# conclusions = ["(\\exclude (A \\uniwedge B) \\uniequiv (\\exclude A \\univee \\exclude B))"]
# settings['N'] = 4

# premises = []
# conclusions = ["(\\exclude (A \\univee B) \\uniequiv (\\exclude A \\uniwedge \\exclude B))"]

# premises = []
# conclusions = ["((A \\univee (B \\uniwedge C)) \\uniequiv ((A \\univee B) \\uniwedge (A \\univee C)))"]
# settings['N'] = 4

# premises = []
# conclusions = ["((A \\uniwedge (B \\univee C)) \\uniequiv ((A \\uniwedge B) \\univee (A \\uniwedge C)))"]

# premises = ['(A \\uniwedge (B \\univee C))']
# conclusions = ['((A \\univee B) \\uniwedge (A \\univee C))']

# premises = ['\\exclude (A \\uniwedge B)']
# conclusions = ['(\\exclude A \\univee \\exclude B)']




#####################
### COUNTERMODELS ###
#####################

# DOUBLE NEGATION ELIMINATION IDENTITY
EX_CM_1_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
}
EX_CM_1_example = [
    [], # premises
    ['(A \\uniequiv \\exclude \\exclude A)'], # conclusions
    EX_CM_1_settings,
]

# REVERSE DISTRIBUTION: DISJUNCTION OVER CONJUNCTION
EX_CM_2_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
}
EX_CM_2_example = [
    ['((A \\univee B) \\uniwedge (A \\univee C))'], # premises
    ['(A \\uniwedge (B \\univee C))'], # conclusions
    EX_CM_2_settings,
]

# DOUBLE NEGATION ELIMINATION
EX_CM_3_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
}
EX_CM_3_example = [
    ['\\exclude \\exclude A'], # premises
    ['A'], # conclusions
    EX_CM_3_settings
]

# TRIPLE NEGATION ENTAILMENT
EX_CM_4_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
}
EX_CM_4_example = [
    ['\\exclude \\exclude \\exclude A'], # premises
    ['\\exclude A'], # conclusions
    EX_CM_4_settings
]

# TRIPLE NEGATION IDENTITY
EX_CM_5_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
}
EX_CM_5_example = [
    [], # premises
    ['(\\exclude A \\uniequiv \\exclude \\exclude \\exclude A)'], # conclusions
    EX_CM_5_settings, # these can be customized by example
]

# QUADRUPLE NEGATION
EX_CM_6_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
}
EX_CM_6_example = [
    ['\\exclude \\exclude \\exclude \\exclude A'], # premises
    ['\\exclude \\exclude A'], # conclusions
    EX_CM_6_settings
]

# CONJUNCTION DEMORGANS
EX_CM_7_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
}
EX_CM_7_example = [ # TODO: fix example
    ['\\exclude \\exclude \\exclude \\exclude A'], # premises
    ['\\exclude \\exclude A'], # conclusions
    EX_CM_7_settings
]



############################
### LOGICAL CONSEQUENCES ###
############################

# DISJUNCTIVE SYLLOGISM
EX_TH_1_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
}
EX_TH_1_example = [
    ['(A \\univee B)', '\\exclude B'], # premises
    ['A'], # conclusions
    EX_TH_1_settings
]

# CONJUNCTION DEMORGANS LR
EX_TH_2_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
}
EX_TH_2_example = [
    ['\\exclude (A \\uniwedge B)'], # premises
    ['(\\exclude A \\univee \\exclude B)'], # conclusions
    EX_TH_2_settings
]

# CONJUNCTION DEMORGANS RL
EX_TH_3_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
}
EX_TH_3_example = [
    ['(\\exclude A \\univee \\exclude B)'], # premises
    ['\\exclude (A \\uniwedge B)'], # conclusions
    EX_TH_3_settings
]

# DISJUNCTION DEMORGANS LR
EX_TH_3_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
}
EX_TH_3_example = [
    ['\\exclude (A \\univee B)'], # premises
    ['(\\exclude A \\uniwedge \\exclude B)'], # conclusions
    EX_TH_3_settings
]

# DISJUNCTION DEMORGANS RL
EX_TH_4_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
}
EX_TH_4_example = [
    ['(\\exclude A \\uniwedge \\exclude B)'], # premises
    ['\\exclude (A \\univee B)'], # conclusions
    EX_TH_4_settings
]

# DISJUNCTION DISTRIBUTION LR
EX_TH_5_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
}
EX_TH_5_example = [
    ['(A \\univee (B \\uniwedge C))'], # premises
    ['((A \\univee B) \\uniwedge (A \\univee C))'], # conclusions
    EX_TH_5_settings
]

# DISJUNCTION DISTRIBUTION RL
EX_TH_6_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
}
EX_TH_6_example = [
    ['((A \\univee B) \\uniwedge (A \\univee C))'], # premises
    ['(A \\univee (B \\uniwedge C))'], # conclusions
    EX_TH_6_settings
]

# CONJUNCTION DISTRIBUTION LR
EX_TH_7_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
}
EX_TH_7_example = [
    ['(A \\uniwedge (B \\univee C))'], # premises
    ['((A \\uniwedge B) \\univee (A \\uniwedge C))'], # conclusions
    EX_TH_7_settings
]

# CONJUNCTION DISTRIBUTION RL
EX_TH_8_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
}
EX_TH_8_example = [
    ['((A \\uniwedge B) \\univee (A \\uniwedge C))'], # premises
    ['(A \\uniwedge (B \\univee C))'], # conclusions
    EX_TH_8_settings
]

# CONJUNCTION ABSORPTION RL
EX_TH_9_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
}
EX_TH_9_example = [
    ['(A \\uniwedge (A \\univee B))'], # premises
    ['A'], # conclusions
    EX_TH_9_settings
]

# CONJUNCTION ABSORPTION LR
EX_TH_10_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
}
EX_TH_10_example = [
    ['A'], # premises
    ['(A \\uniwedge (A \\univee B))'], # conclusions
    EX_TH_10_settings
]

# DISJUNCTION ABSORPTION RL
EX_TH_11_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
}
EX_TH_11_example = [
    ['(A \\univee (A \\uniwedge B))'], # premises
    ['A'], # conclusions
    EX_TH_11_settings
]

# DISJUNCTION ABSORPTION LR
EX_TH_12_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
}
EX_TH_12_example = [
    ['A'], # premises
    ['(A \\univee (A \\uniwedge B))'], # conclusions
    EX_TH_12_settings
]

# CONJUNCTION ASSOCIATIVITY RL
EX_TH_13_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
}
EX_TH_13_example = [
    ['((A \\uniwedge B) \\uniwedge C)'], # premises
    ['(A \\uniwedge (B \\uniwedge C))'], # conclusions
    EX_TH_13_settings
]

# CONJUNCTION ASSOCIATIVITY LR
EX_TH_14_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
}
EX_TH_14_example = [
    ['(A \\uniwedge (B \\uniwedge C))'], # premises
    ['((A \\uniwedge B) \\uniwedge C)'], # conclusions
    EX_TH_14_settings
]

# DISJUNCTION ASSOCIATIVITY RL
EX_TH_15_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
}
EX_TH_15_example = [
    ['((A \\univee B) \\univee C)'], # premises
    ['(A \\univee (B \\univee C))'], # conclusions
    EX_TH_15_settings
]

# DISJUNCTION ASSOCIATIVITY LR
EX_TH_16_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : False,
    'non_null' : False,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
}
EX_TH_16_example = [
    ['(A \\univee (B \\univee C))'], # premises
    ['((A \\univee B) \\univee C)'], # conclusions
    EX_TH_16_settings
]

# UNIEQUIV DEMORGANS
uniequiv_demorgans_settings = {
    'N' : 3,
    'possible' : False,
    'contingent' : False,
    'non_empty' : True,
    'non_null' : True,
    'disjoint' : False,
    'fusion_closure' : False,
    'max_time' : 1,
}
UNIEQUIV_PLAYGROUND = [
    # [], # premises
    # ["(\\exclude (A \\uniwedge B) \\uniequiv (\\exclude A \\univee \\exclude B))"], # conclusions
    # ["(A \\uniequiv (A \\uniwedge B))"],
    ["(A \\uniequiv \\exclude A)"],
    [],
    uniequiv_demorgans_settings
]



###############################################
### DEFINE EXAMPLES AND THEORIES TO COMPUTE ###
###############################################

# NOTE: at least one theory is required, multiple are permitted for comparison
semantic_theories = {
    "ChampollionBernard" : exclusion_theory,
    # "Brast-McKie" : default_theory,
}

# NOTE: at least one example is required, multiple are permitted for comparison
example_range = {
    # Countermodels
    "EX_CM_1" : EX_CM_1_example, # disagree
    # "EX_CM_2" : EX_CM_2_example,
    # "EX_CM_3" : EX_CM_3_example, # disagree
    # "EX_CM_4" : EX_CM_4_example, # disagree
    # "EX_CM_5" : EX_CM_5_example, # disagree
    # "EX_CM_6" : EX_CM_6_example, # disagree
    # "EX_CM_7" : EX_CM_7_example, # disagree

    # Theorems
    "EX_TH_1" : EX_TH_1_example,
    # "EX_TH_2" : EX_TH_2_example,
    # "EX_TH_3" : EX_TH_3_example,
    # "EX_TH_4" : EX_TH_4_example,
    # "EX_TH_5" : EX_TH_5_example,
    # "EX_TH_6" : EX_TH_6_example,
    # "EX_TH_7" : EX_TH_7_example,
    # "EX_TH_8" : EX_TH_8_example,
    # "EX_TH_9" : EX_TH_9_example,
    # "EX_TH_10" : EX_TH_10_example,
    # "EX_TH_11" : EX_TH_11_example,
    # "EX_TH_12" : EX_TH_12_example,
    # "EX_TH_13" : EX_TH_13_example,
    # "EX_TH_14" : EX_TH_14_example,
    # "EX_TH_15" : EX_TH_15_example,
    # "EX_TH_16" : EX_TH_16_example,

    # Testing
    "UNIEQUIV PLAYGROUND" : UNIEQUIV_PLAYGROUND
}


