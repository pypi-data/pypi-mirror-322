from pathlib import Path

from ._assonant_data_retriever_interface import IAssonantDataRetriever
from ._csv_data_retriever import CSVDataRetriever
from .enums import DataSourceFileFormat
from .exceptions import AssonantDataRetrieverError


class DataRetrieverFactory:
    """Data Retriever Factory.

    Class that implements the factory design pattern
    (https://refactoring.guru/design-patterns/factory-method) to fully abstract
    the procedure of creating Assonant Data Retrievers.
    """

    def create_data_retriever(self, data_source_file_path: str) -> IAssonantDataRetriever:
        """Public method that abstracts data retriever creation process for the factory user.

        Internally, this method deals with validation and specific Data Retriever
        creation

        Args:
            data_source_file_path (str): Path to data source file.

        Raises:
            AssonantDataRetrieverError: An error occured during the creation of
            the respective Data Retriever.

        Returns:
            IAssonantDataRetriever: Data Retriever instance which implements the
            IAssonantDataRetriever interface for the given data_source_file_format.
        """
        file_format = self._get_file_format(data_source_file_path)

        self._validate_file_format(file_format)

        if file_format == DataSourceFileFormat.CSV.value:
            return self._create_csv_data_retriever(data_source_file_path)

        raise AssonantDataRetrieverError(
            f"'{file_format}' file format is set as supported but its creation method is not implemented."
        )

    def _create_csv_data_retriever(self, data_source_file_path: str) -> CSVDataRetriever:
        return CSVDataRetriever(csv_file_path=data_source_file_path)

    def _validate_file_format(self, file_format: str):
        """Check if file format is supported

        Args:
            file_format (str): Data source file format extension.

        Raises:
            AssonantDataRetrieverError: File format is not supported
        """

        if file_format not in DataSourceFileFormat._value2member_map_:
            raise AssonantDataRetrieverError(f"'{file_format}' is not supported by Data Retriever!")

    def _get_file_format(self, data_source_file_path: str) -> str:
        """Get file extension from given path

        Args:
            data_source_file_path (str): Path to data source file.

        Raises:
            AssonantDataRetrieverError: Erro raised if path passed is not from a file.

        Returns:
            str: File extesion without '.' character.
        """

        with Path(data_source_file_path) as path:
            if path.is_file():
                # Get file extension and remove the '.' character
                return path.suffix[1:]
            else:
                raise AssonantDataRetrieverError(f"'{data_source_file_path}' is not a file!")
