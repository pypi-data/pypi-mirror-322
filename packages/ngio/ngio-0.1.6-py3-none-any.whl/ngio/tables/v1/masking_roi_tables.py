"""Implementation of the Masking ROI Table class.

This class follows the roi_table specification at:
https://fractal-analytics-platform.github.io/fractal-tasks-core/tables/
"""

from functools import partial
from typing import Literal

import pandas as pd
import zarr
from pydantic import BaseModel

from ngio.core.label_handler import Label
from ngio.core.roi import SpaceUnits, WorldCooROI
from ngio.tables._utils import validate_columns
from ngio.tables.v1._generic_table import REQUIRED_COLUMNS, BaseTable, write_table_ad


class MaskingROITableV1Meta(BaseModel):
    """Metadata for the ROI table."""

    fractal_table_version: Literal["1"] = "1"
    type: Literal["masking_roi_table"] = "masking_roi_table"
    region: dict[Literal["path"], str]
    instance_key: str = "label"


def create_empty_roi_table() -> pd.DataFrame:
    """Create an empty ROI table."""
    table = pd.DataFrame(
        index=pd.Index([], name="label", dtype="str"), columns=REQUIRED_COLUMNS
    )

    return table


class MaskingROITableV1:
    """Class to handle fractal Masking ROI tables.

    To know more about the Masking ROI table format, please refer to the
    specification at:
    https://fractal-analytics-platform.github.io/fractal-tasks-core/tables/
    """

    def __init__(
        self,
        group: zarr.Group,
        name: str,
        validate_metadata: bool = True,
        validate_table: bool = True,
        index_key: str | None = None,
    ):
        """Initialize the class from an existing group.

        Args:
            group (zarr.Group): The group containing the
                ROI table.
            name (str): The name of the ROI table.
            validate_metadata (bool): If True, the metadata is validated.
            validate_table (bool): If True, the table is validated.
            index_key (str): The column name to use as the index of the DataFrame.
        """
        if validate_metadata:
            self._meta = MaskingROITableV1Meta(**group.attrs)
        else:
            self._meta = MaskingROITableV1Meta.model_construct(**group.attrs)

        # Validate the table is not implemented for the Masking ROI table
        validators = [partial(validate_columns, required_columns=REQUIRED_COLUMNS)]
        validators = validators if validate_table else None

        index_key = index_key if index_key is not None else self._meta.instance_key
        self._table_handler = BaseTable(
            group=group,
            index_key=index_key,
            index_type="int",
            validators=validators,
        )
        self._name = name

    def __repr__(self) -> str:
        """Return the string representation of the class."""
        name = "MaskingROITableV1("
        len_name = len(name)
        return (
            f"{name}"
            f"group_path={self.group_path}, \n"
            f"{' ':>{len_name}}name={self.name},\n"
            f"{' ':>{len_name}}source_label={self.source_label()}, \n"
            f"{' ':>{len_name}}num_labels={len(self.table.index)}), \n"
            ")"
        )

    @classmethod
    def _new(
        cls,
        parent_group: zarr.Group,
        name: str,
        label_image: str,
        instance_key: str = "label",
        overwrite: bool = False,
    ) -> "MaskingROITableV1":
        """Create a new Masking ROI table.

        Note this method is not meant to be called directly.
        But should be called from the TablesHandler class.

        Args:
            parent_group (zarr.Group): The parent group where the ROI table
                will be created.
            name (str): The name of the ROI table.
            label_image (str): Name of the label image.
            instance_key (str): The column name to use as the index of the DataFrame.
                Default is 'label'.
            overwrite (bool): Whether to overwrite the table if it already exists.
        """
        group = parent_group.create_group(name, overwrite=overwrite)

        table = pd.DataFrame(
            index=pd.Index([], name=instance_key, dtype="int"), columns=REQUIRED_COLUMNS
        )

        meta = MaskingROITableV1Meta(
            region={"path": label_image}, instance_key=instance_key
        )
        write_table_ad(
            group=group,
            table=table,
            index_key=instance_key,
            index_type="int",
            meta=meta,
        )
        return cls(group=group, name=name)

    @property
    def name(self) -> str:
        """Return the name of the ROI table."""
        return self._name

    @property
    def root_path(self) -> str:
        """Return the path of the root group."""
        return self._table_handler.root_path

    @property
    def group_path(self) -> str:
        """Return the path of the group."""
        return self._table_handler.group_path

    @property
    def meta(self) -> MaskingROITableV1Meta:
        """Return the metadata of the ROI table."""
        return self._meta

    @property
    def table_handler(self) -> BaseTable:
        """Return the table handler."""
        return self._table_handler

    @property
    def table(self) -> pd.DataFrame:
        """Return the ROI table as a DataFrame."""
        return self._table_handler.table

    @table.setter
    def table(self, table: pd.DataFrame) -> None:
        """Set the feature table."""
        raise NotImplementedError(
            "Setting the table is not implemented. Please use the 'set_table' method."
        )

    def source_label(self, get_full_path: bool = False) -> str | None:
        """Return the name of the label image.

        The name is assumed to be after the last '/' in the path.
        Since this might fails, get_full_path is True, the full path is returned.

        Args:
            get_full_path (bool): If True, the full path is returned.
        """
        region = self.meta.region
        if region is None:
            return None
        path = region["path"]

        if get_full_path:
            return path
        return path.split("/")[-1]

    def set_table(self, table: pd.DataFrame) -> None:
        """Set the feature table."""
        self._table_handler.set_table(table)

    @property
    def list_labels(self) -> list[int]:
        """Return a list of all field indexes in the table."""
        return self.table.index.tolist()

    def from_label(self, label: Label, overwrite: bool = False) -> None:
        """Create a new ROI table from a label.

        Args:
            label (Label): The label to create the ROI table from.
            overwrite (bool): Whether to overwrite the elements in the table.
        """
        if not overwrite and self.table.empty:
            raise ValueError(
                "The table is not empty. Set overwrite to True to proceed."
            )
        raise NotImplementedError("Method not implemented yet.")

    def get_roi(self, label: int) -> WorldCooROI:
        """Get an ROI from the table."""
        if label not in self.list_labels:
            raise ValueError(f"Label {label} not found in the table.")

        table_df = self.table.loc[label]

        roi = WorldCooROI(
            x=table_df.loc["x_micrometer"],
            y=table_df.loc["y_micrometer"],
            z=table_df.loc["z_micrometer"],
            x_length=table_df.loc["len_x_micrometer"],
            y_length=table_df.loc["len_y_micrometer"],
            z_length=table_df.loc["len_z_micrometer"],
            unit=SpaceUnits.micrometer,
            infos={
                "label": label,
                "source_label_path": self.source_label(get_full_path=True),
                "source_label": self.source_label(),
            },
        )
        return roi

    @property
    def rois(self) -> list[WorldCooROI]:
        """List all ROIs in the table."""
        return [self.get_roi(label) for label in self.list_labels]

    def consolidate(self) -> None:
        """Write the crrent state of the table to the Zarr file."""
        self._table_handler.consolidate(self.meta)
