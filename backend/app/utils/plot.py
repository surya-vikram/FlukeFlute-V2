import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import os
from flask import abort
from config import Config
image_path = Config().PLOTS_FOLDER

def pie_chart(xdata, ydata, filename):
    try:
        plt.pie(ydata, labels=xdata)
        plt.axis('equal')
        plt.savefig(os.path.join(image_path, filename))
        plt.clf()
    except Exception:
        pass


def column_chart(xdata, ydata, filename):
    try:
        plt.bar(xdata, ydata, width=0.5)
        plt.savefig(os.path.join(image_path, filename))
        plt.clf()
    except Exception:
        pass


def hist_chart(visits, filename):
    try:
        import matplotlib.pyplot as plt
        from collections import Counter
        from datetime import datetime
        import numpy as np
        visit_dates = [visit.visit_date for visit in visits]
        date_counter = Counter(visit_dates)
        dates = np.array(list(date_counter.keys()))
        counts = np.array(list(date_counter.values()))
        sorted_indices = np.argsort(dates)
        dates = dates[sorted_indices]
        counts = counts[sorted_indices]
        plt.figure(figsize=(10, 6))
        plt.bar(dates, counts, align='center', alpha=0.5)
        plt.xlabel('Visit Date')
        plt.ylabel('Number of Visits')
        plt.title('Visits Over Time')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(image_path, filename))
        plt.clf()

    except Exception as e:
        pass
