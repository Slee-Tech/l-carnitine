## About

---

L-Carnitine is an interpreted language written in Python. It is a mix of extremely verbose and cryptic. The SLY libary was utilized to write the lexer and parser, which you can learn more about [here](https://sly.readthedocs.io/en/latest/sly.html).

## Examples

---

The following shows a "Hello World" example with L-Carnitine.

````
PrintToCLI <( ```Goodbye, cruel world.``` >) %%
````

The `PrintToClI` function is used for printing. The `<(` and `>)` act like parenthesis in other languages. Strings are wrapped in \`\`\` (triple backticks). The `%%` act like commas.

### Variables

---

```
The following variable: x Is assigned the following value of: 8 %%
PrintToCLI <( x >) %%
```

A variable is declared using `The following variable:` keyword, followed by the variable name (x in this case). You assign a value to variable using the keyword `Is assigned the following value of:`, followd by the value, and ending the statement with `%%`. The sample above creates a variable x, assigns it a value of 8, then prints it.

### Conditionals

---

````
If is is the case that: <( x Is greater than or equal to: y >)
    <@
        PrintToCLI <( ```Yes.``` >) %%
    >@ %%
````

A conditional statement is performed using the above syntax. It begins with `If is is the case that:` to begin the statement, followed by the condition, which is wrapped in `<(` `>)`. In this case the condition is checking if a variable x is greater than a variable y, using the keyword `Is greater than or equal to:`. Other binary operations follow a similar syntax and can be found in lexer.py. In the above example, if the condition is true, `Yes` is printed.

### Functions

---

Functions in L-Carnitine can be created using the following syntax.

```
Perform the procedure: testFunctionArgs<( test >)
    <@
        Return the value of: test + 2 %%
    >@
```

The `Perform the procedure:` keyword begins function declaration, followed by the name of the function, `testFunctionArgs` in this case, followed by opitional parameters which are enclosed in `<(` `>)`. The above function takes one parameter called `test`. The body of the function is wrapped in `<@` `>@`, which contains one or more statements. In the above example, the function returns the value of the parameter `test` + 2, using the keyword `Return the value of:`.

```
The following variable: atest Is assigned the following value of: testFunctionArgs<( ftest >) %%
PrintToCLI <( atest >) %%
```

The example above calls the function by calling the name, and passing in an argument of previously defined variable `ftest`, and assigns the result to a variable `atest`, then prints out the value.

### Running a program

---

To run an L-Carnitine program, you must write and save your code in a file with a `.lcarn` extension. Then call

```
python main.py yourprogram.lcarn
```

to execute it. You will need to have SLY installed, which your can with

```
pip install requirements.txt
```

You can find more examples in `test.lcarn`.
