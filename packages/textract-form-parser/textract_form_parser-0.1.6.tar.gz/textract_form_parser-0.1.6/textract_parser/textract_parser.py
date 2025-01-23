import json
import logging
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

# Public interfaces - expose only these functions
__all__ = [
    "analyze_document",
    "generate_html_report",
    "create_concise_results",
    "setup_textract_logger",
]


def setup_textract_logger(
    verbose: bool = False, log_dir: str = "logs"
) -> logging.Logger:
    """
    Configure and return a logger for the textract parser.

    This function sets up a dual-output logger that writes to both console and file.
    The file output is always at DEBUG level, while console output level is configurable.

    Args:
        verbose (bool): If True, sets console logging level to DEBUG; if False, uses INFO
        log_dir (str): Directory where log files should be stored

    Returns:
        logging.Logger: Configured logger instance with both console and file handlers

    File Output Format:
        timestamp - name - level - filename:line - message

    Console Output Format:
        timestamp - name - level - message

    Example:
        >>> logger = setup_textract_logger(verbose=True, log_dir='logs/Jan_19_2025_1000')
        >>> logger.debug("Processing block 1")
        >>> logger.info("Analysis complete")
    """
    # Create logs directory if it doesn't exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    # Create logger
    logger = logging.getLogger("textract_parser")
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)

    # Remove any existing handlers
    logger.handlers = []

    # Create console handler with formatting
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if verbose else logging.INFO)
    console_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Create file handler with formatting
    log_file = os.path.join(log_dir, "textract.log")
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)  # Always save all debug messages to file
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Log initial message
    logger.info(f"Logging initialized - Log file: {log_file}")
    if verbose:
        logger.debug("Debug logging enabled")

    return logger


# Create logger instance
logger = setup_textract_logger(verbose=False)


@dataclass
class QueryAnswer:
    question: str
    answer: str
    alias: str
    confidence: float


@dataclass
class FormField:
    key: str
    value: str
    confidence: float


@dataclass
class TableCell:
    text: str
    row: int
    column: int
    row_span: int = 1
    column_span: int = 1
    is_merged: bool = False
    confidence: float = 0.0
    selected: bool = False  # For selection elements


@dataclass
class BoundingBox:
    width: float
    height: float
    left: float
    top: float


@dataclass
class GeometricFormField(FormField):
    key_bbox: BoundingBox
    value_bbox: BoundingBox
    geometric_confidence: float  # Confidence based on geometric alignment


@dataclass
class DocumentContent:
    queries: List[QueryAnswer]
    form_fields: List[FormField]
    lines: List[str]
    tables: List[List[TableCell]]


def get_text_from_block(block: Dict, blocks: List[Dict]) -> str:
    """Extract text from a block and its children"""
    if "Text" in block:
        return block["Text"]

    text = []
    if "Relationships" in block:
        for rel in block["Relationships"]:
            if rel["Type"] == "CHILD":
                for child_id in rel["Ids"]:
                    child = next((b for b in blocks if b["Id"] == child_id), None)
                    if child and "Text" in child:
                        text.append(child["Text"])
    return " ".join(text)


def get_geometric_confidence(key_bbox: Dict, value_bbox: Dict) -> float:
    """
    Calculate confidence based on geometric alignment of key and value
    Returns confidence score between 0 and 100
    """
    # Check if value is to the right of or below the key
    is_aligned = False
    geometric_score = 0.0

    # Check horizontal alignment (value to the right of key)
    if value_bbox["Left"] > key_bbox["Left"]:
        horizontal_distance = value_bbox["Left"] - (
            key_bbox["Left"] + key_bbox["Width"]
        )
        if horizontal_distance < 0.1:  # Threshold for horizontal proximity
            is_aligned = True
            geometric_score = 100.0 - (
                horizontal_distance * 1000
            )  # Reduce score based on distance

    # Check vertical alignment (value below key)
    if (
        not is_aligned and abs(value_bbox["Top"] - key_bbox["Top"]) < 0.05
    ):  # Threshold for vertical alignment
        is_aligned = True
        geometric_score = 90.0  # Slightly lower confidence for vertical alignment

    return max(0.0, min(100.0, geometric_score))


def get_bounding_box(geometry: Dict) -> BoundingBox:
    """Extract bounding box from geometry"""
    bbox = geometry["BoundingBox"]
    return BoundingBox(
        width=bbox["Width"], height=bbox["Height"], left=bbox["Left"], top=bbox["Top"]
    )


def get_text_by_geometry(
    target_bbox: BoundingBox, blocks: List[Dict], max_distance: float = 0.1
) -> List[Dict[str, Any]]:
    """
    Find text blocks near a target bounding box
    Returns list of nearby text blocks with their distances and positions
    """
    nearby_texts = []

    for block in blocks:
        if block["BlockType"] == "LINE" or (
            block["BlockType"] == "WORD" and "Text" in block
        ):
            block_bbox = get_bounding_box(block["Geometry"])

            # Calculate distances
            horizontal_distance = abs(block_bbox.left - target_bbox.left)
            vertical_distance = abs(block_bbox.top - target_bbox.top)

            # Determine position relative to target
            position = "UNKNOWN"
            if block_bbox.left > target_bbox.left + target_bbox.width:
                position = "RIGHT"
            elif block_bbox.left + block_bbox.width < target_bbox.left:
                position = "LEFT"
            elif block_bbox.top > target_bbox.top + target_bbox.height:
                position = "BELOW"
            elif block_bbox.top + block_bbox.height < target_bbox.top:
                position = "ABOVE"

            # Calculate overall proximity score
            distance_score = (horizontal_distance + vertical_distance) / 2

            if distance_score <= max_distance:
                nearby_texts.append(
                    {
                        "text": block.get("Text", ""),
                        "distance": distance_score,
                        "position": position,
                        "confidence": block.get("Confidence", 0.0),
                        "bbox": block_bbox,
                    }
                )

    # Sort by distance
    return sorted(nearby_texts, key=lambda x: x["distance"])


def find_value_by_geometry(key_block: Dict, blocks: List[Dict]) -> Optional[Dict]:
    """Find the most likely value for a key based on geometric position"""
    key_bbox = get_bounding_box(key_block["Geometry"])

    # First look for text to the right
    right_texts = [
        t for t in get_text_by_geometry(key_bbox, blocks) if t["position"] == "RIGHT"
    ]
    if right_texts:
        return right_texts[0]

    # Then look below
    below_texts = [
        t for t in get_text_by_geometry(key_bbox, blocks) if t["position"] == "BELOW"
    ]
    if below_texts:
        return below_texts[0]

    return None


def find_answer_by_geometry(query_block: Dict, blocks: List[Dict]) -> Optional[Dict]:
    """Find the most likely answer for a query based on geometric position"""
    # First get the answer block through relationship
    answer_block = None
    if "Relationships" in query_block:
        for rel in query_block["Relationships"]:
            if rel["Type"] == "ANSWER":
                for answer_id in rel["Ids"]:
                    answer_block = next(
                        (b for b in blocks if b["Id"] == answer_id), None
                    )
                    if answer_block:
                        break

    if not answer_block:
        return None

    # Use the answer block's geometry to find matching blocks
    answer_bbox = get_bounding_box(answer_block["Geometry"])

    # Look for text blocks that share the exact same geometry
    matching_blocks = []
    for block in blocks:
        if "Geometry" in block and block["BlockType"] in ["WORD", "LINE"]:
            block_bbox = get_bounding_box(block["Geometry"])
            if (
                abs(block_bbox.left - answer_bbox.left) < 0.001
                and abs(block_bbox.top - answer_bbox.top) < 0.001
                and abs(block_bbox.width - answer_bbox.width) < 0.001
                and abs(block_bbox.height - answer_bbox.height) < 0.001
            ):
                matching_blocks.append(
                    {
                        "text": block.get("Text", ""),
                        "confidence": block.get("Confidence", 0.0),
                        "bbox": block_bbox,
                        "block_type": block["BlockType"],
                    }
                )

    if matching_blocks:
        # Return the block with highest confidence
        return max(matching_blocks, key=lambda x: x["confidence"])

    return None


def find_blocks_with_matching_geometry(
    target_geometry: Dict, blocks: List[Dict]
) -> List[Dict]:
    """Find all blocks that share the same geometry"""
    matching_blocks = []
    target_bbox = target_geometry["BoundingBox"]

    for block in blocks:
        if "Geometry" in block:
            block_bbox = block["Geometry"]["BoundingBox"]
            # Check if bounding boxes match
            if (
                block_bbox["Width"] == target_bbox["Width"]
                and block_bbox["Height"] == target_bbox["Height"]
                and block_bbox["Left"] == target_bbox["Left"]
                and block_bbox["Top"] == target_bbox["Top"]
            ):
                matching_blocks.append(
                    {
                        "block_type": block["BlockType"],
                        "confidence": block.get("Confidence", 0.0),
                        "text": block.get("Text", ""),
                        "id": block["Id"],
                    }
                )

    return matching_blocks


def find_line_containing_text(text: str, blocks: List[Dict]) -> Optional[Dict]:
    """Find LINE block that contains the given text"""
    for block in blocks:
        if block["BlockType"] == "LINE" and "Text" in block:
            if text in block["Text"]:
                return {
                    "block_type": block["BlockType"],
                    "confidence": block.get("Confidence", 0.0),
                    "text": block["Text"],
                    "id": block["Id"],
                }
    return None


