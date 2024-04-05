from pydantic import BaseModel
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Define request and response models
class InputData(BaseModel):
    fish_age_days: float
    fish_amount: float

class OutputData(BaseModel):
    feed_duration_seconds: float

def feedFuzzy(input_data: InputData):
    # Define fuzzy variables
    fish_age_days = ctrl.Antecedent(np.arange(0, 366, 1), 'fish_age_days')  # Fish age in days
    fish_amount = ctrl.Antecedent(np.arange(0, 101, 1), 'fish_amount')
    feed_duration = ctrl.Consequent(np.arange(0, 61, 1), 'feed_duration')  # Range from 0 to 60 seconds

    # Define membership functions for fish_age_days
    fish_age_days['young'] = fuzz.trimf(fish_age_days.universe, [0, 0, 150])  # Young fish: 0-150 days
    fish_age_days['adult'] = fuzz.trimf(fish_age_days.universe, [100, 200, 300])  # Adult fish: 100-300 days
    fish_age_days['old'] = fuzz.trimf(fish_age_days.universe, [250, 365, 365])  # Old fish: 250-365 days

    # Define membership functions for fish_amount and feed_duration (unchanged)
    fish_amount['few'] = fuzz.trimf(fish_amount.universe, [0, 0, 50])
    fish_amount['average'] = fuzz.trimf(fish_amount.universe, [20, 50, 80])
    fish_amount['many'] = fuzz.trimf(fish_amount.universe, [50, 100, 100])

    feed_duration['short'] = fuzz.trimf(feed_duration.universe, [0, 0, 20])  # Short duration: 0-20 seconds
    feed_duration['medium'] = fuzz.trimf(feed_duration.universe, [10, 30, 50])  # Medium duration: 10-50 seconds
    feed_duration['long'] = fuzz.trimf(feed_duration.universe, [40, 60, 60])  # Long duration: 40-60 seconds

    # Define fuzzy rules (unchanged)
    rule1 = ctrl.Rule(fish_age_days['young'] & fish_amount['few'], feed_duration['short'])
    rule2 = ctrl.Rule(fish_age_days['young'] & fish_amount['average'], feed_duration['medium'])
    rule3 = ctrl.Rule(fish_age_days['young'] & fish_amount['many'], feed_duration['long'])
    rule4 = ctrl.Rule(fish_age_days['adult'] & fish_amount['few'], feed_duration['short'])
    rule5 = ctrl.Rule(fish_age_days['adult'] & fish_amount['average'], feed_duration['medium'])
    rule6 = ctrl.Rule(fish_age_days['adult'] & fish_amount['many'], feed_duration['long'])
    rule7 = ctrl.Rule(fish_age_days['old'] & fish_amount['few'], feed_duration['short'])
    rule8 = ctrl.Rule(fish_age_days['old'] & fish_amount['average'], feed_duration['medium'])
    rule9 = ctrl.Rule(fish_age_days['old'] & fish_amount['many'], feed_duration['long'])

    # Create control system (unchanged)
    feeding_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
    feeding = ctrl.ControlSystemSimulation(feeding_ctrl)

    # Pass inputs to the ControlSystemSimulation
    feeding.input['fish_age_days'] = input_data.fish_age_days
    feeding.input['fish_amount'] = input_data.fish_amount

    # Crunch the numbers
    feeding.compute()

    # Output the result (feeding duration in seconds)
    feeding_duration_seconds = feeding.output['feed_duration']

    converted_duration = round(feeding_duration_seconds)
    return converted_duration