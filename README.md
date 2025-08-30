# React Agent

A test task for an interview: a ReAct (Reasoning and Acting) agent that solves question-answering tasks by interleaving Thought, Action, and Observation steps. The agent uses tools like Wikipedia search to gather information and provide accurate answers.

## How to run 

The package has an entrypoint, so you need to install it first:

```bash
pip install .
# or install with dev dependencies.
pip install .[dev]
```

After installation set necessart environment variables and just type react-agent, it will run interactive session.

```bash
export VERTEXAI_CREDENTIALS_PATH=</path/to/vertexai/serviceaccount>
export VERTEXAI_PROJECT_ID=<project_id>
export VERTEXAI_LOCATION=<global>

react-agent
```

## How to build

The build system uses **Hatch**. To build the package:

```bash
# Install Hatch if you don't have it
pip install hatch
# or install dev dependencies.
pip install .[dev]

# Build the package
hatch build
```

## How to run tests
**Note**: No tests are currently implemented, but the testing framework is set up and ready.

Tests are run via **pytest**:

```bash
# Install pytest if you don't have it
pip install pytest
# or install dev dependencies.
pip install .[dev]

pytest
```

## Example runs
Example 1
```
Question: What type of work were Emmy Noether and David Hilbert primarily known for?
Thought 1: I need to search Emmy Noether and David Hilbert, find their primary work, then state what they were primarily known for.
Action 1: {"tool": "Wikipedia", "action": "search", "args": {"entity": "Emmy Noether"}}
Observation 1: Found page for 'Emmy Noether': Amalie Emmy Noether (23 March 1882 – 14 April 1935) was a German mathematician who made many important contributions to abstract algebra. She also proved Noether's first and second theorems, which are fundamental in mathematical physics. Noether was described by Pavel Alexandrov, Albert Einstein, Jean Dieudonné, Hermann Weyl, and Norbert Wiener as the most important woman in the history of mathematics. As one of the leading mathematicians of her time, she developed theories of rings, fields, and algebras. In physics, Noether's theorem explains the connection between symmetry and conservation laws. Noether was born to a Jewish family in the Franconian town of Erlangen; her father was the mathematician Max Noether. She originally planned to teach French and English after passing the required...
Thought 2: : Emmy Noether was primarily known for her work in mathematics, specifically abstract algebra and mathematical physics. Now I need to search for David Hilbert to find his primary work.
Action 2: {"tool": "Wikipedia", "action": "search", "args": {"entity": "David Hilbert"}}
Observation 2: Found page for 'David Hilbert': David Hilbert  (; German: [ˈdaːvɪt ˈhɪlbɐt]; 23 January 1862 – 14 February 1943) was a German mathematician and philosopher of mathematics and one of the most influential mathematicians of his time. Hilbert discovered and developed a broad range of fundamental ideas including invariant theory, the calculus of variations, commutative algebra, algebraic number theory, the foundations of geometry, spectral theory of operators and its application to integral equations, mathematical physics, and the foundations of mathematics (particularly proof theory). He adopted and defended Georg Cantor's set theory and transfinite numbers. In 1900, he presented a collection of problems that set a course for mathematical research of the 20th century. Hilbert and his students contributed to establishing rigo...
Action 3: {"tool": "Finish", "action": "submit_answer", "args": {"text": "Mathematics, particularly abstract algebra and mathematical physics."}}
Observation 3: Mathematics, particularly abstract algebra and mathematical physics.
Answer: Mathematics, particularly abstract algebra and mathematical physics.
```

