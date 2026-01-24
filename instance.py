import random

def get_subset(array):
    if len(array) == 0:
        return []
    
    subset = []
    list_array = list(array)
    rand_num = format(random.randrange(1, 2**(len(array))), f'0{len(array)}b')
    
    for i in range(len(array)):
        if rand_num[i] == '1':
            subset.append(list_array[i])

    return subset

def create_instance(filename, n, m, probs, max_clauses=None, max_keywords=None):
    """
    Create an instance file with the following format:
    line 1: n m
    line 2: p_1 p_2 ... p_m
    next n lines: rules, each containing x key words sampled from [1, m]
    """

    # Sanity check
    if len(probs) != m:
        raise ValueError("Length of probs must equal m.")

    if max_keywords is None or max_keywords > m:
        max_keywords = m
    if max_clauses is None or max_clauses > int(max_keywords / 2 + 1):
        max_clauses = int(max_keywords / 2 + 1)

    with open(filename, 'w') as f:
        # Line 1: n m
        f.write(f"{n} {m}\n")

        # Line 2: probabilities
        f.write(" ".join(f"{p:.6f}" for p in probs) + "\n")

        # Generate n rules
        for _ in range(n):
            num_clauses = random.randint(1, max_clauses)
            keywords = random.sample(range(1, m + 1), k = random.randint(num_clauses, max_keywords))
            dividers = [0] + sorted(random.sample(range(1, len(keywords)), k = num_clauses - 1))

            cur_rule = []
            for i in range(1, len(dividers)):
                if dividers[i - 1] == dividers[i] - 1:
                    cur_rule.append(str(keywords[dividers[i - 1]]))
                else:
                    cur_rule.append(f"({' '.join(map(str, keywords[dividers[i - 1]:dividers[i]]))})")

            if random.randint(0, 1) == 0 or dividers[-1] == len(keywords) - 1:
                for i in range(dividers[-1], len(keywords)):
                    cur_rule.append(str(keywords[i]))
            else:
                cur_rule.append(f"({' '.join(map(str, keywords[dividers[-1]:]))})")
            
            # Write the rule
            f.write(" ".join(cur_rule) + "\n")

# Example usage
if __name__ == "__main__":
    n = 5     # number of rules
    m = 6     # number of keywords
    probs = [0.1, 0.2, 0.05, 0.15, 0.25, 0.25]
    create_instance("instance_1.tex", n, m, probs)