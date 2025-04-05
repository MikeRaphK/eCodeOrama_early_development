import pandas as pd
import os
from pathlib import Path
import cairosvg

def event_to_string(event : tuple) -> str:
    return ' '.join(event)

def build_codeOrama(sprite_dict : dict) -> None:
    sprite_names = []
    event_names = set() # Initialize this as a set to avoid duplicates
    sprite_icons = []
    for sprite_name, value in sprite_dict.items():
        # Get sprite names
        sprite_names.append(sprite_name)

        # Get event names
        events = value["events"]
        for event in events:
            event_names.add(event_to_string(event))

        # Get costume
        sprite_icons.append(f"./sb3_assets/{value["costume"]}.png")

    # Build the first row and clomuns
    df = pd.DataFrame(index=list(event_names), columns=sprite_names)
    
    for sprite_name, value in sprite_dict.items():
        # Connect events with sprites
        for event in value["events"]:
            event_str = event_to_string(event)
            df.loc[event_str, sprite_name] = f"'{event_str}' triggers '{sprite_name}'"

        # Connect events with broadcasts
        for broadcast in value["broadcasts_sent"]:
            broadcast_name = broadcast[0]
            event_str = broadcast[1]
            df.loc[event_str, sprite_name] += f"\n'{sprite_name}' broadcasts '{broadcast_name}'"

    excel_path = "./codeOrama.xlsx"

    # Create Excel using xlsxwriter
    df.fillna('', inplace=True)
    with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
        # Init xlsxwriter
        df.to_excel(writer, sheet_name='Sheet1', startrow=0, header=True, index=True)
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        n_rows, n_cols = df.shape

        header_format = workbook.add_format({
            'bold': True,
            'font_name': 'Arial',
            'font_size': 14,
            'align': 'center',
            'valign': 'vcenter',
            'text_wrap': True
        })

        normal_format = workbook.add_format({
            'bold': False,
            'font_name': 'Arial',
            'font_size': 12,
            'align': 'center',
            'valign': 'vcenter',
            'text_wrap': True
        })

        # Apply formats to all cells
        for row in range(n_rows + 1):
            for col in range(n_cols + 1):
                cell_value = (
                    df.columns[col - 1] if row == 0 and col > 0 else
                    df.index[row - 1] if col == 0 and row > 0 else
                    df.iloc[row - 1, col - 1] if row > 0 and col > 0 else ''
                )
                cell_format = header_format if row == 0 or col == 0 else normal_format
                worksheet.write(row, col, cell_value, cell_format)
        worksheet.set_column(0, n_cols, 60)

        # Convert all .svg files in ./extracted/ to .png files in ./sb3_assets/
        Path("./sb3_assets").mkdir(exist_ok=True)
        svg_paths = Path("./extracted").glob("*.svg")
        for svg_path in svg_paths:
            png_filename = svg_path.stem + ".png"  # Get base filename
            png_path = Path("./sb3_assets") / png_filename
            cairosvg.svg2png(url=str(svg_path), write_to=str(png_path))

        # Add icons
        for col, image_path in enumerate(sprite_icons):
            if os.path.exists(image_path):
                worksheet.insert_image(0, col + 1, image_path, {'x_offset': 15, 'y_offset': 5, 'x_scale': 0.5, 'y_scale': 0.5})
        worksheet.set_row(0, 80)  # height in points (adjust as needed)