"""Dimension metadata.

This is not related to the NGFF metadata,
but it is based on the actual metadata of the image data.
"""

from collections import OrderedDict


class Dimensions:
    """Dimension metadata."""

    def __init__(
        self,
        on_disk_shape: tuple[int, ...],
        axes_names: list[str],
        axes_order: list[int],
    ) -> None:
        """Create a Dimension object from a Zarr array.

        Args:
            on_disk_shape (tuple[int, ...]): The shape of the array on disk.
            axes_names (list[str]): The names of the axes in the canonical order.
            axes_order (list[int]): The mapping between the canonical order and the on
                disk order.
        """
        self._on_disk_shape = on_disk_shape

        for s in on_disk_shape:
            if s < 1:
                raise ValueError("The shape must be greater equal to 1.")

        if len(self._on_disk_shape) != len(axes_names):
            raise ValueError(
                "The number of axes names must match the number of dimensions."
            )

        self._axes_names = axes_names
        self._axes_order = axes_order

        self._shape = [self._on_disk_shape[i] for i in axes_order]
        self._shape_dict = OrderedDict(zip(axes_names, self._shape, strict=True))

    def __str__(self) -> str:
        """Return the string representation of the object."""
        _dimensions = ", ".join(
            [f"{name}={self._shape_dict[name]}" for name in self._axes_names]
        )
        return f"Dimensions({_dimensions})"

    def __repr__(self) -> str:
        """Return the string representation of the object."""
        return str(self)

    @property
    def shape(self) -> tuple[int, ...]:
        """Return the shape as a tuple in the canonical order."""
        return tuple(self._shape)

    @property
    def on_disk_shape(self) -> tuple[int, ...]:
        """Return the shape as a tuple."""
        return self._on_disk_shape

    def ad_dict(self) -> dict[str, int]:
        """Return the shape as a dictionary."""
        return self._shape_dict

    def get(self, ax_name: str, default: int = 1) -> int:
        """Return the dimension of the given axis name."""
        return self._shape_dict.get(ax_name, default)

    @property
    def on_disk_ndim(self) -> int:
        """Return the number of dimensions on disk."""
        return len(self._on_disk_shape)

    @property
    def is_time_series(self) -> bool:
        """Return whether the data is a time series."""
        t = self._shape_dict.get("t", 1)
        if t == 1:
            return False
        return True

    @property
    def is_2d(self) -> bool:
        """Return whether the data is 2D."""
        z = self._shape_dict.get("z", 1)
        if z != 1:
            return False
        return True

    @property
    def is_2d_time_series(self) -> bool:
        """Return whether the data is a 2D time series."""
        return self.is_2d and self.is_time_series

    @property
    def is_3d(self) -> bool:
        """Return whether the data is 3D."""
        return not self.is_2d

    @property
    def is_3d_time_series(self) -> bool:
        """Return whether the data is a 3D time series."""
        return self.is_3d and self.is_time_series

    @property
    def is_multi_channels(self) -> bool:
        """Return whether the data has multiple channels."""
        c = self._shape_dict.get("c", 1)
        if c == 1:
            return False
        return True

    def find_axis(self, ax_name: str) -> int | None:
        """Return the index of the axis name."""
        for i, ax in enumerate(self._axes_names):
            if ax == ax_name:
                return i
        return None
