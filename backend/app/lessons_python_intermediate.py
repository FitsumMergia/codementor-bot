"""Python intermediate lessons (L16-L30). Builds on the beginner track."""

LESSONS_PYTHON_INTERMEDIATE = [
    {
        "id": 16,
        "topic": "Dictionaries",
        "content": (
            "<b>Lesson 16 — Dictionaries</b>\n\n"
            "A <b>dictionary</b> stores key-value pairs — like a phone book.\n\n"
            "<b>Example:</b>\n"
            "<pre>person = {\"name\": \"Sara\", \"age\": 25}\n"
            "print(person[\"name\"])   # Sara\n"
            "person[\"city\"] = \"Addis\"\nprint(person)</pre>\n\n"
            "<b>Your turn:</b>\n"
            "Create a dictionary called <code>student</code> with keys "
            "<code>name</code>, <code>grade</code>, and <code>subject</code>. Print it.\n\n"
            "Send me your code. 👇"
        ),
        "exercise": "Create a dict `student` with name, grade, subject keys. Print it.",
        "rubric": "Pass if: a dict named `student` has at least 2 key-value pairs and is printed.",
        "concepts": ["dictionaries"],
    },
    {
        "id": 17,
        "topic": "Looping through dictionaries",
        "content": (
            "<b>Lesson 17 — Looping through dictionaries</b>\n\n"
            "<pre>scores = {\"math\": 90, \"science\": 85}\n\n"
            "for subject, score in scores.items():\n"
            "    print(subject, score)</pre>\n\n"
            "<b>Your turn:</b>\n"
            "Create a dictionary of 3 items and loop through it, printing each key and value.\n\n"
            "Send me your code. 👇"
        ),
        "exercise": "Create a dict with 3+ items, loop with .items(), print each key-value.",
        "rubric": "Pass if: a dict exists, .items() is used in a for loop, and keys/values are printed.",
        "concepts": ["dictionaries", "for loop"],
    },
    {
        "id": 18,
        "topic": "While loops",
        "content": (
            "<b>Lesson 18 — While loops</b>\n\n"
            "A <code>while</code> loop repeats as long as a condition is true.\n\n"
            "<pre>count = 1\nwhile count <= 5:\n"
            "    print(count)\n    count += 1</pre>\n\n"
            "<b>Your turn:</b>\n"
            "Use a while loop to print numbers from 10 down to 1 (countdown).\n\n"
            "Send me your code. 👇"
        ),
        "exercise": "Use a while loop to count down from 10 to 1, printing each number.",
        "rubric": "Pass if: a while loop counts down from 10 (or similar) to 1, printing each number. Accept any decrement approach.",
        "concepts": ["while loop"],
    },
    {
        "id": 19,
        "topic": "String formatting with f-strings",
        "content": (
            "<b>Lesson 19 — f-strings</b>\n\n"
            "f-strings let you put variables directly inside text:\n\n"
            "<pre>name = \"Sara\"\nage = 25\n"
            "print(f\"{name} is {age} years old\")</pre>\n"
            "Shows: <code>Sara is 25 years old</code>\n\n"
            "<b>Your turn:</b>\n"
            "Create variables for a product name and price, then use an f-string "
            "to print: <code>The [product] costs [price] ETB</code>\n\n"
            "Send me your code. 👇"
        ),
        "exercise": "Create product/price variables, print with f-string formatting.",
        "rubric": "Pass if: an f-string (f\"...\") is used with at least one variable inside curly braces, and the result is printed.",
        "concepts": ["f-strings", "string formatting"],
    },
    {
        "id": 20,
        "topic": "Lists inside lists (2D)",
        "content": (
            "<b>Lesson 20 — Lists inside lists</b>\n\n"
            "A list can contain other lists — like a table:\n\n"
            "<pre>grid = [[1, 2, 3],\n        [4, 5, 6]]\n\n"
            "print(grid[0][1])  # 2 (row 0, col 1)\n\n"
            "for row in grid:\n    print(row)</pre>\n\n"
            "<b>Your turn:</b>\n"
            "Create a 3x3 grid (list of 3 lists, each with 3 numbers). "
            "Loop through and print each row.\n\n"
            "Send me your code. 👇"
        ),
        "exercise": "Create a 3x3 grid (list of lists) and loop to print each row.",
        "rubric": "Pass if: a list contains at least 2 inner lists, and a for loop prints each row.",
        "concepts": ["nested lists", "for loop"],
    },
    {
        "id": 21,
        "topic": "Try/except (handling errors)",
        "content": (
            "<b>Lesson 21 — Handling errors with try/except</b>\n\n"
            "Errors crash your program — unless you catch them:\n\n"
            "<pre>try:\n    num = int(input(\"Number: \"))\n    print(10 / num)\n"
            "except ValueError:\n    print(\"That's not a number!\")\n"
            "except ZeroDivisionError:\n    print(\"Can't divide by zero!\")</pre>\n\n"
            "<b>Your turn:</b>\n"
            "Write code that tries to convert a string to an integer. "
            "If it fails, print an error message.\n\n"
            "<pre>try:\n    x = int(\"hello\")\nexcept ValueError:\n    print(\"Not a number!\")</pre>\n\n"
            "Send me your code. 👇"
        ),
        "exercise": "Use try/except to catch a ValueError when converting a bad string to int.",
        "rubric": "Pass if: try/except is used, int() conversion is attempted, and a ValueError (or generic except) is caught with a print.",
        "concepts": ["try/except", "error handling"],
    },
    {
        "id": 22,
        "topic": "Reading and writing files",
        "content": (
            "<b>Lesson 22 — Files</b>\n\n"
            "Python can read and write files:\n\n"
            "<pre># Write\nwith open(\"notes.txt\", \"w\") as f:\n"
            "    f.write(\"Hello file!\")\n\n"
            "# Read\nwith open(\"notes.txt\", \"r\") as f:\n"
            "    content = f.read()\n    print(content)</pre>\n\n"
            "<b>Your turn:</b>\n"
            "Write code that opens a file, writes your name to it, then reads "
            "and prints the content. (Don't worry — this is graded by reading "
            "your code, not running it.)\n\n"
            "Send me your code. 👇"
        ),
        "exercise": "Write code that opens a file with 'w' mode, writes text, then reads it back with 'r' mode and prints.",
        "rubric": "Pass if: open() is used with both 'w' and 'r' modes (or 'a'), write/read methods are called, and content is printed. Accept with or without 'with' statement.",
        "concepts": ["files", "open", "with"],
    },
    {
        "id": 23,
        "topic": "List comprehensions",
        "content": (
            "<b>Lesson 23 — List comprehensions</b>\n\n"
            "A shortcut to build lists:\n\n"
            "<pre>squares = [n * n for n in range(1, 6)]\n"
            "print(squares)  # [1, 4, 9, 16, 25]\n\n"
            "# With a filter:\n"
            "evens = [n for n in range(10) if n % 2 == 0]\n"
            "print(evens)   # [0, 2, 4, 6, 8]</pre>\n\n"
            "<b>Your turn:</b>\n"
            "Use a list comprehension to create a list of all numbers from 1-20 "
            "that are divisible by 3. Print it.\n\n"
            "Send me your code. 👇"
        ),
        "exercise": "Use a list comprehension to get numbers 1-20 divisible by 3. Print the list.",
        "rubric": "Pass if: a list comprehension with `for` and `if` is used, checking % 3 == 0, and result is printed. Accept range(1,21) or range(20).",
        "concepts": ["list comprehension", "filter"],
    },
    {
        "id": 24,
        "topic": "Lambda and map/filter",
        "content": (
            "<b>Lesson 24 — Lambda functions</b>\n\n"
            "A <code>lambda</code> is a tiny one-line function:\n\n"
            "<pre>double = lambda x: x * 2\nprint(double(5))  # 10\n\n"
            "# map applies a function to every item:\n"
            "nums = [1, 2, 3, 4]\n"
            "doubled = list(map(lambda x: x * 2, nums))\n"
            "print(doubled)  # [2, 4, 6, 8]</pre>\n\n"
            "<b>Your turn:</b>\n"
            "Use <code>map</code> with a <code>lambda</code> to square every "
            "number in <code>[1, 2, 3, 4, 5]</code>. Print the result.\n\n"
            "Send me your code. 👇"
        ),
        "exercise": "Use map() with lambda to square each number in [1,2,3,4,5]. Print result.",
        "rubric": "Pass if: map() is called with a lambda, the lambda squares its input (x*x or x**2), and the result is printed. Accept list() wrapping.",
        "concepts": ["lambda", "map"],
    },
    {
        "id": 25,
        "topic": "Classes and objects",
        "content": (
            "<b>Lesson 25 — Classes (your first object)</b>\n\n"
            "A <b>class</b> is a blueprint for creating objects:\n\n"
            "<pre>class Dog:\n    def __init__(self, name, breed):\n"
            "        self.name = name\n        self.breed = breed\n\n"
            "    def bark(self):\n        print(f\"{self.name} says Woof!\")\n\n"
            "my_dog = Dog(\"Rex\", \"German Shepherd\")\n"
            "my_dog.bark()  # Rex says Woof!</pre>\n\n"
            "<b>Your turn:</b>\n"
            "Create a class <code>Student</code> with <code>name</code> and "
            "<code>grade</code>. Add a method <code>info()</code> that prints "
            "both. Create an instance and call <code>info()</code>.\n\n"
            "Send me your code. 👇"
        ),
        "exercise": "Create a Student class with name/grade and an info() method. Create an instance and call info().",
        "rubric": "Pass if: class Student is defined with __init__ setting name and grade, an info/display method prints them, and an instance is created and the method called.",
        "concepts": ["classes", "objects", "__init__"],
    },
    {
        "id": 26,
        "topic": "Importing modules",
        "content": (
            "<b>Lesson 26 — Modules</b>\n\n"
            "Python has thousands of built-in tools. Import them:\n\n"
            "<pre>import random\nprint(random.randint(1, 100))\n\n"
            "import math\nprint(math.sqrt(144))  # 12.0\n\n"
            "from datetime import date\nprint(date.today())</pre>\n\n"
            "<b>Your turn:</b>\n"
            "Import the <code>random</code> module. Generate and print "
            "a random number between 1 and 10.\n\n"
            "Send me your code. 👇"
        ),
        "exercise": "Import random module and print a random number between 1 and 10.",
        "rubric": "Pass if: `import random` is present, and random.randint() or random.choice() or random.random() is used with print. Accept any random function.",
        "concepts": ["import", "modules", "random"],
    },
    {
        "id": 27,
        "topic": "Tuples and unpacking",
        "content": (
            "<b>Lesson 27 — Tuples</b>\n\n"
            "A <b>tuple</b> is like a list that can't be changed:\n\n"
            "<pre>point = (3, 7)\nx, y = point  # unpacking\n"
            "print(f\"x={x}, y={y}\")\n\n"
            "# Functions can return tuples:\n"
            "def min_max(nums):\n    return min(nums), max(nums)\n\n"
            "lo, hi = min_max([5, 2, 8, 1])\n"
            "print(f\"min={lo}, max={hi}\")</pre>\n\n"
            "<b>Your turn:</b>\n"
            "Write a function that returns a tuple of (sum, average) for a list. "
            "Unpack and print both values.\n\n"
            "Send me your code. 👇"
        ),
        "exercise": "Write a function returning (sum, average) of a list. Unpack and print both.",
        "rubric": "Pass if: a function returns a tuple with sum and average (sum/len), the result is unpacked into two variables, and both are printed.",
        "concepts": ["tuples", "unpacking", "return"],
    },
    {
        "id": 28,
        "topic": "Sets and set operations",
        "content": (
            "<b>Lesson 28 — Sets</b>\n\n"
            "A <b>set</b> holds unique items (no duplicates):\n\n"
            "<pre>fruits = {\"apple\", \"banana\", \"apple\"}\n"
            "print(fruits)  # {'apple', 'banana'}\n\n"
            "a = {1, 2, 3}\nb = {2, 3, 4}\n"
            "print(a &amp; b)   # {2, 3} intersection\n"
            "print(a | b)   # {1, 2, 3, 4} union</pre>\n\n"
            "<b>Your turn:</b>\n"
            "Create two sets of numbers. Print their intersection (shared items) "
            "and union (all items combined).\n\n"
            "Send me your code. 👇"
        ),
        "exercise": "Create two sets, print their intersection and union.",
        "rubric": "Pass if: two sets are created, intersection (& or .intersection()) and union (| or .union()) are computed and printed.",
        "concepts": ["sets", "intersection", "union"],
    },
    {
        "id": 29,
        "topic": "Building a to-do list app",
        "content": (
            "<b>Lesson 29 — Mini project: To-Do List</b>\n\n"
            "Combine everything to build a simple to-do app:\n\n"
            "<pre>todos = []\n\ndef add(task):\n    todos.append(task)\n"
            "    print(f\"Added: {task}\")\n\n"
            "def show():\n    if not todos:\n        print(\"No tasks!\")\n"
            "    for i, task in enumerate(todos, 1):\n"
            "        print(f\"{i}. {task}\")\n\n"
            "add(\"Buy milk\")\nadd(\"Study Python\")\nshow()</pre>\n\n"
            "<b>Your turn:</b>\n"
            "Add a <code>remove(index)</code> function that removes a task by "
            "number. Show the full program with add, show, and remove.\n\n"
            "Send me your code. 👇"
        ),
        "exercise": "Build a to-do list with add(), show(), and remove() functions. Demo all three.",
        "rubric": "Pass if: a list is used, there are at least add and show functions (or equivalent), items are added and displayed. A remove function earns bonus score. Accept any approach.",
        "concepts": ["lists", "functions", "enumerate"],
    },
    {
        "id": 30,
        "topic": "Final project: Number guessing game",
        "content": (
            "<b>Lesson 30 — Final Project: Guessing Game!</b>\n\n"
            "Build a number guessing game using everything you've learned:\n\n"
            "<pre>import random\n\nsecret = random.randint(1, 20)\nattempts = 0\n\n"
            "while True:\n    guess = int(input(\"Guess (1-20): \"))\n"
            "    attempts += 1\n\n    if guess == secret:\n"
            "        print(f\"Correct! {attempts} tries\")\n        break\n"
            "    elif guess &lt; secret:\n        print(\"Too low!\")\n"
            "    else:\n        print(\"Too high!\")</pre>\n\n"
            "<b>Your turn:</b>\n"
            "Write the complete guessing game. Add a maximum of 5 attempts "
            "and print \"Game over\" if they run out.\n\n"
            "Send me your code. 👇"
        ),
        "exercise": "Write a number guessing game with random, while loop, if/elif, max 5 attempts, and game-over message.",
        "rubric": "Pass if: import random is used, a secret number is generated, a while loop takes guesses, if/elif compares guess vs secret with too high/low feedback, and there is some attempt limit or break condition. Accept input() or hardcoded test guesses.",
        "concepts": ["random", "while loop", "if/elif", "break", "game"],
    },
]
