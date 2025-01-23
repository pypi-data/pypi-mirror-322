from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .education_synchronization_customizations import EducationSynchronizationCustomizations
    from .education_synchronization_data_provider import EducationSynchronizationDataProvider

from .education_synchronization_data_provider import EducationSynchronizationDataProvider

@dataclass
class EducationCsvDataProvider(EducationSynchronizationDataProvider, Parsable):
    # The OdataType property
    odata_type: Optional[str] = "#microsoft.graph.educationCsvDataProvider"
    # The customizations property
    customizations: Optional[EducationSynchronizationCustomizations] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> EducationCsvDataProvider:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: EducationCsvDataProvider
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return EducationCsvDataProvider()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .education_synchronization_customizations import EducationSynchronizationCustomizations
        from .education_synchronization_data_provider import EducationSynchronizationDataProvider

        from .education_synchronization_customizations import EducationSynchronizationCustomizations
        from .education_synchronization_data_provider import EducationSynchronizationDataProvider

        fields: dict[str, Callable[[Any], None]] = {
            "customizations": lambda n : setattr(self, 'customizations', n.get_object_value(EducationSynchronizationCustomizations)),
        }
        super_fields = super().get_field_deserializers()
        fields.update(super_fields)
        return fields
    
    def serialize(self,writer: SerializationWriter) -> None:
        """
        Serializes information the current object
        param writer: Serialization writer to use to serialize this model
        Returns: None
        """
        if writer is None:
            raise TypeError("writer cannot be null.")
        super().serialize(writer)
        writer.write_object_value("customizations", self.customizations)
    

