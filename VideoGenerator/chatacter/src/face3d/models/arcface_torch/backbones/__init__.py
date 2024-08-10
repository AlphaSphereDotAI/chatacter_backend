from .iresnet import iresnet18, iresnet34, iresnet50, iresnet100, iresnet200
from .mobilefacenet import get_mbf


def get_model(name, **kwargs):
    # resnet
    if name == "r18":
        return iresnet18(False, **kwargs)
    if name == "r34":
        return iresnet34(False, **kwargs)
    if name == "r50":
        return iresnet50(False, **kwargs)
    if name == "r100":
        return iresnet100(False, **kwargs)
    if name == "r200":
        return iresnet200(False, **kwargs)
    if name == "r2060":
        from .iresnet2060 import iresnet2060
        return iresnet2060(False, **kwargs)
    if name == "mbf":
        fp16 = kwargs.get("fp16", False)
        num_features = kwargs.get("num_features", 512)
        return get_mbf(fp16=fp16, num_features=num_features)
    raise ValueError()