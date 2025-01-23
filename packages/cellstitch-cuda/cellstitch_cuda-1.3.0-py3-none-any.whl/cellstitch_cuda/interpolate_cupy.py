import ot
import ot.plot
import numpy as np
from scipy import ndimage as ndi

from cellpose import utils as cp_utils
from joblib import Parallel, delayed
from skimage.measure import regionprops


# -------------------------------
# interpolation helper functions
# -------------------------------


def comp_match_plan(pc1, pc2, dist="sqeuclidean"):
    """Compute optimal matching plans between 2 sets of point clouds"""
    # compute cost matrix
    C = ot.dist(pc1, pc2, metric=dist).astype(np.float64)
    C /= C.max()

    # convert point clouds to uniform distributions
    n_pts1, n_pts2 = pc1.shape[0], pc2.shape[0]
    mu1, mu2 = np.ones(n_pts1) / n_pts1, np.ones(n_pts2) / n_pts2

    # compute transport plan
    plan = ot.emd(mu1, mu2, C)

    return plan


def interpolate(pc1, pc2, dist="sqeuclidean", anisotropy=2):
    """
    Calculate interpolated predictions

    Parameters
    ----------
    pc1 : np.ndarray
        Point cloud representing cell boundary in frame 1

    pc2 : np.ndarray
        Point cloud representing cell boundary in frame 2

    anisotropy : int
        Ratio of sampling rate between different axes

    Returns
    -------
    interp_pcs : list
        Smoothed boundary locations along interpolated layers
    """
    alphas = np.linspace(0, 1, anisotropy + 1)[1:-1]
    plan = comp_match_plan(pc1, pc2, dist=dist)
    normalized_plan = plan / plan.sum(
        axis=1, keepdims=1
    )  # normalize so that the row sum is 1

    interp_pcs = []

    for alpha in alphas:
        n_pts = pc1.shape[0]
        avg_pc = np.zeros((n_pts, 2), dtype=int)

        for i in range(n_pts):
            point = pc1[i]
            target_weights = normalized_plan[i]

            weighted_target = np.array(
                [np.sum(target_weights * pc2[:, 0]), np.sum(target_weights * pc2[:, 1])]
            )

            avg_pc[i, :] = point * (1 - alpha) + alpha * weighted_target

        interp_pcs.append(avg_pc)

    return interp_pcs


# -----------------------------------------
# Util functions for interp reconstruction
# -----------------------------------------


def get_lbls(mask):
    """Get unique labels from the predicted masks"""
    return np.unique(mask[mask != 0])


def min_size_filter(res, thld=100):
    """Filter out all masks with area below threshold"""
    assert len(res) == 4, "Invalid Cellpose 4-tuple result"
    preds = res[0]

    for i in range(len(preds)):
        lbls = get_lbls(preds[i])
        for lbl in lbls:
            msk = preds[i] == lbl
            if msk.sum() < thld:
                coords = np.nonzero(msk)
                preds[i][coords] = 0

    res_filtered = (preds, res[1], res[2], res[3])
    return res_filtered


def get_contours(masks):
    """Transfer solid mask predictions to non-overlapping contours w/ distinct integers"""
    masks_new = masks.copy()
    outlines = cp_utils.masks_to_outlines(masks)
    masks_new[~outlines] = 0

    return masks_new


def get_mask_perimeter(masks, lbl, is_contour=False):
    assert lbl in get_lbls(
        masks
    ), "Label {} doesn't in current mask predictions".format(lbl)

    if is_contour:
        p = (masks == lbl).sum()
    else:
        mask_lbl = (masks == lbl).astype(np.uint8)
        p = cp_utils.masks_to_outlines(mask_lbl).sum()

    return p


def calc_vols(pred):
    """
    Calculate volumes of each mask from predictions
    """
    lbls = get_lbls(pred)
    vols = [(pred == lbl).sum() for lbl in lbls]
    return vols


def calc_depth(masks):
    """
    Calculate z-layer depth of predictions
    """
    assert masks.ndim == 3, "Mask predictions must be 3D to calculate depth"

    lbls = get_lbls(masks)
    depths = np.vectorize(lambda lbl: np.diff(np.nonzero(masks == lbl)[0][[0, -1]])[0])(
        lbls
    )

    return depths


def mask_to_coord(mask):
    """Return (n, 2) coordinates from masks"""
    coord = np.asarray(np.nonzero(mask)).T
    return coord


def coord_to_mask(coord, size, lbl):
    """Convert from coordinates to original labeled masks"""
    mask = np.zeros(size)
    mask[tuple(coord.T)] = lbl
    return mask


