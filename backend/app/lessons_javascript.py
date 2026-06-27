"""JavaScript beginner track — 15 lessons, mirrors the Python beginner structure."""

LESSONS_JAVASCRIPT = [
    {
        "id": 1, "topic": "Say hello with console.log()",
        "content": (
            "<b>Lesson 1 — Say hello with console.log()</b>\n\n"
            "In JavaScript, <code>console.log()</code> shows text.\n\n"
            "<pre>console.log(\"Hello, world!\");</pre>\n\n"
            "<b>Your turn:</b>\nWrite one line that prints a sentence with your name.\n"
            "<pre>console.log(\"My name is Sara\");</pre>\n\nSend me your code. 👇"
        ),
        "exercise": "Write a console.log() statement with your name.",
        "rubric": "Pass if: console.log() is used with a string. Any text passes.",
        "concepts": ["console.log"],
    },
    {
        "id": 2, "topic": "Variables with let and const",
        "content": (
            "<b>Lesson 2 — Variables</b>\n\n"
            "<code>let</code> creates a variable. <code>const</code> creates one that can't change.\n\n"
            "<pre>let age = 25;\nconst name = \"Sara\";\nconsole.log(name, age);</pre>\n\n"
            "<b>Your turn:</b>\nCreate a <code>let</code> variable called <code>fav</code> with your "
            "favourite number. Print it.\n"
            "<pre>let fav = 7;\nconsole.log(\"My favourite:\", fav);</pre>\n\nSend me your code. 👇"
        ),
        "exercise": "Create a let variable `fav` with a number and console.log it.",
        "rubric": "Pass if: `let fav` or `const fav` is assigned a number and console.log includes it.",
        "concepts": ["let", "const", "variables"],
    },
    {
        "id": 3, "topic": "Doing math",
        "content": (
            "<b>Lesson 3 — Math</b>\n\n"
            "<pre>let width = 5;\nlet height = 3;\nlet area = width * height;\n"
            "console.log(\"Area:\", area);</pre>\n\n"
            "<b>Your turn:</b>\nCalculate and print the area of a rectangle with your own numbers.\n\n"
            "Send me your code. 👇"
        ),
        "exercise": "Create width/height variables, multiply into area, console.log the result.",
        "rubric": "Pass if: two number variables are multiplied and the result is logged.",
        "concepts": ["variables", "math"],
    },
    {
        "id": 4, "topic": "if/else decisions",
        "content": (
            "<b>Lesson 4 — if/else</b>\n\n"
            "<pre>let score = 75;\n\nif (score >= 50) {\n"
            "    console.log(\"You passed!\");\n} else {\n"
            "    console.log(\"Try again\");\n}</pre>\n\n"
            "Note: JavaScript uses <code>{ }</code> braces, not indentation.\n\n"
            "<b>Your turn:</b>\nCreate a <code>score</code> variable and write if/else to check pass/fail.\n\n"
            "Send me your code. 👇"
        ),
        "exercise": "Create score variable, if >= 50 log pass, else log fail.",
        "rubric": "Pass if: a variable, an if with comparison, and an else block, each with console.log.",
        "concepts": ["if/else", "comparison"],
    },
    {
        "id": 5, "topic": "Arrays (lists)",
        "content": (
            "<b>Lesson 5 — Arrays</b>\n\n"
            "<pre>let fruits = [\"apple\", \"banana\", \"mango\"];\n"
            "fruits.push(\"grape\");\nconsole.log(fruits);\nconsole.log(fruits.length);</pre>\n\n"
            "<b>Your turn:</b>\nCreate an array with 3 items. Add one with <code>.push()</code>. Print it.\n\n"
            "Send me your code. 👇"
        ),
        "exercise": "Create an array, push an item, console.log it.",
        "rubric": "Pass if: an array is created, .push() is called, and the array is logged.",
        "concepts": ["arrays", "push"],
    },
    {
        "id": 6, "topic": "for loops",
        "content": (
            "<b>Lesson 6 — for loops</b>\n\n"
            "<pre>let colors = [\"red\", \"blue\", \"green\"];\n\n"
            "for (let color of colors) {\n    console.log(color);\n}\n\n"
            "// Classic style:\nfor (let i = 0; i &lt; 5; i++) {\n    console.log(i);\n}</pre>\n\n"
            "<b>Your turn:</b>\nCreate an array of 3 items and use a for loop to print each one.\n\n"
            "Send me your code. 👇"
        ),
        "exercise": "Create an array and use for-of or for loop to log each item.",
        "rubric": "Pass if: an array exists and a for loop (for-of, for-in, or classic for) iterates and logs each.",
        "concepts": ["for loop", "arrays"],
    },
    {
        "id": 7, "topic": "Functions",
        "content": (
            "<b>Lesson 7 — Functions</b>\n\n"
            "<pre>function greet(name) {\n    return \"Hello \" + name;\n}\n\n"
            "console.log(greet(\"Sara\"));</pre>\n\n"
            "Arrow function shortcut:\n<pre>const double = (n) => n * 2;\nconsole.log(double(5));</pre>\n\n"
            "<b>Your turn:</b>\nWrite a function <code>double(n)</code> that returns n * 2. Call it.\n\n"
            "Send me your code. 👇"
        ),
        "exercise": "Write function double(n) returning n*2. Call it and log the result.",
        "rubric": "Pass if: a function named double is defined (function or arrow), returns n*2, and is called with console.log.",
        "concepts": ["functions", "return"],
    },
    {
        "id": 8, "topic": "Objects",
        "content": (
            "<b>Lesson 8 — Objects</b>\n\n"
            "Objects hold key-value pairs (like Python dicts):\n\n"
            "<pre>let person = {\n    name: \"Sara\",\n    age: 25\n};\n\n"
            "console.log(person.name);\nperson.city = \"Addis\";\nconsole.log(person);</pre>\n\n"
            "<b>Your turn:</b>\nCreate an object <code>student</code> with name, grade, subject. Print it.\n\n"
            "Send me your code. 👇"
        ),
        "exercise": "Create a student object with name, grade, subject. Log it.",
        "rubric": "Pass if: an object literal with at least 2 properties is created and logged.",
        "concepts": ["objects"],
    },
    {
        "id": 9, "topic": "Template literals",
        "content": (
            "<b>Lesson 9 — Template literals</b>\n\n"
            "Use backticks and <code>${}</code> for string formatting:\n\n"
            "<pre>let name = \"Sara\";\nlet age = 25;\n"
            "console.log(`${name} is ${age} years old`);</pre>\n\n"
            "<b>Your turn:</b>\nCreate product/price variables and use a template literal to print a sentence.\n\n"
            "Send me your code. 👇"
        ),
        "exercise": "Create variables and use a template literal with ${} to log a sentence.",
        "rubric": "Pass if: backtick template literal with ${} containing a variable is used in console.log.",
        "concepts": ["template literals", "string formatting"],
    },
    {
        "id": 10, "topic": "Array methods: map and filter",
        "content": (
            "<b>Lesson 10 — map and filter</b>\n\n"
            "<pre>let nums = [1, 2, 3, 4, 5];\n\n"
            "let doubled = nums.map(n => n * 2);\n"
            "console.log(doubled);  // [2, 4, 6, 8, 10]\n\n"
            "let evens = nums.filter(n => n % 2 === 0);\n"
            "console.log(evens);    // [2, 4]</pre>\n\n"
            "<b>Your turn:</b>\nUse <code>.map()</code> to square every number in <code>[1,2,3,4,5]</code>. Print it.\n\n"
            "Send me your code. 👇"
        ),
        "exercise": "Use .map() with arrow function to square [1,2,3,4,5]. Log result.",
        "rubric": "Pass if: .map() is called on an array with an arrow function or callback that squares, and result is logged.",
        "concepts": ["map", "arrow functions"],
    },
    {
        "id": 11, "topic": "try/catch",
        "content": (
            "<b>Lesson 11 — Error handling</b>\n\n"
            "<pre>try {\n    let result = JSON.parse(\"not json\");\n} catch (error) {\n"
            "    console.log(\"Error:\", error.message);\n}</pre>\n\n"
            "<b>Your turn:</b>\nWrite a try/catch that attempts to parse an invalid JSON string and logs the error.\n\n"
            "Send me your code. 👇"
        ),
        "exercise": "Use try/catch to catch a JSON.parse error and log the message.",
        "rubric": "Pass if: try/catch is used, JSON.parse or similar is attempted on bad input, catch logs the error.",
        "concepts": ["try/catch", "error handling"],
    },
    {
        "id": 12, "topic": "Destructuring",
        "content": (
            "<b>Lesson 12 — Destructuring</b>\n\n"
            "Pull values out of arrays/objects in one line:\n\n"
            "<pre>let [a, b, c] = [1, 2, 3];\nconsole.log(a, b);  // 1 2\n\n"
            "let {name, age} = {name: \"Sara\", age: 25};\n"
            "console.log(name);  // Sara</pre>\n\n"
            "<b>Your turn:</b>\nCreate an object and use destructuring to extract two properties. Print them.\n\n"
            "Send me your code. 👇"
        ),
        "exercise": "Create an object, destructure 2 properties into variables, log them.",
        "rubric": "Pass if: destructuring syntax ({...} = or [...] =) is used to extract values, and they are logged.",
        "concepts": ["destructuring"],
    },
    {
        "id": 13, "topic": "Promises and async/await",
        "content": (
            "<b>Lesson 13 — async/await</b>\n\n"
            "Handle tasks that take time (like fetching data):\n\n"
            "<pre>function wait(ms) {\n    return new Promise(resolve =>\n"
            "        setTimeout(resolve, ms));\n}\n\n"
            "async function main() {\n    console.log(\"Start\");\n"
            "    await wait(1000);\n    console.log(\"Done!\");\n}\n\nmain();</pre>\n\n"
            "<b>Your turn:</b>\nWrite an async function that logs \"Loading...\", waits, then logs \"Done!\".\n\n"
            "Send me your code. 👇"
        ),
        "exercise": "Write an async function that logs Loading, uses await, then logs Done.",
        "rubric": "Pass if: async function is defined, await is used, and console.log appears before and after. Accept setTimeout or Promise.",
        "concepts": ["async", "await", "Promise"],
    },
    {
        "id": 14, "topic": "Building a calculator",
        "content": (
            "<b>Lesson 14 — Calculator</b>\n\n"
            "<pre>function calc(a, b, op) {\n    switch(op) {\n"
            "        case \"+\": return a + b;\n        case \"-\": return a - b;\n"
            "        default: return \"Unknown\";\n    }\n}\n\n"
            "console.log(calc(10, 3, \"+\"));  // 13</pre>\n\n"
            "<b>Your turn:</b>\nAdd * and / operations. Call with each.\n\nSend me your code. 👇"
        ),
        "exercise": "Write a calculator function handling +, -, *, /. Call with at least 2 operations.",
        "rubric": "Pass if: a function handles 3+ operations with if/switch, returns results, and is called.",
        "concepts": ["functions", "switch/if"],
    },
    {
        "id": 15, "topic": "FizzBuzz in JavaScript",
        "content": (
            "<b>Lesson 15 — FizzBuzz!</b>\n\n"
            "The classic challenge:\n"
            "- Numbers 1-20\n- Divisible by 3: Fizz\n- Divisible by 5: Buzz\n- Both: FizzBuzz\n\n"
            "<pre>for (let i = 1; i &lt;= 20; i++) {\n"
            "    if (i % 15 === 0) console.log(\"FizzBuzz\");\n"
            "    else if (i % 3 === 0) console.log(\"Fizz\");\n"
            "    // finish it!\n}</pre>\n\n"
            "Send me your code. 👇"
        ),
        "exercise": "FizzBuzz 1-20: Fizz for 3, Buzz for 5, FizzBuzz for both.",
        "rubric": "Pass if: a loop, modulo checks for 3 and 5, FizzBuzz for combined (% 15 or both), and console.log.",
        "concepts": ["for loop", "if/else", "modulo"],
    },
]
