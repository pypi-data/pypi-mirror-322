"""Module for handling the /tables group in an OME-NGFF file."""

from typing import Literal
from warnings import warn

import zarr
from pydantic import ValidationError

from ngio.core.utils import State
from ngio.io import AccessModeLiteral, StoreLike
from ngio.tables.v1 import FeatureTableV1, MaskingROITableV1, ROITableV1
from ngio.utils import ngio_logger
from ngio.utils._pydantic_utils import BaseWithExtraFields

ROITable = ROITableV1
IMPLEMENTED_ROI_TABLES = {"1": ROITableV1}

FeatureTable = FeatureTableV1
IMPLEMENTED_FEATURE_TABLES = {"1": FeatureTableV1}

MaskingROITable = MaskingROITableV1
IMPLEMENTED_MASKING_ROI_TABLES = {"1": MaskingROITableV1}

Table = ROITable | FeatureTable | MaskingROITable

TableType = Literal["roi_table", "feature_table", "masking_roi_table"]


class CommonMeta(BaseWithExtraFields):
    """Common metadata for all tables."""

    type: TableType
    fractal_table_version: str = "1"


def _find_table_impl(
    table_type: TableType,
    version: str,
) -> Table:
    """Find the type of table in the group."""
    if table_type == "roi_table":
        if version not in IMPLEMENTED_ROI_TABLES:
            raise ValueError(f"ROI Table version {version} not implemented.")
        return IMPLEMENTED_ROI_TABLES[version]

    elif table_type == "feature_table":
        if version not in IMPLEMENTED_FEATURE_TABLES:
            raise ValueError(f"Feature Table version {version} not implemented.")
        return IMPLEMENTED_FEATURE_TABLES[version]

    elif table_type == "masking_roi_table":
        if version not in IMPLEMENTED_MASKING_ROI_TABLES:
            raise ValueError(f"Masking ROI Table version {version} not implemented.")
        return IMPLEMENTED_MASKING_ROI_TABLES[version]

    else:
        raise ValueError(f"Table type {table_type} not recognized.")


def _get_table_impl(
    group: zarr.Group,
    name: str,
    validate_metadata: bool = True,
    table_type: TableType | None = None,
    validate_table: bool = True,
    index_key: str | None = None,
) -> Table:
    if validate_metadata:
        common_meta = CommonMeta(**group.attrs)
        table_type = common_meta.type
    else:
        common_meta = CommonMeta.model_construct(**group.attrs)
        if table_type is None:
            raise ValueError(
                "Table type must be provided if metadata is not validated."
            )

    version = common_meta.fractal_table_version
    return _find_table_impl(table_type=table_type, version=version)(
        group=group,
        name=name,
        validate_metadata=validate_metadata,
        validate_table=validate_table,
        index_key=index_key,
    )


class TableGroup:
    """A class to handle the /labels group in an OME-NGFF file."""

    def __init__(
        self, group: StoreLike | zarr.Group, mode: AccessModeLiteral = "r+"
    ) -> None:
        """Initialize the LabelGroupHandler."""
        self._mode = mode
        if not isinstance(group, zarr.Group):
            group = zarr.open_group(group, mode=self._mode)

        table_group = group.get("tables", None)

        if table_group is None and not group.read_only:
            table_group = group.create_group("tables")
            table_group.attrs["tables"] = []

        assert isinstance(table_group, zarr.Group) or table_group is None
        self._table_group = table_group

        if table_group is None or table_group.read_only:
            self._state = State.MEMORY
        else:
            self._state = State.CONSOLIDATED

        self._virtual_tables: list[Table] = []

    def _validate_list_of_tables(self, list_of_tables: list[str]) -> None:
        """Validate the list of tables.

        Args:
            list_of_tables (list[str]): The list of tables to validate.
        """
        if self._table_group is None:
            return None

        for table_name in list_of_tables:
            table = self._table_group.get(table_name, None)
            if table is None:
                ngio_logger.warning(
                    f"Table {table_name} not found in the group. "
                    "Consider removing it from the list of tables."
                )

    def _get_list_of_tables(self) -> list[str]:
        """Return the list of tables."""
        if self._table_group is None:
            return []

        list_of_tables = self._table_group.attrs.get("tables", [])
        self._validate_list_of_tables(list_of_tables)
        assert isinstance(list_of_tables, list)
        assert all(isinstance(table_name, str) for table_name in list_of_tables)
        return list_of_tables

    def list(
        self,
        table_type: TableType | None = None,
    ) -> list[str]:
        """List all labels in the group.

        Args:
            table_type (str): The type of table to list.
                If None, all tables are listed.
                Allowed values are: 'roi_table', 'feature_table', 'masking_roi_table'.
        """
        if self._table_group is None:
            return []

        list_of_tables = self._get_list_of_tables()
        self._validate_list_of_tables(list_of_tables=list_of_tables)

        all_table_types = ["roi_table", "feature_table", "masking_roi_table"]

        if table_type is None:
            return list_of_tables

        else:
            if table_type not in all_table_types:
                raise ValueError(
                    f"Table type {table_type} not recognized. "
                    f" Allowed values are: {all_table_types}"
                )
            list_of_typed_tables = []
            for table_name in list_of_tables:
                table = self._table_group[table_name]
                try:
                    common_meta = CommonMeta(**table.attrs)
                    if common_meta.type == table_type:
                        list_of_typed_tables.append(table_name)
                except ValidationError:
                    warn(
                        f"Table {table_name} metadata is not correctly formatted.",
                        stacklevel=1,
                    )
            return list_of_typed_tables

    def get_table(
        self,
        name: str,
        table_type: TableType | None = None,
        validate_metadata: bool = True,
        validate_table: bool = True,
        index_key: str | None = None,
    ) -> Table:
        """Get a label from the group.

        Args:
            name (str): The name of the table to get.
            table_type (str): The type of table to get.
                If None, all the table type will be inferred from the metadata.
                Allowed values are: 'roi_table', 'feature_table', 'masking_roi_table'.
            validate_metadata (bool): Whether to validate the metadata of the table.
            validate_table (bool): Whether to validate the table.
            index_key (str): The column name to use as the index of the DataFrame.
                This is usually defined in the metadata of the table, if given here,
                it will overwrite the metadata.
        """
        if self._table_group is None:
            raise ValueError("No tables group found in the group.")

        list_of_tables = self._get_list_of_tables()
        if name not in list_of_tables:
            raise ValueError(f"Table {name} not found in the group.")

        return _get_table_impl(
            group=self._table_group[name],
            name=name,
            validate_metadata=validate_metadata,
            table_type=table_type,
            validate_table=validate_table,
            index_key=index_key,
        )

    def new(
        self,
        name: str,
        table_type: TableType = "roi_table",
        overwrite: bool = False,
        version: str = "1",
        **type_specific_kwargs: dict,
    ) -> Table:
        """Add a new table to the group."""
        if self._table_group is None:
            raise ValueError("No tables group found in the group.")

        list_of_tables = self._get_list_of_tables()
        if not overwrite and name in list_of_tables:
            raise ValueError(f"Table {name} already exists in the group.")

        if overwrite and name in list_of_tables:
            list_of_tables.remove(name)

        table_impl = _find_table_impl(table_type=table_type, version=version)
        new_table = table_impl._new(
            parent_group=self._table_group,
            name=name,
            overwrite=overwrite,
            **type_specific_kwargs,
        )

        self._table_group.attrs["tables"] = [*list_of_tables, name]

        assert isinstance(new_table, ROITable | FeatureTable | MaskingROITable)
        return new_table