def contour_to_mask(contour):
    lbl = get_lbls(contour)[0]
    """ Convert contour to solid masks with fill-in labels"""
    binary_contour = contour > 0
    binary_mask = ndi.binary_fill_holes(np.asarray(binary_contour))

    mask = np.zeros_like(binary_contour)
    mask[binary_mask] = lbl

    return mask


def connect(coord1, coord2, mask):
    """
    Modify the mask by connecting the two given coordinates.

    Parameters
    ----------
    coord1 : [x1, y1]
        Coordinate of the first pixel.

    coord2 : [x2, y2]
        Coordinate of the second pixel.

    mask : binary np.narray
        Binary mask of the boundary.
    """
    x1, y1 = coord1
    x2, y2 = coord2

    x_offset, y_offset = x2 - x1, y2 - y1

    # skip if the two coordinates are already connected
    if x_offset**2 + y_offset**2 <= 2:
        return

    diag_length = min(abs(x_offset), abs(y_offset))

    # initialize at coord1
    added_x, added_y = x1, y1

    # first, add diagonal pixels
    for i in range(1, diag_length + 1):
        added_x = x1 + i * np.sign(x_offset)
        added_y = y1 + i * np.sign(y_offset)

        mask[added_x, added_y] = 1

        # need to walk vertically
    if added_x == x2 and added_y != y2:
        offset = abs(added_y - y2)
        for i in range(1, offset + 1):
            mask[added_x, added_y + i * np.sign(y_offset)] = 1

            # or, now need to walk horizonally
    if added_y == y2 and added_x != x2:
        offset = abs(added_x - x2)
        for i in range(1, offset + 1):
            mask[added_x + i * np.sign(x_offset), added_y] = 1


def calc_angles(source_point, target_points, eps=1e-20):
    """
    Calculate angle (rad) between source point (source_point) & list of target points(target_points, dim=(n, 2))
    """
    source_points = np.tile(source_point, (target_points.shape[0], 1))
    diff = target_points - source_points
    angles = np.apply_along_axis(
        lambda x: np.arctan2(x[1], x[0] + eps), axis=1, arr=diff
    )

    return angles


def connect_boundary(coords, size, lbl=1):
    """
    Connect interpolation coordinates to generate close-loop mask contours

    Parameters
    ----------
    coords : ndarray, shape (ns,2)
        Boundary coordinates (might be disconnected).

    size: (n1, n2)
        Shape of the final mask.

    lbl: int
        Label of the original mask.

    Returns
    -------
    mask: ndarray, shape (n1, n2)
        Connected boundary mask.

    """
    # Sort boundary labels by angle to mask's mass center
    mass_center = np.round(coords.mean(0)).astype(np.int64)
    angles = calc_angles(mass_center, coords)
    sorted_coords = coords[angles.argsort()]

    mask = coord_to_mask(coords, size, lbl)

    for i, (x, y) in enumerate(sorted_coords[:-1]):
        next_x, next_y = sorted_coords[i + 1]
        connect((x, y), (next_x, next_y), mask)

    connect(tuple(sorted_coords[-1]), tuple(sorted_coords[0]), mask)

    return mask


# -----------------------------
# Core Interpolation functions
# -----------------------------


def process_label(lbl, source_region, target_region, shape, dist="sqeuclidean", anisotropy=2):
    """
    Process a single label for interpolation using bounding boxes to limit scope.

    Parameters
    ----------
    lbl : int
        The label to process.
    source_regions : list
        Region properties of source layer regions.
    target_regions : list
        Region properties of target layer regions.
    shape : tuple
        Shape of the final mask (height, width).
    dist : str
        Distance metric for interpolation.
    anisotropy : int
        Number of interpolated layers.

    Returns
    -------
    interp_layers : list
        List of interpolated binary masks for the given label.
    """

    if not source_region or not target_region:
        return []

    # Extract bounding box and corresponding regions
    src_minr, src_minc, src_maxr, src_maxc = source_region.bbox
    tgt_minr, tgt_minc, tgt_maxr, tgt_maxc = target_region.bbox

    # Determine the bounding box for the interpolated region
    minr = min(src_minr, tgt_minr)
    minc = min(src_minc, tgt_minc)
    maxr = max(src_maxr, tgt_maxr)
    maxc = max(src_maxc, tgt_maxc)

    # Crop the source and target contours
    source_ct = (source_region.image).astype(np.uint8)
    target_ct = (target_region.image).astype(np.uint8)

    # Translate cropped region to full-coordinate space
    source_coords = mask_to_coord(source_ct)
    target_coords = mask_to_coord(target_ct)

    # Perform interpolation
    interp_coords = interpolate(source_coords, target_coords, dist=dist, anisotropy=anisotropy)

    # Create binary masks for each interpolated layer
    interp_masks = [
        ndi.binary_fill_holes(connect_boundary(interp, (maxr - minr, maxc - minc), lbl))
        for interp in interp_coords
    ]

    # Place interpolated masks back into the full-sized array
    full_interp_masks = []
    for mask in interp_masks:
        full_mask = np.zeros(shape, dtype=np.uint8)
        full_mask[minr:maxr, minc:maxc] = mask
        full_interp_masks.append(full_mask)

    return full_interp_masks


