def calculate_matiere_stats(data_school):
    """
    Calculer les stats de chaque matière pour une établissement
    """
    matiere_note_stats = data_school.groupby("matière").agg(
        {"G3": ["mean", "min", "max", "median"]}
    )
    matiere_note_stats.index = matiere_note_stats.index.map(
        {"mat": "Mathématiques", "por": "Portugais"}
    )
    matiere_note_stats.columns = ["Moyenne", "Min", "Max", "Médiane"]
    #matiere_note_stats = matiere_note_stats.applymap(lambda note:f"{note:.1f}")
    return matiere_note_stats
