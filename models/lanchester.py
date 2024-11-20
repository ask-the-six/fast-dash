# lanchester.py

import pandas as pd
from typing import Optional, Dict, Any


class LanchesterModel:
    """
    A class to simulate Lanchester's linear and square combat models.
    
    Attributes:
        x0 (float): Initial number of units for Force X.
        y0 (float): Initial number of units for Force Y.
        D (float): Attrition rate constant for Force Y's effect on Force X.
        A (float): Attrition rate constant for Force X's effect on Force Y.
        model (str): The combat model to use ('linear' or 'square').
        time_step (float): The time increment for the simulation.
        max_steps (int): Maximum number of steps for the simulation.
        stopping_condition (str): Condition to stop the simulation ('defeat' or 'attrition').
        attrition_threshold (float): Percentage of initial force at which to stop (for 'attrition' condition).
        data (pd.DataFrame): DataFrame containing simulation results.
    """

    def __init__(
        self,
        x0: float = 150,
        y0: float = 160,
        D: float = 0.02,
        A: float = 0.01,
        model: str = 'linear',
        time_step: float = 0.1,
        max_steps: int = 1000,
        stopping_condition: str = 'defeat',
        attrition_threshold: float = 30.0
    ):
        """
        Initializes the LanchesterModel instance with provided parameters.

        Args:
            x0 (float): Initial number of units for Force X.
            y0 (float): Initial number of units for Force Y.
            D (float): Attrition rate constant for Force Y's effect on Force X.
            A (float): Attrition rate constant for Force X's effect on Force Y.
            model (str, optional): The combat model to use ('linear' or 'square'). Defaults to 'linear'.
            time_step (float, optional): The time increment for the simulation. Defaults to 0.1.
            max_steps (int, optional): Maximum number of steps for the simulation. Defaults to 1000.
            stopping_condition (str, optional): Condition to stop the simulation ('defeat' or 'attrition'). Defaults to 'defeat'.
            attrition_threshold (float, optional): Percentage of initial force at which to stop (for 'attrition' condition). Defaults to 30.0.
        """
        self.x0 = x0
        self.y0 = y0
        self.D = D
        self.A = A
        self.model = model.lower()
        self.time_step = time_step
        self.max_steps = max_steps
        self.stopping_condition = stopping_condition.lower()
        self.attrition_threshold = attrition_threshold
        self.data: Optional[pd.DataFrame] = None

        self.validate_parameters()

    def validate_parameters(self):
        """Validates initial parameters to ensure they are within acceptable ranges."""
        if self.model not in ('linear', 'square'):
            raise ValueError("Model must be either 'linear' or 'square'")
        if self.stopping_condition not in ('defeat', 'attrition'):
            raise ValueError("Stopping condition must be either 'defeat' or 'attrition'")
        if self.x0 <= 0 or self.y0 <= 0:
            raise ValueError("Initial forces must be positive numbers")
        if self.D < 0 or self.A < 0:
            raise ValueError("Attrition rates must be non-negative")
        if self.time_step <= 0:
            raise ValueError("Time step must be a positive number")
        if self.max_steps <= 0:
            raise ValueError("Max steps must be a positive integer")
        if self.stopping_condition == 'attrition' and not (0 < self.attrition_threshold < 100):
            raise ValueError("Attrition threshold must be between 0 and 100")

    def run_simulation(self):
        """
        Runs the combat simulation based on the initialized parameters.

        Populates the 'data' attribute with a pandas DataFrame containing the simulation results.
        """
        records = []

        x = self.x0
        y = self.y0

        records.append({'Step': 0, 'Force X': x, 'Force Y': y})

        for step in range(1, self.max_steps + 1):
            if self.model == 'linear':
                dx = -self.D * y * self.time_step
                dy = -self.A * x * self.time_step
            elif self.model == 'square':
                dx = -self.D * x * y * self.time_step
                dy = -self.A * x * y * self.time_step

            x = max(x + dx, 0)
            y = max(y + dy, 0)

            records.append({'Step': step, 'Force X': x, 'Force Y': y})

            # Check stopping conditions
            if self.stopping_condition == 'defeat':
                if x <= 0 or y <= 0:
                    break
            elif self.stopping_condition == 'attrition':
                x_attrition = (1 - (x / self.x0)) * 100
                y_attrition = (1 - (y / self.y0)) * 100
                if x_attrition >= self.attrition_threshold or y_attrition >= self.attrition_threshold:
                    break

        self.data = pd.DataFrame.from_records(records)

    def get_results(self) -> pd.DataFrame:
        """
        Retrieves the simulation results.

        Returns:
            pd.DataFrame: DataFrame containing the simulation steps and force levels.
        """
        if self.data is None:
            raise RuntimeError("Simulation has not been run yet. Call 'run_simulation()' first.")
        return self.data

    def get_summary(self) -> Dict[str, Any]:
        """
        Provides a summary of the simulation results, including final force levels and the winner.

        Returns:
            Dict[str, Any]: A dictionary containing summary statistics.
        """
        if self.data is None:
            raise RuntimeError("Simulation has not been run yet. Call 'run_simulation()' first.")

        final_force_x = self.data['Force X'].iloc[-1]
        final_force_y = self.data['Force Y'].iloc[-1]

        if final_force_x > final_force_y:
            winner = 'Force X'
        elif final_force_y > final_force_x:
            winner = 'Force Y'
        else:
            winner = 'Tie'

        x_attrition = (1 - (final_force_x / self.x0)) * 100
        y_attrition = (1 - (final_force_y / self.y0)) * 100

        summary = {
            'Final Force X': final_force_x,
            'Final Force Y': final_force_y,
            'Force X Attrition (%)': x_attrition,
            'Force Y Attrition (%)': y_attrition,
            'Winner': winner
        }

        return summary

    def reset(self):
        """
        Resets the simulation data, allowing the model to be run again.
        """
        self.data = None