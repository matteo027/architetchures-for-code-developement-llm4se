from typing import List

            def parse_nested_parens(paren_string: str) -> List[int]:
                if not paren_string.replace(" ", ""):
                    raise ValueError("Invalid input string")
                
                stack = []
                max_depths = []
                current_depth = 0
                
                for char in paren_string:
                    if char == '(':
                        stack.append(char)
                        current_depth += 1
                        if current_depth > max_depths:
                            max_depths.append(current_depth)
                    elif char == ')':
                        stack.pop()
                        current_depth -= 1
                
                return max_depths