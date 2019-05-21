import os 

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'how_can_we_prove_that_computers_dont_have_feelings_what_if_we_are_in_a_simulation_for_a_fifth_graders_science_fair_project'