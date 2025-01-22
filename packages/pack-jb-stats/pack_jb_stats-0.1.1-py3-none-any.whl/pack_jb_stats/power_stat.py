import math
import scipy.stats as stats

# Définition de la fonction de calcul
def power_stat(effect_size, control_group_rate, proportion_treated, alpha):
    power = 0.8
    effect_size = effect_size / 100
    base1 = ((effect_size + control_group_rate) * (1 - (effect_size + control_group_rate)) / proportion_treated)
    base2 = (control_group_rate * (1 - control_group_rate) / (1 - proportion_treated))
    
    full_base = base1 + base2
    
    alpha_2 = stats.norm.ppf(alpha / 2)
    power_2 = stats.norm.ppf(1 - power)
    
    normal_term = (alpha_2 + power_2) ** 2
    
    result = full_base * normal_term * (1 / (effect_size ** 2))
    
    sample_size_control = result * (1 - proportion_treated)
    sample_size_treated = result * proportion_treated
    
    result = math.ceil(result)
    sample_size_treated = math.ceil(sample_size_treated)
    sample_size_control = math.ceil(sample_size_control)
    
    return result, sample_size_control, sample_size_treated

# Définition de la fonction principale
def processus_power_stat():
    try:
        effect_size = float(input("Veuillez entrer la taille de l'impact attendu (impact de deux points -> 2) : "))
        control_group_rate = float(input("Veuillez entrer le niveau de base de l'indicateur de résultat : "))
        proportion_treated = float(input("Veuillez entrer la part de la population totale que vous souhaitez traiter : "))
        alpha = float(input("Veuillez entrer le niveau de significativité (95% -> 0.05, 90% -> 0.1): "))
        
        # Appeler la fonction avec les valeurs fournies
        result, sample_size_control, sample_size_treated = power_stat(effect_size, control_group_rate, proportion_treated, alpha)
        
        print()
        print(f"La taille totale de l'échantillon nécessaire est : {result} observations")
        print(f"Avec une taille du groupe contrôle de : {sample_size_control} observations")
        print(f"Avec une taille du groupe traité de : {sample_size_treated} observations")
    
    except ValueError:
        print("Veuillez entrer des valeurs numériques valides.")
