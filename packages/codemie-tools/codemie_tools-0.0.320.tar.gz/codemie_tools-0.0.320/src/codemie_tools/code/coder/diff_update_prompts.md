# Business Description for `diff_update_prompts.py`

The `diff_update_prompts.py` file contains code that facilitates the update of prompts based on user requests. It employs best practices in software development, ensuring that modifications are made efficiently and in accordance with existing conventions within the codebase. The file primarily utilizes a structured approach for handling user requests to change specific functions or methods, with an emphasis on clear communication and adherence to coding standards. 

## Examples of Change Requests

### Change Request: Update `get_factorial()` to Use `math.factorial`

This change involves:
1. Importing the `math` package.
2. Removing the existing `factorial()` function.
3. Updating `get_factorial()` to invoke `math.factorial` instead.

Here are the *SEARCH/REPLACE* blocks for this change:

!!!python
<<<<<<< SEARCH
# factorial_example.py

from flask import Flask, request, jsonify
import sys

app = Flask(__name__)
=======
# factorial_example.py

from flask import Flask, request, jsonify
import math
import sys

app = Flask(__name__)
>>>>>>> REPLACE
!!!

!!!python
<<<<<<< SEARCH
app = Flask(__name__)

def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

@app.route('/factorial', methods=['GET'])
def get_factorial():
=======
app = Flask(__name__)

@app.route('/factorial', methods=['GET'])
def get_factorial():
>>>>>>> REPLACE
!!!

!!!python
<<<<<<< SEARCH
        n = int(request.args.get('number'))
        if n < 0:
            return jsonify({"error": "Input must be a non-negative integer."}), 400
        result = factorial(n)
        return jsonify({"number": n, "factorial": result}), 200
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid input. Please provide a non-negative integer."}), 400
=======
        n = int(request.args.get('number'))
        if n < 0:
            return jsonify({"error": "Input must be a non-negative integer."}), 400
        result = math.factorial(n)
        return jsonify({"number": n, "factorial": result}), 200
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid input. Please provide a non-negative integer."}), 400
>>>>>>> REPLACE
!!!