def create_dashboard():
    import math
    import datetime as dt
    import numpy as np
    import yfinance as yf
    from bokeh.io import curdoc
    from bokeh.plotting import figure
    from bokeh.layouts import column, row
    from bokeh.models import TextInput, Button, DatePicker, MultiChoice

    def load_data(ticker1, ticker2, start, end):
        print(f"Fetching data for {ticker1} and {ticker2} from {start} to {end}")
        df1 = yf.download(ticker1, start, end)
        df2 = yf.download(ticker2, start, end)
        print(f"Fetched {len(df1)} rows for {ticker1} and {len(df2)} rows for {ticker2}")
        return df1, df2

    def update_plot(data, indicators, sync_axis=None):
        print(f"Updating plot with {len(data)} rows and indicators: {indicators}")
        df = data
        gain = df.Close > df.Open
        loss = df.Open > df.Close
        width = 12 * 60 * 60 * 1000  # half day in ms

        if sync_axis is not None:
            p = figure(x_axis_type="datetime", tools="pan,wheel_zoom,box_zoom,reset,save", width=1000, x_range=sync_axis)
        else:
            p = figure(x_axis_type="datetime", tools="pan,wheel_zoom,box_zoom,reset,save", width=1000)

        p.xaxis.major_label_orientation = math.pi / 4
        p.grid.grid_line_alpha = 0.3

        p.segment(df.index, df.High, df.index, df.Low, color="black")
        p.vbar(df.index[gain], width, df.Open[gain], df.Close[gain], fill_color="#00ff00", line_color="#00ff00")
        p.vbar(df.index[loss], width, df.Open[loss], df.Close[loss], fill_color="#ff0000", line_color="#ff0000")

        for indicator in indicators:
            if indicator == "30 Day SMA":
                df['SMA30'] = df['Close'].rolling(30).mean()
                p.line(df.index, df.SMA30, color="purple", legend_label="30 Day SMA")
            elif indicator == "100 Day SMA":
                df['SMA100'] = df['Close'].rolling(100).mean()
                p.line(df.index, df.SMA100, color="blue", legend_label="100 Day SMA")
            elif indicator == "Linear Regression Line":
                par = np.polyfit(range(len(df.index.values)), df.Close.values, 1, full=True)
                slope = par[0][0]
                intercept = par[0][1]
                y_predicted = [slope * i + intercept for i in range(len(df.index.values))]
                p.segment(df.index[0], y_predicted[0], df.index[-1], y_predicted[-1], legend_label="Linear Regression", color="red")

            p.legend.location = "top_left"
            p.legend.click_policy = "hide"

        return p

    def on_button_click():
        print("Button clicked!")
        main_stock = stock1_text.value
        comparison_stock = stock2_text.value
        start = date_picker_from.value
        end = date_picker_to.value
        indicators = indicator_choice.value

        source1, source2 = load_data(main_stock, comparison_stock, start, end)
        p = update_plot(source1, indicators)
        p2 = update_plot(source2, indicators, sync_axis=p.x_range)

        layout.children[1] = row(p, p2)
        print("Layout updated!")

    stock1_text = TextInput(title="Main Stock")
    stock2_text = TextInput(title="Comparison Stock")
    date_picker_from = DatePicker(title='Start Date', value="2020-01-01", min_date="2000-01-01", max_date=dt.datetime.now().strftime("%Y-%m-%d"))
    date_picker_to = DatePicker(title='End Date', value="2020-02-01", min_date="2000-01-01", max_date=dt.datetime.now().strftime("%Y-%m-%d"))
    indicator_choice = MultiChoice(options=["100 Day SMA", "30 Day SMA", "Linear Regression Line"])

    load_button = Button(label="Load Data 1", button_type="success")
    load_button.on_click(on_button_click)

    layout = column(stock1_text, stock2_text, date_picker_from, date_picker_to, indicator_choice, load_button, row())

    return layout
