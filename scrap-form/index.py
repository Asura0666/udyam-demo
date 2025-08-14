import json
from bs4 import BeautifulSoup
import re

from udyam_page import FULL_UDYAM_REGISTRATION_HTML_CONTENT


def extract_label_text(element, global_soup):
    """
    Extracts the label text for a given form element.
    Prioritizes <label for="..."> (searching globally), then preceding <label>, then placeholder,
    then tries to infer from ID/name.
    """
    element_id = element.get("id")

    # 1. Check for <label for="element_id"> globally
    if element_id:
        label_tag = global_soup.find("label", {"for": element_id})
        if label_tag:
            return label_tag.get_text(strip=True).replace("/", " / ").strip()

    # 2. Check for preceding <label> sibling (directly within the current element's parents)
    # This covers cases where the label isn't 'for' but is physically before the input.
    label_tag = element.find_previous_sibling("label")
    if label_tag:
        return label_tag.get_text(strip=True).replace("/", " / ").strip()

    # 3. Fallback to placeholder (already extracted directly in scrape_full_form_schema)
    # This function's role is primarily to get the *label text*, not the placeholder content.
    # The placeholder content is extracted directly from the element where it's found.

    # 4. Attempt to infer from ASP.NET ID/name if all else fails
    field_name_attr = element.get("name") or element_id
    if field_name_attr:
        parts = field_name_attr.split("$")
        clean_name = (
            parts[-1]
            .replace("txt", "")
            .replace("ddl", "")
            .replace("rbl", "")
            .replace("chk", "")
        )
        inferred_label = re.sub(r"([a-z])([A-Z])", r"\1 \2", clean_name).strip()
        inferred_label = inferred_label.replace("No Of", "Number of")  # Common fix
        inferred_label = inferred_label.replace(
            "P H", "Physically Handicapped"
        )  # Specific fix
        if inferred_label:
            return inferred_label

    return "Unknown Field"  # Last resort


def is_field_required(element):
    """
    Checks if a field is required by looking for associated validation spans.
    Looks for any span within the same form-group or as a direct next sibling
    with 'color:Red' and text 'Required'.
    """
    parent_form_group = element.find_parent("div", class_="form-group")
    if parent_form_group:
        # Search within the immediate form-group for a required span
        required_span = parent_form_group.find(
            "span",
            style=lambda s: s
            and "color:red" in s.lower()
            and "display:none" not in s.lower(),
        )
        if required_span and required_span.get_text(strip=True).lower() == "required":
            return True

    # Fallback: check direct next sibling if not found in parent form group (less common for Udyam, but good for robustness)
    next_sibling = element.find_next_sibling()
    if next_sibling and next_sibling.name == "span":
        style = next_sibling.get("style", "").lower()
        text = next_sibling.get_text(strip=True).lower()
        if "color:red" in style and text == "required":
            return True

    return False


