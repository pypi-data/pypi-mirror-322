from typing import Any, Optional

class MBTARoute:
    """A route object to hold information about a route."""

    ROUTE_TYPES= {
        # 0: 'Light Rail',   # Example: Green Line
        # 1: 'Heavy Rail',   # Example: Red Line
        0: 'Subway (Light Rail)',   
        1: 'Subway (Heavy Rail)',  
        2: 'Commuter Rail',
        3: 'Bus',
        4: 'Ferry'
    }
    
    def __init__(self, route: dict[ str, Any]) -> None:
        # ID
        self.id:  Optional[str] = route.get('id', None)
        
        # Attributes
        attributes = route.get('attributes', {})
        self.type: Optional[str] = attributes.get('type', None)
        self.text_color: Optional[str] = attributes.get('text_color', None)
        self.sort_order: Optional[int] = attributes.get('sort_order', None)
        self.short_name: Optional[str] = attributes.get('short_name', None)
        self.long_name: Optional[str] = attributes.get('long_name', None)
        self.fare_class: Optional[str] = attributes.get('fare_class', None)
        self.direction_names: list[Optional[str]] = attributes.get('direction_names', [])
        self.direction_destinations: list[Optional[str]] = attributes.get('direction_destinations', [])
        self.description: Optional[str] = attributes.get('description', None)
        self.color: Optional[str] = attributes.get('color', None)

    def __repr__(self) ->  Optional[str]:
        return (f"MBTAroute(id={self.id}, long_name={self.long_name})")

    @staticmethod
    def get_route_type_desc_by_type_id(route_type: int) ->  Optional[str]:
        """Get a description of the route type."""
        return MBTARoute.ROUTE_TYPES.get(route_type, 'Unknown')