def get_cell_text(cell_block: Dict, blocks: List[Dict]) -> str:
    """Extract text from a cell block by following WORD/child relationships"""
    text = []

    if "Relationships" in cell_block:
        for relationship in cell_block["Relationships"]:
            if relationship["Type"] == "CHILD":
                for child_id in relationship["Ids"]:
                    child_block = next((b for b in blocks if b["Id"] == child_id), None)
                    if child_block and child_block["BlockType"] == "WORD":
                        text.append(child_block.get("Text", ""))

    return " ".join(text)


def parse_table(table_block: Dict, blocks: List[Dict]) -> List[List[TableCell]]:
    """Parse a table block into a 2D array of cells"""
    table_cells = []
    max_row = 0
    max_col = 0

    # First pass: Get table dimensions and collect all cells
    if "Relationships" in table_block:
        for rel in table_block["Relationships"]:
            if rel["Type"] == "CHILD":
                for cell_id in rel["Ids"]:
                    cell_block = next((b for b in blocks if b["Id"] == cell_id), None)
                    if cell_block:
                        if cell_block["BlockType"] in ["CELL", "MERGED_CELL"]:
                            # Get cell indices
                            row_index = cell_block.get("RowIndex", 0)
                            col_index = cell_block.get("ColumnIndex", 0)
                            row_span = cell_block.get("RowSpan", 1)
                            col_span = cell_block.get("ColumnSpan", 1)

                            # Update table dimensions
                            max_row = max(max_row, row_index + row_span - 1)
                            max_col = max(max_col, col_index + col_span - 1)

                            # Get cell text
                            cell_text = get_cell_text(cell_block, blocks)

                            # Check for selection elements within the cell
                            selection_status = None
                            if "Relationships" in cell_block:
                                for child_rel in cell_block["Relationships"]:
                                    if child_rel["Type"] == "CHILD":
                                        for child_id in child_rel["Ids"]:
                                            child_block = next(
                                                (
                                                    b
                                                    for b in blocks
                                                    if b["Id"] == child_id
                                                ),
                                                None,
                                            )
                                            if (
                                                child_block
                                                and child_block["BlockType"]
                                                == "SELECTION_ELEMENT"
                                            ):
                                                selection_status = child_block.get(
                                                    "SelectionStatus"
                                                )

                            # Create TableCell object
                            table_cells.append(
                                TableCell(
                                    text=cell_text,
                                    row=row_index - 1,  # Convert to 0-based indexing
                                    column=col_index - 1,
                                    row_span=row_span,
                                    column_span=col_span,
                                    is_merged=row_span > 1 or col_span > 1,
                                    confidence=cell_block.get("Confidence", 0.0),
                                    selected=selection_status == "SELECTED"
                                    if selection_status
                                    else None,
                                )
                            )

    # Create 2D array with empty cells
    table_data = [[None for _ in range(max_col)] for _ in range(max_row)]

    # Fill in the cells and handle merged cells
    for cell in table_cells:
        row_idx = cell.row
        col_idx = cell.column

        # For merged cells, fill in all spanned positions
        if cell.is_merged:
            for r in range(row_idx, min(row_idx + cell.row_span, max_row)):
                for c in range(col_idx, min(col_idx + cell.column_span, max_col)):
                    if r == row_idx and c == col_idx:
                        # Primary position gets the actual cell
                        table_data[r][c] = cell
                    else:
                        # Spanned positions get empty cells marked as part of merge
                        table_data[r][c] = TableCell(
                            text="",
                            row=r,
                            column=c,
                            is_merged=True,
                            confidence=0.0,
                            row_span=0,  # Indicates this is a continuation cell
                            column_span=0,
                        )
        else:
            # Regular cell
            if 0 <= row_idx < max_row and 0 <= col_idx < max_col:
                table_data[row_idx][col_idx] = cell

    # Fill any remaining None cells
    for i in range(max_row):
        for j in range(max_col):
            if table_data[i][j] is None:
                table_data[i][j] = TableCell(text="", row=i, column=j, confidence=0.0)

    return table_data


def print_table(table_data: List[List[TableCell]]):
    """
    Print table data in a formatted ASCII table structure.

    This function creates a human-readable representation of table data,
    including confidence scores and cell merge information.

    Args:
        table_data (List[List[TableCell]]): 2D array of table cells, each containing:
            - text: Cell content
            - confidence: Detection confidence
            - row/column: Position information
            - is_merged: Merge status
            - row_span/column_span: Merge dimensions

    Output Format:
        +----------+----------+
        | Cell 1   | Cell 2   |
        | (95.5%)  | (87.2%)  |
        +----------+----------+

    Features:
        - Handles merged cells with span indicators
        - Shows confidence scores for each cell
        - Adjusts column widths automatically
        - Indicates empty cells with "<NO VALUE GIVEN>"

    Example:
        >>> print_table(table_data)
        +----------+----------+
        | Header 1 | Header 2 |
        +----------+----------+
        | Data     | 95.5%    |
        +----------+----------+
    """
    if not table_data or not table_data[0]:
        return

    # Get column widths
    col_widths = []
    for col in range(len(table_data[0])):
        width = (
            max(
                len(cell.text if cell.text.strip() else "<NO VALUE GIVEN>")
                + (12 if cell.is_merged else 0)
                + 15  # Space for merge markers  # Space for confidence score
                for row in table_data
                for cell in [row[col]]
            )
            + 2
        )
        col_widths.append(min(width, 40))  # Cap width at 40 characters

    # Print header separator
    separator = "+"
    for width in col_widths:
        separator += "-" * width + "+"
    logger.info(separator)

    # Print rows
    for row in table_data:
        # Print cells
        line = "|"
        for cell, width in zip(row, col_widths):
            # Format confidence score
            conf_str = f"({cell.confidence:.1f}%)" if cell.confidence > 0 else ""

            # Format cell text
            cell_text = cell.text.strip() if cell.text else "<NO VALUE GIVEN>"

            # Handle selection elements
            if hasattr(cell, "selected") and cell.selected is not None:
                cell_text = "☒" if cell.selected else "☐"

            # Handle merged cells
            if cell.is_merged:
                if cell.row_span > 0 and cell.column_span > 0:
                    # Primary merged cell
                    merge_marker = f"[{cell.row_span}×{cell.column_span}]"
                    cell_text = f"{cell_text} {merge_marker}"
                else:
                    # Continuation of merged cell
                    cell_text = "┊" if cell.row_span == 0 else "━"
                    conf_str = ""  # Don't show confidence for continuation cells

            # Combine text and confidence
            if conf_str:
                display_text = f"{cell_text} {conf_str}"
            else:
                display_text = cell_text

            line += f" {display_text:<{width-1}}|"
        logger.info(line)
        logger.info(separator)

    # Enhanced table summary
    total_cells = sum(1 for row in table_data for cell in row)
    filled_cells = sum(
        1
        for row in table_data
        for cell in row
        if cell.text.strip() and not cell.is_merged
    )
    empty_cells = sum(
        1
        for row in table_data
        for cell in row
        if not cell.text.strip() and not cell.is_merged
    )
    merged_cells = sum(
        1 for row in table_data for cell in row if cell.is_merged and cell.row_span > 0
    )
    merged_spans = sum(
        1 for row in table_data for cell in row if cell.is_merged and cell.row_span == 0
    )

    valid_cells = [
        cell
        for row in table_data
        for cell in row
        if cell.text.strip() and not cell.is_merged
    ]
    avg_confidence = (
        (sum(cell.confidence for cell in valid_cells) / len(valid_cells))
        if valid_cells
        else 0
    )

    logger.info("\nTable Summary:")
    logger.info(f"Total Cells: {total_cells}")
    logger.info(f"├─ Filled Cells: {filled_cells}")
    logger.info(f"├─ Empty Cells: {empty_cells}")
    logger.info(
        f"├─ Merged Cells: {merged_cells} (spanning {merged_spans} additional cells)"
    )
    logger.info(f"└─ Average Confidence: {avg_confidence:.1f}%")


