from django.template import Library


register = Library()

@register.filter
def model_type(value):
    """
    Renvoie le nom du type du modèle.
    Args: value: La valeur du modèle.
    Returns: str: Le nom du type du modèle.
    """
    return type(value).__name__

@register.filter(name='range')
def filter_range(start, end):
    """
    Génère une séquence de nombres dans une plage donnée.
    Args: start: Le nombre de départ de la séquence.
            end: Le nombre de fin de la séquence.
    Returns: range: La séquence de nombres dans la plage spécifiée.
    """
    if isinstance(end, str):
        end_nb = int(end)
    else:
        end_nb = end
    return range(start, end_nb)

@register.filter(name='get_range')
def get_range(value):
    """
    Génère une séquence de nombres de 0 à la valeur spécifiée.
    Args: value: La valeur de fin de la séquence.
    Returns: range: La séquence de nombres de 0 à la valeur spécifiée.
    """
    return range(value)

@register.filter(name='get_complement_range')
def get_complement_range(value):
    """
    Génère une séquence de nombres de la différence entre 5 et la valeur spécifiée.
    Args: value: La valeur pour laquelle on souhaite obtenir la différence avec 5.
    Returns: range: La séquence de nombres de la différence entre 5 et la valeur spécifiée.
    """
    return range(5 - value)

@register.filter
def add_class(field, css_class):
    """
    Ajoute une classe CSS au champ du formulaire.
    Args: field: Le champ du formulaire.
          css_class: La classe CSS à ajouter.
    Returns: str: Le champ du formulaire avec la classe CSS ajoutée.
    """
    return field.as_widget(attrs={'class': css_class})
