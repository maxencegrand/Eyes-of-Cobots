import tobii_transposer as tobii
import fovio_transposer as fovio

def transpose(user, figure):
    tobii.transpose(user, figure)
    fovio.transpose(user, figure)