def scrape_full_form_schema():
    """
    Scrapes the entire Udyam registration form (Aadhaar, PAN, Udyam Details)
    from the provided static HTML content to identify fields and validation rules.
    """
    form_schema = {
        "steps": [
            {"step": 1, "name": "Aadhaar & OTP Verification", "fields": []},
            {"step": 2, "name": "PAN Verification", "fields": []},
            {"step": 3, "name": "Udyam Registration Details", "fields": []},
        ]
    }

    soup = BeautifulSoup(FULL_UDYAM_REGISTRATION_HTML_CONTENT, "html.parser")

    # Find the main section divs first
    aadhaar_section = soup.find("div", id="ctl00_ContentPlaceHolder1_divMainAadhaar")
    pan_section = soup.find("div", id="ctl00_ContentPlaceHolder1_divpanmain")
    udyam_details_section = soup.find(
        "div", id="ctl00_ContentPlaceHolder1_divpartb"
    )

    if not aadhaar_section:
        #     # Fallback to general search if the specific ID isn't found
        aadhaar_section = soup

    # --- Step 1: Aadhaar & OTP Verification Section ---
    print("Scraping form fields for Step 1: Aadhaar & OTP Verification...")
    aadhaar_fields = []

    # Directly find elements by their specific IDs/names as requested for Step 1
    aadhaar_input = aadhaar_section.find(
        "input", {"name": "ctl00$ContentPlaceHolder1$txtadharno"}
    )
    name_input = aadhaar_section.find(
        "input", {"name": "ctl00$ContentPlaceHolder1$txtownername"}
    )
    aadhaar_consent_checkbox = aadhaar_section.find(
        "input", {"name": "ctl00$ContentPlaceHolder1$chkDecarationA"}
    )
    otp_input = aadhaar_section.find(
        "input", {"name": "ctl00$ContentPlaceHolder1$txtotp"}
    )

    if aadhaar_input:
        aadhaar_fields.append(
            {
                "name": "aadhaarNumber",
                "label": extract_label_text(aadhaar_input, soup),
                "type": aadhaar_input.get("type") or "text",
                "placeholder": aadhaar_input.get("placeholder"),  # Added placeholder
                "validation": {
                    "required": is_field_required(aadhaar_input),
                    "maxlength": (
                        int(aadhaar_input.get("maxlength"))
                        if aadhaar_input.get("maxlength")
                        else None
                    ),
                    "pattern": "^\\d{12}$",  # Aadhaar is a 12-digit number
                },
            }
        )
    if name_input:
        aadhaar_fields.append(
            {
                "name": "entrepreneurName",
                "label": extract_label_text(name_input, soup),
                "type": name_input.get("type") or "text",
                "placeholder": name_input.get("placeholder"),  # Added placeholder
                "validation": {
                    "required": is_field_required(name_input),
                    "maxlength": (
                        int(name_input.get("maxlength"))
                        if name_input.get("maxlength")
                        else None
                    ),
                },
            }
        )
    if aadhaar_consent_checkbox:
        aadhaar_fields.append(
            {
                "name": "consent",
                "label": extract_label_text(aadhaar_consent_checkbox, soup),
                "type": "checkbox",
                "placeholder": aadhaar_consent_checkbox.get(
                    "placeholder"
                ),  # Added placeholder (will likely be None for checkbox)
                "validation": {
                    "required": is_field_required(aadhaar_consent_checkbox),
                    "checked": True,
                },
            }
        )
    if otp_input:  # OTP field is included if present in the HTML
        aadhaar_fields.append(
            {
                "name": "otp",
                "label": extract_label_text(otp_input, soup),
                "type": otp_input.get("type") or "text",
                "placeholder": otp_input.get("placeholder"),  # Added placeholder
                "validation": {
                    "required": is_field_required(otp_input),
                    "maxlength": (
                        int(otp_input.get("maxlength"))
                        if otp_input.get("maxlength")
                        else None
                    ),
                    "pattern": "^\\d{4,6}$",  # OTP usually 4-6 digits
                },
            }
        )
    form_schema["steps"][0]["fields"] = aadhaar_fields

    # --- Step 2: PAN Verification Section ---
    print("\nScraping form fields for Step 2: PAN Verification...")
    pan_fields = []
    seen_pan_field_names = set()

    # Iterate through form-group divs within the identified PAN section
    for form_group_div in pan_section.find_all("div", class_="form-group"):
        element = form_group_div.find(["input", "select", "textarea"])
        if not element:
            continue

        field_name = element.get("name")
        if not field_name or field_name in seen_pan_field_names:
            continue

        field_type = element.get("type") if element.name == "input" else element.name
        label = extract_label_text(element, soup)  # Pass global soup for label search

        field_info = {
            "name": field_name,
            "label": label,
            "type": field_type,
            "placeholder": element.get("placeholder"),  # Added placeholder
            "validation": {"required": is_field_required(element)},
        }

        if field_type == "radio":
            radio_group_inputs = form_group_div.find_all(
                "input", {"name": field_name, "type": "radio"}
            )
            radio_options = []
            for radio_input in radio_group_inputs:
                radio_label = soup.find(
                    "label", {"for": radio_input.get("id")}
                )  # Search globally for radio labels
                if radio_label:
                    radio_options.append(
                        {
                            "text": radio_label.get_text(strip=True),
                            "value": radio_input.get("value"),
                        }
                    )

            field_info["options"] = radio_options
            field_info["type"] = "radio"
            field_info["validation"]["required"] = any(
                is_field_required(ri) for ri in radio_group_inputs
            )
            for radio_input in radio_group_inputs:
                if radio_input.get("name"):
                    seen_pan_field_names.add(radio_input.get("name"))

        elif field_type == "select":
            options = [
                {"text": opt.get_text(strip=True), "value": opt.get("value")}
                for opt in element.find_all("option")
            ]
            field_info["options"] = options

        elif field_type == "checkbox":
            if element.get("checked") is not None:
                field_info["validation"]["checked"] = True

        if field_type in ["text", "number", "date", "email", "tel", "url", "textarea"]:
            maxlength = element.get("maxlength")
            if maxlength:
                try:
                    field_info["validation"]["maxlength"] = int(maxlength)
                except ValueError:
                    pass

            if "pan" in field_name.lower() and field_type == "text":
                field_info["validation"]["pattern"] = "^[A-Z]{5}[0-9]{4}[A-Z]{1}$"
            elif (
                field_type == "date"
                and (element.get("placeholder") or "").lower() == "dd/mm/yyyy"
            ):
                field_info["validation"]["pattern"] = "^\\d{2}/\\d{2}/\\d{4}$"
            # Add more specific patterns if needed for PAN section fields

        pan_fields.append(field_info)
        seen_pan_field_names.add(field_name)

    form_schema["steps"][1]["fields"] = pan_fields

    # --- Step 3: Udyam Registration Details Section ---
    print(
        "\nScraping form fields for Step 3: Udyam Registration Details (22+ questions)..."
    )
    udyam_details_fields = []
    seen_udyam_field_names = set()

    if udyam_details_section:  # Only process if section is found
        for form_group_div in udyam_details_section.find_all(
            "div", class_="form-group"
        ):
            element = form_group_div.find(["input", "select", "textarea"])
            if not element:
                continue

            field_name = element.get("name")
            if not field_name or field_name in seen_udyam_field_names:
                continue

            field_type = (
                element.get("type") if element.name == "input" else element.name
            )
            label = extract_label_text(
                element, soup
            )  # Pass global soup for label search

            field_info = {
                "name": field_name,
                "label": label,
                "type": field_type,
                "placeholder": element.get("placeholder"),  # Added placeholder
                "validation": {"required": is_field_required(element)},
            }

            if field_type == "radio":
                radio_group_inputs = form_group_div.find_all(
                    "input", {"name": field_name, "type": "radio"}
                )
                radio_options = []
                for radio_input in radio_group_inputs:
                    radio_label = soup.find(
                        "label", {"for": radio_input.get("id")}
                    )  # Search globally for radio labels
                    if radio_label:
                        radio_options.append(
                            {
                                "text": radio_label.get_text(strip=True),
                                "value": radio_input.get("value"),
                            }
                        )

                field_info["options"] = radio_options
                field_info["type"] = "radio"
                field_info["validation"]["required"] = any(
                    is_field_required(ri) for ri in radio_group_inputs
                )
                for radio_input in radio_group_inputs:
                    if radio_input.get("name"):
                        seen_udyam_field_names.add(radio_input.get("name"))

            elif field_type == "select":
                options = [
                    {"text": opt.get_text(strip=True), "value": opt.get("value")}
                    for opt in element.find_all("option")
                ]
                field_info["options"] = options

            elif field_type == "checkbox":
                if element.get("checked") is not None:
                    field_info["validation"]["checked"] = True

            if field_type in [
                "text",
                "number",
                "date",
                "email",
                "tel",
                "url",
                "textarea",
            ]:
                maxlength = element.get("maxlength")
                if maxlength:
                    try:
                        field_info["validation"]["maxlength"] = int(maxlength)
                    except ValueError:
                        pass

                # Add more specific patterns for Udyam details fields
                if "niccode" in field_name.lower() and field_type == "text":
                    field_info["validation"][
                        "pattern"
                    ] = "^\\d{5}$"  # Example pattern for NIC Code
                elif "investment" in field_name.lower() and field_type == "number":
                    field_info["validation"][
                        "pattern"
                    ] = "^\\d+(\\.\\d{1,2})?$"  # For decimal values like Lacs

            udyam_details_fields.append(field_info)
            seen_udyam_field_names.add(field_name)

    form_schema["steps"][2]["fields"] = udyam_details_fields

    # Output the result as a formatted JSON string
    print("\nGenerated Form Schema (JSON):")
    print(json.dumps(form_schema, indent=4, ensure_ascii=False))

    # Save the output to a file
    with open("udyam_form_schema.json", "w", encoding="utf-8") as f:
        json.dump(form_schema, f, indent=4, ensure_ascii=False)
        print("\nSchema saved to 'udyam_form_schema.json'")


