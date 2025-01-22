import os
import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        "streamlit_pivottable",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    if not os.path.exists(build_dir):
        raise FileNotFoundError(f"Frontend build directory not found: {build_dir}")
    _component_func = components.declare_component("Streamlit_pivottable", path=build_dir)


def streamlit_pivottable(name="streamlit_pivottable", data=None, show_render_option=True, default_settings = {
   "rows":[],
   "cols":[],
   "aggregatorName":"Count",
   "vals":[],
   "rendererName":"Table",
   "rowOrder":"",
   "colOrder":"",
   "valueFilter":{},
   "hiddenAttributes":[],
   "hiddenFromAggregators":[],
   "hiddenFromDragDrop":[],
   "menuLimit":500,
   "unusedOrientationCutoff":85
},style_config = {
    # General UI Colors
    "uiTextColor": "",

    # Table Headers
    "headerBackgroundColor": "",
    "headerBorderColor": "",

    # Table Cells
    "cellTextColor": "",
    "cellBackgroundColor": "",
    "cellBorderColor": "",

    # Totals
    "totalTextColor": "",
    "totalBackgroundColor": "",

    # Axis and Attributes
    "axisBorderColor": "",
    "axisBackgroundColor": "",
    "axisPlaceholderBorderColor": "",
    "attrBackgroundColor": "",
    "attrBorderColor": "",

    # Dropdown
    "dropdownIconColor": "",
    "dropdownMenuBackgroundColor": "",
    "dropdownMenuBorderColor": "",
    "dropdownMenuTopBorderColor": "",
    "dropdownActiveBackgroundColor": "",

    # Triangle
    "triangleColor": "",

    # Drag Handle
    "dragHandleColor": "",

    # Buttons
    "buttonTextColor": "",
    "buttonBackgroundColor": "",
    "buttonBorderColor": "",
    "buttonHoverBackgroundColor": "",
    "buttonHoverBorderColor": "",
    "buttonActiveBackgroundColor": "",

    # Filter Box
    "filterBoxBackgroundColor": "",
    "filterBoxBorderColor": "",
    "filterBoxInputTextColor": "",
    "filterBoxInputFocusBorderColor": "",
    "filterBoxHeaderColor": "",
    "filterBoxButtonTextColor": "",

    # Check Container
    "checkContainerBorderColor": "",
    "selectedItemBackgroundColor": "",

    # Render Table Option
    "optionTableBorderColor": "",
    "optionTableBackgroundColor": "",
}
, height=100, width=100, use_container_width=False, key="streamlit-pivottable"):

    """
    Parameters:
    1. name (str): 
       - A string representing the name or title of the pivot table. 
       - Used to identify the component, often displayed as a header or label.
       - Default: "streamlit_pivottable".

    2. data (list): 
       - A list containing the dataset for the pivot table. 
       - Each item in the list represents a row, where the first sublist defines the headers (columns).
       - Example:
         [
             ["Name", "Age", "City"],
             ["Alice", 30, "New York"],
             ["Bob", 25, "Los Angeles"]
         ]
       - Default: None (initializes to an empty list).

    3. height (int): 
       - An integer representing the height of the pivot table in rem units.
       - Determines how much vertical space the pivot table occupies.
       - Default: 100 (which typically translates to 1600px if 1rem = 16px).

    4. use_container_width (bool): 
       - A boolean that specifies whether the pivot table should stretch to fit the full width of the container.
       - If `True`, the pivot table will take up the entire width of its parent container.
       - If `False`, it uses its default or explicitly set width.
       - Default: False.

    5 key (str or None): 
       - An optional string to uniquely identify this Streamlit component.
       - Useful for maintaining state across reruns of the Streamlit app, especially if you have multiple instances of the component.
       - Default: None.

    Pivot Table Configuration:

    - **rows** (`list`): A list of attribute names to be used as rows in the pivot table.
    - Example: `['Customer Type']` sets "Customer Type" as the row dimension.

    - **cols** (`list`): A list of attribute names to be used as columns in the pivot table.
    - Example: `['Category']` sets "Category" as the column dimension.

    - **aggregatorName** (`str`): The name of the aggregation function to use for computations.
    - Common options: `"Count"`, `"Sum"`, `"Average"`, etc.
    - Example: `'Count'` calculates the number of occurrences for each combination of rows and columns.

    - **vals** (`list`): A list of attribute names to be used as values for the aggregator function.
    - Example: `[]` means no specific values are used (default for `'Count'`).

    - **rendererName** (`str`): The name of the renderer to use for displaying the pivot table.
    - Common options: `"Table"`, `"Line Chart"`, `"Bar Chart"`, etc.
    - Example: `'Line Chart'` visualizes the pivot table as a line chart.

    - **rowOrder** (`str`): Determines the order of row labels in the pivot table.
    - Options: `"key_a_to_z"`, `"value_a_to_z"`, `"value_z_to_a"`.
    - Example: `'key_a_to_z'` orders rows alphabetically by their keys.

    - **colOrder** (`str`): Determines the order of column labels in the pivot table.
    - Options: `"key_a_to_z"`, `"value_a_to_z"`, `"value_z_to_a"`.
    - Example: `'key_a_to_z'` orders columns alphabetically by their keys.

    - **valueFilter** (`dict`): A dictionary specifying which values to include or exclude in the computation.
    - Structure: `{attribute_name: {value: true_or_false}}`
    - Example: `{}` means no filters are applied.

    - **hiddenAttributes** (`list`): A list of attribute names to hide completely from the UI.
    - Example: `[]` means no attributes are hidden.

    - **hiddenFromAggregators** (`list`): A list of attribute names to exclude from the aggregation dropdown.
    - Example: `[]` means no attributes are excluded.

    - **hiddenFromDragDrop** (`list`): A list of attribute names to exclude from the drag-and-drop area of the UI.
    - Example: `[]` means no attributes are excluded.

    - **menuLimit** (`int`): The maximum number of unique values to display in the dropdown menu for filtering.
    - Example: `500` means show up to 500 unique values.

    - **unusedOrientationCutoff** (`int`): Controls when the unused attributes area switches between vertical and horizontal display.
    - Example: `85` means switch to vertical if the combined attribute names exceed 85 characters.

    - **List of style_config Keys**

    General UI Colors:**
    uiTextColor: Text color for general UI elements.

    - **Table Headers:**
    headerBackgroundColor: Background color for table headers.
    headerBorderColor: Border color for table headers.

    - **Table Cells:**
    cellTextColor: Text color for table cells.
    cellBackgroundColor: Background color for table cells.
    cellBorderColor: Border color for table cells.

    - **Totals:**
    totalTextColor: Text color for totals.
    totalBackgroundColor: Background color for totals.

    - **Axis and Attributes:**
    axisBorderColor: Border color for axis containers.
    axisBackgroundColor: Background color for axis containers.
    axisPlaceholderBorderColor: Border color for axis container placeholders.
    attrBackgroundColor: Background color for attribute spans.
    attrBorderColor: Border color for attribute spans.

    - **Dropdown:**
    dropdownIconColor: Color of the dropdown icon.
    dropdownMenuBackgroundColor: Background color of the dropdown menu.
    dropdownMenuBorderColor: Border color of the dropdown menu.
    dropdownMenuTopBorderColor: Top border color of the dropdown menu.
    dropdownActiveBackgroundColor: Background color for active dropdown values.

    - **Triangle:**
    triangleColor: Color of the triangle icon.

    - **Drag Handle:**
    dragHandleColor: Color of the drag handle.

    - **Buttons:**
    buttonTextColor: Text color for buttons.
    buttonBackgroundColor: Background color for buttons.
    buttonBorderColor: Border color for buttons.
    buttonHoverBackgroundColor: Background color for buttons on hover.
    buttonHoverBorderColor: Border color for buttons on hover.
    buttonActiveBackgroundColor: Background color for buttons when active.

    - **Filter Box:**
    filterBoxBackgroundColor: Background color of the filter box.
    filterBoxBorderColor: Border color of the filter box.
    filterBoxInputTextColor: Text color for filter box inputs.
    filterBoxInputFocusBorderColor: Border color for filter box inputs when focused.
    filterBoxHeaderColor: Color of the filter box header (<h4>).
    filterBoxButtonTextColor: Text color for buttons inside the filter box.

    - **Check Container:**
    checkContainerBorderColor: Border color for the check container.
    selectedItemBackgroundColor: Background color for selected items in the check container.
    
    - **show_render_option**
    show_render_option: Set it True to show else false for hide.

    Here're the example of Code:   
    ############################################################################################################################################
    import streamlit as st
    from streamlit_pivottable import streamlit_pivottable
    import pandas as pd
    import numpy as np

    # Set page configuration    
    st.set_page_config(layout='wide')

    # Limit the number of rows
    num_rows = 1000000

    # Generate sample DataFrame for Pivot Table
    df = pd.DataFrame({
        "Category": np.random.choice(
            ["Category A", "Category B", "Category C", "Category D", 
            "Category E", "Category F", "Category G", "Category H", 
            "Category I", "Category J"], size=num_rows),
        "Region": np.random.choice(
            ["North", "South", "East", "West", "Central", "Northeast", 
            "Southeast", "Northwest", "Southwest", "International"], size=num_rows),
        "Priority": np.random.choice(
            ["Very Low", "Low", "Medium Low", "Medium", "Medium High", 
            "High", "Very High", "Critical", "Non-Critical", "Undefined"], size=num_rows),
        "Product Type": np.random.choice(
            ["Product A", "Product B", "Product C", "Product D", "Product E", 
            "Product F", "Product G", "Product H", "Product I", "Product J"], size=num_rows),
        "Quarter": np.random.choice(
            ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8", "Q9", "Q10"], size=num_rows),
        "Source": np.random.choice(
            ["Online", "Offline", "In-Store", "Marketplace", "Subscription", 
            "Direct Sales", "Wholesale", "Retail", "Auction", "Flash Sale"], size=num_rows),
        "Gender": np.random.choice(
            ["Male", "Female", "Other", "Prefer Not to Say", "Non-Binary", 
            "Transgender", "Intersex", "Androgynous", "Genderqueer", "Agender"], size=num_rows),
        "Age Range": np.random.choice(
            ["18-24", "25-34", "35-44", "45-54", "55-64", "65-74", 
            "75-84", "85-94", "95+", "Under 18"], size=num_rows),
        "Customer Type": np.random.choice(
            ["New Customer", "Returning Customer", "VIP", "Wholesale Buyer", 
            "Gift Buyer", "Seasonal Buyer", "Frequent Shopper", "Rare Shopper", 
            "Business Client", "Occasional Buyer"], size=num_rows),
        "Promotion": np.random.choice(
            ["Discounted", "Full Price", "Clearance", "Premium", "Subscription Plan", 
            "Limited Offer", "Flash Sale", "Bundle Deal", "Gift Pack", "Exclusive"], size=num_rows),
    })

    df["Value"] = np.random.uniform(1000000, 999999999, size=num_rows).round(2)


    sample_size = 50000  # Adjust this to improve performance
    df_sample = df.sample(n=sample_size, random_state=42)
    data_2d = [df_sample.columns.tolist()] + df_sample.values.tolist()


    default_settings = {
    "rows":[],
    "cols":[],
    "aggregatorName":"Count",
    "vals":[],
    "rendererName":"Table",
    "rowOrder":"",
    "colOrder":"",
    "valueFilter":{},
    "hiddenAttributes":[],
    "hiddenFromAggregators":[],
    "hiddenFromDragDrop":[],
    "menuLimit":500,
    "unusedOrientationCutoff":85
    }

    # Display Streamlit component Pivot Table
    with st.spinner("Loading Pivot Table..."):
        with st.container():
            pivot_table_settings = streamlit_pivottable(
                data=data_2d, 
                default_settings=default_settings,
                height=40, 
                use_container_width=True, 
            )

    # Display pivot table configuration
    if pivot_table_settings:
        st.write("Pivot Table Configuration:")
        st.json(pivot_table_settings)

    ############################################################################################################################################
    """
    if data is None:
        data = []
    # Pass parameters to the Streamlit component
    component_value = _component_func(
        name=name,
        data=data,
        show_render_option=show_render_option,
        default_settings=default_settings,
        height=height,
        width=width,
        style_config=style_config,
        use_container_width=use_container_width,
        key=key,
        default=default_settings
    )

    return component_value
