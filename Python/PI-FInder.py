# ========================================== CLASSES ========================================== #
class minterm:
    def __init__(self, id, numOfVariables):
        self.id = [id]
        self.binary = bin(id)[2:].zfill(numOfVariables)
        self.group = self.binary.count('1')
        self.flag = False

    def __str__(self):
        return f"{','.join(str(i) for i in self.id)}: {self.binary}"


# ========================================== FUNCTIONS ========================================== #

def vars_generator(numOfVariables):
    vars = []
    for i in range(numOfVariables):
        vars.append(chr(ord('A') + i)) #chr betconvert el unicode integer into a character
    return vars

def combine_terms(mintermsList):
    groups = {} #key -> grp num, value -> list of terms in that group

    for term in mintermsList:
        group = term.group
        if group not in groups:
            groups[group] = []
        groups[group].append(term)
    
    combinedTerms = [] 
    groupNumbers = sorted(groups.keys())

    for i in range(len(groupNumbers) - 1):
        groupA = groups[groupNumbers[i]]
        groupB = groups[groupNumbers[i + 1]]

        for term1 in groupA:
            for term2 in groupB:
                diffCount = 0
                newBinary = ""
                for b1, b2 in zip(term1.binary, term2.binary):
                    if b1 != b2:
                        if b1 == '-' or b2 == '-':
                            diffCount = 2 
                            break
                        diffCount += 1
                        newBinary += '-'
                    else:
                        newBinary += b1

                if diffCount == 1:
                    new_ids = []
                    for id in term1.id:
                        if id not in new_ids:
                            new_ids.append(id)
                    for id in term2.id:
                        if id not in new_ids:
                            new_ids.append(id)

                    new_term = minterm(0, len(newBinary)) 
                    new_term.id = sorted(new_ids)
                    new_term.binary = newBinary
                    new_term.group = newBinary.count('1')
                    new_term.flag = False

                    combinedTerms.append(new_term)
                    term1.flag = True
                    term2.flag = True

    return combinedTerms

def find_PIs_and_EPIs(mintermList, dontcareList):
    PIs = []
    currentTerms = mintermList + dontcareList

    while True:
        combined = combine_terms(currentTerms)

        for term in currentTerms:
            if not term.flag:
                already_included = False
                for existing in PIs:
                    if term.id == existing.id and term.binary == existing.binary:
                        already_included = True
                        break
                if not already_included:
                    PIs.append(term)

        if not combined:
            break

        currentTerms = combined

    minterm_to_implicants = {} #key -> minterm id from original mintermsList, values -> id of prime implicants that contain that minterm
    for minterm in mintermList:
        for pi in PIs:
            if minterm.id[0] in pi.id:
                minterm_to_implicants[minterm.id[0]] = minterm_to_implicants.get(minterm.id[0], [])
                minterm_to_implicants[minterm.id[0]].append(pi)

    minterm_to_implicants_copy = {k: v[:] for k, v in minterm_to_implicants.items()}

    EPIs = []
    for minterm_id, implicants in minterm_to_implicants.items():
        if len(implicants) == 1:
            epi = implicants[0]
            if epi not in EPIs:
                EPIs.append(epi)


    equation = []
    for epi in EPIs:
        if epi not in equation:
            equation.append(epi)

    minterm_to_implicants_copy = {k: v[:] for k, v in minterm_to_implicants.items()}

    for covered in epi.id:
        if covered in minterm_to_implicants_copy:
            del minterm_to_implicants_copy[covered]

    while minterm_to_implicants_copy:
        pi_coverage = {} # key-> PI, value-> set of minterm ids
        for minterm_id, implicants in minterm_to_implicants_copy.items():
            for pi in implicants:
                pi_coverage[pi] = pi_coverage.get(pi, set())
                pi_coverage[pi].add(minterm_id)
    
        best_pi = max(pi_coverage, key=lambda pi: len(pi_coverage[pi]))
        if best_pi not in equation:
            equation.append(best_pi)

        for covered in best_pi.id:
            if covered in minterm_to_implicants_copy:
                del minterm_to_implicants_copy[covered]

    return PIs, EPIs, equation

