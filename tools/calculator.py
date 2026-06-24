from langchain_core.tools import tool

@tool
def calculator(expression: str) -> str:
    """Useful for mathematical calculations. Provide the math expression as a string."""
    try:
        # We restrict the environment to just math operations for safety
        allowed_names = {"abs": abs, "round": round, "min": min, "max": max, "pow": pow}
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return f"The result is: {result}"
    except Exception as e:
        return f"Error evaluating expression: {e}"