import Augmentor

p = Augmentor.Pipeline("D:\Project\\newdataset")

p.resize(probability=1.0, width=64, height=64)

p.sample(120)