import dash
from dash import dcc, html, Input, Output, State, ctx
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import yfinance as yf
from flask_caching import Cache
import datetime

# --- Dash Setup ---
app = dash.Dash(__name__, suppress_callback_exceptions=True) # suppress_callback_exceptions is crucial for multi-page apps
server = app.server

# --- Cache Configuration ---
CACHE_CONFIG = {'CACHE_TYPE': 'simple', 'CACHE_DEFAULT_TIMEOUT': 300}
cache = Cache(app.server, config=CACHE_CONFIG)

# --- Constants ---
periods = [28, 55, 84]
DATA_POINTS_ZOOM = 50
DEFAULT_TICKER = 'AAPL'

# --- Data Fetching and Processing Functions ---
# (Keeping these outside callbacks for memoization)

def fetch_yahoo_finance_data(ticker, start_date, end_date):
    try:
        ticker_obj = yf.Ticker(ticker)
        info = ticker_obj.info
        long_name = info.get("longName", ticker)

        df = ticker_obj.history(start=start_date, end=end_date)

        if df.empty:
            return pd.DataFrame(), long_name, "no_data"

        df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
        df.columns = [col.lower() for col in df.columns]
        df.index.name = 'Date'
        return df, long_name, None
    except yf.TickerError:
        return pd.DataFrame(), ticker, "invalid_ticker"
    except Exception as e:
        return pd.DataFrame(), ticker, f"error: {str(e)}"

@cache.memoize(timeout=CACHE_CONFIG['CACHE_DEFAULT_TIMEOUT'])
def get_processed_data(ticker, start_date, end_date):
    df, long_name, status = fetch_yahoo_finance_data(ticker, start_date, end_date)
    if status is not None:
        return pd.DataFrame(), [], [], [], pd.Series(), long_name, status

    df['pivot_point'] = (df['high'] + df['low'] + df['close']) / 3
    for period in periods:
        df[f'sma_pp_{period}'] = df['pivot_point'].rolling(window=period).mean()

    df = df.dropna(subset=['close', 'high', 'low', 'open', 'volume'] + [f'sma_pp_{p}' for p in periods])

    volume_profile_data = pd.Series()
    bin_mid_points, bin_ranges, normalized_volume = [], [], []

    if not df.empty and df['volume'].sum() > 0:
        price_bins = np.linspace(df['low'].min() * 0.98, df['high'].max() * 1.02, 50)
        df['price_bin'] = pd.cut(df['close'], bins=price_bins, include_lowest=True)
        volume_profile_data = df.groupby('price_bin', observed=False)['volume'].sum()

        if not volume_profile_data.empty:
            bin_mid_points = [interval.mid for interval in volume_profile_data.index]
            max_volume = volume_profile_data.values.max()
            normalized_volume = volume_profile_data.values / max_volume if max_volume > 0 else np.zeros_like(volume_profile_data.values)
            bin_ranges = [f"{interval.left:.2f} - {interval.right:.2f}" for interval in volume_profile_data.index]

    return df, bin_mid_points, bin_ranges, normalized_volume, volume_profile_data, long_name, None

# --- Shared Header and Controls Layout ---
header_and_controls = html.Div([
    html.H1("Market Analysis Suite", style={'color': '#333', 'marginRight': '20px'}),
    dcc.Link('Candlestick Chart', href='/candlestick', style={'marginRight': '15px', 'fontSize': '18px', 'color': '#007bff'}),
    dcc.Link('Daily Returns', href='/daily-returns', style={'marginRight': '20px', 'fontSize': '18px', 'color': '#007bff'}),
    dcc.Input(id='ticker-input', type='text', value=DEFAULT_TICKER,
              placeholder='Enter Ticker',
              style={'fontSize': '16px', 'height': '36px', 'width': '120px'}),
    dcc.DatePickerSingle(
        id='start-date-picker',
        date=(datetime.datetime.today() - datetime.timedelta(days=730)).date(),
        display_format='YYYY-MM-DD'
    ),
    dcc.DatePickerSingle(
        id='end-date-picker',
        date=datetime.datetime.today().date(),
        display_format='YYYY-MM-DD'
    ),
    html.Button("Update Charts", id='update-button', n_clicks=0,
                style={'backgroundColor': '#007bff', 'color': 'white', 'height': '40px', 'fontSize': '16px', 'marginLeft': '10px'}),
], style={
    'display': 'flex',
    'gap': '10px',
    'padding': '10px',
    'flexWrap': 'wrap',
    'justifyContent': 'center',
    'alignItems': 'center',
    'backgroundColor': '#f4f4f4',
    'borderBottom': '1px solid #ddd'
})