if __name__ == "__main__":
    scrape_full_form_schema()


# def extract_label_text(element, soup_obj):
#     """
#     Extracts the label text for a given form element.
#     Prioritizes <label for="...">, then preceding <label>, then placeholder,
#     then tries to infer from ID/name.
#     """
#     element_id = element.get("id")
#     if element_id:
#         # Check for <label for="element_id"> within the same form-group or globally
#         label_tag = soup_obj.find("label", {"for": element_id})
#         if label_tag and label_tag.find_parent(
#             "div", class_="form-group"
#         ) == element.find_parent("div", class_="form-group"):
#             return label_tag.get_text(strip=True).replace("/", " / ").strip()
#         elif label_tag:  # Fallback to global label if not in same form-group
#             return label_tag.get_text(strip=True).replace("/", " / ").strip()

#     # Check for preceding <label> sibling within the same form-group
#     label_tag = element.find_previous_sibling("label")
#     if label_tag and label_tag.find_parent(
#         "div", class_="form-group"
#     ) == element.find_parent("div", class_="form-group"):
#         return label_tag.get_text(strip=True).replace("/", " / ").strip()
#     elif (
#         label_tag
#         and not element.find_previous_sibling("input")
#         and not element.find_previous_sibling("select")
#         and not element.find_previous_sibling("textarea")
#     ):
#         # This is a heuristic for labels that directly precede the input, not necessarily a sibling to the input itself.
#         # Check if the previous sibling isn't another input, to prevent misattributing labels.
#         return label_tag.get_text(strip=True).replace("/", " / ").strip()

