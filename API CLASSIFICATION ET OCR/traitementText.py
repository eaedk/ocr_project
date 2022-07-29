def sup_saut(objet):
    if "\n" in objet:
        objet= objet.replace("\n", "")
    if "\f" in objet:
        objet = objet.replace("\f", "") 
    return objet 

def sup_espace(objet):
    if " " in objet:
        objet= objet.replace(" ", "")
    return objet

def modif_chiffre(resul):
    if "S" in resul :
        resul = resul.replace("S", "5")
    if "Q" in resul :
        resul = resul.replace("Q", "0")
    if "O" in resul :
        resul = resul.replace("O", "0")
    if "D" in resul :
        resul = resul.replace("D", "4")
    if "\\" in resul :
        resul = resul.replace("\\", "")
    if "I" in resul :
        resul = resul.replace("I", "1")
    if "B" in resul :
        resul = resul.replace("B", "8")
    if "Z" in resul :
        resul = resul.replace("Z", "2")
    if "T" in resul :
        resul = resul.replace("T", "7")
    if "G" in resul :
        resul = resul.replace("G", "C")
    if "E" in resul :
        resul = resul.replace("E", "8")
    if "©" in resul :
        resul = resul.replace("©", "C")
    if "¡" in resul :
        resul = resul.replace("¡", "")
    if "|" in resul :
        resul = resul.replace("|", "")
    if "]" in resul :
        resul = resul.replace("]", "")
    if "(" in resul :
        resul = resul.replace("(", "C")
    if "H" in resul :
        resul = resul.replace("H", "6")
    if ")" in resul :
        resul = resul.replace(")", "7")
    if "W" in resul :
        resul = resul.replace("W", "00")
    if "A" in resul :
        resul = resul.replace("A", "4")
    if ":" in resul :
        resul = resul.replace(":", "")
    if "/" in resul :
        resul = resul.replace("/", "")
    if "[" in resul :
        resul = resul.replace("[", "")
    if "_" in resul :
        resul = resul.replace("_", "")
    if "_" in resul :
        resul = resul.replace("_", "")
    if "," in resul :
        resul = resul.replace(",", "")
    if "." in resul :
        resul = resul.replace(".", "")
    if ":" in resul :
        resul = resul.replace(":", "")
    if "*" in resul :
        resul = resul.replace("*", "")
    if "$" in resul :
        resul = resul.replace("$", "S")
    if ";" in resul :
        resul = resul.replace(";", "")
    if "<" in resul :
        resul = resul.replace("<", "")
    if ">" in resul :
        resul = resul.replace(">", "")
    return(resul)

def modif_lettre(resul):
    if "5" in resul :
        resul = resul.replace("5", "S")
    if "1" in resul :
        resul = resul.replace("1", "I")
    if "!" in resul :
        resul = resul.replace("!", "I")
    if "4" in resul :
        resul = resul.replace("4", "D")
    if "8" in resul :
        resul = resul.replace("8", "B")
    if "\\" in resul :
        resul = resul.replace("\\", "")
    if "3" in resul :
        resul = resul.replace("3", "E")
    if "2" in resul :
        resul = resul.replace("2", "Z")
    if "7" in resul :
        resul = resul.replace("7", "T")
    if "0" in resul :
        resul = resul.replace("0", "O")
    if ":" in resul :
        resul = resul.replace(":", "")
    if "/" in resul :
        resul = resul.replace("/", "")
    if "[" in resul :
        resul = resul.replace("[", "")
    if "_" in resul :
        resul = resul.replace("_", "")
    if "_" in resul :
        resul = resul.replace("_", "")
    if "," in resul :
        resul = resul.replace(",", "")
    if "." in resul :
        resul = resul.replace(".", "")
    if ":" in resul :
        resul = resul.replace(":", "")
    if "*" in resul :
        resul = resul.replace("*", "")
    if "$" in resul :
        resul = resul.replace("$", "S")
    if ";" in resul :
        resul = resul.replace(";", "")
    if "<" in resul :
        resul = resul.replace("<", "")
    if ">" in resul :
        resul = resul.replace(">", "")
    return(resul)

def modif_visa(resul):

    if "4" in resul :
        resul = resul.replace("4", "")
    if "EE" in resul :
        resul = resul.replace("EE", "")
    if "EEE" in resul :
        resul = resul.replace("EEE", "")
    if "AA" in resul :
        resul = resul.replace("AA", "")
    if "AAA" in resul :
        resul = resul.replace("AAA", "")
    if "\f" in resul :
        resul = resul.replace("\f", "")
    if "0" in resul :
        resul = resul.replace("0", "")
    if "\\" in resul :
        resul = resul.replace("\\", "")
    if "|" in resul :
        resul = resul.replace("|", "")
    if "/" in resul :
        resul = resul.replace("/", "")
    if "|" in resul :
        resul = resul.replace("|'", "")
    if "1" in resul :
        resul = resul.replace("1", "")
    if "2" in resul :
        resul = resul.replace("2", "")
    if "3" in resul :
        resul = resul.replace("3", "")
    if "5" in resul :
        resul = resul.replace("5", "")
    if "6" in resul :
        resul = resul.replace("6", "")
    if "7" in resul :
        resul = resul.replace("7", "")
    if "8" in resul :
        resul = resul.replace("8", "")
    if "9" in resul :
        resul = resul.replace("9", "")
    if ")" in resul :
        resul = resul.replace(")", "")
    if "(" in resul :
        resul = resul.replace("(", "")
    if "_" in resul :
        resul = resul.replace("_", "")
    if "—" in resul :
        resul = resul.replace("—", "") 
    if "\"" in resul :
        resul = resul.replace("\"", "")
    if "~" in resul :
        resul = resul.replace("~", "")
    if "*" in resul :
        resul = resul.replace("*", "")
    if "—" in resul :
        resul = resul.replace("—", "") 
    if "<" in resul :
        resul = resul.replace("<", "")
    if ">" in resul :
        resul = resul.replace(">", "")
    if "," in resul :
        resul = resul.replace(",", "")
    if "." in resul :
        resul = resul.replace(".", " ")
    if "{" in resul :
        resul = resul.replace("{", "")
    if "}" in resul :
        resul = resul.replace("}", "")
    if "]" in resul :
        resul = resul.replace("]", "") 
    if "^" in resul :
        resul = resul.replace("^", "")
    if "[" in resul :
        resul = resul.replace("[", "")
    if "=" in resul :
        resul = resul.replace("=", "")
    if ":" in resul :
        resul = resul.replace(":", "")
    if ";" in resul :
        resul = resul.replace(";", "")
    if "?" in resul :
        resul = resul.replace("?", "")
    if "€" in resul :
        resul = resul.replace("€", " ")

    resul = resul.split('\n')
    return(resul)