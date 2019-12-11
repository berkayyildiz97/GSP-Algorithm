import sys


def generate_candidates(frequent_k_minus_1_sequences):
    candidate_k_sequences = {}
    for sequence1 in frequent_k_minus_1_sequences:
        sequence1_last = sequence1[2:]
        for sequence2 in frequent_k_minus_1_sequences:
            sequence2_first = sequence2[:-2]
            if sequence2_first == sequence1_last:
                candidate_k_sequences[sequence1+sequence2[-2:]] = 0
    return candidate_k_sequences


def prune_candidates(candidate_k_sequences, frequent_k_minus_1_sequences):
    pruned_candidates = dict(candidate_k_sequences)
    for candidate_sequence in candidate_k_sequences:
        for i in range(0, len(candidate_sequence), 2):
            subsequence = ""
#            Son itemsetin son elemani --> kendisi ve oncesi atilir
            if i == len(candidate_sequence)-1:
                subsequence = candidate_sequence[:-2]
#            Bir itemsetin ilk elemani --> kendisi ve sonrasi atilir
            elif i == 0 or candidate_sequence[i-1] == ',':
                subsequence = candidate_sequence[:i] + candidate_sequence[i+2:]
            else:
                subsequence = candidate_sequence[:i-1] + candidate_sequence[i+1:]
            if subsequence not in frequent_k_minus_1_sequences:
                pruned_candidates.pop(candidate_sequence)
                break
    return pruned_candidates


def print_frequent_sequences(frequent_sequences, output_file_path):
    output_file = open(output_file_path, "w")
    for sequence in frequent_sequences:
        itemsets = sequence.split(',')
        for i in range(len(itemsets)):
            itemset = itemsets[i]
            print('(', end='', file=output_file)
            elements = itemset.split(' ')
            for j in range(len(elements)):
                element = elements[j]
                if j == len(elements)-1:
                    print(element, end='', file=output_file)
                else:
                    print(element+" ", end='', file=output_file)
            if i == len(itemsets)-1:
                print(')', end='', file=output_file)
            else:
                print('), ', end='', file=output_file)
        print(" #SUP:",frequent_sequences[sequence], file=output_file)
    output_file.close()


def is_subitemset(itemset, candidate_subitemset):
    for elementInCandidate in candidate_subitemset.split(' '):
        is_element_in_candidate_found = False
        for element in itemset.split(' '):
            if elementInCandidate == element:
                is_element_in_candidate_found = True
                break
        if not is_element_in_candidate_found:
            return False
    return True


inputFilePath = sys.argv[1]
outputFilePath = sys.argv[2]
minSup = float(sys.argv[3])
sequences = []

with open(inputFilePath, "r") as inputFile:
    for line in inputFile:
        line = line.rstrip('\n')
        line = line.replace(' (', '')
        line = line.replace(') ', '')
        line = line.replace('(', '')
        line = line.replace(')', '')
        sequence = []
        for itemset in line.split(','):
            sequence.append(itemset)
        sequences.append(sequence)

candidate1SequencesArray = []
for sequence in sequences:
    for itemset in sequence:
        for element in itemset.split(' '):
            if element not in candidate1SequencesArray:
                candidate1SequencesArray.append(element)

candidate1SequencesArray.sort()
candidate1Sequences = {}
for element in candidate1SequencesArray:
    candidate1Sequences[element] = 0

for candidate1Sequence in candidate1Sequences:
    for sequence in sequences:
        for itemset in sequence:
            if candidate1Sequence in itemset:
                candidate1Sequences[candidate1Sequence] += 1
                break

frequentSequences = {}

for candidate1Sequence in candidate1Sequences:
    if candidate1Sequences[candidate1Sequence]/len(sequences) >= minSup:
        frequentSequences[candidate1Sequence] = candidate1Sequences[candidate1Sequence]

candidate2Sequences = {}

for frequentSequence1 in frequentSequences:
    for frequentSequence2 in frequentSequences:
        if frequentSequence1 < frequentSequence2:
            candidate2Sequences[frequentSequence1+' '+frequentSequence2] = 0

for frequentSequence1 in frequentSequences:
    for frequentSequence2 in frequentSequences:
        candidate2Sequences[frequentSequence1+','+frequentSequence2] = 0

candidateKSequences = candidate2Sequences
while True:
    for candidate in candidateKSequences:
        for sequence in sequences:
            isCandidateFound = True
            isItemsetInCandidateFound = False
            matchedItemsetIndex = -1
            for itemsetInCandidate in candidate.split(','):
                i = 0
                while i < len(sequence):
                    if isItemsetInCandidateFound and (matchedItemsetIndex == len(sequence)-1):
                        isItemsetInCandidateFound = False
                        matchedItemsetIndex = -1
                        break
                    if isItemsetInCandidateFound:
                        i = matchedItemsetIndex+1
                        isItemsetInCandidateFound = False
                        matchedItemsetIndex = -1
                    itemset = sequence[i]
                    if is_subitemset(itemset, itemsetInCandidate):
                        isItemsetInCandidateFound = True
                        matchedItemsetIndex = i
                        break
                    i += 1
                if isItemsetInCandidateFound is False:
                    isCandidateFound = False
                    break
            if isCandidateFound:
                candidateKSequences[candidate] += 1

    isAnyCandidateSelected = False
    frequentKMinus1Sequences = {}
    for candidateKSequence in candidateKSequences:
        if candidateKSequences[candidateKSequence]/len(sequences) >= minSup:
            frequentSequences[candidateKSequence] = candidateKSequences[candidateKSequence]
            frequentKMinus1Sequences[candidateKSequence] = candidateKSequences[candidateKSequence]
            isAnyCandidateSelected = True
    if isAnyCandidateSelected is False:
        break
    candidateKSequences = generate_candidates(frequentKMinus1Sequences)
    candidateKSequences = prune_candidates(candidateKSequences, frequentKMinus1Sequences)


print_frequent_sequences(frequentSequences, outputFilePath)