def convert_to_variables(implicants, varNames):
    result = []
    for imp in implicants:
        term = ''
        for idx, val in enumerate(imp.binary):
            if val == '1':
                term += varNames[idx]
            elif val == '0':
                term += varNames[idx] + "'"
            
        result.append(term if term else '1')
    return result

# ========================================== EXTRA FUNCTIONS ========================================== #
def SOP_to_minterms(terms, vars): #convert fubction in terms of a & a' to a list that's the sum of minterms
    all_minterms = []

    for term in terms: #loop over all terms 
        fixed = {}

        i = 0
        while i<len(term):
            var = term[i]
            if i + 1 < len(term) and term[i + 1] == "'":
               fixed[var] = 0 #complements
               i += 2 #term and the ' after it
            else:
                fixed[var] = 1  
                i += 1 
        
        missing = [v for v in vars if v not in fixed]

        def generate_combos(n): #for the missing variables, create all possible combinations
            combos = []
            for i in range(2 ** n):
                combo = []
                for j in range(n - 1, -1, -1):
                    combo.append((i >> j) & 1)
                combos.append(combo) #list of list of ones and zeors lol
            return combos
        
        combos = generate_combos(len(missing)) # call the function for the variables missing in this particular term el e7na feeh

        for combo in combos: #loop over kol el combos
            full_binary = []
            combo_index = 0
            for v in vars: #loop over kol el vars
                if v in fixed: #law howa already in the list of variables, add it 3ala tool
                    full_binary.append(fixed[v])
                else:
                    full_binary.append(combo[combo_index]) #otherwise add the combo
                    combo_index += 1

            minterm = 0
            for bit in full_binary:
                minterm = (minterm << 1) | bit  # Left shift and add bit to build the binary number
            all_minterms.append(minterm)

    return sorted(set(all_minterms))

def maxterms_to_minterms(maxterms, numOfVariables):
    minterms = []
    total_terms = 2 ** numOfVariables

    for term in range(total_terms):
        if term not in maxterms:
            minterms.append(term)

    return minterms

# ========================================== UTILITY FUNCTIONS ========================================== #
def colorprint(text, color=None, *args):
    """
    Prints colored text to the terminal. Color options: 'G', 'Y', 'R', 'O', 'B', 'T', 'r'.
    """
    color_codes = {
        'G': '\033[32m',  # Green
        'Y': '\033[33m',  # Yellow
        'R': '\033[31m',  # Red
        'O': '\033[38;2;255;103;0m',  # Orange
        'B': '\033[94m',  # Blue
        'T': '\033[96m',  # Turquoise
        'r': '\033[91m',  # Pinkish-red
        None: '\033[0m'   # Reset
    }
    code = color_codes.get(color, '\033[0m')
    print(code + (text % args if args else text) + '\033[0m', end='')