def format_readable_output(
    blocks: List[Dict], selection_mode: str = "selected"
) -> DocumentContent:
    """
    Format blocks into structured content

    Args:
        blocks: List of Textract blocks
        selection_mode: How to handle selection elements
            - "selected": Only show SELECTED items (default)
            - "switch": Show as YES/NO
            - "all": Show both SELECTED/NOT_SELECTED
    """
    try:
        queries = []
        form_fields = []
        lines = []
        tables = []

        # Process KEY_VALUE_SET blocks
        for block in blocks:
            if block["BlockType"] == "KEY_VALUE_SET" and "KEY" in block.get(
                "EntityTypes", []
            ):
                key_text = get_text_from_block(block, blocks)
                value_text = ""
                selection_status = None

                # Store geometry information for the key
                key_geometry = block.get("Geometry", {})
                value_geometry = None

                # Get value through relationships
                if "Relationships" in block:
                    for rel in block["Relationships"]:
                        if rel["Type"] == "VALUE":
                            for value_id in rel["Ids"]:
                                value_block = next(
                                    (b for b in blocks if b["Id"] == value_id), None
                                )
                                if value_block:
                                    value_geometry = value_block.get("Geometry", {})

                                    # Check for selection elements
                                    if "Relationships" in value_block:
                                        for child_rel in value_block["Relationships"]:
                                            if child_rel["Type"] == "CHILD":
                                                for child_id in child_rel["Ids"]:
                                                    child_block = next(
                                                        (
                                                            b
                                                            for b in blocks
                                                            if b["Id"] == child_id
                                                        ),
                                                        None,
                                                    )
                                                    if (
                                                        child_block
                                                        and child_block["BlockType"]
                                                        == "SELECTION_ELEMENT"
                                                    ):
                                                        selection_status = (
                                                            child_block.get(
                                                                "SelectionStatus"
                                                            )
                                                        )

                                                        # Handle different selection modes
                                                        if selection_mode == "selected":
                                                            if (
                                                                selection_status
                                                                == "SELECTED"
                                                            ):
                                                                value_text = "SELECTED"
                                                            else:
                                                                continue  # Skip unselected items
                                                        elif selection_mode == "switch":
                                                            value_text = (
                                                                "YES"
                                                                if selection_status
                                                                == "SELECTED"
                                                                else "NO"
                                                            )
                                                        elif selection_mode == "all":
                                                            value_text = (
                                                                selection_status
                                                            )
                                                        break

                                    # If no selection element found or not in selected-only mode, get regular text
                                    if not value_text and selection_mode != "selected":
                                        value_text = get_text_from_block(
                                            value_block, blocks
                                        ).strip()

                                    # Only add form field if there's a value
                                    if value_text:
                                        # Rest of the existing code for matching blocks etc...
                                        matching_blocks = (
                                            find_blocks_with_matching_geometry(
                                                value_block["Geometry"], blocks
                                            )
                                        )

                                        line_block = find_line_containing_text(
                                            f"{key_text}: {value_text}", blocks
                                        )
                                        if line_block:
                                            matching_blocks.append(line_block)

                                        form_fields.append(
                                            {
                                                "key": key_text.strip(),
                                                "value": value_text,
                                                "confidence": value_block.get(
                                                    "Confidence", 0.0
                                                ),
                                                "source": "relationship",
                                                "matching_blocks": matching_blocks,
                                                "line_context": line_block["text"]
                                                if line_block
                                                else None,
                                                "is_selection": selection_status
                                                is not None,
                                                "selection_status": selection_status,
                                                "geometry": {
                                                    "key_bbox": key_geometry.get(
                                                        "BoundingBox", {}
                                                    ),
                                                    "value_bbox": value_geometry.get(
                                                        "BoundingBox", {}
                                                    )
                                                    if value_geometry
                                                    else {},
                                                    "key_polygon": key_geometry.get(
                                                        "Polygon", []
                                                    ),
                                                    "value_polygon": value_geometry.get(
                                                        "Polygon", []
                                                    )
                                                    if value_geometry
                                                    else [],
                                                },
                                            }
                                        )

        # Process standalone SELECTION_ELEMENT blocks
        for block in blocks:
            if block["BlockType"] == "SELECTION_ELEMENT":
                selection_status = block.get("SelectionStatus")

                # Handle different selection modes
                if selection_mode == "selected":
                    if selection_status != "SELECTED":
                        continue  # Skip unselected items
                    value_text = "SELECTED"
                elif selection_mode == "switch":
                    value_text = "YES" if selection_status == "SELECTED" else "NO"
                elif selection_mode == "all":
                    value_text = selection_status

                # Try to find associated label/text
                nearby_text = find_text_by_geometry(block, blocks, max_distance=0.05)
                label = next(
                    (
                        t["text"]
                        for t in nearby_text
                        if t["position"] in ["LEFT", "RIGHT"]
                    ),
                    "",
                )

                form_fields.append(
                    {
                        "key": label.strip() if label else "<NO LABEL>",
                        "value": value_text,
                        "confidence": block.get("Confidence", 0.0),
                        "source": "selection_element",
                        "is_selection": True,
                        "selection_status": selection_status,
                        "geometry": {
                            "key_bbox": {},
                            "value_bbox": block.get("Geometry", {}).get(
                                "BoundingBox", {}
                            ),
                            "key_polygon": [],
                            "value_polygon": block.get("Geometry", {}).get(
                                "Polygon", []
                            ),
                        },
                    }
                )

        return DocumentContent(
            queries=queries, form_fields=form_fields, lines=lines, tables=tables
        )

    except Exception as e:
        logger.error(f"Error formatting output: {str(e)}")
        raise


def print_key_value_table(form_fields: List[Dict]):
    """Print key-value pairs in a table format with confidence scores"""
    if not form_fields:
        return

    # Calculate column widths
    key_width = max(len(field["key"]) for field in form_fields) + 2
    # Include "<NO VALUE GIVEN>" in width calculation
    value_width = max(
        max(
            len(field["value"] if field["value"].strip() else "<NO VALUE GIVEN>")
            for field in form_fields
        )
        + 15,  # Extra space for confidence
        20,  # Minimum width
    )

    # Cap widths
    key_width = min(key_width, 40)
    value_width = min(value_width, 50)

    # Print header
    separator = f"+{'-' * key_width}+{'-' * value_width}+"
    logger.info("\nKEY-VALUE PAIRS:")
    logger.info(separator)
    logger.info(f"| {'Key':<{key_width-1}}| {'Value':<{value_width-1}}|")
    logger.info(separator)

    # Print rows
    for field in form_fields:
        key = field["key"]
        # Handle empty or whitespace-only values
        value = field["value"].strip() if field["value"] else "<NO VALUE GIVEN>"
        confidence = field["confidence"]

        # Format value with confidence
        value_text = f"{value} ({confidence:.1f}%)"

        # Handle long text with wrapping
        if len(key) > key_width - 4:
            key = key[: key_width - 7] + "..."
        if len(value_text) > value_width - 4:
            value_text = value_text[: value_width - 7] + "..."

        logger.info(f"| {key:<{key_width-1}}| {value_text:<{value_width-1}}|")
        logger.info(separator)

    # Print summary
    non_empty_fields = sum(1 for field in form_fields if field["value"].strip())
    total_fields = len(form_fields)
    avg_confidence = sum(field["confidence"] for field in form_fields) / total_fields

    logger.info(f"\nSummary:")
    logger.info(f"Total Key-Value Pairs: {total_fields}")
    logger.info(f"Filled Values: {non_empty_fields}")
    logger.info(f"Empty Values: {total_fields - non_empty_fields}")
    logger.info(f"Average Confidence: {avg_confidence:.1f}%")


def print_query_table(queries: List[Dict]):
    """Print queries and answers in a table format with confidence scores"""
    if not queries:
        return

    # Calculate column widths
    question_width = max(len(qa["question"]) for qa in queries) + 2
    answer_width = (
        max(len(qa["answer"]) for qa in queries) + 15
    )  # Extra space for confidence
    alias_width = max(len(qa["alias"]) for qa in queries) + 2

    # Cap widths
    question_width = min(question_width, 40)
    answer_width = min(answer_width, 40)
    alias_width = min(alias_width, 20)

    # Print header
    separator = f"+{'-' * question_width}+{'-' * answer_width}+{'-' * alias_width}+"
    logger.info("\nQUERIES AND ANSWERS:")
    logger.info(separator)
    logger.info(
        f"| {'Question':<{question_width-1}}| {'Answer':<{answer_width-1}}| {'Alias':<{alias_width-1}}|"
    )
    logger.info(separator)

    # Print rows
    for qa in queries:
        question = qa["question"]
        answer = qa["answer"]
        alias = qa["alias"]
        confidence = qa["confidence"]

        # Format answer with confidence
        answer_text = f"{answer} ({confidence:.1f}%)"

        # Handle long text with wrapping
        if len(question) > question_width - 4:
            question = question[: question_width - 7] + "..."
        if len(answer_text) > answer_width - 4:
            answer_text = answer_text[: answer_width - 7] + "..."
        if len(alias) > alias_width - 4:
            alias = alias[: alias_width - 7] + "..."

        logger.info(
            f"| {question:<{question_width-1}}| {answer_text:<{answer_width-1}}| {alias:<{alias_width-1}}|"
        )
        logger.info(separator)

    # Print summary
    avg_confidence = sum(qa["confidence"] for qa in queries) / len(queries)
    logger.info(f"\nSummary:")
    logger.info(f"Total Queries: {len(queries)}")
    logger.info(f"Average Confidence: {avg_confidence:.1f}%")


def get_section_position(geometry: Dict) -> str:
    """
    Determine document section based on geometric position.

    This function maps vertical positions to logical document sections
    using predefined boundaries.

    Args:
        geometry (Dict): Geometric information containing:
            - BoundingBox: Box coordinates
                - Top: Vertical position (0-1)
                - Left: Horizontal position (0-1)
                - Width/Height: Dimensions

    Returns:
        str: Section identifier:
            - "HEADER": Top section (0-0.25)
            - "SECTION_1": Upper middle (0.25-0.5)
            - "SECTION_2": Lower middle (0.5-0.75)
            - "FOOTER": Bottom section (0.75-1)

    Note:
        - Positions are normalized (0-1 scale)
        - Boundaries can be adjusted for different layouts

    Example:
        >>> pos = get_section_position({"BoundingBox": {"Top": 0.15}})
        >>> print(pos)
        'HEADER'
    """
    bbox = geometry["BoundingBox"]
    top = bbox["Top"]

    # Define section boundaries (these can be adjusted based on your document)
    if top < 0.25:
        return "HEADER"
    elif top < 0.5:
        return "SECTION_1"
    elif top < 0.75:
        return "SECTION_2"
    else:
        return "FOOTER"


def group_by_sections(blocks: List[Dict]) -> Dict[str, List[Dict]]:
    """
    Group document blocks by their vertical sections.

    This function organizes blocks into logical sections based on their
    vertical position in the document.

    Args:
        blocks (List[Dict]): List of text blocks containing:
            - Geometry: Position information
            - BlockType: Type of block
            - Text: Content

    Returns:
        Dict[str, List[Dict]]: Blocks grouped by section:
            - HEADER: Top section blocks
            - SECTION_1: Upper middle blocks
            - SECTION_2: Lower middle blocks
            - FOOTER: Bottom section blocks

    Note:
        - Uses get_section_position() for classification
        - Maintains original block information
        - Skips blocks without geometry

    Example:
        >>> sections = group_by_sections(blocks)
        >>> for section, blocks in sections.items():
        ...     print(f"{section}: {len(blocks)} blocks")
    """
    sections = {"HEADER": [], "SECTION_1": [], "SECTION_2": [], "FOOTER": []}

    for block in blocks:
        if "Geometry" in block:
            section = get_section_position(block["Geometry"])
            sections[section].append(block)

    return sections


