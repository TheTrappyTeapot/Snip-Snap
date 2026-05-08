#!/usr/bin/env python3
"""Add barbershop tests to new_test_plan.csv"""

# Barbershop tests to add (IDs 217-239)
barbershop_tests = [
    (217, 'Barbershop Page Loads', 'Page Loading', 'Open /barbershop/1', 'Page loads successfully', 'Verify barbershop profile page loads', 'v', 'PASS', 'test_barbershop_page_loads_with_valid_id'),
    (218, 'Invalid ID Handling', 'Error Handling', 'Open /barbershop/99999', 'Display error message', 'Handle non-existent barbershop', 'i', 'PASS', 'test_barbershop_page_handles_invalid_id'),
    (219, 'Header Section', 'Shop Info', 'Open /barbershop/1', 'Shop name and location display', 'Check header displays correctly', 'v', 'PASS', 'test_barbershop_page_header_section'),
    (220, 'Opening Hours Display', 'Working Hours', 'Open /barbershop/1', 'Opening hours display', 'Check hours loads', 'v', 'PASS', 'test_shop_opening_hours_display'),
    (221, 'Current Day Highlight', 'Working Hours', 'Open /barbershop/1', 'Current day highlighted', 'Check today is highlighted', 'v', 'PASS', 'test_shop_hours_current_day_highlight'),
    (222, 'Phone Number Display', 'Contact Info', 'Open /barbershop/1', 'Phone number displays', 'Check phone loads', 'v', 'PASS', 'test_shop_phone_number_display'),
    (223, 'Website Link', 'Contact Info', 'Open /barbershop/1', 'Website link displays', 'Check website link loads', 'v', 'PASS', 'test_shop_website_link_display'),
    (224, 'Map Widget', 'Location', 'Open /barbershop/1', 'Map widget shows location', 'Check map loads', 'v', 'PASS', 'test_shop_location_map_widget'),
    (225, 'Reviews Load', 'Reviews', 'Open /barbershop/1', 'Reviews display', 'Check reviews load', 'v', 'PASS', 'test_barbershop_reviews_load'),
    (226, 'Average Rating', 'Reviews', 'Open /barbershop/1', 'Average rating displays', 'Check rating loads', 'v', 'PASS', 'test_barbershop_average_rating_display'),
    (227, 'No Reviews Message', 'Reviews', 'Open /barbershop/1', 'No reviews message', 'Check empty reviews', 'i', 'PASS', 'test_barbershop_no_reviews_message'),
    (228, 'Gallery With Photos', 'Gallery', 'Open /barbershop/1', 'Gallery displays photos', 'Check gallery loads', 'v', 'PASS', 'test_barbershop_gallery_loads_with_photos'),
    (229, 'Gallery Many Photos', 'Gallery', 'Open /barbershop/1', 'Gallery displays 16+ photos', 'Check large gallery', 'v', 'PASS', 'test_barbershop_gallery_with_many_photos'),
    (230, 'Gallery Empty Message', 'Gallery', 'Open /barbershop/1', 'No gallery message', 'Check empty gallery', 'i', 'PASS', 'test_barbershop_gallery_empty_message'),
    (231, 'Lists All Barbers', 'Barbers', 'Open /barbershop/1', 'All barbers display', 'Check barber list', 'v', 'PASS', 'test_barbershop_lists_all_barbers'),
    (232, 'Barber Links', 'Barbers', 'Open /barbershop/1', 'Links are clickable', 'Check barber links', 'v', 'PASS', 'test_barbershop_barber_links_clickable'),
    (233, 'Empty Barbers Message', 'Barbers', 'Open /barbershop/1', 'No barbers message', 'Check empty barbers', 'i', 'PASS', 'test_barbershop_empty_barbers_message'),
    (234, 'Customer Access', 'Access Control', 'Customer opens /barbershop/1', 'Page loads', 'Check customer access', 'v', 'PASS', 'test_barbershop_page_accessible_to_customers'),
    (235, 'Guest Access', 'Access Control', 'Guest opens /barbershop/1', 'Page loads', 'Check guest access', 'v', 'PASS', 'test_barbershop_page_accessible_to_guests'),
    (236, 'Barber Access', 'Access Control', 'Barber opens /barbershop/1', 'Page loads', 'Check barber access', 'v', 'PASS', 'test_barbershop_page_accessible_to_barbers'),
    (237, 'Invalid ID String', 'Error Handling', 'Open /barbershop/abc', 'Page handles error', 'Handle invalid ID format', 'i', 'PASS', 'test_barbershop_profile_with_string_id'),
    (238, 'Invalid ID Format', 'Error Handling', 'Open /barbershop/invalid', 'Page loads or redirects', 'Handle invalid format', 'i', 'PASS', 'test_barbershop_profile_with_invalid_id'),
    (239, 'Support: Page Loads', 'Support', 'Open /barbershop/1', 'Page loads', 'Support test', 'v', 'PASS', 'test_barbershop_profile_page_loads'),
]

# Read existing CSV
with open('app/automated_tests/new_test_plan.csv', 'r', encoding='utf-8') as f:
    content = f.read()

# Append barbershop section
barbershop_section = '\n,Barbershop Profile,-,-,-,-,-,-,-\n'
for test_id, func, partition, inputs, outputs, desc, valid, status, test_name in barbershop_tests:
    barbershop_section += f'{test_id},{func},{partition},"{inputs}",{outputs},{desc},{valid},{status},{test_name}\n'

with open('app/automated_tests/new_test_plan.csv', 'w', encoding='utf-8') as f:
    f.write(content + barbershop_section)

print('✅ Barbershop tests added to new_test_plan.csv (IDs 217-239)')
