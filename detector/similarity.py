def ngrams(items, n):
    if len(items) < n or n <= 0:
        return []
    output = []
    idx = 0
    while idx + n <= len(items):
        output.append(tuple(items[idx : idx + n]))
        idx += 1
    return output


def jaccard_similarity(seq_a, seq_b):
    set_a = set(seq_a)
    set_b = set(seq_b)
    if not set_a and not set_b:
        return 0.0
    inter = len(set_a.intersection(set_b))
    union = len(set_a.union(set_b))
    if union == 0:
        return 0.0
    return inter / union


def lcs_length(seq_a, seq_b):
    a_len = len(seq_a)
    b_len = len(seq_b)
    dp = []
    row_idx = 0
    while row_idx <= a_len:
        dp.append([0] * (b_len + 1))
        row_idx += 1

    i = 1
    while i <= a_len:
        j = 1
        while j <= b_len:
            if seq_a[i - 1] == seq_b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                left = dp[i][j - 1]
                up = dp[i - 1][j]
                dp[i][j] = left if left > up else up
            j += 1
        i += 1

    return dp[a_len][b_len]


def normalized_lcs_similarity(seq_a, seq_b):
    if not seq_a or not seq_b:
        return 0.0
    lcs = lcs_length(seq_a, seq_b)
    base = len(seq_a) if len(seq_a) > len(seq_b) else len(seq_b)
    if base == 0:
        return 0.0
    return lcs / base


def combined_similarity(tokens_a, tokens_b, structure_a, structure_b):
    token_grams_a = ngrams(tokens_a, 3)
    token_grams_b = ngrams(tokens_b, 3)
    token_unigrams_a = ngrams(tokens_a, 1)
    token_unigrams_b = ngrams(tokens_b, 1)
    structural_grams_a = ngrams(structure_a, 2)
    structural_grams_b = ngrams(structure_b, 2)

    token_j = jaccard_similarity(token_grams_a, token_grams_b)
    token_u = jaccard_similarity(token_unigrams_a, token_unigrams_b)
    structural_j = jaccard_similarity(structural_grams_a, structural_grams_b)
    token_l = normalized_lcs_similarity(tokens_a, tokens_b)
    structural_l = normalized_lcs_similarity(structure_a, structure_b)

    # Weighted blend tuned to handle short template snippets.
    score = (0.30 * token_j) + (0.20 * token_u) + (0.20 * structural_j) + (0.20 * token_l) + (0.10 * structural_l)
    return score