def get_block_content(block: Dict, blocks: List[Dict]) -> str:
    """Get readable content from a block"""
    if "Text" in block:
        return block["Text"]

    # For blocks that might have child relationships
    if "Relationships" in block:
        texts = []
        for rel in block["Relationships"]:
            if rel["Type"] == "CHILD":
                for child_id in rel["Ids"]:
                    child_block = next((b for b in blocks if b["Id"] == child_id), None)
                    if child_block and "Text" in child_block:
                        texts.append(child_block["Text"])
        return " ".join(texts)
    return ""


def print_section_structure(sections: Dict[str, List[Dict]], blocks: List[Dict]):
    """
    Print hierarchical document structure by sections.

    This function creates a tree-like visualization of document structure,
    organizing blocks by type within each section.

    Args:
        sections (Dict[str, List[Dict]]): Blocks grouped by section
        blocks (List[Dict]): All document blocks for reference

    Output Format:
        SECTION_NAME:
        ├─ Layout Elements:
        │  ├─ LAYOUT_TITLE: 2 blocks
        │  └─ "Title text..."
        ├─ Form Elements:
        │  └─ KEY_VALUE_SET: 5 blocks

    Features:
        - Groups blocks by category (layout, form, table)
        - Shows block counts by type
        - Displays content for certain block types
        - Uses tree structure for visualization

    Categories:
        - Layout Elements: Document structure
        - Form Elements: Interactive fields
        - Table Elements: Tabular data
        - Page Elements: Page-level blocks
    """
    logger.info("DOCUMENT STRUCTURE:")
    logger.info("-" * 50)

    # Define block type categories for better organization
    layout_types = {
        "LAYOUT",
        "LAYOUT_HEADER",
        "LAYOUT_TITLE",
        "LAYOUT_SECTION_HEADER",
        "LAYOUT_TEXT",
        "LAYOUT_FOOTER",
    }
    form_types = {"KEY_VALUE_SET", "QUERY", "QUERY_RESULT", "SELECTION_ELEMENT"}
    table_types = {"TABLE", "TABLE_TITLE", "MERGED_CELL", "CELL"}
    page_types = {"PAGE", "HEADER", "FOOTER"}
    skip_types = {"LINE", "WORD"}

    # Types that should show their text content
    show_content_types = layout_types | {"TABLE_TITLE"}

    for section_name, section_blocks in sections.items():
        if not section_blocks:
            continue

        logger.info(f"\n{section_name}:")
        # Group blocks by their type
        type_blocks = {}
        for block in section_blocks:
            block_type = block["BlockType"]
            if block_type not in skip_types:
                if block_type not in type_blocks:
                    type_blocks[block_type] = []
                type_blocks[block_type].append(block)

        # Print counts and content by category
        if any(t in type_blocks for t in layout_types):
            logger.info("├─ Layout Elements:")
            for block_type in layout_types:
                if block_type in type_blocks:
                    blocks_of_type = type_blocks[block_type]
                    logger.info(f"│  ├─ {block_type}: {len(blocks_of_type)} blocks")
                    if block_type in show_content_types:
                        for block in blocks_of_type:
                            content = get_block_content(block, blocks)
                            if content:
                                # Truncate long content
                                if len(content) > 60:
                                    content = content[:57] + "..."
                                logger.info(f'│  │  └─ "{content}"')

        # Print other categories without content
        if any(t in type_blocks for t in form_types):
            logger.info("├─ Form Elements:")
            for block_type in form_types:
                if block_type in type_blocks:
                    logger.info(
                        f"│  ├─ {block_type}: {len(type_blocks[block_type])} blocks"
                    )

        if any(t in type_blocks for t in table_types):
            logger.info("├─ Table Elements:")
            for block_type in table_types:
                if block_type in type_blocks:
                    blocks_of_type = type_blocks[block_type]
                    logger.info(f"│  ├─ {block_type}: {len(blocks_of_type)} blocks")
                    if block_type in show_content_types:
                        for block in blocks_of_type:
                            content = get_block_content(block, blocks)
                            if content:
                                logger.info(f'│  │  └─ "{content}"')

        if any(t in type_blocks for t in page_types):
            logger.info("├─ Page Elements:")
            for block_type in page_types:
                if block_type in type_blocks:
                    logger.info(
                        f"│  ├─ {block_type}: {len(type_blocks[block_type])} blocks"
                    )

        # Print any remaining block types
        other_types = (
            set(type_blocks.keys())
            - layout_types
            - form_types
            - table_types
            - page_types
        )
        if other_types:
            logger.info("├─ Other Elements:")
            for block_type in other_types:
                logger.info(
                    f"│  ├─ {block_type}: {len(type_blocks[block_type])} blocks"
                )

    logger.info("\n" + "=" * 50 + "\n")


def get_form_elements(json_response: Dict) -> List[Dict[str, Any]]:
    """
    Get both key-value pairs and selection elements from a form combined into one list
    Returns list of form elements with type identifier
    """
    try:
        form_elements = []

        # Get key-value pairs
        kv_pairs = get_kv(json_response)
        for kv in kv_pairs:
            form_elements.append(
                {
                    "type": "KEY_VALUE",
                    "key": kv["key"],
                    "value": kv["value"],
                    "confidence": kv["confidence"],
                    "geometry": kv["geometry"],
                }
            )

        # Get selection elements
        selections = get_selection_elements(json_response)
        for sel in selections:
            form_elements.append(
                {
                    "type": "SELECTION",
                    "label": sel.get("label", "<NO LABEL FOUND>"),
                    "selected": sel["selected"],
                    "confidence": sel["confidence"],
                    "position": sel["position"],
                }
            )

        return form_elements
    except Exception as e:
        logger.error(f"Error getting form elements: {str(e)}")
        raise


def print_layout_structure(blocks: List[Dict]) -> None:
    """Print document layout structure with content"""
    logger.info("\nDOCUMENT LAYOUT STRUCTURE:")
    logger.info("-" * 50)

    # Define layout categories and their descriptions
    layout_types = {
        "LAYOUT_TITLE": "Document Title",
        "LAYOUT_HEADER": "Header Text",
        "LAYOUT_FOOTER": "Footer Text",
        "LAYOUT_SECTION_HEADER": "Section Titles",
        "LAYOUT_PAGE_NUMBER": "Page Numbers",
        "LAYOUT_LIST": "List Elements",
        "LAYOUT_FIGURE": "Figures/Images",
        "LAYOUT_TABLE": "Table Locations",
        "LAYOUT_KEY_VALUE": "Form Fields",
        "LAYOUT_TEXT": "Paragraph Text",
        "TABLE_TITLE": "Table Titles",
    }

    # Group blocks by layout type
    layout_blocks = {}
    for block in blocks:
        block_type = block["BlockType"]
        if block_type in layout_types:
            if block_type not in layout_blocks:
                layout_blocks[block_type] = []
            layout_blocks[block_type].append(block)

    # Print layout information
    for layout_type, description in layout_types.items():
        blocks_of_type = layout_blocks.get(layout_type, [])
        if blocks_of_type:
            logger.info(f"\n{description}:")
            logger.info(f"├─ Found {len(blocks_of_type)} {layout_type} blocks")

            # Show content for each block
            for block in blocks_of_type:
                content = get_block_content(block, blocks)
                if content:
                    # Truncate long content
                    if len(content) > 60:
                        content = content[:57] + "..."
                    confidence = block.get("Confidence", 0.0)
                    logger.info(f'│  └─ "{content}" ({confidence:.1f}%)')

    logger.info("\n" + "=" * 50)


def print_readable_analysis(json_response: Dict) -> None:
    try:
        blocks = json_response.get("Blocks", [])
        content = format_readable_output(blocks)

        logger.info("=== Document Content Analysis ===\n")

        # Print Layout Structure
        print_layout_structure(blocks)

        # Print Form Fields as table
        if content.form_fields:
            print_key_value_table(content.form_fields)
            logger.info("\n" + "=" * 50 + "\n")

        # Print Queries and Answers as table
        if content.queries:
            print_query_table(content.queries)
            logger.info("\n" + "=" * 50 + "\n")

        # Print Tables
        if content.tables:
            logger.info("\nTABLES:")
            logger.info("-" * 50)
            for i, table in enumerate(content.tables, 1):
                logger.info(f"\nTable {i}:")
                print_table(table)
                logger.info("")

    except Exception as e:
        logger.error(f"Error analyzing document: {str(e)}")
        raise


