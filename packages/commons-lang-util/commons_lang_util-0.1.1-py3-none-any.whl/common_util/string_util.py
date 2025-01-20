def split(s, separator):
    if s is None: return []
    s = s.strip()
    if s == "": return []
    return s.split(separator)
