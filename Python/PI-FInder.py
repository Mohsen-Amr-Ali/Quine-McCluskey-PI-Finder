# ========================================== CLASSES ========================================== #
class minterm:
    def __init__(self, id, numOfVariables):
        self.id = id
        self.binary = bin(self.id)[2:].zfill(numOfVariables)
        self.group = self.binary.count('1')

class CombinedTerm:
    def __init__(self, binary, original_ids):
        self.binary = binary              
        self.original_ids = original_ids  
        self.group = self.binary.count('1')  
        self.combined = False             

    def __repr__(self):
        return f"CombinedTerm(binary='{self.binary}', ids={self.original_ids}, combined={self.combined})"


# ========================================== FUNCTIONS ========================================== #

def vars_generator(numOfVariables):
    for i in range(numOfVariables):
        vars.append(chr(ord('a') + i)) #chr betconvert el unicode integer into a character
    return vars

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