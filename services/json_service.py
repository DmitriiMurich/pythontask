# Function to parse conditions into a list
def parse_conditions(condition_str):
    conditions = []
    if condition_str:
        cond_parts = condition_str.split(',')
        for part in cond_parts:
            condition_type, value = part.split('=')
            conditions.append({'type': condition_type, 'value': value})
    return conditions

# Function to parse highlights into a list, taking color into account
def parse_highlights(highlight_str):
    highlights = []
    if highlight_str:
        highlight_parts = highlight_str.split(',')
        for part in highlight_parts:
            if '=' in part:
                highlight_info = part.split('=')
                if len(highlight_info) == 3:  # If color highlighting is specified
                    condition_type, value, color = highlight_info
                    highlights.append({'type': condition_type, 'value': value, 'color': color})
                else:
                    condition_type, value = highlight_info
                    highlights.append({'type': condition_type, 'value': value, 'color': ''})
    return highlights

# Main function to transform table data into JSON
def transform_table_to_json(table, websocket_response, base_ws):
    result = {'columns': [], 'conditions_data': {}, 'color_conditions': {}, 'module': 'SO'}

    for index, row in enumerate(table):
        # Add column with index and sort order
        column_view = row['Columns View']
        if column_view in websocket_response:
            column_data = websocket_response[column_view]
            result['columns'].append({'index': column_data['index'], 'sort': index})

            # Add sorting
            if row['Sort By']:
                result['order_by'] = {'direction': row['Sort By'], 'index': column_data['index']}

            # Process conditions
            conditions = parse_conditions(row['Condition'])
            if conditions:
                result['conditions_data'].setdefault(column_data['filter'], []).extend(conditions)

            # Process highlights
            highlights = parse_highlights(row['Highlight By'])
            if highlights:
                result['color_conditions'].setdefault(column_data['filter'], []).extend(highlights)

        # Add other parameters (page_size, row_height)
        if row['Lines per page']:
            result['page_size'] = row['Lines per page']
        if row['Row Height']:
            result['row_height'] = row['Row Height']

    # Transform keys according to base_ws
    final_result = {}
    for key, ws_key in base_ws.items():
        if ws_key in result:
            final_result[ws_key] = result[ws_key]

    return result
