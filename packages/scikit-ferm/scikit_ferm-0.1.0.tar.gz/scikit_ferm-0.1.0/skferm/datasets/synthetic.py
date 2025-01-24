from skferm.growth_models.logistic import logistic_growth
import numpy as np

def generate_synthetic_growth(time, model="logistic", noise_std=0.0, **kwargs):
    """
    Generate synthetic growth data using specified growth model.
    
    Parameters:
    - time (array-like): Time points.
    - model (str): Growth model to use ("logistic", "monod", etc.).
    - noise_std (float): Standard deviation of Gaussian noise to add.
    - **kwargs: Parameters for the growth model.
    
    Returns:
    - dict: A dictionary with time and population arrays.
    """
    if model == "logistic":
        growth_function = logistic_growth
    else:
        raise ValueError(f"Unsupported model: {model}")

    population = growth_function(time, **kwargs)
    noise = np.random.normal(0, noise_std, size=len(population))
    return {"time": time, "population": population + noise}