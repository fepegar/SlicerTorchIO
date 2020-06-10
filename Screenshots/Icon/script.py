import numpy as np
from PIL import Image
nw = np.array(Image.open('motion.png'))
ne = np.array(Image.open('ghosting.png'))
sw = np.array(Image.open('spike.png'))
se = np.array(Image.open('bias.png'))
result = nw.copy()
si, sj, _ = result.shape
sih = si // 2
sjh = sj // 2 + 28
result[sih:] = sw[sih:]
result[:, sjh:] = ne[:, sjh:]
result[:, sjh:] = ne[:, sjh:]
result[sih:, sjh:] = se[sih:, sjh:]
result = result[:, 80:-74]  # make square
image = Image.fromarray(result)
image = image.resize((128, 128), Image.LANCZOS)
image.save('mosaic.png')