def analyze_document(json_response: Dict) -> Dict[str, Any]:
    """
    Analyze AWS Textract JSON output and extract structured data.

    This function processes raw Textract output and organizes it into a structured format.
    It performs several types of analysis:
    1. Layout Analysis: Identifies document structure and sections
    2. Form Field Extraction: Finds and processes form fields
    3. Table Detection: Identifies and extracts tabular data
    4. Query Processing: Handles any query-answer pairs

    Args:
        json_response (Dict): Raw Textract JSON response containing:
            - Blocks: List of detected text blocks with geometry and relationships
            - DocumentMetadata: Document metadata including page count
            - AnalyzeDocumentModelVersion: Textract model version used

    Returns:
        Dict[str, Any]: Structured data containing:
            layout (Dict): Document layout information
                - LAYOUT_TITLE: Document titles and headings
                - LAYOUT_SECTION_HEADER: Section headers with positions
                - LAYOUT_TEXT: Regular text blocks with confidence
            form_fields (Dict): Extracted form fields
                - fields: List of key-value pairs with geometry
                - summary: Statistical summary of extraction
            queries (Optional[Dict]): Query results if present
                - QUERIES: List of query-answer pairs
                - confidence scores for each answer
            tables (Optional[List]): Table data if present
                - cell data with row/column information
                - merged cell information
                - confidence scores for each cell

    Raises:
        ValueError: If JSON response is invalid or missing required fields
        KeyError: If required block information is missing
        Exception: For other processing errors

    Example:
        >>> with open('textract_output.json', 'r') as f:
        ...     textract_json = json.load(f)
        >>> results = analyze_document(textract_json)
        >>> print(f"Found {len(results['form_fields']['fields'])} form fields")
        >>> print(f"Document layout has {len(results['layout']['LAYOUT_TITLE'])} titles")

    Notes:
        - Confidence scores are normalized to 0-100 range
        - Geometric relationships are preserved in output
        - Empty or invalid fields are marked with '<NO VALUE GIVEN>'
        - Table structure maintains original layout
    """
    try:
        blocks = json_response.get("Blocks", [])
        content = format_readable_output(blocks)

        # Get layout structure
        layout_analysis = analyze_layout_structure(blocks)

        # Get form fields
        form_fields_analysis = analyze_key_value_pairs(content.form_fields, blocks)

        # Get queries and answers
        queries_analysis = analyze_queries(content.queries) if content.queries else None

        # Get tables
        tables_analysis = analyze_tables(content.tables) if content.tables else None

        return {
            "layout": layout_analysis,
            "form_fields": form_fields_analysis,
            "queries": queries_analysis,
            "tables": tables_analysis,
        }

    except Exception as e:
        logger.error(f"Error analyzing document: {str(e)}")
        raise


def analyze_layout_structure(blocks: List[Dict]) -> Dict[str, Any]:
    """Analyze layout structure and return data instead of printing"""
    layout_types = {
        "LAYOUT_TITLE": "Document Title",
        "LAYOUT_HEADER": "Header Text",
        "LAYOUT_FOOTER": "Footer Text",
        "LAYOUT_SECTION_HEADER": "Section Titles",
        "LAYOUT_PAGE_NUMBER": "Page Numbers",
        "LAYOUT_LIST": "List Elements",
        "LAYOUT_FIGURE": "Figures/Images",
        "LAYOUT_TABLE": "Table Locations",
        "LAYOUT_KEY_VALUE": "Form Fields",
        "LAYOUT_TEXT": "Paragraph Text",
        "TABLE_TITLE": "Table Titles",
    }

    layout_analysis = {}
    for block in blocks:
        block_type = block["BlockType"]
        if block_type in layout_types:
            if block_type not in layout_analysis:
                layout_analysis[block_type] = []

            content = get_block_content(block, blocks)
            if content:
                # Find nearby text for all layout blocks
                nearby_text = find_text_by_geometry(block, blocks)

                block_data = {
                    "content": content,
                    "confidence": block.get("Confidence", 0.0),
                    "nearby_text": nearby_text,
                    "position": {
                        "top": block["Geometry"]["BoundingBox"]["Top"],
                        "left": block["Geometry"]["BoundingBox"]["Left"],
                        "width": block["Geometry"]["BoundingBox"]["Width"],
                        "height": block["Geometry"]["BoundingBox"]["Height"],
                    }
                    if "Geometry" in block
                    else None,
                }

                # Add special handling for table titles
                if block_type == "TABLE_TITLE":
                    table_id = None
                    if "Relationships" in block:
                        for rel in block["Relationships"]:
                            if rel["Type"] == "TABLE":
                                table_id = rel["Ids"][0] if rel["Ids"] else None
                    block_data["table_id"] = table_id

                layout_analysis[block_type].append(block_data)

    return layout_analysis


def analyze_key_value_pairs(
    form_fields: List[Dict], blocks: List[Dict] = None
) -> Dict[str, Any]:
    """Analyze key-value pairs and return data instead of printing"""
    if not form_fields:
        return None

    analyzed_fields = []
    for field in form_fields:
        field_data = {
            "key": field["key"],
            "value": field["value"].strip() if field["value"] else "<NO VALUE GIVEN>",
            "confidence": field["confidence"],
            "source": field.get("source"),
            "geometry": field.get("geometry", {}),
            "nearby_text": field.get("nearby_text", []),
            "matching_text": [],
        }

        if blocks and field.get(
            "geometry"
        ):  # Only process geometry if blocks are provided
            key_block = {"Geometry": {"BoundingBox": field["geometry"]["key_bbox"]}}
            value_block = {"Geometry": {"BoundingBox": field["geometry"]["value_bbox"]}}

            field_data["key_nearby_text"] = find_text_by_geometry(
                key_block, blocks, max_distance=0.05
            )
            field_data["value_nearby_text"] = find_text_by_geometry(
                value_block, blocks, max_distance=0.05
            )

            for block in blocks:
                if block["BlockType"] in ["WORD", "LINE", "TEXT"] and "Text" in block:
                    block_text = block["Text"].strip()
                    if block_text in field["key"] or field["key"] in block_text:
                        field_data["matching_text"].append(
                            {
                                "text": block_text,
                                "block_type": block["BlockType"],
                                "confidence": block.get("Confidence", 0.0),
                                "geometry": block["Geometry"]["BoundingBox"],
                                "match_type": "KEY",
                                "block_id": block["Id"],
                            }
                        )
                    elif block_text in field["value"] or field["value"] in block_text:
                        field_data["matching_text"].append(
                            {
                                "text": block_text,
                                "block_type": block["BlockType"],
                                "confidence": block.get("Confidence", 0.0),
                                "geometry": block["Geometry"]["BoundingBox"],
                                "match_type": "VALUE",
                                "block_id": block["Id"],
                            }
                        )

        analyzed_fields.append(field_data)

    # Calculate summary statistics
    non_empty_fields = sum(1 for field in form_fields if field["value"].strip())
    total_fields = len(form_fields)
    avg_confidence = sum(field["confidence"] for field in form_fields) / total_fields

    return {
        "fields": analyzed_fields,
        "summary": {
            "total_fields": total_fields,
            "filled_values": non_empty_fields,
            "empty_values": total_fields - non_empty_fields,
            "average_confidence": avg_confidence,
        },
    }


def analyze_queries(queries: List[Dict]) -> Dict[str, Any]:
    """Analyze queries and return data instead of printing"""
    if not queries:
        return None

    analyzed_queries = []
    for query in queries:
        query_data = {
            "query": query["question"],
            "query_answer": query["answer"] if query["answer"] else "<NO VALUE GIVEN>",
            "confidence": query["confidence"],
            "matchingblocks": [],
        }

        # Add matching blocks if they exist
        if query.get("matching_blocks"):
            query_data["matchingblocks"] = [
                {
                    "block_type": block["block_type"],
                    "confidence": block["confidence"],
                    "id": block["id"],
                }
                for block in query["matching_blocks"]
            ]

        analyzed_queries.append(query_data)

    return {"QUERIES": analyzed_queries}


def analyze_tables(tables: List[List[TableCell]]) -> List[Dict[str, Any]]:
    """Analyze tables and return data instead of printing"""
    if not tables:
        return None

    analyzed_tables = []
    for table in tables:
        table_data = []
        for row in table:
            row_data = []
            for cell in row:
                row_data.append(
                    {
                        "text": cell.text.strip() if cell.text else "<NO VALUE GIVEN>",
                        "row": cell.row,
                        "column": cell.column,
                        "row_span": cell.row_span,
                        "column_span": cell.column_span,
                        "is_merged": cell.is_merged,
                        "confidence": cell.confidence,
                        "selected": cell.selected,
                    }
                )
            table_data.append(row_data)

        # Calculate table statistics
        total_cells = sum(1 for row in table for cell in row)
        filled_cells = sum(
            1
            for row in table
            for cell in row
            if cell.text.strip() and not cell.is_merged
        )
        empty_cells = sum(
            1
            for row in table
            for cell in row
            if not cell.text.strip() and not cell.is_merged
        )
        merged_cells = sum(
            1 for row in table for cell in row if cell.is_merged and cell.row_span > 0
        )
        merged_spans = sum(
            1 for row in table for cell in row if cell.is_merged and cell.row_span == 0
        )

        valid_cells = [
            cell
            for row in table
            for cell in row
            if cell.text.strip() and not cell.is_merged
        ]
        avg_confidence = (
            (sum(cell.confidence for cell in valid_cells) / len(valid_cells))
            if valid_cells
            else 0
        )

        analyzed_tables.append(
            {
                "data": table_data,
                "summary": {
                    "total_cells": total_cells,
                    "filled_cells": filled_cells,
                    "empty_cells": empty_cells,
                    "merged_cells": merged_cells,
                    "merged_spans": merged_spans,
                    "average_confidence": avg_confidence,
                },
            }
        )

    return analyzed_tables