#     # Fallback to placeholder
#     placeholder = element.get("placeholder")
#     if placeholder:
#         return (
#             placeholder.replace("Enter ", "")
#             .replace("Select ", "")
#             .replace("Your ", "")
#             .strip()
#         )

#     # Attempt to infer from ASP.NET ID/name if all else fails
#     field_name_attr = element.get("name") or element_id
#     if field_name_attr:
#         parts = field_name_attr.split("$")
#         clean_name = (
#             parts[-1]
#             .replace("txt", "")
#             .replace("ddl", "")
#             .replace("rbl", "")
#             .replace("chk", "")
#         )
#         inferred_label = re.sub(r"([a-z])([A-Z])", r"\1 \2", clean_name).strip()
#         inferred_label = inferred_label.replace("No Of", "Number of")  # Common fix
#         inferred_label = inferred_label.replace(
#             "P H", "Physically Handicapped"
#         )  # Specific fix
#         if inferred_label:
#             return inferred_label

#     return "Unknown Field"  # Last resort


# def is_field_required(element):
#     """
#     Checks if a field is required by looking for associated validation spans.
#     Looks for any span within the same form-group or as a direct next sibling
#     with 'color:Red' and text 'Required'.
#     """
#     parent_form_group = element.find_parent("div", class_="form-group")
#     if parent_form_group:
#         required_span = parent_form_group.find(
#             "span",
#             style=lambda s: s
#             and "color:red" in s.lower()
#             and "display:none" not in s.lower(),
#         )
#         if required_span and required_span.get_text(strip=True).lower() == "required":
#             return True

