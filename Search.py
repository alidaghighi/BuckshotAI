import time
import random
from Buckshot import *

class Search:
    def __init__(self):
        pass
    
    def search(state: Buckshot):
        all_actions = state.generate_moves()
        
