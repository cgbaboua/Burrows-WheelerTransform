#!/bin/python3

def get_match_ignore_mismatch(pattern, FM, C, my_string, n_mismatch=1):
    """
    Find matches of a pattern in a string allowing for a specified number of mismatches.

    Args:
        pattern (str): The pattern to be matched.
        FM (list): The FM-index of the string.
        C (dict): A dictionary containing the count of characters.
        my_string (str): The string in which the pattern is to be searched.
        n_mismatch (int): The number of allowed mismatches.

    Returns:
        list: A list of tuples representing the range of matches.
    """
    # Initialize a stack for DFS with initial parameters.
    stack = [(pattern[::-1].upper(), 0, n_mismatch, 0, 0, len(FM) - 1)]
    results = []
    string_length = len(my_string)
    # Process each item in the stack.
    while stack:
        curr_pattern, curr_pos, allowed_mismatches, curr_mismatches, curr_top, curr_bot = stack.pop()
        # Skip if the current position plus pattern length exceeds string length.
        if string_length is not None and curr_pos + len(curr_pattern) > string_length:
            continue
        # Skip if the number of mismatches exceeded the allowed limit.
        if curr_mismatches > allowed_mismatches:
            continue
        # If the pattern is fully processed, add the range to the results.
        if len(curr_pattern) == 0:
            results.append((curr_top, curr_bot))
            continue
        # Process the next character in the pattern.
        curr_char = curr_pattern[0]
        for char in C:
            # Handle mismatch case.
            if char != curr_char:
                updated_top = C[char] + FM[curr_top][char]
                updated_bot = C[char] + FM[curr_bot][char]
                if updated_top != updated_bot:
                    stack.append((curr_pattern[1:], curr_pos + 1, allowed_mismatches, curr_mismatches + 1, updated_top, updated_bot))
            # Handle match case.
            else:
                updated_top = C[curr_char] + FM[curr_top][curr_char]
                updated_bot = C[curr_char] + FM[curr_bot][curr_char]
                if updated_top != updated_bot:
                    stack.append((curr_pattern[1:], curr_pos + 1, allowed_mismatches, curr_mismatches, updated_top, updated_bot))
    return results

def n_match(match):
    """
    Calculate the total number of positions in a set of match ranges.

    Args:
        match (list): A list of tuples representing match ranges.

    Returns:
        int: The total number of positions in the match ranges.
    """
    tot=0
    # Calculate the number of positions in each match range and add to the total.
    for m in match:
        tot+= len(range(*m))
    return tot

def get_match_pos_mismatch(match, L, all_pos, my_string):
    """
    Get the start and end positions of matches allowing mismatches in a string.

    Args:
        match (list): A list of tuples representing match ranges.
        L (int): Length of the pattern being matched.
        all_pos (list): A list of positions for each character in the string.
        my_string (str): The string in which the pattern is being matched.

    Returns:
        list: A list of lists, where each inner list contains the start and end positions of a match.
    """
    string_length = len(my_string)
    l_range = n_match(match)
    if l_range == 0:
        print('This is not a match')
        return ()
    pos = []
    # Iterate through each match range.
    for m_range in match:
        for m in range(*m_range):
            start_pos = all_pos[m]
            end_pos = start_pos + L - 1
            # Check if the end position is valid and the entire pattern can be placed.
            if end_pos < string_length:
                pos.append([start_pos, end_pos])
    # Sort the positions for clarity.
    sorted_pos = sorted(pos, key=lambda x: x[0])
    return sorted_pos