#     next_sibling = element.find_next_sibling()
#     if next_sibling and next_sibling.name == "span":
#         style = next_sibling.get("style", "").lower()
#         text = next_sibling.get_text(strip=True).lower()
#         if "color:red" in style and text == "required":
#             return True

#     return False


# def scrape_full_form_schema():
#     """
#     Scrapes the entire Udyam registration form (Aadhaar, PAN, Udyam Details)
#     from the provided static HTML content to identify fields and validation rules.
#     """
#     form_schema = {
#         "steps": [
#             {"step": 1, "name": "Aadhaar & OTP Verification", "fields": []},
#             {"step": 2, "name": "PAN Verification", "fields": []},
#             {"step": 3, "name": "Udyam Registration Details", "fields": []},
#         ]
#     }

#     soup = BeautifulSoup(FULL_UDYAM_REGISTRATION_HTML_CONTENT, "html.parser")

#     # Find the main section divs first
#     aadhaar_section = soup.find("div", id="ctl00_ContentPlaceHolder1_divMainAadhaar")
#     pan_section = soup.find("div", id="ctl00_ContentPlaceHolder1_divpanmain")
#     udyam_details_section = soup.find("div", id="ctl00_ContentPlaceHolder1_divpartb")

#     if not aadhaar_section:
#         # Fallback to general search if the specific ID isn't found
#         aadhaar_section = soup

#     print("Scraping form fields for Step 1: Aadhaar & OTP Verification...")
#     aadhaar_fields = []

#     # Directly find elements by their specific IDs/names as requested for Step 1
#     aadhaar_input = aadhaar_section.find(
#         "input", {"name": "ctl00$ContentPlaceHolder1$txtadharno"}
#     )
#     name_input = aadhaar_section.find(
#         "input", {"name": "ctl00$ContentPlaceHolder1$txtownername"}
#     )
#     aadhaar_consent_checkbox = aadhaar_section.find(
#         "input", {"name": "ctl00$ContentPlaceHolder1$chkDecarationA"}
#     )
#     otp_input = aadhaar_section.find(
#         "input", {"name": "ctl00$ContentPlaceHolder1$txtotp"}
#     )