def get_ordinal(n):
    m = n % 10
    tens = (n // 10) % 10
    if tens == 1:
        return 'th'
    if m == 1:
        return 'st'
    if m == 2:
        return 'nd'
    if m == 3:
        return 'rd'
    return 'th'

# ========================================== MAIN FUNCTION ========================================== #
def main():
    inputError = False
    while True:
        colorprint("<Mohsen Amr - 9655>\n", 'T')
        colorprint("Digital Logic Circuits 1", 'B')
        colorprint("\t\t[Quine McClusky PI & EPI Finder]\n\n", 'B')

        if inputError:
            colorprint("Input must be an integer between 1 and 26\n", 'R')
        colorprint("Enter the number of variables (1-26): ", 'Y')

        numOfVars = input().strip()

        if not numOfVars.isdigit():
            inputError = True
            continue

        numOfVars = int(numOfVars)
        if 1 <= numOfVars <= 26:
            break
        else:
            inputError = True
            continue

    varNames = vars_generator(numOfVars)
    colorprint(f"\nF({', '.join(varNames)})\n\n", 'O')

    colorprint("Function input forms:\n", 'O')
    print("1] F = \u03A3m(...) + \u03A3d(...) (summation of minterms + don't care values)\n2] F = \u03A0M(...) (product of maxterms)\n3] F = ... + ... (sum of product form)\n")

    inputError = False
    while True:
        if inputError:
            colorprint("Invalid choice. Please enter 1, 2, or 3.\n", 'R')
        colorprint("Choose input form (1,2 or 3): ", 'Y')
        choice = input().strip()
        if choice in ['1', '2', '3']:
            break
        else:
            inputError = True

    colorprint("\n\n\n\n<Mohsen Amr - 9655>\n", 'T')
    colorprint("Digital Logic Circuits 1", 'B')
    colorprint("\t\t[Quine McClusky PI & EPI Finder]\n\n", 'B')

    minterms = []
    dontcares = []
    if choice == '1':
        colorprint(f"F({', '.join(varNames)}) = Σm(...) + \u03A3d(...) (summation of minterms + don't care values)\n", 'G')
        max_minterm = 2 ** numOfVars - 1
        colorprint(f"Minterms in range (0-{max_minterm}). Enter -1 to stop.\n", 'O')
        inputError = False
        while True:
            if inputError:
                colorprint(f"Invalid input. Please enter an integer between 0 and {max_minterm}, or -1 to stop.\n", 'R')
            colorprint(f"Enter {len(minterms)+1}{get_ordinal(len(minterms)+1)} minterm: ", 'Y')
            user_input = input().strip()
            if user_input == '-1':
                break
            if not user_input.isdigit():
                inputError = True
                continue
            m_value = int(user_input)
            if 0 <= m_value <= max_minterm:
                if m_value not in minterms:
                    minterms.append(m_value)
                    inputError = False
                else:
                    colorprint("Minterm already entered.\n", 'R')
            else:
                inputError = True

        colorprint(f"\nDon't care values in range (0-{max_minterm}). Enter -1 to stop.\n", 'O')
        inputError = False
        while True:
            if inputError:
                colorprint(f"Invalid input. Please enter an integer between 0 and {max_minterm}, or -1 to stop.\n", 'R')
            colorprint(f"Enter {len(dontcares)+1}{get_ordinal(len(dontcares)+1)} don't care value: ", 'Y')
            user_input = input().strip()
            if user_input == '-1':
                break
            if not user_input.isdigit():
                inputError = True
                continue
            d_value = int(user_input)
            if 0 <= d_value <= max_minterm:
                if d_value not in dontcares and d_value not in minterms:
                    dontcares.append(d_value)
                    inputError = False
                elif d_value in minterms:
                    colorprint("Value already entered as a minterm.\n", 'R')
                else:
                    colorprint("Don't care value already entered.\n", 'R')
            else:
                inputError = True

        minterms = sorted(minterms)
        dontcares = sorted(dontcares)
    
    elif choice == '2':
        colorprint(f"F({', '.join(varNames)}) = Πm(...) (product of maxterms)\n", 'G')
        maxterms = []
        max_maxterm = 2 ** numOfVars - 1
        colorprint(f"Maxterms in range (0-{max_maxterm}). Enter -1 to stop.\n", 'O')
        inputError = False
        while True:
            if inputError:
                colorprint(f"Invalid input. Please enter an integer between 0 and {max_maxterm}, or -1 to stop.\n", 'R')
            colorprint(f"Enter {len(maxterms)+1}{get_ordinal(len(maxterms)+1)} maxterm: ", 'Y')
            user_input = input().strip()
            if user_input == '-1':
                break
            if not user_input.isdigit():
                inputError = True
                continue
            maxterm = int(user_input)
            if 0 <= maxterm <= max_maxterm:
                if maxterm not in maxterms:
                    maxterms.append(maxterm)
                    inputError = False
                else:
                    colorprint("Maxterm already entered.\n", 'R')
            else:
                inputError = True

        maxterms = sorted(maxterms)
        minterms = maxterms_to_minterms(maxterms, numOfVars)
        
    elif choice == '3':
        colorprint(f"F({', '.join(varNames)}) = ... + ... (sum of product form)\n", 'G')
        sop_terms = []
        colorprint(f"Enter product terms using variables {', '.join(varNames)}. For complement, use a single quote (e.g., A'). Enter an empty line to stop.\n", 'O')
        inputError = False
        while True:
            if inputError:
                colorprint(f"Invalid input. Use only variables {', '.join(varNames)} optionally followed by a single quote for complement.\n", 'R')
            colorprint(f"Enter {len(sop_terms)+1}{get_ordinal(len(sop_terms)+1)} product term: ", 'Y')
            user_input = input().strip()
            if user_input == '':
                break
            term = user_input.replace(" ", "").upper()
            valid = True
            i = 0
            while i < len(term):
                if term[i] not in varNames:
                    valid = False
                    break
                i += 1
                if i < len(term) and term[i] == "'":
                    i += 1
            if valid and term:
                duplicate = False
                for existing in sop_terms:
                    if existing == term:
                        duplicate = True
                        break
                if duplicate:
                    colorprint("Product term already entered.\n", 'R')
                    inputError = False
                else:
                    sop_terms.append(term)
                    inputError = False
            else:
                inputError = True
        
        minterms = sorted(SOP_to_minterms(sop_terms, varNames))

    minterms = [minterm(m, numOfVars) for m in minterms]
    dontcares = [minterm(m, numOfVars) for m in dontcares]

    PIs, EPIs, equation = find_PIs_and_EPIs(minterms, dontcares)
    PIs = convert_to_variables(PIs, varNames)
    EPIs = convert_to_variables(EPIs, varNames)
    equation = convert_to_variables(equation, varNames)

    colorprint("\n\n\n\n<Mohsen Amr - 9655>\n", 'T')
    colorprint("Digital Logic Circuits 1", 'B')
    colorprint("\t\t[Quine McClusky PI & EPI Finder]\n\n", 'B')

    if choice == '2':
        colorprint(f"F({', '.join(varNames)}) = Πm(", 'O')
        for i, m in enumerate(maxterms):
            colorprint(str(m), None)
            if i != len(maxterms) - 1:
                colorprint(", ", 'O')
        colorprint(")\n", 'O')
    elif choice == '3':
        colorprint(f"F({', '.join(varNames)}) = ", 'O')
        for i, term in enumerate(sop_terms):
            for v in term:
                colorprint(v, None)
            if i != len(sop_terms) - 1:
                colorprint(" + ", 'O')
        colorprint("\n", 'O')

    colorprint(f"F({', '.join(varNames)}) = Σm(", 'O')
    for i, m in enumerate(sorted([mt.id[0] for mt in minterms])):
        colorprint(str(m), None)
        if i != len(minterms) - 1:
            colorprint(", ", 'O')
    colorprint(")", 'O')

    if choice == '1' and dontcares:
        colorprint(f" + Σd(", 'O')
        for i, m in enumerate(sorted([mt.id[0] for mt in minterms])):
            colorprint(str(m), None)
            if i != len(minterms) - 1:
                colorprint(", ", 'O')
        colorprint(")", 'O')

    colorprint("\n\nPI(s): ", 'O')
    for i, pi in enumerate(PIs):
        colorprint(pi, None)
        if i != len(PIs) - 1:
            colorprint(", ", 'O')
    colorprint(".\n", 'O')

    colorprint("EPI(s): ", 'O')
    for i, epi in enumerate(EPIs):
        colorprint(epi, None)
        if i != len(EPIs) - 1:
            colorprint(", ", 'O')
    colorprint(".\n", 'O')

    colorprint("\nMinimised SOP:", 'O')
    colorprint(f"\nF({', '.join(varNames)}) = ", 'T')
    for i, term in enumerate(equation):
        colorprint(term, None)
        if i != len(equation) - 1:
            colorprint(" + ", 'T')

    

if __name__ == "__main__":
    while True:
        main()
        colorprint("\n\nWould you like to find the PIs and EPIs of another function? (y/N): ", 'Y')
        again = input().strip()
        if again.lower() != 'y':
            colorprint("Goodbye...\n", 'R')
            input("Press Enter to exit...")
            break