def get_kv(json_response: Dict) -> List[Dict[str, Any]]:
    """
    Extract key-value pairs from Textract JSON response.

    This function identifies and extracts key-value pairs from form fields,
    including their confidence scores and geometric information.

    Args:
        json_response (Dict): Raw Textract JSON response containing:
            - Blocks: List of text blocks
            - Relationships: Block relationships
            - BlockType: Type identifiers

    Returns:
        List[Dict[str, Any]]: List of key-value pairs, each containing:
            - key: Field identifier/label
            - value: Field content (or "<NO VALUE GIVEN>" if empty)
            - confidence: Detection confidence score (0-100)
            - geometry: Geometric information for key and value

    Raises:
        Exception: If error occurs during extraction

    Example:
        >>> kv_pairs = get_kv(textract_json)
        >>> for pair in kv_pairs:
        ...     print(f"{pair['key']}: {pair['value']} ({pair['confidence']}%)")
    """
    try:
        blocks = json_response.get("Blocks", [])
        content = format_readable_output(blocks)

        kv_pairs = []
        if content.form_fields:
            for field in content.form_fields:
                kv_pairs.append(
                    {
                        "key": field["key"],
                        "value": field["value"].strip()
                        if field["value"]
                        else "<NO VALUE GIVEN>",
                        "confidence": field["confidence"],
                        "geometry": field["geometry"],
                    }
                )
        return kv_pairs
    except Exception as e:
        logger.error(f"Error getting key-value pairs: {str(e)}")
        raise


def get_tables(json_response: Dict) -> List[Dict[str, Any]]:
    """
    Extract table data from Textract JSON response.

    This function identifies and processes table structures, handling merged cells
    and maintaining row/column relationships.

    Args:
        json_response (Dict): Raw Textract JSON response containing:
            - Blocks: List of text blocks
            - Relationships: Table structure relationships
            - BlockType: Type identifiers including TABLE, CELL

    Returns:
        List[Dict[str, Any]]: List of tables, each containing:
            - data: 2D array of cells with text and confidence
            - structure: Table structure information
            - merged_cells: Information about merged cells
            - confidence: Overall table confidence score

    Raises:
        Exception: If error occurs during table extraction

    Example:
        >>> tables = get_tables(textract_json)
        >>> for i, table in enumerate(tables):
        ...     print(f"Table {i+1}: {len(table['data'])} rows")
    """
    try:
        blocks = json_response.get("Blocks", [])
        content = format_readable_output(blocks)

        tables = []
        if content.tables:
            for table in content.tables:
                table_data = []
                for row in table:
                    row_data = []
                    for cell in row:
                        row_data.append(
                            {
                                "text": cell.text.strip()
                                if cell.text
                                else "<NO VALUE GIVEN>",
                                "confidence": cell.confidence,
                                "row": cell.row,
                                "column": cell.column,
                            }
                        )
                    table_data.append(row_data)
                tables.append(table_data)
        return tables
    except Exception as e:
        logger.error(f"Error getting tables: {str(e)}")
        raise


def search_in_lines(json_response: Dict, search_text: str) -> List[Dict[str, Any]]:
    """
    Search for text in LINE blocks
    Returns list of matching lines with their confidence scores and positions
    """
    try:
        blocks = json_response.get("Blocks", [])
        matching_lines = []

        for block in blocks:
            if block["BlockType"] == "LINE" and "Text" in block:
                line_text = block["Text"]
                if search_text.lower() in line_text.lower():  # Case-insensitive search
                    matching_lines.append(
                        {
                            "text": line_text,
                            "confidence": block.get("Confidence", 0.0),
                            "position": {
                                "left": block["Geometry"]["BoundingBox"]["Left"],
                                "top": block["Geometry"]["BoundingBox"]["Top"],
                            },
                            "block_id": block["Id"],
                        }
                    )

        return matching_lines
    except Exception as e:
        logger.error(f"Error searching in lines: {str(e)}")
        raise


def search_in_words(json_response: Dict, search_text: str) -> List[Dict[str, Any]]:
    """
    Search for text in WORD blocks
    Returns list of matching words with their confidence scores and positions
    """
    try:
        blocks = json_response.get("Blocks", [])
        matching_words = []

        for block in blocks:
            if block["BlockType"] == "WORD" and "Text" in block:
                word_text = block["Text"]
                if search_text.lower() in word_text.lower():  # Case-insensitive search
                    matching_words.append(
                        {
                            "text": word_text,
                            "confidence": block.get("Confidence", 0.0),
                            "position": {
                                "left": block["Geometry"]["BoundingBox"]["Left"],
                                "top": block["Geometry"]["BoundingBox"]["Top"],
                                "width": block["Geometry"]["BoundingBox"]["Width"],
                                "height": block["Geometry"]["BoundingBox"]["Height"],
                            },
                            "block_id": block["Id"],
                        }
                    )

        return matching_words
    except Exception as e:
        logger.error(f"Error searching in words: {str(e)}")
        raise


def get_table_titles(json_response: Dict) -> List[Dict[str, Any]]:
    """
    Get table titles by analyzing text blocks above tables
    Returns list of potential table titles with their positions and confidence
    """
    try:
        blocks = json_response.get("Blocks", [])
        table_titles = []

        for block in blocks:
            if block["BlockType"] == "TABLE":
                table_bbox = block["Geometry"]["BoundingBox"]
                table_top = table_bbox["Top"]
                table_left = table_bbox["Left"]

                # Look for text blocks just above the table
                potential_titles = []
                for text_block in blocks:
                    if text_block["BlockType"] in [
                        "LINE",
                        "LAYOUT_TITLE",
                        "LAYOUT_SECTION_HEADER",
                    ]:
                        text_bbox = text_block["Geometry"]["BoundingBox"]
                        text_bottom = text_bbox["Top"] + text_bbox["Height"]

                        # Check if text is just above table (within reasonable distance)
                        vertical_distance = table_top - text_bottom
                        horizontal_overlap = (
                            text_bbox["Left"] < (table_left + table_bbox["Width"])
                            and (text_bbox["Left"] + text_bbox["Width"]) > table_left
                        )

                        if (
                            0 <= vertical_distance < 0.05 and horizontal_overlap
                        ):  # Adjust threshold as needed
                            potential_titles.append(
                                {
                                    "text": get_text_from_block(text_block, blocks),
                                    "confidence": text_block.get("Confidence", 0.0),
                                    "position": {
                                        "left": text_bbox["Left"],
                                        "top": text_bbox["Top"],
                                        "width": text_bbox["Width"],
                                        "height": text_bbox["Height"],
                                    },
                                    "distance_to_table": vertical_distance,
                                    "block_id": text_block["Id"],
                                }
                            )

                # Sort by distance and take the closest one
                if potential_titles:
                    closest_title = min(
                        potential_titles, key=lambda x: x["distance_to_table"]
                    )
                    table_titles.append(
                        {
                            "table_id": block["Id"],
                            "title": closest_title["text"],
                            "confidence": closest_title["confidence"],
                            "position": closest_title["position"],
                        }
                    )
                else:
                    # If no title found, add None
                    table_titles.append(
                        {
                            "table_id": block["Id"],
                            "title": "<NO TITLE FOUND>",
                            "confidence": 0.0,
                            "position": None,
                        }
                    )

        return table_titles
    except Exception as e:
        logger.error(f"Error getting table titles: {str(e)}")
        raise


def get_text_in_reading_order(json_response: Dict) -> List[Dict[str, Any]]:
    """
    Get all text blocks in reading order (top to bottom, left to right)
    Returns list of text blocks with their positions and confidence scores
    """
    try:
        blocks = json_response.get("Blocks", [])
        text_blocks = []

        # Get all text blocks (LINE and WORD)
        for block in blocks:
            if block["BlockType"] in ["LINE", "WORD"] and "Text" in block:
                text_blocks.append(
                    {
                        "text": block["Text"],
                        "type": block["BlockType"],
                        "confidence": block.get("Confidence", 0.0),
                        "position": {
                            "left": block["Geometry"]["BoundingBox"]["Left"],
                            "top": block["Geometry"]["BoundingBox"]["Top"],
                            "width": block["Geometry"]["BoundingBox"]["Width"],
                            "height": block["Geometry"]["BoundingBox"]["Height"],
                        },
                        "block_id": block["Id"],
                    }
                )

        # Sort blocks by position (top to bottom, then left to right)
        # Using a small threshold for "same line" detection
        SAME_LINE_THRESHOLD = 0.01

        def sort_key(block):
            top = block["position"]["top"]
            left = block["position"]["left"]
            # Group blocks that are roughly on the same line
            row = int(top / SAME_LINE_THRESHOLD)
            return (row, left)

        return sorted(text_blocks, key=sort_key)

    except Exception as e:
        logger.error(f"Error getting text in reading order: {str(e)}")
        raise


def get_page_json(json_response: Dict, page_number: int = 1) -> Dict:
    """
    Get JSON data for a specific page
    Returns the page's blocks and metadata
    """
    try:
        blocks = json_response.get("Blocks", [])
        page_blocks = []
        page_found = False

        # Find the PAGE block for the requested page
        for block in blocks:
            if block["BlockType"] == "PAGE" and len(page_blocks) + 1 == page_number:
                page_found = True
                page_metadata = {
                    "page_number": page_number,
                    "geometry": block["Geometry"],
                    "id": block["Id"],
                }

                # Get all child blocks for this page
                if "Relationships" in block:
                    for rel in block["Relationships"]:
                        if rel["Type"] == "CHILD":
                            for child_id in rel["Ids"]:
                                child_block = next(
                                    (b for b in blocks if b["Id"] == child_id), None
                                )
                                if child_block:
                                    page_blocks.append(child_block)

                return {"metadata": page_metadata, "blocks": page_blocks}

        if not page_found:
            return {
                "error": f"Page {page_number} not found in document",
                "total_pages": sum(
                    1 for block in blocks if block["BlockType"] == "PAGE"
                ),
            }

    except Exception as e:
        logger.error(f"Error getting page JSON: {str(e)}")
        raise


