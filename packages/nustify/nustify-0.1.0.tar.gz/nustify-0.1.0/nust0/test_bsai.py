import sys
import os

# Add the parent directory of 'NUST' to sys.path
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

# Import the function using 'nust'
from nust0.seecs.experimental.bsai import semester_1

# Print the first semester experience
print(semester_1())
