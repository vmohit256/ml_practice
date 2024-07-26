import numpy as np
from IPython.display import display, HTML

def display_colored_text(tokens, scores, color1=(255, 0, 0), color2=(0, 255, 0), skip_tokens=['[PAD]']):
    # vary color as linear interpolation from color1 to color2 based on score from -1 to 1
    # clips scores to -1 and 1
    final_html = []
    skip_tokens = set(skip_tokens)
    for token, score in zip(tokens, scores):
        score = max(-1, min(1, score))
        if token in skip_tokens: continue
        color = tuple(int((1 + score) / 2 * (c2 - c1) + c1) for c1, c2 in zip(color1, color2))
        final_html.append(f'<span style="color:rgb{color}">{token}</span>')
    display(HTML(' '.join(final_html)))


"""
Returns cosine similarity between embeddings and a target vector

Args:
    E: numpy array of shape (vocab_size, embed_dim)
    target_vector: numpy array of shape (embed_dim,)

Returns:
    cossim: numpy array of shape (vocab_size,)
"""
def get_embedding_cosine_similarities(E, target_vector):
    Enormed = E / np.linalg.norm(E, axis=1)[:, None]
    target_vector = target_vector / np.linalg.norm(target_vector)
    return np.matmul(Enormed, target_vector)