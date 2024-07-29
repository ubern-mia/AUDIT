import plotly.graph_objects as go
from plotly.colors import qualitative
from src.commons.commons import pretty_string


def plot_longitudinal(data, temporal_axis='timepoint', lines=['lesion_size', 'lesion_size_pred']):
    fig = go.Figure()

    colors = qualitative.Pastel

    for n, l in enumerate(lines):
        fig.add_trace(go.Scatter(x=data[temporal_axis], y=data[l], mode='markers+lines', name=pretty_string(l),
                                 line=dict(color=colors[n], width=3), marker=dict(color=colors[n], size=8)))

    # add vertical dashed lines to measure the distance between points and add annotation for distance
    for i in range(len(data)):
        lesion_size = data[lines[0]][i]
        lesion_size_pred = data[lines[1]][i]
        distance = 100 * (lesion_size - lesion_size_pred) / lesion_size
        mid_y = (lesion_size + lesion_size_pred) / 2

        fig.add_trace(go.Scatter(x=[data[temporal_axis][i], data[temporal_axis][i]],
                                 y=[lesion_size, lesion_size_pred],
                                 mode='lines',
                                 line=dict(color=colors[len(lines)], dash='dot', width=2),
                                 showlegend=False,
                                 hoverinfo='skip'
                                 ))

        # Add annotation for the distance
        fig.add_annotation(
            x=data[temporal_axis][i]+0.1, y=mid_y,
            text=f"{distance:.1f}%",
            showarrow=False,
            font=dict(color=colors[len(lines)], size=16)
        )

    fig.update_layout(title="", template='simple_white', height=600, width=1000,
                      xaxis_title=pretty_string(temporal_axis), yaxis_title="Lesion size",
                      legend=dict(
                          orientation="h",
                          yanchor="bottom",
                          y=1.02,
                          xanchor="left",
                          x=.7
                      ),
                      hovermode="x unified"
                      )
    fig.update_xaxes(tickmode='linear', dtick=1, tickformat=',d')

    return fig


def plot_longitudinal2(data, temporal_axis='timepoint', lines=['lesion_size', 'lesion_size_pred']):
    fig = go.Figure()

    colors = qualitative.Pastel

    for n, l in enumerate(lines):
        fig.add_trace(go.Scatter(x=data[temporal_axis], y=data[l], mode='markers+lines', name=pretty_string(l),
                                 line=dict(color=colors[n], width=3), marker=dict(color=colors[n], size=8)))

    # add lines to measure the distance between points and calculate the difference in slopes
    for i in range(len(data) - 1):
        x1, x2 = data[temporal_axis][i], data[temporal_axis][i + 1]
        V1, V2 = data[lines[0]][i], data[lines[0]][i + 1]
        GT1, GT2 = data[lines[1]][i], data[lines[1]][i + 1]

        term1 = abs(V2 - V1) / V1
        term2 = abs(GT2 - GT1) / GT1
        difference = term1 - term2

        mid_x = (x1 + x2) / 2
        mid_y = (V1 + V2 + GT1 + GT2) / 4  # To place the annotation approximately in the middle

        # Add annotation for the calculated difference
        fig.add_annotation(
            x=mid_x, y=mid_y,
            text=f"{difference:.2f}",
            showarrow=False,
            arrowhead=2,
            ax=0, ay=-20,
            font=dict(color=colors[n+1], size=16)
        )



    fig.update_layout(template='simple_white', height=600, width=1000,
                      xaxis_title=pretty_string(temporal_axis), yaxis_title="Lesion size",
                      title="",
                      legend=dict(
                          orientation="h",
                          yanchor="bottom",
                          y=1.02,
                          xanchor="left",
                          x=.7
                      ),
                      hovermode="x unified"
                      )
    fig.update_xaxes(tickmode='linear', dtick=1, tickformat=',d')

    return fig


#
# def plot_longitudinal3(data, temporal_axis='timepoint', lines=['lesion_size', 'lesion_size_pred']):
#     fig = go.Figure()
#
#     colors = qualitative.Pastel
#
#     for n, l in enumerate(lines):
#         fig.add_trace(go.Scatter(x=data[temporal_axis], y=data[l], mode='markers+lines', name=l, line=dict(color=colors[n]), marker=dict(color=colors[n])))
#
#         # Normalize y-values for slope calculation
#         y_min, y_max = data[l].min(), data[l].max()
#         data_normalized = (data[l] - y_min) / (y_max - y_min)
#
#         # Add annotations for the slope of each line
#         for i in range(len(data) - 1):
#             x1, x2 = data[temporal_axis][i], data[temporal_axis][i + 1]
#             y1, y2 = data_normalized[i], data_normalized[i + 1]
#             slope = (y2 - y1) / (x2 - x1)
#             mid_x = (x1 + x2) / 2
#             mid_y = (data[l][i] + data[l][i + 1]) / 2  # Place annotation at actual mid-y value
#
#             # Add annotation for the slope
#             fig.add_annotation(
#                 x=mid_x, y=mid_y,
#                 text=f"{slope:.2f}",
#                 showarrow=True,
#                 arrowhead=2,
#                 ax=0, ay=-20,
#                 font=dict(color=colors[n])
#             )
#
#     fig.update_layout(template='simple_white', height=600, width=1000, xaxis_title="Timepoint", yaxis_title="Lesion size")
#     fig.update_xaxes(tickmode='linear', dtick=1, tickformat=',d')
#
#     return fig
#
#
#
#
# def plot_longitudinal4(data, temporal_axis='timepoint', lines=['lesion_size', 'lesion_size_pred']):
#     fig = go.Figure()
#
#     colors = qualitative.Pastel
#
#     for n, l in enumerate(lines):
#         fig.add_trace(go.Scatter(x=data[temporal_axis], y=data[l], mode='markers+lines', name=l, line=dict(color=colors[n]), marker=dict(color=colors[n])))
#
#         # Add annotations for the slope of each line
#         for i in range(len(data) - 1):
#             x1, x2 = data[temporal_axis][i], data[temporal_axis][i + 1]
#             y1, y2 = data[l][i], data[l][i + 1]
#             slope = (y2 - y1) / (x2 - x1)
#             mid_x = (x1 + x2) / 2
#             mid_y = (y1 + y2) / 2
#
#             # Add annotation for the slope
#             fig.add_annotation(
#                 x=mid_x, y=mid_y,
#                 text=f"{slope:.2f}",
#                 showarrow=True,
#                 arrowhead=2,
#                 ax=0, ay=-20,
#                 font=dict(color=colors[n])
#             )
#
#
#     fig.update_layout(template='simple_white', height=600, width=1000, xaxis_title="Timepoint", yaxis_title="Lesion size")
#     fig.update_xaxes(tickmode='linear', dtick=1, tickformat=',d')
#
#     return fig
