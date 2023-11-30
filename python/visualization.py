#!/bin/python3

import plotly.graph_objs as go
from plotly.offline import plot

def plot_BWT_mapping(my_string_sorted, my_string, match_list, match_pos,my_pattern):
    """
    Generates a Plotly visualization to map the positions of pattern matches in a string.

    This function takes the sorted string, the original string, a list of matches, 
    and their positions, then creates a Plotly figure to visualize where each 
    match occurs in the original string.

    Args:
        my_string_sorted (list): The sorted version of the original string.
        my_string (str): The original string.
        match_list (list): A list of match information (not used in the current function).
        match_pos (list of tuples): Each tuple contains the start and end positions 
                                    of a match in the format (start, end).

    The function creates a line for each match in the original string. It also 
    adds hover text for each character in the match to provide more information 
    on hover in the visualization.
    """
    # Sort the match positions by their start position for better visualization.
    match_pos = sorted(match_pos, key=lambda x: x[0])
    # Convert the string to uppercase 
    my_string = my_string.upper()
    # Initialize a counter to track the match number (used for Y-axis in the plot).
    match_counter = 1 
    # Create a new Plotly figure.
    fig = go.Figure()
    # Iterate through each match position.
    for pos in match_pos:
        # Add a line shape to represent the match in the plot.
        fig.add_shape(type="line",
                      x0=pos[0], y0=match_counter, x1=pos[1], y1=match_counter,
                      line=dict(color="pink", width=2))

        # For each position in the match, add a scatter plot point.
        for i in range(pos[0], pos[1]+1):
            fig.add_trace(go.Scatter(
                x=[i], y=[match_counter],
                mode='text',
                text='',  # No text inside the points.
                textposition='bottom center',
                hoverinfo='text',
                hovertext=f'{my_string[i]}{i+1}',  # Show character and position on hover.
                showlegend=False
            ))
            # Add an annotation for each character in the match.
            fig.add_annotation(x=i, y=match_counter, text=f"<b>{my_string[i]}</b>",
                               showarrow=False, font=dict(color='black', size=12))
        # Increment the match counter for the next match.
        match_counter += 1
    # Configure X and Y axes of the plot.
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black',
                     tickvals=list(range(len(my_string))),
                     ticktext=list(my_string),
                     range=[-1, 71] if len(my_string) >= 70 else [-1, len(my_string)])
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black', range=[0, match_counter + 1])
    # Set layout properties of the figure.
    fig.update_layout(
        title={
            'text': f"Mapping of Pattern {my_pattern} in the string of interest" if len(my_string) > 20 else f"Mapping of Pattern {my_pattern} in {my_string}",
            'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top', 'font': dict(color='black')},
        xaxis=dict(title="Characters of the sequence", color='black'),
        yaxis=dict(title="Match Number", color='black'),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    # Render the plot in a web browser.
    plot(fig, filename='mapping_plot.html',auto_open=True)