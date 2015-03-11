import os


def get_shared_cache_folder():
    home = os.path.expanduser('~/')
    return home + "Library/Application Support/EVE Online/p_drive/Local Settings/Application Data/CCP/EVE/SharedCache"


def set_shared_cache_folder(folder_path):
    pass


def get_index_path(hint):
    if os.path.exists(hint):
        return hint

    candidate = \
        "/Applications/%s/Contents/Resources/EVE Online.app/Contents/Resources/transgaming/c_drive/Program Files/CCP/EVE/resfileindex.txt" \
        % hint

    if os.path.exists(candidate):
        return candidate

    candidate = \
        "/Applications/EVE Online.app/Contents/Resources/EVE Online.app/Contents/Resources/transgaming/c_drive/Program Files/CCP/EVE/%s" \
        % hint

    if os.path.exists(candidate):
        return candidate

    return hint

