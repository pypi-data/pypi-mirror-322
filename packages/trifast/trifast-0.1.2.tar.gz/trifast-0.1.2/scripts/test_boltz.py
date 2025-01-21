from pathlib import Path
from trifast import triangle_attention
import torch


for p in (Path(__file__).parent.parent / "data").glob("*.pth"):
    d = torch.load(p)

    inputs = d["inputs"]
    q = inputs["query"]
    k = inputs["key"]
    v = inputs["value"]
    biases = inputs["biases"]

    o_tru = d["output"]
    grads = d["gradients"]
    do = grads["output"]
    dq = grads["query"]
    dk = grads["key"]
    dv = grads["value"]
    dbiases = grads["biases"]

    dout = triangle_attention(q, k, v, biases)

    # d = torch.load(p)
    #
    # q, k, v, biases = d["q"], d["k"], d["v"], d["biases"]
    # o_true = d["o"].cuda()
    #
    # if len(q.shape) != 4:
    #     raise ValueError(f"Trifast expects q/k/v to be 4D, found {len(q.shape)}")
    #
    # # Reorder q/k/v
    # q = rearrange(q, "i h j d -> h i j d").cuda()
    # k = rearrange(k, "i h j d -> h i j d").cuda()
    # v = rearrange(v, "i h j d -> h i j d").cuda()
    #
    # # Check biases are compatible.
    # if len(biases) > 2 or len(biases) == 0:
    #     raise ValueError(
    #         f"Trifast only 1 or 2 bias terms (triangle_bias and optional mask), found {len(biases)}"
    #     )
    #
    # # It should be triangle_bias, create fake mask
    # if len(biases) == 1:
    #     b = biases[0]
    #     n = q.shape[-2]
    #     mask = torch.zeros((n, 1, 1, n), device=q.device, dtype=torch.bool)
    # else:
    #     # must be two terms
    #     mask, b = biases
    #
    # b = rearrange(b, "() h i j -> h i j").cuda()
    # mask = rearrange(mask, "i () () j -> i j").bool().cuda()
    #
    # o = triangle_attention(q, k, v, b, mask)
    # o = rearrange(o, "h i j d -> i j h d")
    #
    # o_ref = attention_reference(q, k, v, b, mask)
    #
    # max_diff = (o - o_true).abs().max()
    # print(max_diff)
    #
    # assert torch.allclose(o, o_true, atol=1e-5), f"Failed {p}"