def get_selection_elements(json_response: Dict) -> List[Dict[str, Any]]:
    """
    Get all selection elements (checkboxes, radio buttons, etc.)
    Returns list of selection elements with their status and position
    """
    try:
        blocks = json_response.get("Blocks", [])
        selection_elements = []

        for block in blocks:
            if block["BlockType"] == "SELECTION_ELEMENT":
                element = {
                    "selected": block.get("SelectionStatus") == "SELECTED",
                    "confidence": block.get("Confidence", 0.0),
                    "position": {
                        "left": block["Geometry"]["BoundingBox"]["Left"],
                        "top": block["Geometry"]["BoundingBox"]["Top"],
                        "width": block["Geometry"]["BoundingBox"]["Width"],
                        "height": block["Geometry"]["BoundingBox"]["Height"],
                    },
                    "block_id": block["Id"],
                }

                # Try to find associated text label
                label_text = find_selection_element_label(block, blocks)
                if label_text:
                    element["label"] = label_text

                selection_elements.append(element)

        return selection_elements

    except Exception as e:
        logger.error(f"Error getting selection elements: {str(e)}")
        raise


def find_selection_element_label(
    element_block: Dict, blocks: List[Dict], max_distance: float = 0.05
) -> Optional[str]:
    """Helper function to find text label associated with a selection element"""
    element_bbox = element_block["Geometry"]["BoundingBox"]
    element_center = {
        "x": element_bbox["Left"] + element_bbox["Width"] / 2,
        "y": element_bbox["Top"] + element_bbox["Height"] / 2,
    }

    nearest_text = None
    min_distance = float("inf")

    for block in blocks:
        if block["BlockType"] in ["WORD", "LINE"] and "Text" in block:
            text_bbox = block["Geometry"]["BoundingBox"]
            text_center = {
                "x": text_bbox["Left"] + text_bbox["Width"] / 2,
                "y": text_bbox["Top"] + text_bbox["Height"] / 2,
            }

            # Calculate distance between centers
            distance = (
                (text_center["x"] - element_center["x"]) ** 2
                + (text_center["y"] - element_center["y"]) ** 2
            ) ** 0.5

            if distance < min_distance and distance < max_distance:
                min_distance = distance
                nearest_text = block["Text"]

    return nearest_text


def generate_html_report(
    analysis_results: Dict, output_file: str = "textract_report.html"
) -> None:
    """
    Generate an HTML report from the analysis results.

    Args:
        analysis_results (Dict): Results from analyze_document()
        output_file (str): Path where HTML report should be saved

    The HTML report includes:
        - Document layout visualization
        - Form fields with values and confidence scores
        - Tables with cell data
        - Query results if present
        - Geometric information and relationships

    Example:
        >>> generate_html_report(analysis_results, 'report.html')
    """

    def format_layout_section(layout_data: Dict) -> str:
        if not layout_data:
            return "<p>No layout information available</p>"

        content = []
        for layout_type, blocks in layout_data.items():
            content.append(f"<h3>{layout_type}</h3>")
            if blocks:
                content.append("<ul>")
                for block in blocks:
                    basic_info = f"<li class='basic-info'>{block['content']}</li>"

                    detailed_info = []
                    if block.get("confidence"):
                        detailed_info.append(
                            f"<span class='confidence'>({block['confidence']:.1f}%)</span>"
                        )
                    if block.get("position"):
                        pos = block["position"]
                        detailed_info.append(
                            f"<div class='detailed-info'>Position: "
                            f"Top {pos['top']:.3f}, Left {pos['left']:.3f}, "
                            f"Width {pos['width']:.3f}, Height {pos['height']:.3f}</div>"
                        )

                    content.append(
                        f"<li>{block['content']} {''.join(detailed_info)}</li>"
                    )
                content.append("</ul>")
        return "\n".join(content)

    def format_form_fields_section(form_data: Dict) -> str:
        if not form_data:
            return "<p>No form fields found</p>"

        content = [
            "<table>",
            "<tr><th>Key</th><th>Value</th><th>Confidence</th><th class='detailed-info'>Details</th></tr>",
        ]

        for field in form_data["fields"]:
            basic_info = (
                f"<tr>"
                f"<td>{field['key']}</td>"
                f"<td>{field['value']}</td>"
                f"<td class='confidence'>{field['confidence']:.1f}%</td>"
            )

            detailed_info = format_detailed_info(field)

            content.append(
                f"{basic_info}"
                f"<td class='detailed-info geometric'>{detailed_info}</td>"
                f"</tr>"
            )

        content.append("</table>")

        # Add summary
        summary = form_data["summary"]
        content.append("<div class='summary'>")
        content.append(f"<p>Total Fields: {summary['total_fields']}</p>")
        content.append(f"<p>Filled Values: {summary['filled_values']}</p>")
        content.append(f"<p>Empty Values: {summary['empty_values']}</p>")
        content.append(
            f"<p>Average Confidence: {summary['average_confidence']:.1f}%</p>"
        )
        content.append("</div>")

        return "\n".join(content)

    def format_queries_section(queries_data: Dict) -> str:
        if not queries_data:
            return "<p>No queries found</p>"

        content = [
            "<table>",
            "<tr><th>Question</th><th>Answer</th><th>Confidence</th></tr>",
        ]
        for query in queries_data.get("QUERIES", []):
            content.append(
                f"<tr><td>{query['query']}</td>"
                f"<td>{query['query_answer']}</td>"
                f"<td class='confidence'>{query['confidence']:.1f}%</td></tr>"
            )
        content.append("</table>")
        return "\n".join(content)

    def format_tables_section(tables_data: List) -> str:
        if not tables_data:
            return "<p>No tables found</p>"

        content = []
        for i, table in enumerate(tables_data, 1):
            content.append(f"<h3>Table {i}</h3>")
            content.append("<table>")
            for row in table["data"]:
                content.append("<tr>")
                for cell in row:
                    basic_info = f"<td>{cell['text']}</td>"
                    detailed_info = (
                        f"<td class='detailed-info'>({cell['confidence']:.1f}%)</td>"
                    )
                    content.append(f"{basic_info}{detailed_info}")
                content.append("</tr>")
            content.append("</table>")
        return "\n".join(content)

    html_template = r"""<!DOCTYPE html>
    <html>
    <head>
        <title>Textract Analysis Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                line-height: 1.6;
            }}
            .section {{
                margin: 20px 0;
                padding: 15px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 10px 0;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f5f5f5;
            }}
            .confidence {{
                color: #666;
                font-size: 0.9em;
            }}
            .summary {{
                background-color: #f8f9fa;
                padding: 10px;
                margin-top: 10px;
            }}
            .geometric {{
                font-size: 0.9em;
                color: #555;
                background-color: #f8f9fa;
                padding: 5px;
            }}
            .toggle-container {{
                position: fixed;
                top: 20px;
                right: 20px;
                background: white;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .detailed-info {{
                display: none;
            }}
            .switch {{
                position: relative;
                display: inline-block;
                width: 60px;
                height: 34px;
            }}
            .switch input {{
                opacity: 0;
                width: 0;
                height: 0;
            }}
            .slider {{
                position: absolute;
                cursor: pointer;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background-color: #ccc;
                transition: .4s;
                border-radius: 34px;
            }}
            .slider:before {{
                position: absolute;
                content: "";
                height: 26px;
                width: 26px;
                left: 4px;
                bottom: 4px;
                background-color: white;
                transition: .4s;
                border-radius: 50%;
            }}
            input:checked + .slider {{
                background-color: #2196F3;
            }}
            input:checked + .slider:before {{
                transform: translateX(26px);
            }}
        </style>
    </head>
    <body>
        <div class="toggle-container">
            <label class="switch">
                <input type="checkbox" id="detailToggle">
                <span class="slider"></span>
            </label>
            <span>Show Details</span>
        </div>

        <h1>Textract Analysis Report</h1>
        <div class="timestamp">Generated on: {timestamp}</div>

        <div class="section">
            <h2>Document Layout</h2>
            {layout_content}
        </div>

        <div class="section">
            <h2>Form Fields</h2>
            {form_fields_content}
        </div>

        <div class="section">
            <h2>Queries and Answers</h2>
            {queries_content}
        </div>

        <div class="section">
            <h2>Tables</h2>
            {tables_content}
        </div>

        <script>
            document.getElementById('detailToggle').addEventListener('change', function() {{
                const detailedInfo = document.querySelectorAll('.detailed-info');
                const basicInfo = document.querySelectorAll('.basic-info');
                detailedInfo.forEach(el => {{
                    el.style.display = this.checked ? 'table-cell' : 'none';
                }});
                basicInfo.forEach(el => {{
                    el.style.display = this.checked ? 'none' : 'table-cell';
                }});
            }});
        </script>
    </body>
    </html>"""

    try:
        # Format each section
        layout_content = format_layout_section(analysis_results.get("layout", {}))
        form_fields_content = format_form_fields_section(
            analysis_results.get("form_fields", {})
        )
        queries_content = format_queries_section(analysis_results.get("queries", {}))
        tables_content = format_tables_section(analysis_results.get("tables", []))

        # Generate the complete HTML
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        html_content = html_template.format(
            timestamp=timestamp,
            layout_content=layout_content,
            form_fields_content=form_fields_content,
            queries_content=queries_content,
            tables_content=tables_content,
        )

        # Write to file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_content)

        logger.info(f"HTML report generated: {output_file}")

    except Exception as e:
        logger.error(f"Error generating HTML report: {str(e)}")
        raise