# --- Main App Layout ---
app.layout = html.Div([
    dcc.Location(id='url', refresh=False), # Monitors URL changes for navigation
    header_and_controls, # Always visible
    dcc.Store(id="global-params", data={ # Store for shared global state
        'ticker': DEFAULT_TICKER,
        'start_date': (datetime.datetime.today() - datetime.timedelta(days=730)).date().isoformat(),
        'end_date': datetime.datetime.today().date().isoformat()
    }),
    dcc.Store(id="zoom-range"), # Specific to candlestick chart's zoom
    dcc.Store(id="full-data-length"), # Specific to candlestick chart's zoom reset
    html.Div(id='page-content', style={'marginTop': '20px'}), # Content changes based on URL
    html.Div(id='status-message', style={'color': 'red', 'marginTop': '10px', 'textAlign': 'center'})
])

# --- Callbacks for Global State (Input to dcc.Store) ---
@app.callback(
    Output('global-params', 'data'),
    Input('update-button', 'n_clicks'),
    State('ticker-input', 'value'),
    State('start-date-picker', 'date'),
    State('end-date-picker', 'date'),
    prevent_initial_call=False # Allow initial load
)
def update_global_params(n_clicks, ticker, start_date_str, end_date_str):
    # This callback updates the dcc.Store with the latest global selections
    # on button click.
    if not n_clicks: # For initial load, use default values
        return dash.no_update

    if not ticker:
        # Handle empty ticker: return current state or a default if desired
        return dash.no_update

    return {
        'ticker': ticker,
        'start_date': start_date_str,
        'end_date': end_date_str
    }

# --- Page 1: Candlestick Chart (Reusing your logic) ---
def create_candlestick_layout():
    return html.Div([
        html.H2("Candlestick Chart", style={'textAlign': 'center'}),
        html.Div([
            html.Button("+", id="zoom-in", n_clicks=0, style={'marginLeft': '10px'}),
            html.Button("-", id="zoom-out", n_clicks=0),
            html.Button("Reset Zoom", id="zoom-reset", n_clicks=0)
        ], style={
            'display': 'flex',
            'gap': '5px',
            'padding': '10px',
            'justifyContent': 'center',
            'alignItems': 'center',
        }),
        dcc.Loading(id="loading-candlestick", type="default", children=[
            html.Div(id='candlestick-graph-container', style={'display': 'flex', 'justifyContent': 'center'})
        ])
    ])

@app.callback(
    Output("zoom-range", "data"),
    Output("full-data-length", "data"),
    Input("global-params", "data"), # Trigger initialization when global params change
    prevent_initial_call=False
)
def initialize_candlestick_zoom(global_params):
    if not global_params:
        return {'start': 0, 'end': 0}, 0

    ticker = global_params.get('ticker', DEFAULT_TICKER)
    start_date = pd.to_datetime(global_params.get('start_date'))
    end_date = pd.to_datetime(global_params.get('end_date'))

    df, *_ = get_processed_data(ticker, start_date, end_date)
    if df.empty:
        return {'start': 0, 'end': 0}, 0
    total = len(df)
    initial_start = max(0, total - 252) # Default to last year
    return {"start": initial_start, "end": total}, total


