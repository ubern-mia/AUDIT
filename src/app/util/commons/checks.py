

def health_checks(selected_sets, select_feature_names: list = []):
    if len(selected_sets) == 0:
        return False, "Please, select a dataset from the left sidebar."
    elif any(k is None for k in select_feature_names):
        return False, f'Please, select an available category.'
    else:
        return True, ''
