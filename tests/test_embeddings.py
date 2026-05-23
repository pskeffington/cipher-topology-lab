from ciphertopology.embeddings import byte_pair_embedding, cubical_image_embedding, sliding_window_embedding


def test_byte_pair_embedding_shape():
    data = bytes(range(10))
    pts = byte_pair_embedding(data)
    assert pts.shape == (5, 2)


def test_sliding_window_embedding_shape():
    data = bytes(range(16))
    pts = sliding_window_embedding(data, dimension=4, stride=2)
    assert pts.shape == (7, 4)


def test_cubical_image_embedding_shape():
    data = bytes(range(64))
    image = cubical_image_embedding(data, side=8)
    assert image.shape == (8, 8)
    assert image.min() >= 0.0
    assert image.max() <= 1.0