@app.callback(
    Output('candlestick-graph-container', 'children'),
    # Output('status-message', 'children', allow_duplicate=True), # Status message will be updated by the main router
    Input('global-params', 'data'), # Trigger update on global param changes
    Input('zoom-range', 'data'),    # Trigger update on zoom changes
    prevent_initial_call=False
)
def update_candlestick_chart(global_params, zoom_range):
    if not global_params:
        return dcc.Graph(figure=go.Figure())

    ticker = global_params.get('ticker')
    start_date_str = global_params.get('start_date')
    end_date_str = global_params.get('end_date')

    if not ticker:
        return dcc.Graph(figure=go.Figure())

    df, bin_mid_points, bin_ranges, normalized_volume, volume_profile_data, long_name, status = get_processed_data(
        ticker, pd.to_datetime(start_date_str), pd.to_datetime(end_date_str)
    )

    if status == "invalid_ticker":
        return dcc.Graph(figure=go.Figure()) # Let the main status message handle this
    elif status == "no_data":
        return dcc.Graph(figure=go.Figure())
    elif status and "error" in status:
        return dcc.Graph(figure=go.Figure())
    elif df.empty:
        return dcc.Graph(figure=go.Figure())

    display_df = df.copy()
    if zoom_range and zoom_range['end'] > zoom_range['start']:
        display_df = df.iloc[zoom_range["start"]:zoom_range["end"]]

    if display_df.empty:
        return dcc.Graph(figure=go.Figure())

    last_date = display_df.index.max()
    xaxis_range = [display_df.index.min(), last_date + pd.Timedelta(days=20)]

    fig = go.Figure()

    # Candlestick chart (main plot)
    fig.add_trace(go.Candlestick(
        x=display_df.index,
        open=display_df['open'], high=display_df['high'],
        low=display_df['low'], close=display_df['close'],
        increasing_line_color='green', decreasing_line_color='red',
        showlegend=False,
        name='Candlestick'
    ))

    # Volume Bars Left Overlay (Volume Profile)
    if bin_mid_points and normalized_volume.size > 0:
        top_indices = np.argsort(volume_profile_data.values)[-2:]
        colors = ['rgba(150,150,150,0.2)'] * len(volume_profile_data)
        for i in top_indices:
            colors[i] = 'orange'

        fig.add_trace(go.Bar(
            y=bin_mid_points,
            x=normalized_volume,
            orientation='h',
            marker=dict(color=colors, opacity=0.33),
            showlegend=False,
            xaxis='x2', yaxis='y'
        ))

        annotations = []
        for idx in top_indices:
            annotations.append(dict(
                x=normalized_volume[idx] + 0.01,
                y=bin_mid_points[idx],
                text=f"${bin_mid_points[idx]:.2f}",
                showarrow=False,
                xanchor='left',
                font=dict(size=12, color='black'),
                xref='x2', yref='y'
            ))
        fig.update_layout(annotations=annotations)

    # SMA overlays
    for period in periods:
        fig.add_trace(go.Scatter(
            x=display_df.index,
            y=display_df[f'sma_pp_{period}'],
            mode='lines',
            name=f'SMA PP {period}',
            line=dict(width=1.5)
        ))

    # Volume Indicator at the bottom
    colors_volume = ['green' if display_df['close'].iloc[i] > display_df['open'].iloc[i] else 'red' for i in range(len(display_df))]
    fig.add_trace(go.Bar(
        x=display_df.index,
        y=display_df['volume'],
        marker_color=colors_volume,
        name='Volume',
        yaxis='y3', # Corrected: 'y3'
        showlegend=False
    ))

    # Layout & Styling
    fig.update_layout(
        height=700,
        autosize=True,
        font=dict(family="Roboto", size=13),
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(domain=[0.1, 1], range=xaxis_range,
                   showgrid=True, gridcolor='rgba(211,211,211,0.3)',
                   tickfont=dict(size=14), rangeslider_visible=False, type='date'),
        yaxis=dict(
            title=dict(text=f"{long_name} Price", font=dict(size=16)),
            domain=[0.3, 1],
            showgrid=True,
            gridcolor='lightgray',
            tickfont=dict(size=14)
        ),
        yaxis3=dict( # Corrected: yaxis3 for the third y-axis definition
            title=dict(text='Volume', font=dict(size=12)),
            domain=[0, 0.25],
            showgrid=True,
            gridcolor='lightgray',
            tickfont=dict(size=10)
        ),
        xaxis2=dict(domain=[0, 0.1], overlaying='x',
                    side='left', showgrid=False, showticklabels=False),
        hovermode='x unified',
        margin=dict(l=60, r=60, b=60, t=60),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=12),
            bgcolor="rgba(255,255,255,0.7)"
        )
    )

    return dcc.Graph(figure=fig, style={'width': '100%', 'height': '700px'})


