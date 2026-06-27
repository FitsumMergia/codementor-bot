"""Intellisense features — zero API cost, instant response.

1. Progressive hints per lesson (3 levels)
2. Python keyword/concept quick reference
3. Pre-grading syntax error detection with beginner-friendly explanations
"""
import re

# ---------------------------------------------------------------------------
# 1. Progressive hints (3 levels per lesson)
# ---------------------------------------------------------------------------

HINTS = {
    0: [  # L1: Say hello with print()
        "Use <code>print()</code> with text inside quotes.",
        'The text goes inside parentheses and quotes: <code>print("...")</code>',
        'Almost there! Try: <code>print("My name is Sara")</code> but use your own name.',
    ],
    1: [  # L2: Variables
        "First create the variable: <code>fav = 7</code> (pick any number).",
        "After creating <code>fav</code>, use <code>print()</code> to show it.",
        'Try: <code>fav = 7</code> then <code>print("My favourite number is", fav)</code>',
    ],
    2: [  # L3: Doing math
        "Create two variables for width and height, then multiply them.",
        "Use the <code>*</code> operator to multiply: <code>area = width * height</code>",
        'Try: <code>width = 5</code>, <code>height = 3</code>, <code>area = width * height</code>, <code>print("Area:", area)</code>',
    ],
    3: [  # L4: if/else
        "Start with <code>score = 75</code> (or any number). Then use <code>if</code>.",
        "The condition is <code>if score >= 50:</code> — don't forget the colon!",
        'Try:\n<pre>score = 75\nif score >= 50:\n    print("You passed!")\nelse:\n    print("Try again")</pre>',
    ],
    4: [  # L5: input()
        "Use <code>input()</code> to ask a question: <code>name = input(\"Your name? \")</code>",
        "After getting the name, print a greeting with it.",
        'Try: <code>name = input("Your name? ")</code> then <code>print("Welcome,", name)</code>',
    ],
    5: [  # L6: elif
        "You need three branches: <code>if</code>, <code>elif</code>, and <code>else</code>.",
        "Check the highest threshold first: <code>if grade >= 90:</code>",
        'Try:\n<pre>grade = 85\nif grade >= 90:\n    print("Excellent")\nelif grade >= 70:\n    print("Good")\nelse:\n    print("Keep trying")</pre>',
    ],
    6: [  # L7: for loops
        "Create a list with square brackets: <code>items = [\"a\", \"b\", \"c\"]</code>",
        "Loop with: <code>for item in items:</code> — don't forget the colon and indent!",
        'Try:\n<pre>colors = ["red", "blue", "green"]\nfor color in colors:\n    print(color)</pre>',
    ],
    7: [  # L8: range()
        "<code>range(1, 11)</code> gives numbers 1 through 10.",
        "Put it in a for loop: <code>for i in range(1, 11):</code>",
        'Try: <code>for i in range(1, 11):</code> then <code>    print(i)</code>',
    ],
    8: [  # L9: append
        "Start with an empty list: <code>my_list = []</code>",
        "Add items with <code>my_list.append(\"something\")</code>",
        'Try:\n<pre>my_list = []\nmy_list.append("apple")\nmy_list.append("banana")\nmy_list.append("mango")\nprint(my_list)</pre>',
    ],
    9: [  # L10: first function
        "Define with <code>def double(n):</code> — don't forget the colon!",
        "Inside the function, <code>print(n * 2)</code>. Then call it: <code>double(5)</code>",
        'Try:\n<pre>def double(n):\n    print(n * 2)\n\ndouble(5)</pre>',
    ],
    10: [  # L11: return
        "<code>return</code> sends a value back. Different from <code>print</code>!",
        "Use <code>return n * n</code> inside the function, then <code>print(square(5))</code> outside.",
        'Try:\n<pre>def square(n):\n    return n * n\n\nprint(square(5))</pre>',
    ],
    11: [  # L12: default parameters
        "A default value goes in the function definition: <code>def power(base, exp=2):</code>",
        "Inside, use <code>return base ** exp</code>. The <code>**</code> operator is exponentiation.",
        'Try:\n<pre>def power(base, exp=2):\n    return base ** exp\n\nprint(power(3))\nprint(power(2, 3))</pre>',
    ],
    12: [  # L13: strings
        "<code>.upper()</code> converts text to UPPERCASE. <code>len()</code> counts characters.",
        "Call them like: <code>print(text.upper())</code> and <code>print(len(text))</code>",
        'Try:\n<pre>text = "python is fun"\nprint(text.upper())\nprint(len(text))</pre>',
    ],
    13: [  # L14: calculator
        "Start with the example, then add <code>elif op == \"*\":</code> and <code>elif op == \"/\":</code>",
        "Each branch returns the math result: <code>return a * b</code>",
        'Add these branches:\n<pre>elif op == "*":\n    return a * b\nelif op == "/":\n    return a / b</pre>',
    ],
    14: [  # L15: FizzBuzz
        "Check divisible by 15 (both 3 and 5) FIRST, before checking 3 or 5 alone.",
        "Use <code>%</code> (modulo): <code>if i % 15 == 0:</code> means divisible by both.",
        'Try:\n<pre>for i in range(1, 21):\n    if i % 15 == 0:\n        print("FizzBuzz")\n    elif i % 3 == 0:\n        print("Fizz")\n    elif i % 5 == 0:\n        print("Buzz")\n    else:\n        print(i)</pre>',
    ],
}