def find_text_by_geometry(
    block: Dict, blocks: List[Dict], max_distance: float = 0.05
) -> List[Dict[str, Any]]:
    """Find text blocks near a given block based on geometric proximity"""
    if "Geometry" not in block or "BoundingBox" not in block["Geometry"]:
        return []

    source_bbox = block["Geometry"]["BoundingBox"]
    # Check if required keys exist in source_bbox
    if not all(key in source_bbox for key in ["Left", "Top", "Width", "Height"]):
        return []

    source_polygon = get_polygon_points(block)
    source_center = {
        "x": source_bbox["Left"] + source_bbox["Width"] / 2,
        "y": source_bbox["Top"] + source_bbox["Height"] / 2,
    }

    nearby_texts = []

    for other_block in blocks:
        if other_block["BlockType"] in ["LINE", "WORD"] and "Text" in other_block:
            if (
                "Geometry" not in other_block
                or "BoundingBox" not in other_block["Geometry"]
            ):
                continue

            other_bbox = other_block["Geometry"]["BoundingBox"]
            # Check if required keys exist in other_bbox
            if not all(key in other_bbox for key in ["Left", "Top", "Width", "Height"]):
                continue

            other_polygon = get_polygon_points(other_block)
            other_center = {
                "x": other_bbox["Left"] + other_bbox["Width"] / 2,
                "y": other_bbox["Top"] + other_bbox["Height"] / 2,
            }

            # Calculate distances
            horizontal_distance = abs(other_center["x"] - source_center["x"])
            vertical_distance = abs(other_center["y"] - source_center["y"])
            euclidean_distance = (
                horizontal_distance**2 + vertical_distance**2
            ) ** 0.5

            # Determine relative position
            position = "UNKNOWN"
            if other_bbox["Left"] > source_bbox["Left"] + source_bbox["Width"]:
                position = "RIGHT"
            elif other_bbox["Left"] + other_bbox["Width"] < source_bbox["Left"]:
                position = "LEFT"
            elif other_bbox["Top"] > source_bbox["Top"] + source_bbox["Height"]:
                position = "BELOW"
            elif other_bbox["Top"] + other_bbox["Height"] < source_bbox["Top"]:
                position = "ABOVE"

            # Calculate polygon overlap if both have polygons
            polygon_overlap = 0.0
            if source_polygon and other_polygon:
                polygon_overlap = calculate_polygon_overlap(
                    source_polygon, other_polygon
                )

            if euclidean_distance <= max_distance or polygon_overlap > 0:
                nearby_texts.append(
                    {
                        "text": other_block["Text"],
                        "block_type": other_block["BlockType"],
                        "confidence": other_block.get("Confidence", 0.0),
                        "position": position,
                        "distance": euclidean_distance,
                        "polygon_overlap": polygon_overlap,
                        "geometry": {
                            "bounding_box": other_bbox,
                            "polygon": other_polygon,
                        },
                        "block_id": other_block["Id"],
                    }
                )

    # Sort by distance and polygon overlap (prioritize overlapping text)
    return sorted(
        nearby_texts, key=lambda x: (x["polygon_overlap"] == 0, x["distance"])
    )


def get_polygon_points(block: Dict) -> List[Dict[str, float]]:
    """Extract polygon points from a block's geometry"""
    if "Geometry" in block and "Polygon" in block["Geometry"]:
        return [
            {"x": point["X"], "y": point["Y"]} for point in block["Geometry"]["Polygon"]
        ]
    return []


def calculate_polygon_overlap(
    poly1: List[Dict[str, float]], poly2: List[Dict[str, float]]
) -> float:
    """
    Calculate overlap between two polygons
    Returns overlap score between 0 and 1
    """
    # Simple overlap check using bounding boxes of polygons
    x1_min = min(p["x"] for p in poly1)
    x1_max = max(p["x"] for p in poly1)
    y1_min = min(p["y"] for p in poly1)
    y1_max = max(p["y"] for p in poly1)

    x2_min = min(p["x"] for p in poly2)
    x2_max = max(p["x"] for p in poly2)
    y2_min = min(p["y"] for p in poly2)
    y2_max = max(p["y"] for p in poly2)

    # Check if polygons overlap
    if x1_max < x2_min or x2_max < x1_min or y1_max < y2_min or y2_max < y1_min:
        return 0.0

    # Calculate overlap area
    x_overlap = min(x1_max, x2_max) - max(x1_min, x2_min)
    y_overlap = min(y1_max, y2_max) - max(y1_min, y2_min)
    overlap_area = x_overlap * y_overlap

    # Calculate total area of both polygons
    area1 = (x1_max - x1_min) * (y1_max - y1_min)
    area2 = (x2_max - x2_min) * (y2_max - y2_min)

    # Return overlap ratio
    return overlap_area / min(area1, area2)


def format_detailed_info(field: Dict) -> str:
    """
    Format detailed information for a form field with geometric and confidence data.

    This function creates a detailed HTML representation of a form field,
    including position information, nearby text, and confidence scores.

    Args:
        field (Dict): Form field data containing:
            - key: Field identifier/label
            - value: Field content
            - confidence: Detection confidence
            - geometry: Geometric information
                - key_bbox: Bounding box for key
                - value_bbox: Bounding box for value
            - key_nearby_text: Text near the key
            - value_nearby_text: Text near the value
            - matching_text: Exact text matches

    Returns:
        str: HTML-formatted string containing:
            - Position information for key and value
            - Up to 3 nearest text blocks for key
            - Up to 3 nearest text blocks for value
            - Matching text blocks with confidence

    Notes:
        - All geometric measurements are normalized (0-1)
        - Confidence scores are displayed as percentages
        - Empty fields are marked as "No detailed information available"
        - HTML formatting uses <strong>, <ul>, <li> tags

    Example:
        >>> field_data = {
        ...     "key": "Name",
        ...     "value": "John Doe",
        ...     "geometry": {...},
        ...     "key_nearby_text": [...]
        ... }
        >>> html = format_detailed_info(field_data)
    """
    details = []

    # Add position information
    if field.get("geometry"):
        details.append("<strong>Position Info:</strong>")
        if field["geometry"].get("key_bbox"):
            key_bbox = field["geometry"]["key_bbox"]
            details.append(
                f"Key: (Top: {key_bbox['Top']:.3f}, "
                f"Left: {key_bbox['Left']:.3f}, "
                f"Width: {key_bbox['Width']:.3f}, "
                f"Height: {key_bbox['Height']:.3f})"
            )
        if field["geometry"].get("value_bbox"):
            value_bbox = field["geometry"]["value_bbox"]
            details.append(
                f"Value: (Top: {value_bbox['Top']:.3f}, "
                f"Left: {value_bbox['Left']:.3f}, "
                f"Width: {value_bbox['Width']:.3f}, "
                f"Height: {value_bbox['Height']:.3f})"
            )

    # Add nearby text information
    if field.get("key_nearby_text"):
        details.append("<strong>Key Nearby Text:</strong><ul>")
        for text in field["key_nearby_text"][:3]:  # Show top 3 nearest texts
            details.append(
                f"<li>{text['block_type']} ({text['position']}): '{text['text']}' "
                f"(Distance: {text['distance']:.3f}, "
                f"Confidence: {text['confidence']:.1f}%)</li>"
            )
        details.append("</ul>")

    if field.get("value_nearby_text"):
        details.append("<strong>Value Nearby Text:</strong><ul>")
        for text in field["value_nearby_text"][:3]:  # Show top 3 nearest texts
            details.append(
                f"<li>{text['block_type']} ({text['position']}): '{text['text']}' "
                f"(Distance: {text['distance']:.3f}, "
                f"Confidence: {text['confidence']:.1f}%)</li>"
            )
        details.append("</ul>")

    # Add matching text information
    if field.get("matching_text"):
        details.append("<strong>Matching Text Blocks:</strong><ul>")
        for match in field["matching_text"]:
            details.append(
                f"<li>{match['block_type']} ({match['match_type']}): '{match['text']}' "
                f"(Confidence: {match['confidence']:.1f}%)</li>"
            )
        details.append("</ul>")

    return "<br>".join(details) if details else "No detailed information available"


def create_concise_results(analysis_results: Dict) -> Dict:
    """
    Create a simplified version of the analysis results.

    Args:
        analysis_results (Dict): Full results from analyze_document()

    Returns:
        Dict: Simplified results containing only essential information:
            - Basic form field data (key-value pairs)
            - Table content without geometric data
            - Query results without detailed analysis

    Example:
        >>> concise = create_concise_results(analysis_results)
        >>> print(len(concise['form_fields']))
    """
    concise = {}

    if "layout" in analysis_results:
        concise["layout"] = {
            k: [{"content": b["content"], "confidence": b["confidence"]} for b in v]
            for k, v in analysis_results["layout"].items()
        }

    if "form_fields" in analysis_results and analysis_results["form_fields"]:
        concise["form_fields"] = {
            "fields": [
                {"key": f["key"], "value": f["value"], "confidence": f["confidence"]}
                for f in analysis_results["form_fields"]["fields"]
            ],
            "summary": analysis_results["form_fields"]["summary"],
        }

    if "queries" in analysis_results and analysis_results["queries"]:
        concise["queries"] = {
            "QUERIES": [
                {
                    "query": q["query"],
                    "query_answer": q["query_answer"],
                    "confidence": q["confidence"],
                }
                for q in analysis_results["queries"]["QUERIES"]
            ]
        }

    if "tables" in analysis_results and analysis_results["tables"]:
        concise["tables"] = [
            {
                "data": [
                    [
                        {"text": cell["text"], "confidence": cell["confidence"]}
                        for cell in row
                    ]
                    for row in table["data"]
                ],
                "summary": table["summary"],
            }
            for table in analysis_results["tables"]
        ]

    return concise
