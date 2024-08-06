import plotly.graph_objects as go
from src.commons.commons import pretty_string
from src.visualization.constants import Dashboard

constants = Dashboard()


def aggregated_pairwise_model_performance(data):
    metric, set_ = data.metric.unique()[0], data.set.unique()[0]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=data["relative_diff"], y=data["region"], orientation='h',
                         marker_color=data["gain"], marker_line=dict(width=1, color='black'),
                         hovertemplate="% diff " + pretty_string(metric) + ": %{x:.2f}%<br>Region: %{y}<br>Dataset: " + set_))
    fig.update_xaxes(showline=False)
    fig.update_traces(width=constants.bar_width)
    fig.update_layout(template=constants.template,
                      height=300,
                      width=800,
                      showlegend=False,
                      margin=dict(b=20, t=20)
                      )

    return fig


def individual_pairwise_model_performance(data):
    figures = []
    metric, set_ = data.metric.unique()[0], data.set.unique()[0]
    for case in data.ID.unique():
        df = data[data.ID == case]
        lesion_location = round(df["whole_tumor_location"].unique()[0], 2)
        lesion_size = int(df["lesion_size"].unique()[0])

        fig = go.Figure()
        fig.add_trace(go.Bar(x=df["relative_diff"], y=df["region"], orientation='h',
                             marker_color=df["gain"], marker_line=dict(width=1, color='black'),
                             hovertemplate="Patient: "f'{case}'" <br>" +
                                            pretty_string(metric) + " : %{x:.2f}%<br>"
                                           "Region: %{y}<br>Dataset: " + set_))
        fig.update_xaxes(showline=False)
        fig.update_traces(width=constants.bar_width)
        fig.update_layout(template=constants.template,
                          height=200,
                          width=800,
                          showlegend=False,
                          xaxis_range=[data['relative_diff'].min() - .5, data['relative_diff'].max() + .5],
                          margin=dict(b=20, t=30),
                          title=f"{case} - Lesion location: {lesion_location} - Lesion size: {lesion_size:,}",
                          )

        figures.append(fig)

    return figures