Example 2
```
Question: Which Nobel Prize-winning physicist developed the theory of photoelectric effect?
Thought 1: I need to find out which Nobel Prize-winning physicist developed the theory of the photoelectric effect. I will start by searching for "photoelectric effect" on Wikipedia.
Action 1: {"tool": "Wikipedia", "action": "search", "args": {"entity": "photoelectric effect"}}
Observation 1: Found page for 'photoelectric effect': The photoelectric effect is the emission of electrons from a material caused by electromagnetic radiation such as ultraviolet light. Electrons emitted in this manner are called photoelectrons. The phenomenon is studied in condensed matter physics, solid state, and quantum chemistry to draw inferences about the properties of atoms, molecules and solids. The effect has found use in electronic devices specialized for light detection and precisely timed electron emission. The experimental results disagree with classical electromagnetism, which predicts that continuous light waves transfer energy to electrons, which would then be emitted when they accumulate enough energy. An alteration in the intensity of light would theoretically change the kinetic energy of the emitted electrons, with suffic...
Thought 2: : The current page describes the photoelectric effect but doesn't explicitly state who developed the theory or won a Nobel Prize for it. I should look for keywords like "Nobel Prize" or "theory" within this page to find the relevant information.
Action 2: {"tool": "Wikipedia", "action": "lookup", "args": {"keyword": "Nobel Prize"}}
Observation 2: (Result 1 / 3) ...e Planck constant from the photoelectric effect supported Einstein's model, even though a corpuscular theory of light was for Millikan, at the time, "quite unthinkable". Einstein was awarded the 1921 Nobel Prize in Physics for "his discovery of the law of the photoelectric effect", and Millikan was awarded the Nobel Prize in 1923 for "his work on the elementary charge of electricity and on the photoelectric...
(Result 2 / 3) ...light was for Millikan, at the time, "quite unthinkable". Einstein was awarded the 1921 Nobel Prize in Physics for "his discovery of the law of the photoelectric effect", and Millikan was awarded the Nobel Prize in 1923 for "his work on the elementary charge of electricity and on the photoelectric effect". In quantum perturbation theory of atoms and solids acted upon by electromagnetic radiation, the photoel...
(Result 3 / 3) ...rocess. However, a seminal role in this field was played by experimental techniques on attosecond generation of pulses of light for studies on electron dynamics, which was recognised through the 2023 Nobel Prize in physics to Pierre Agostini, Ferenc Krausz and Anne L’Huillier. For example, in 2010, it was discovered that electron emission takes 20 attoseconds and that photoemission is associated with complex...
Action 3: {"tool": "Finish", "action": "submit_answer", "args": {"text": "Albert Einstein"}}
Observation 3: Albert Einstein
Answer: Albert Einstein
```

## Explanation Notes
- To not just copy a propmts from the resarch papaer code, and also to make toolest more verstile I decided to change action names to json, But I understand that it will add cost becuse (,[]{}:) will be counted as tokens. So in production maybe it necessary to think about more compact string representation of the tools, and create conversion mechanism.
- I decided to support both HotpotQA questions and FEVER fact checkickg style questions. (Actually not have time to implement FEVER).
- For now I don't know what is prefferd type to pass tools json to the llm, for example it's good to pass it like its done for now, or maybe have generic commands, like for example search, and list all search tools in the strentgs togheter, or instruction to the lllm to use more apporite tool would be enough no matter of tool list order, furhter reserach needed.
- As I understand in more complex sceniaors you can create a like a Controller/Manager Agent which will delegate tasks to its sub agents to achive a sub goals.
- Tools should be stateless, agent manages sessions. Current implementation uses internal caching for development simplicity.
- Use pydantic models to validate actions responses from the llm client in the take_action method of a tool.
- In the production I will use async generate_content method.

## Extension (Optional)
- Add memory to your agent so it can reference past queries and answers.
- Implement a more sophisticated search mechanism that retrieves actual information from a knowledge base.
- Extend the action space with additional capabilities such as mathematical calculations.

### Extensions Implementation Notes

**Memory**: I think we can vectorize and store previous queries and answers in a database, allowing the agent to perform semantic search and retrieve relevant information for the current context.

**Knowledge base.**: Again integrate with vector databases. However, collecting documents from the internet and creating embeddings is time-consuming. Alternative approach: implement dynamic database updates based on user queries. When a user retrieves a Wikipedia page, save it in the database for faster future responses. This creates a growing knowledge base organically from actual user interactions.

**Mathematical Calculations**: 
- **Option 1**: Create a Calculator tool with actions like `add`, `subtract`, `multiply`, `divide`, etc. This provides controlled, safe mathematical operations with predefined functions.
- **Option 2**: Ask LLM to generate Python expressions, then sanitize and evaluate them using `ast.literal_eval()`. This requires careful input validation and security measures to prevent code injection.