#     if aadhaar_input:
#         aadhaar_fields.append(
#             {
#                 "name": "aadhaarNumber",
#                 "label": extract_label_text(aadhaar_input, soup),
#                 "type": aadhaar_input.get("type") or "text",
#                 "placeholder": aadhaar_input.get('placeholder'),
#                 "validation": {
#                     "required": is_field_required(aadhaar_input),
#                     "maxlength": (
#                         int(aadhaar_input.get("maxlength"))
#                         if aadhaar_input.get("maxlength")
#                         else None
#                     ),
#                     "pattern": "^\\d{12}$",  # Aadhaar is a 12-digit number
#                 },
#             }
#         )
#     if name_input:
#         aadhaar_fields.append(
#             {
#                 "name": "entrepreneurName",
#                 "label": extract_label_text(name_input, soup),
#                 "type": name_input.get("type") or "text",
#                 "validation": {
#                     "required": is_field_required(name_input),
#                     "maxlength": (
#                         int(name_input.get("maxlength"))
#                         if name_input.get("maxlength")
#                         else None
#                     ),
#                 },
#             }
#         )
#     if aadhaar_consent_checkbox:
#         aadhaar_fields.append(
#             {
#                 "name": "consent",
#                 "label": extract_label_text(aadhaar_consent_checkbox, soup),
#                 "type": "checkbox",
#                 "validation": {
#                     "required": is_field_required(aadhaar_consent_checkbox),
#                     "checked": True,
#                 },
#             }
#         )
#     if otp_input:  # OTP field is included if present in the HTML
#         aadhaar_fields.append(
#             {
#                 "name": "otp",
#                 "label": extract_label_text(otp_input, soup),
#                 "type": otp_input.get("type") or "text",
#                 "validation": {
#                     "required": is_field_required(otp_input),
#                     "maxlength": (
#                         int(otp_input.get("maxlength"))
#                         if otp_input.get("maxlength")
#                         else None
#                     ),
#                     "pattern": "^\\d{4,6}$",  # OTP usually 4-6 digits
#                 },
#             }
#         )
#     form_schema["steps"][0]["fields"] = aadhaar_fields

#     # --- Step 2: PAN Verification Section ---
#     print("\nScraping form fields for Step 2: PAN Verification...")
#     pan_fields = []
#     seen_pan_field_names = set()

#     if pan_section:  # Only process if section is found
#         # Iterate through form-group divs within the identified PAN section
#         for form_group_div in pan_section.find_all("div", class_="form-group"):
#             element = form_group_div.find(["input", "select", "textarea"])
#             if not element:
#                 continue

#             field_name = element.get("name")
#             if not field_name or field_name in seen_pan_field_names:
#                 continue

#             field_type = (
#                 element.get("type") if element.name == "input" else element.name
#             )
#             label = extract_label_text(element, soup)

#             field_info = {
#                 "name": field_name,
#                 "label": label,
#                 "type": field_type,
#                 "validation": {"required": is_field_required(element)},
#             }

#             if field_type == "radio":
#                 radio_group_inputs = form_group_div.find_all(
#                     "input", {"name": field_name, "type": "radio"}
#                 )
#                 radio_options = []
#                 for radio_input in radio_group_inputs:
#                     radio_label = form_group_div.find(
#                         "label", {"for": radio_input.get("id")}
#                     )
#                     if radio_label:
#                         radio_options.append(
#                             {
#                                 "text": radio_label.get_text(strip=True),
#                                 "value": radio_input.get("value"),
#                             }
#                         )

#                 field_info["options"] = radio_options
#                 field_info["type"] = "radio"
#                 field_info["validation"]["required"] = any(
#                     is_field_required(ri) for ri in radio_group_inputs
#                 )
#                 for radio_input in radio_group_inputs:
#                     if radio_input.get("name"):
#                         seen_pan_field_names.add(radio_input.get("name"))

#             elif field_type == "select":
#                 options = [
#                     {"text": opt.get_text(strip=True), "value": opt.get("value")}
#                     for opt in element.find_all("option")
#                 ]
#                 field_info["options"] = options

#             elif field_type == "checkbox":
#                 if element.get("checked") is not None:
#                     field_info["validation"]["checked"] = True

#             if field_type in [
#                 "text",
#                 "number",
#                 "date",
#                 "email",
#                 "tel",
#                 "url",
#                 "textarea",
#             ]:
#                 maxlength = element.get("maxlength")
#                 if maxlength:
#                     try:
#                         field_info["validation"]["maxlength"] = int(maxlength)
#                     except ValueError:
#                         pass

#                 if "pan" in field_name.lower() and field_type == "text":
#                     field_info["validation"]["pattern"] = "^[A-Z]{5}[0-9]{4}[A-Z]{1}$"
#                 elif (
#                     field_type == "date"
#                     and (element.get("placeholder") or "").lower() == "dd/mm/yyyy"
#                 ):
#                     field_info["validation"]["pattern"] = "^\\d{2}/\\d{2}/\\d{4}$"
#                 # Add more specific patterns if needed for PAN section fields

