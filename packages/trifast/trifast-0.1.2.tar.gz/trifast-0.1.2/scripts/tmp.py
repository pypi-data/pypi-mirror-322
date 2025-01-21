import torch
from einops import rearrange


q= torch.randn((2, 3, 4, 5))

collapsed = rearrange(q, "b h i j -> (b h) i j").contiguous()

expanded = rearrange(collapsed, "(b h) i j -> b h i j", h=3).contiguous()

assert (q == expanded).all()

