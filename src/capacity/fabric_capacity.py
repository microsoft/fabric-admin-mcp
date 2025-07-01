class FabricCapacity:
    def __init__(self, raw):
        self.raw = raw
        self.id = self._get('id')
        self.name = self._get('name')
        self.type = self._get('type')
        self.location = self._get('location')
        self.sku = self._get('sku', {})
        self.tags = self._get('tags', {})
        self.properties = self._get('properties', {})
        self.resource_group = self._extract_resource_group()
        self.state = self.properties.get('state')
        self.provisioning_state = self.properties.get('provisioningState')
        self.administrators = self.properties.get('administration', {}).get('members', [])
        self.sku_name = self.sku.get('name')
        self.sku_tier = self.sku.get('tier')

    def _get(self, key, default=None):
        if isinstance(self.raw, dict):
            return self.raw.get(key, default)
        return getattr(self.raw, key, default)

    def _extract_resource_group(self):
        """Extract the resource group from the ID. Not the ideal solution, but simplifies for now"""
        id_val = self.id
        if id_val and "/resourceGroups/" in id_val:
            try:
                return id_val.split("/resourceGroups/")[1].split("/")[0]
            except Exception:
                return None
        return None

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "location": self.location,
            "sku": self.sku,
            "tags": self.tags,
            "properties": self.properties,
            "resource_group": self.resource_group,
            "administrators": self.administrators,
            "state": self.state,
            "provisioningState": self.provisioning_state,
            "sku_name": self.sku_name,
            "sku_tier": self.sku_tier,
        }
