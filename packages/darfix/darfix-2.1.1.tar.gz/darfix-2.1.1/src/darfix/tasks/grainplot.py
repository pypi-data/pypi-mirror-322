import os

import logging
from silx.io.dictdump import dicttonx
from ewokscore import Task

from .. import dtypes
from ..core.dataset import ImageDataset
from ..core.grainplot import (
    OrientationDistImage,
    compute_mosaicity,
    compute_orientation_dist_data,
    generate_grain_maps_nxdict,
    get_image_parameters,
)

_logger = logging.getLogger(__file__)


class GrainPlot(
    Task,
    input_names=["dataset"],
    optional_input_names=["filename", "dimensions", "third_motor", "save_maps"],
    output_names=["dataset"],
):
    """Generates and saves maps of Center of Mass, FWHM, Skewness, Kurtosis, Orientation distribution and Mosaicity"""

    def run(self):
        input_dataset: dtypes.Dataset = self.inputs.dataset
        default_filename = os.path.join(input_dataset.dataset._dir, "maps.h5")
        filename: str = self.get_input_value("filename", default_filename)
        dimensions: tuple[int, int] = self.get_input_value("dimensions", (0, 1))
        save_maps: bool = self.get_input_value("save_maps", True)
        third_motor: int | None = self.get_input_value("third_motor", None)

        dataset: ImageDataset = input_dataset.dataset
        moments = dataset.apply_moments()

        if dataset.dims.ndim <= 1:
            _logger.warning(
                "Grain plot maps cannot be computed for 1D datasets. Skipping task."
            )
            self.outputs.dataset = dtypes.Dataset(
                dataset=dataset,
                indices=input_dataset.indices,
                bg_indices=input_dataset.bg_indices,
                bg_dataset=input_dataset.bg_dataset,
            )
            return

        dimension1, dimension2 = dimensions

        mosaicity = compute_mosaicity(moments, dimension1, dimension2)

        orientation_dist_data = compute_orientation_dist_data(
            dataset,
            dimension1=dimension1,
            dimension2=dimension2,
            third_motor=third_motor,
        )
        assert orientation_dist_data is not None
        # TODO: What should origin be here ?
        image_parameters = get_image_parameters(
            dataset, x_dimension=dimension1, y_dimension=dimension2, origin="dims"
        )
        orientation_dist_image = OrientationDistImage(
            xlabel=image_parameters.xlabel,
            ylabel=image_parameters.ylabel,
            scale=image_parameters.scale,
            origin=image_parameters.origin,
            data=orientation_dist_data.data,
            as_rgb=orientation_dist_data.as_rgb,
            contours=dict(),
        )

        # Save data if asked
        if save_maps:
            nxdict = generate_grain_maps_nxdict(
                dataset, mosaicity, orientation_dist_image
            )
            dicttonx(nxdict, filename)

        self.outputs.dataset = dtypes.Dataset(
            dataset=dataset,
            indices=input_dataset.indices,
            bg_indices=input_dataset.bg_indices,
            bg_dataset=input_dataset.bg_dataset,
        )
