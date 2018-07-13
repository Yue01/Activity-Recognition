import Augmentor

p = Augmentor.Pipeline("D:\Project\pic1")

p.rotate90(probability=0.2)
p.rotate270(probability=0.1)
p.flip_left_right(probability=0.8)
p.flip_top_bottom(probability=0.1)
p.resize(probability=1.0, width=64, height=64)
p.crop_random(probability=0.8, percentage_area=0.9)

p.sample(2200)