def interp_layers_parallel(source_mask, target_mask, dist="sqeuclidean", anisotropy=2):
    """
    Interpolating adjacent z-layers
    """

    def _dilation(coords, lims):
        y, x = coords
        ymax, xmax = lims
        dy, dx = np.meshgrid(
            np.arange(y - 2, y + 3), np.arange(x - 2, x + 3), indexing="ij"
        )
        dy, dx = dy.flatten(), dx.flatten()
        mask = np.logical_and(
            np.logical_and(dy >= 0, dx >= 0), np.logical_and(dy < ymax, dx < xmax)
        )
        return dy[mask], dx[mask]

    shape = source_mask.shape
    source_contour = get_contours(source_mask)
    target_contour = get_contours(target_mask)

    # Boundary condition: if empty on source / target label
    # align the empty slice w/ mass centers to represent instance endings
    source_dummy = np.zeros_like(source_mask)
    target_dummy = np.zeros_like(target_mask)
    if not np.intersect1d(get_lbls(source_contour), get_lbls(target_contour)).size:
        if (source_contour.sum() == target_contour.sum() == 0) or (
            np.logical_and(source_mask, target_mask).sum() > 0
        ):
            return np.zeros(shape)
        get_mask_center = lambda x: (
            np.round(np.nonzero(x)[0].sum() / x.sum()).astype(np.uint16),
            np.round(np.nonzero(x)[1].sum() / x.sum()).astype(np.uint16),
        )
        for lbl in get_lbls(source_contour):
            yc, xc = _dilation(get_mask_center(source_mask == lbl), source_mask.shape)
            target_dummy[yc, xc] = lbl
        for lbl in get_lbls(target_contour):
            yc, xc = _dilation(get_mask_center(target_mask == lbl), target_mask.shape)
            source_dummy[yc, xc] = lbl
        source_contour += source_dummy
        target_contour += target_dummy

    source_regions = regionprops(source_contour)
    target_regions = regionprops(target_contour)

    joint_lbls = np.intersect1d(get_lbls(source_contour), get_lbls(target_contour))

    results = Parallel(n_jobs=1)(
        delayed(process_label)(
            lbl,
            source_region=next((region for region in source_regions if region.label == lbl), None),
            target_region=next((region for region in target_regions if region.label == lbl), None),
            shape=shape,
            dist=dist,
            anisotropy=anisotropy,
        )
        for lbl in joint_lbls
    )

    interp_masks = np.zeros((anisotropy + 2, *shape), dtype=source_mask.dtype)
    interp_masks[0] = source_mask
    interp_masks[-1] = target_mask

    for z, interp_layers in enumerate(zip(*results), start=1):
        for mask in interp_layers:
            interp_masks[z] += mask

    return interp_masks


def full_interpolate(masks, anisotropy=2, dist="sqeuclidean", verbose=False):
    """
    Interpolating between all adjacent z-layers

    Parameters
    ----------
    masks : np.ndarray
        layers of 2D predictions
        (dim: (Depth, H, W))

    anisotropy : int
        Ratio of sampling rate between xy-axes & z-axis

    Returns
    -------|
    interp_masks : np.ndarray
        interpolated masks
        (dim: (Depth * anisotropy - (anisotropy-1), H, W))

    """
    if masks.max() < 256:
        masks = masks.astype("uint8")
    elif masks.max() < 65536:
        masks = masks.astype("uint16")

    dtype = masks.dtype

    interp_masks = np.zeros(
        (
            len(masks) + (len(masks) - 1) * (anisotropy - 1),
            masks.shape[1],
            masks.shape[2],
        ),
        dtype=dtype,
    )

    idx = 0
    for i, source_mask in enumerate(masks[:-1]):
        if verbose:
            print("Interpolating layer {} & {}...".format(i, i + 1))
        target_mask = masks[i + 1]
        interps = interp_layers_parallel(
            source_mask, target_mask, dist=dist, anisotropy=anisotropy
        )
        interp_masks[idx : idx + anisotropy + 1] = interps
        idx += anisotropy

    return interp_masks