#             pan_fields.append(field_info)
#             seen_pan_field_names.add(field_name)

#     form_schema["steps"][1]["fields"] = pan_fields

#     # --- Step 3: Udyam Registration Details Section ---
#     print(
#         "\nScraping form fields for Step 3: Udyam Registration Details (22+ questions)..."
#     )
#     udyam_details_fields = []
#     seen_udyam_field_names = set()

#     if udyam_details_section:  # Only process if section is found
#         for form_group_div in udyam_details_section.find_all(
#             "div", class_="form-group"
#         ):
#             element = form_group_div.find(["input", "select", "textarea"])
#             if not element:
#                 continue

#             field_name = element.get("name")
#             if not field_name or field_name in seen_udyam_field_names:
#                 continue

#             field_type = (
#                 element.get("type") if element.name == "input" else element.name
#             )
#             label = extract_label_text(element, soup)

#             field_info = {
#                 "name": field_name,
#                 "label": label,
#                 "type": field_type,
#                 "validation": {"required": is_field_required(element)},
#             }

#             if field_type == "radio":
#                 radio_group_inputs = form_group_div.find_all(
#                     "input", {"name": field_name, "type": "radio"}
#                 )
#                 radio_options = []
#                 for radio_input in radio_group_inputs:
#                     radio_label = form_group_div.find(
#                         "label", {"for": radio_input.get("id")}
#                     )
#                     if radio_label:
#                         radio_options.append(
#                             {
#                                 "text": radio_label.get_text(strip=True),
#                                 "value": radio_input.get("value"),
#                             }
#                         )

#                 field_info["options"] = radio_options
#                 field_info["type"] = "radio"
#                 field_info["validation"]["required"] = any(
#                     is_field_required(ri) for ri in radio_group_inputs
#                 )
#                 for radio_input in radio_group_inputs:
#                     if radio_input.get("name"):
#                         seen_udyam_field_names.add(radio_input.get("name"))

#             elif field_type == "select":
#                 options = [
#                     {"text": opt.get_text(strip=True), "value": opt.get("value")}
#                     for opt in element.find_all("option")
#                 ]
#                 field_info["options"] = options

#             elif field_type == "checkbox":
#                 if element.get("checked") is not None:
#                     field_info["validation"]["checked"] = True

#             if field_type in [
#                 "text",
#                 "number",
#                 "date",
#                 "email",
#                 "tel",
#                 "url",
#                 "textarea",
#             ]:
#                 maxlength = element.get("maxlength")
#                 if maxlength:
#                     try:
#                         field_info["validation"]["maxlength"] = int(maxlength)
#                     except ValueError:
#                         pass

#                 # Add more specific patterns for Udyam details fields
#                 if "niccode" in field_name.lower() and field_type == "text":
#                     field_info["validation"][
#                         "pattern"
#                     ] = "^\\d{5}$"  # Example pattern for NIC Code
#                 elif "investment" in field_name.lower() and field_type == "number":
#                     field_info["validation"][
#                         "pattern"
#                     ] = "^\\d+(\\.\\d{1,2})?$"  # For decimal values like Lacs

#             udyam_details_fields.append(field_info)
#             seen_udyam_field_names.add(field_name)

#     form_schema["steps"][2]["fields"] = udyam_details_fields

#     # Output the result as a formatted JSON string
#     print("\nGenerated Form Schema (JSON):")
#     print(json.dumps(form_schema, indent=4, ensure_ascii=False))

#     # Save the output to a file
#     with open("udyam_form_schema.json", "w", encoding="utf-8") as f:
#         json.dump(form_schema, f, indent=4, ensure_ascii=False)
#         print("\nSchema saved to 'udyam_form_schema.json'")


# if __name__ == "__main__":
#     scrape_full_form_schema()