@app.callback(
    Output("zoom-range", "data", allow_duplicate=True),
    Input("zoom-in", "n_clicks"),
    Input("zoom-out", "n_clicks"),
    Input("zoom-reset", "n_clicks"),
    State("zoom-range", "data"),
    State("full-data-length", "data"),
    prevent_initial_call=True
)
def update_candlestick_zoom(zin, zout, reset, current_zoom, full_data_length):
    if not current_zoom:
        return {'start': 0, 'end': 0}

    triggered = ctx.triggered_id
    start, end = current_zoom['start'], current_zoom['end']
    total_data_points = full_data_length if full_data_length is not None else (end - start)

    span = end - start

    if triggered == "zoom-in" and span > DATA_POINTS_ZOOM * 2:
        new_start = min(end - DATA_POINTS_ZOOM * 2, start + DATA_POINTS_ZOOM)
        new_end = max(start + DATA_POINTS_ZOOM * 2, end - DATA_POINTS_ZOOM)
        return {"start": new_start, "end": new_end}
    elif triggered == "zoom-out":
        new_start = max(0, start - DATA_POINTS_ZOOM)
        new_end = min(total_data_points, end + DATA_POINTS_ZOOM)
        return {"start": new_start, "end": new_end}
    elif triggered == "zoom-reset":
        return {"start": 0, "end": total_data_points}
    return current_zoom


# --- Page 2: Simple Daily Returns Chart ---
def create_daily_returns_layout():
    return html.Div([
        html.H2("Daily Returns Chart", style={'textAlign': 'center'}),
        dcc.Loading(id="loading-returns", type="default", children=[
            html.Div(id='daily-returns-graph-container', style={'display': 'flex', 'justifyContent': 'center'})
        ])
    ])

@app.callback(
    Output('daily-returns-graph-container', 'children'),
    # Output('status-message', 'children', allow_duplicate=True),
    Input('global-params', 'data'),
    prevent_initial_call=False
)
def update_daily_returns_chart(global_params):
    if not global_params:
        return dcc.Graph(figure=go.Figure())

    ticker = global_params.get('ticker')
    start_date_str = global_params.get('start_date')
    end_date_str = global_params.get('end_date')

    if not ticker:
        return dcc.Graph(figure=go.Figure())

    df, _, _, _, _, long_name, status = get_processed_data(
        ticker, pd.to_datetime(start_date_str), pd.to_datetime(end_date_str)
    )

    if status == "invalid_ticker":
        return dcc.Graph(figure=go.Figure())
    elif status == "no_data":
        return dcc.Graph(figure=go.Figure())
    elif status and "error" in status:
        return dcc.Graph(figure=go.Figure())
    elif df.empty:
        return dcc.Graph(figure=go.Figure())

    df['daily_return'] = df['close'].pct_change() * 100 # Percentage change

    fig = go.Figure(data=[go.Scatter(
        x=df.index,
        y=df['daily_return'],
        mode='lines',
        name='Daily Return',
        line=dict(color='blue')
    )])

    fig.update_layout(
        title=f'{long_name} Daily Percentage Returns',
        xaxis_title='Date',
        yaxis_title='Daily Return (%)',
        height=600,
        autosize=True,
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=60, r=60, b=60, t=60)
    )
    return dcc.Graph(figure=fig, style={'width': '100%', 'height': '600px'})

# --- Main Routing Callback ---
@app.callback(
    Output('page-content', 'children'),
    Output('status-message', 'children'),
    Input('url', 'pathname'),
    State('global-params', 'data') # To get current params for initial status check
)
def display_page(pathname, global_params):
    status_msg = ""
    # Check for initial status based on default or current global params
    if global_params:
        ticker = global_params.get('ticker')
        start_date = pd.to_datetime(global_params.get('start_date'))
        end_date = pd.to_datetime(global_params.get('end_date'))
        _, _, _, _, _, _, status = get_processed_data(ticker, start_date, end_date)
        if status == "invalid_ticker":
            status_msg = f"Invalid ticker symbol: {ticker}. Please check and try again."
        elif status == "no_data":
            status_msg = f"No data found for {ticker} in the specified date range. Please try a different range."
        elif status and "error" in status:
            status_msg = f"An error occurred: {status.replace('error: ', '')}. Please try again later."


    if pathname == '/candlestick':
        return create_candlestick_layout(), status_msg
    elif pathname == '/daily-returns':
        return create_daily_returns_layout(), status_msg
    else:
        # Default to candlestick chart if no path is specified
        return create_candlestick_layout(), status_msg

if __name__ == '__main__':
    app.run(debug=True)
