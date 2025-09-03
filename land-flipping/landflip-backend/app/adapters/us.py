class USAdapter:
    country_code = "US"
    currency = "USD"
    units = "acres"

    @staticmethod
    def normalize_address(address: str) -> str:
        return address.strip()

    @staticmethod
    def default_contract_template() -> str:
        return (
            "# Purchase Agreement\n\n"
            "Buyer: {{buyer_name}}\n\n"
            "Seller: {{seller_name}}\n\n"
            "Parcel ID: {{parcel_id}} (APN: {{apn}})\n\n"
            "County/State: {{county}}, {{state}}\n\n"
            "Purchase Price: ${{price}} USD\n\n"
            "Closing: {{closing_date}} at {{closing_location}}\n\n"
            "This agreement is governed by the laws of the state of {{state}}.\n"
        )
