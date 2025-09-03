class NGAdapter:
    country_code = "NG"
    currency = "NGN"
    units = "hectares"

    @staticmethod
    def normalize_address(address: str) -> str:
        return address.strip()

    @staticmethod
    def default_contract_template() -> str:
        return (
            "# Purchase Agreement (Nigeria)\n\n"
            "Buyer: {{buyer_name}}\n\n"
            "Seller: {{seller_name}}\n\n"
            "Parcel ID: {{parcel_id}}\n\n"
            "LGA/State: {{county}}, {{state}}\n\n"
            "Purchase Price: ₦{{price}} NGN\n\n"
            "Closing: {{closing_date}} at {{closing_location}}\n\n"
            "This agreement is governed by the laws of the Federal Republic of Nigeria.\n"
        )
