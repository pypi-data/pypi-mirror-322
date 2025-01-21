import numpy as np
from PIL import Image
from PIL.ImageFile import ImageFile
import torch

from palm_liner.common.model import UNet


def detect_lines(
    u_net: UNet,
    image_warped_clean_mini: ImageFile,
    device=torch.device("cpu"),
) -> ImageFile:
    img_array = np.asarray(image_warped_clean_mini) / 255
    img_tensor: torch.Tensor = (
        torch.tensor(img_array, dtype=torch.float32)
        .unsqueeze(0)
        .permute(0, 3, 1, 2)
        .to(device)
    )

    pred = u_net(img_tensor).squeeze(0)
    pred = torch.Tensor(
        np.apply_along_axis(
            lambda x: [1, 1, 1] if x > 0.03 else [0, 0, 0], 0, pred.cpu().detach()
        )
    )

    return Image.fromarray((pred.permute((1, 2, 0)).numpy() * 255).astype(np.uint8))