def get_hint(lesson_index: int, hint_level: int) -> tuple[str, int]:
    """Returns (hint_html, next_level). Level wraps at max."""
    hints = HINTS.get(lesson_index, HINTS[0])
    level = min(hint_level, len(hints) - 1)
    next_level = min(level + 1, len(hints) - 1)
    prefix = ["💡 <b>Hint:</b>", "💡💡 <b>Bigger hint:</b>", "💡💡💡 <b>Almost the answer:</b>"][level]
    return f"{prefix}\n\n{hints[level]}", next_level


# ---------------------------------------------------------------------------
# 2. Python quick reference (/explain keyword)
# ---------------------------------------------------------------------------

PYTHON_REF = {
    "print": (
        "<b>print()</b> — show text on screen\n\n"
        '<pre>print("Hello")          # Hello\n'
        'print("Age:", 25)       # Age: 25\n'
        'print(3 + 4)            # 7</pre>'
    ),
    "variable": (
        "<b>Variables</b> — store values with a name\n\n"
        "<pre>name = \"Sara\"     # text (string)\n"
        "age = 25            # number (int)\n"
        "price = 9.99        # decimal (float)\n"
        "is_student = True   # yes/no (bool)</pre>"
    ),
    "if": (
        "<b>if / elif / else</b> — make decisions\n\n"
        "<pre>if x > 10:\n"
        "    print(\"big\")\n"
        "elif x > 5:\n"
        "    print(\"medium\")\n"
        "else:\n"
        "    print(\"small\")</pre>\n\n"
        "Comparisons: <code>==</code> equal, <code>!=</code> not equal, "
        "<code>&gt;</code> <code>&lt;</code> <code>&gt;=</code> <code>&lt;=</code>"
    ),
    "for": (
        "<b>for loop</b> — repeat for each item\n\n"
        '<pre>for x in [1, 2, 3]:\n    print(x)\n\n'
        'for i in range(5):    # 0,1,2,3,4\n    print(i)\n\n'
        'for ch in "hello":   # h,e,l,l,o\n    print(ch)</pre>'
    ),
    "while": (
        "<b>while loop</b> — repeat while condition is true\n\n"
        "<pre>count = 0\nwhile count &lt; 5:\n"
        "    print(count)\n    count += 1</pre>\n\n"
        "Be careful: if the condition never becomes False, the loop runs forever!"
    ),
    "def": (
        "<b>def</b> — define a function\n\n"
        '<pre>def greet(name):\n    return "Hello " + name\n\n'
        "result = greet(\"Sara\")\n"
        'print(result)  # Hello Sara</pre>\n\n'
        "<code>return</code> sends a value back. <code>print</code> just shows it."
    ),
    "list": (
        "<b>Lists</b> — ordered collection\n\n"
        "<pre>fruits = [\"apple\", \"banana\"]\n"
        "fruits.append(\"mango\")   # add\n"
        "print(fruits[0])          # apple\n"
        "print(len(fruits))        # 3\n\n"
        "for f in fruits:          # loop\n"
        "    print(f)</pre>"
    ),
    "string": (
        "<b>Strings</b> — text operations\n\n"
        '<pre>s = "Hello World"\n'
        "s.upper()       # HELLO WORLD\n"
        "s.lower()       # hello world\n"
        "s.replace(\"o\",\"0\")  # Hell0 W0rld\n"
        "len(s)          # 11\n"
        "s[0]            # H\n"
        "s[0:5]          # Hello</pre>"
    ),
    "input": (
        "<b>input()</b> — get text from the user\n\n"
        '<pre>name = input("Your name? ")\n'
        "print(\"Hi\", name)\n\n"
        "# For numbers, convert with int():\n"
        'age = int(input("Age? "))\n'
        "print(age + 1)</pre>"
    ),
    "range": (
        "<b>range()</b> — generate numbers\n\n"
        "<pre>range(5)       # 0, 1, 2, 3, 4\n"
        "range(1, 6)    # 1, 2, 3, 4, 5\n"
        "range(0, 10, 2) # 0, 2, 4, 6, 8\n\n"
        "for i in range(3):\n"
        "    print(i)   # 0, 1, 2</pre>"
    ),
    "return": (
        "<b>return</b> — send a value back from a function\n\n"
        "<pre>def add(a, b):\n    return a + b\n\n"
        "result = add(3, 4)\n"
        "print(result)  # 7</pre>\n\n"
        "<code>return</code> exits the function. Code after <code>return</code> won't run.\n"
        "<code>print</code> shows on screen but doesn't send a value back."
    ),
    "dict": (
        "<b>Dictionary</b> — key-value pairs\n\n"
        '<pre>person = {"name": "Sara", "age": 25}\n'
        "print(person[\"name\"])  # Sara\n"
        "person[\"city\"] = \"Addis\"  # add\n"
        "for key in person:\n"
        "    print(key, person[key])</pre>"
    ),
}

