# Import necessary libraries
            import numpy as np
            from scipy.optimize import minimize

            # Define the objective function
            def objective_function(x):
                """
                Calculate the value of the objective function.

                Args:
                    x: A list containing two elements [x0, x1].

                Returns:
                    The value of the objective function at point x.
                """
                return x[0]**2 + x[1]**2

            # Define the constraint function
            def constraint_function(x):
                """
                Calculate the value of the constraint function.

                Args:
                    x: A list containing two elements [x0, x1].

                Returns:
                    The value of the constraint function at point x.
                """
                return x[0] - 2*x[1]

            # Define the bounds for the variables
            bounds = [(0, None), (None, None)]

            # Perform the minimization using SLSQP method
            result = minimize(objective_function, [1, 1], method='SLSQP', bounds=bounds,
                            constraints={'type': 'eq', 'fun': constraint_function})

            # Print the results
            print(result)