def read_file_to_string(filename):
    with open(filename, 'r') as f:
        content = f.read()
        return content


def read_fasta_to_string(fasta_file):
    sequence_string = ""
    with open(fasta_file, 'r') as f:
        f.readline()
        for line in f:
          sequence_string += line.strip()
    return sequence_string


def create_corpus(genome_string: str, overlapping: bool = True, D: int = 10000):
    L = len(genome_string)

    # 1. replace 'T' with 'U'
    m_rna = ''
    for c in genome_string:
        if c == 'T': m_rna += 'U'
        else: m_rna += c

    # 2. add anti-parallel (reverse complement) DNA strand
    complement_map = {"A": "U", "U": "A", "C": "G", "G": "C"}
    reversed_m_rna = m_rna[::-1]

    reverse_complement_m_rna = ''
    for c in reversed_m_rna:
        reverse_complement_m_rna += complement_map[c]

    # 3. make corpus (collection of documents) out of m_rna and reverse_complement_m_rna
    corpus = []

    for i in range(L // D):
        document = m_rna[i * D: (i+1) * D]
        corpus.append(document)
    corpus.append(m_rna[(L//D) * D:])

    for i in range(L // D):
        document = reverse_complement_m_rna[i * D: (i+1) * D]
        corpus.append(document)
    corpus.append(reverse_complement_m_rna[(L//D) * D:])

    # 4. tokenization
    processed_corpus = []

    if overlapping:
        for document in corpus:
            kmers_list = []
            if len(document) - 3 + 1 > 0:
                for i in range(len(document) - 3 + 1):
                    kmers_list.append(document[i:i + 3])
                processed_corpus.append(kmers_list)
    else:
        for document in corpus:
            kmers_list1, kmers_list2, kmers_list3 = [], [], []
            for i in range(0, len(document)//3):
                if len(document[i * 3: i * 3 + 3]) == 3:
                    kmers_list1.append(document[i * 3: i * 3 + 3])
                if len(document[i * 3 + 1: i * 3 + 3 + 1]) == 3:
                    kmers_list2.append(document[i * 3 + 1: i * 3 + 3 + 1])
                if len(document[i * 3 + 2: i * 3 + 3 + 2]) == 3:
                    kmers_list3.append(document[i * 3 + 2: i * 3 + 3 + 2])
            if len(kmers_list1) > 0: processed_corpus.append(kmers_list1)
            if len(kmers_list2) > 0: processed_corpus.append(kmers_list2)
            if len(kmers_list3) > 0: processed_corpus.append(kmers_list3)
    return processed_corpus


if __name__ == '__main__':
    # corpus = create_corpus(genome_string='AAUCCUGAAUCCUG', overlapping=False, D=7)

    v_colare_string = read_file_to_string('Vibrio_cholerae_genome.txt')
    v_colare_corpus = create_corpus(genome_string=v_colare_string, overlapping=True)

    e_coli_string = read_fasta_to_string('Escherichi_coli.fna')
    e_coli_corpus = create_corpus(genome_string=e_coli_string, overlapping=False)
