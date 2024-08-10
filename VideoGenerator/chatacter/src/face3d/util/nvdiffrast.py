"""This script is the differentiable renderer for Deep3DFaceRecon_pytorch
Attention, antialiasing step is missing in current version.
"""

from typing import List

import pytorch3d.ops
import torch
from pytorch3d.renderer import (
    FoVPerspectiveCameras,
    MeshRasterizer,
    MeshRenderer,
    RasterizationSettings,
)
from pytorch3d.structures import Meshes
from torch import nn


class MeshRenderer(nn.Module):

    def __init__(self, rasterize_fov, znear=0.1, zfar=10, rasterize_size=224):
        super(MeshRenderer, self).__init__()

        self.rasterize_size = rasterize_size
        self.fov = rasterize_fov
        self.znear = znear
        self.zfar = zfar

        self.rasterizer = None

    def forward(self, vertex, tri, feat=None):
        """
        Return:
            mask               -- torch.tensor, size (B, 1, H, W)
            depth              -- torch.tensor, size (B, 1, H, W)
            features(optional) -- torch.tensor, size (B, C, H, W) if feat is not None

        Parameters:
            vertex          -- torch.tensor, size (B, N, 3)
            tri             -- torch.tensor, size (B, M, 3) or (M, 3), triangles
            feat(optional)  -- torch.tensor, size (B, N ,C), features
        """
        device = vertex.device
        rsize = int(self.rasterize_size)
        # ndc_proj = self.ndc_proj.to(device)
        # trans to homogeneous coordinates of 3d vertices, the direction of y is the same as v
        if vertex.shape[-1] == 3:
            vertex = torch.cat(
                [vertex, torch.ones([*vertex.shape[:2], 1]).to(device)], dim=-1
            )
            vertex[..., 0] = -vertex[..., 0]

        if self.rasterizer is None:
            self.rasterizer = MeshRasterizer()
            print("create rasterizer on device cuda:%d" % device.index)

        # for range_mode vetex: [B*N, 4], tri: [B*M, 3], for instance_mode vetex: [B, N, 4], tri: [M, 3]
        tri = tri.type(torch.int32).contiguous()

        # rasterize
        cameras = FoVPerspectiveCameras(
            device=device,
            fov=self.fov,
            znear=self.znear,
            zfar=self.zfar,
        )

        raster_settings = RasterizationSettings(image_size=rsize)

        mesh = Meshes(
            vertex.contiguous()[..., :3],
            tri.unsqueeze(0).repeat((vertex.shape[0], 1, 1)),
        )

        fragments = self.rasterizer(
            mesh, cameras=cameras, raster_settings=raster_settings
        )
        rast_out = fragments.pix_to_face.squeeze(-1)
        depth = fragments.zbuf

        # render depth
        depth = depth.permute(0, 3, 1, 2)
        mask = (rast_out > 0).float().unsqueeze(1)
        depth = mask * depth

        image = None
        if feat is not None:
            attributes = feat.reshape(-1, 3)[mesh.faces_packed()]
            image = pytorch3d.ops.interpolate_face_attributes(
                fragments.pix_to_face, fragments.bary_coords, attributes
            )
            image = image.squeeze(-2).permute(0, 3, 1, 2)
            image = mask * image

        return mask, depth, image
