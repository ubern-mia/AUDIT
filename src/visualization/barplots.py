import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from src.commons.commons import pretty_string


def custom_barplot(data, orderby="patient", metric='dice'):
    # defining order
    order_col = orderby
    order = sorted(data[order_col].unique().tolist())
    data[order_col] = pd.Categorical(data[order_col], categories=order, ordered=True)

    # defining colorscale
    color_scale = px.colors.diverging.RdYlGn

    # building the bar plot
    fig = px.bar(data, x=metric, y='region',
                 color=metric,
                 facet_row=order_col,
                 orientation='h',
                 color_continuous_scale=color_scale,
                 title=metric,
                 labels={metric: metric, 'Category': 'Category'},
                 category_orders={"order": order})

    # custom layout
    fig.update_layout(template='simple_white',
                      title="Comparison model performance",
                      height=int(2000),
                      width=800,
                      showlegend=False
                     )

    fig.update(layout_coloraxis_showscale=False)  # remove scale color bar
    fig.update_traces(width=.7)  # narrow bars
    fig.update_xaxes(showline=True)  # hide x-axis

    return fig


def barplot(data):
    all_figures = []
    metric, set_ = data.metric.unique()[0], data.set.unique()[0]
    for case in data.ID.unique():
        df = data[data.ID == case]
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df["dice"], y=df["region"], orientation='h',
                             marker_color=df["gain"], marker_line=dict(width=1, color='black'),
                             hovertemplate="Patient: "f'{case}'" <br>"
                                           "f'{metric}': %{x:.2f}%<br>"
                                           "Region: %{y}<br>Dataset: " + set_))
        fig.update_xaxes(showline=False)
        fig.update_yaxes(title_text=f"Patient ID - {case}")
        fig.update_traces(width=.8)  # narrow bars
        fig.update_layout(template='simple_white',
                          height=200,
                          width=800,
                          showlegend=False,
                          xaxis_range=[data['dice'].min() - .5, data['dice'].max() + .5],
                          margin=dict(b=20, t=20)
                          )

        all_figures.append(fig)

    return all_figures


def aggregated_barplot(data):
    metric, set_ = data.metric.unique()[0], data.set.unique()[0]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=data["relative_diff"], y=data["region"], orientation='h',
                         marker_color=data["gain"], marker_line=dict(width=1, color='black'),
                         hovertemplate="% diff " + pretty_string(metric) + ": %{x:.2f}%<br>Region: %{y}<br>Dataset: " + set_))
    fig.update_xaxes(showline=False)
    fig.update_traces(width=.8)  # narrow bars
    fig.update_layout(template='simple_white',
                      height=300,
                      width=800,
                      showlegend=False,
                      margin=dict(b=20, t=20)
                      )

    return fig


def barplot_v2(data):
    all_figures = []
    metric, set_ = data.metric.unique()[0], data.set.unique()[0]
    for case in data.ID.unique():
        df = data[data.ID == case]
        lesion_location = round(df["enh_tumor_location"].unique()[0], 2)
        lesion_size = int(df["lesion_size"].unique()[0])

        fig = go.Figure()
        fig.add_trace(go.Bar(x=df["relative_diff"], y=df["region"], orientation='h',
                             marker_color=df["gain"], marker_line=dict(width=1, color='black'),
                             hovertemplate="Patient: "f'{case}'" <br>" + pretty_string(metric) + " : %{x:.2f}%<br>"
                                           "Region: %{y}<br>Dataset: " + set_))
        fig.update_xaxes(showline=False)
        # fig.update_yaxes(title_text=f"Patient ID - {case}")
        # fig.update_yaxes(title_text="Region")
        fig.update_traces(width=.8)  # narrow bars
        fig.update_layout(template='simple_white',
                          height=200,
                          width=800,
                          showlegend=False,
                          xaxis_range=[data['relative_diff'].min() - .5, data['relative_diff'].max() + .5],
                          margin=dict(b=20, t=30),
                          title=f"{case} - Lesion location: {lesion_location} - Lesion size: {lesion_size:,}",
                          )

        all_figures.append(fig)

    return all_figures