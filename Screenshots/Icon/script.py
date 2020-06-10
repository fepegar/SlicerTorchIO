from skimage import io
nw = io.imread('motion.png')
ne = io.imread('ghosting.png')
sw = io.imread('spike.png')
se = io.imread('bias.png')
result = nw.copy()
si, sj, _ = result.shape
sih = si // 2
sjh = sj // 2 + 28
result[sih:] = sw[sih:]
result[:, sjh:] = ne[:, sjh:]
result[:, sjh:] = ne[:, sjh:]
result[sih:, sjh:] = se[sih:, sjh:]
result = result[:, 80:-74]  # make square
io.imsave('mosaic.png', result)
