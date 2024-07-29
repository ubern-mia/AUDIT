import plotly.express as px
from src.commons.commons import pretty_string
from src.commons.commons import all_capitals
from src.visualization.constants import Dashboard

constants = Dashboard()

def scatter_plot_features(data, x_axis, y_axis, y_label=None, x_label=None, color="Dataset", log_x=False, log_y=False,
                          legend_title=None):

    if y_label is None:
        y_label = f"{pretty_string(y_axis)}"

    if x_label is None:
        x_label = f"{pretty_string(x_axis)}"

    # define the scatterplot
    if color == "Dataset":
        fig = px.scatter(data, x=x_axis, y=y_axis, color='set', custom_data=["ID", x_axis, y_axis],
                         color_discrete_sequence=constants.discrete_color_palette, log_x=log_x, log_y=log_y)
        fig.update_layout(legend_title=color, legend=dict(yanchor="top", xanchor="right"))
    else:
        fig = px.scatter(data, x=x_axis, y=y_axis, color=color, custom_data=["ID", x_axis, y_axis],
                         color_continuous_scale=constants.continuous_color_palette, log_x=log_x, log_y=log_y)
        fig.update_layout(coloraxis_colorbar=dict(
            title=legend_title,
            y=0.5,
            x=1.05,
            len=0.85,
            yanchor="middle",
            xanchor="left",
            ticks="outside")
        )

    # set up template
    fig.update_layout(template='simple_white', height=600, width=1000, xaxis_title=x_label, yaxis_title=y_label)

    # set up traces and markers
    fig.update_traces(marker=dict(size=12, line=dict(width=1, color='DarkSlateGrey')),
                      selector=dict(mode='markers'),
                      hovertemplate='ID: %{customdata[0]}<br>'
                                    f'{pretty_string(x_axis)}: ' + '%{customdata[1]:,}<br>'
                                    f'{pretty_string(y_axis)}: ' + '%{customdata[2]:,}')

    return fig


def scatter_plot_metric_feature(data, x_axis, y_axis, y_label=None, x_label=None, color="Dataset", facet_col=None,
                                highlighted_patients=None):

    if y_label is None:
        y_label = f"{pretty_string(y_axis)}"

    if x_label is None:
        x_label = f"{pretty_string(x_axis)}"

    color_axis = 'set'
    if color != "Dataset":
        color_axis = color

    # Use a predefined Plotly color palette
    color_palette = constants.discrete_color_palette

    fig = px.scatter(data, x=x_axis, y=y_axis, color=color_axis, facet_col=facet_col,
                     custom_data=["ID", x_axis, y_axis, data["model"].apply(pretty_string).apply(all_capitals)],
                     color_discrete_sequence=color_palette)

    fig.update_layout(template='simple_white',
                      height=600,
                      width=1000,
                      showlegend=True,
                      xaxis_title=x_label,
                      yaxis_title=y_label,
                      legend_title=color,
                      legend=dict(yanchor="top", xanchor="right")
                      )

    fig.update_traces(marker=dict(size=12,
                                  line=dict(width=1, color='DarkSlateGrey')),
                      selector=dict(mode='markers'),
                      hovertemplate='ID: %{customdata[0]}<br>'
                                    f'{pretty_string(x_axis)}: ' + '%{customdata[1]:,.2f}<br>'
                                    f'{pretty_string(y_axis)}: ' + '%{customdata[2]:,.3f}<br>'
                                    'Model: %{customdata[3]}'
                      )

    # fig.for_each_yaxis(lambda y: pretty_string(y_label))

    # highligting specific patients
    if highlighted_patients is not None:
        highlighted_data = data[data["ID"].isin(highlighted_patients)]
        fig.add_traces(
            px.scatter(highlighted_data, x=x_axis, y=y_axis, facet_col=facet_col,
                       custom_data=["ID", x_axis, y_axis, highlighted_data["model"].apply(pretty_string).apply(all_capitals)]
                       ).update_traces(
                marker=dict(size=12, line=dict(width=2, color='Black'), color="red"),
                selector=dict(mode='markers'), hovertemplate='ID: %{customdata[0]}<br>'
                                    f'{pretty_string(x_axis)}: ' + '%{customdata[1]:,.2f}<br>'
                                    f'{pretty_string(y_axis)}: ' + '%{customdata[2]:,.3f}<br>'
                                    'Model: %{customdata[3]}', hoverlabel=dict(bgcolor = ['#ff99c8'])).data
        )

    return fig