# Aliases
PYTHON_REF["elif"] = PYTHON_REF["if"]
PYTHON_REF["else"] = PYTHON_REF["if"]
PYTHON_REF["loop"] = PYTHON_REF["for"]
PYTHON_REF["function"] = PYTHON_REF["def"]
PYTHON_REF["str"] = PYTHON_REF["string"]
PYTHON_REF["append"] = PYTHON_REF["list"]
PYTHON_REF["variables"] = PYTHON_REF["variable"]


def explain_keyword(keyword: str) -> str | None:
    """Returns HTML explanation or None if keyword not found."""
    return PYTHON_REF.get(keyword.lower().strip())


def list_keywords() -> str:
    unique = sorted(set(k for k, v in PYTHON_REF.items() if not any(
        PYTHON_REF[other] is v and other < k for other in PYTHON_REF
    )))
    return ", ".join(f"<code>{k}</code>" for k in unique)


# ---------------------------------------------------------------------------
# 3. Pre-grading syntax error detection
# ---------------------------------------------------------------------------

_CHECKS = [
    (
        r'(?:if|elif|else|for|while|def|class)\s+[^:]*$',
        "Missing colon <code>:</code> — Python needs a colon at the end of <code>if</code>, <code>for</code>, <code>def</code>, etc.\n\n"
        "Example: <code>if score >= 50:</code> (note the colon at the end)",
    ),
    (
        r'print\s+["\']',
        "Missing parentheses — <code>print</code> needs parentheses in Python 3.\n\n"
        'Use <code>print("Hello")</code> not <code>print "Hello"</code>',
    ),
    (
        None,  # custom check for unmatched parens
        "Unmatched parenthesis — you have {open} opening <code>(</code> but {close} closing <code>)</code>.",
    ),
    (
        None,  # custom check for unmatched quotes
        "Unmatched quotes — check that every opening quote has a closing one.",
    ),
]


def check_syntax(code: str) -> str | None:
    """Returns a beginner-friendly error message, or None if no issues found."""
    lines = code.strip().split("\n")

    # Check each line for missing colons
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            if re.match(r'^(if|elif|for|while|def)\s+.*[^:]$', stripped):
                if not stripped.endswith(",") and ":" not in stripped:
                    keyword = stripped.split()[0]
                    return (
                        f"⚠️ Looks like you're missing a colon after your <code>{keyword}</code> statement.\n\n"
                        f"Python needs <code>:</code> at the end:\n"
                        f"<code>{keyword} ...:</code>"
                    )

    # Check print without parens
    for line in lines:
        stripped = line.strip()
        if re.match(r'^print\s+["\']', stripped):
            return (
                '⚠️ <code>print</code> needs parentheses in Python 3.\n\n'
                'Use: <code>print("Hello")</code>\n'
                'Not: <code>print "Hello"</code>'
            )

    # Check unmatched parentheses
    opens = code.count("(")
    closes = code.count(")")
    if opens != closes:
        return (
            "⚠️ Unmatched parentheses — you have {o} <code>(</code> but {c} <code>)</code>.\n\n"
            "Check that every <code>(</code> has a matching <code>)</code>.".format(o=opens, c=closes)
        )

    # Check unmatched quotes (simple check)
    for q in ['"', "'"]:
        # Skip triple quotes
        stripped = code.replace(f"{q}{q}{q}", "")
        if stripped.count(q) % 2 != 0:
            return (
                "⚠️ Unmatched quotes — you have an odd number of <code>{q}</code> marks.\n\n"
                "Make sure every opening quote has a closing one.".format(q=q)
            )

    return None
