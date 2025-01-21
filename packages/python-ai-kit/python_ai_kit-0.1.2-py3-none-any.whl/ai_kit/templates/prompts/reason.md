---
name: reason
description: Generate a reasoned response using AI
args:
  - prompt
---

# Using the reasoning script

There are a few situations when you should use an external LLM to reason about
a problem.

You have access to a script with `aik run reason [prompt]` that will connect
to an external LLM to reason about a problem and return you an answer.


**when to use reasoning**

- there is a highly tecnical and complex problem to solve

- you need to reason about a problem

- you need to plan or orchestrate

- you have tried to debug a problem and need to reason about the solution


**when not to use reasoning**

- there is a simple problem to solve

- you know the answer to the problem already

- you havent tried any solutions yet and the problem is not notably complex

