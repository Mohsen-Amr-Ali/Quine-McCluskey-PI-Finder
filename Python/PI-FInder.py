# ========================================== CLASSES ========================================== #
class minterm:
    def __init__(self, id, numOfVariables):
        self.id = [id]
        self.binary = bin(self.id)[2:].zfill(numOfVariables)
        self.group = self.binary.count('1')
        self.flag = False

    def __str__(self):
        return f"{','.join(str(i) for i in self.id)}: {self.binary}"


# ========================================== FUNCTIONS ========================================== #

def vars_generator(numOfVariables):
    for i in range(numOfVariables):
        vars.append(chr(ord('a') + i)) #chr betconvert el unicode integer into a character
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

def find_PIs_and_EPIs(mintermList):
    allPIs = []
    currentTerms = mintermList

    while True:
        combined = combine_terms(currentTerms)

        for term in currentTerms:
            if not term.flag:
                already_included = False
                for existing in allPIs:
                    if term.id == existing.id and term.binary == existing.binary:
                        already_included = True
                        break
                if not already_included:
                    allPIs.append(term)

        if not combined:
            break

        currentTerms = combined

    minterm_to_implicants = {} #key -> minterm id from original mintermsList, values -> id of prime implicants that contain that minterm
    for minterm in mintermList:
        for pi in allPIs:
            if minterm.id[0] in pi.id:
                if minterm.id[0] not in minterm_to_implicants:
                    minterm_to_implicants[minterm.id[0]] = []
                minterm_to_implicants[minterm.id[0]].append(pi)

    epis = []
    for minterm_id, implicants in minterm_to_implicants.items():
        if len(implicants) == 1:
            epi = implicants[0]
            if epi not in epis:
                epis.append(epi)

    return allPIs, epis


        

# ========================================== MAIN FUNCTION ========================================== #

def main():
    print("Hello, World! This is the main function.")

if __name__ == "__main__":
    main()

# ========================================== EXTRA FUNCTIONS ========================================== #
def variables_to_minterms(terms, vars): #convert fubction in terms of a & a' to a list that's the sum of minterms
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